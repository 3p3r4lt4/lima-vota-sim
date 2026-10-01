-- Analítica de visitas propia y bloqueo de intentos del panel /admin.
-- Migración idempotente, separada de schema.sql (no toca las tablas del corpus).
-- Ejecutar con un usuario administrador: psql "$DATABASE_URL_ADMIN" -f db/analytics.sql
-- Requiere Postgres 13+ (gen_random_uuid en el núcleo).

create table if not exists visitas_sesion (
  id                uuid primary key default gen_random_uuid(),
  sesion_id         uuid not null unique,                -- crypto.randomUUID() del navegador (sessionStorage)
  inicio            timestamptz not null default now(),
  ultima_senal      timestamptz not null default now(),  -- último «latido»; es la desconexión si no hay «fin»
  fin               timestamptz,
  duracion_seg      int generated always as
                      (greatest(0, extract(epoch from (coalesce(fin, ultima_senal) - inicio)))::int) stored,
  dispositivo_tipo  text check (dispositivo_tipo in ('movil','tablet','escritorio','desconocido')),
  so                text,
  so_version        text,
  navegador         text,
  navegador_version text,
  es_bot            boolean not null default false,
  pais              text,                                 -- código ISO 3166-1 (PE, US…)
  departamento      text,
  provincia         text,
  distrito          text,
  ubigeo_geo        varchar(6),                           -- ubigeo INEI cuando se pudo resolver
  precision_geo     text check (precision_geo in ('pais','departamento','provincia','distrito')),
  ambito_inicial    varchar(6),                           -- ?ambito= al cargar
  ambitos_visitados text[] not null default '{}',
  ip_hash           char(64),                             -- HMAC-SHA256(ip, sal + fecha Lima); nunca la IP
  referer_host      text,
  idioma            text,
  pantalla          text,                                 -- "390x844"
  creado_en         timestamptz not null default now()
);

create index if not exists visitas_sesion_inicio on visitas_sesion (inicio);
create index if not exists visitas_sesion_departamento on visitas_sesion (departamento);
create index if not exists visitas_sesion_ambito_inicial on visitas_sesion (ambito_inicial);

-- Intentos fallidos de login en /admin (5 fallos → 15 min de bloqueo por ip_hash)
create table if not exists admin_intentos (
  ip_hash          char(64) primary key,
  fallos           int not null default 0,
  primer_fallo     timestamptz not null default now(),
  bloqueado_hasta  timestamptz
);

-- Retención: borra sesiones con más de N días (90 por defecto) e intentos viejos.
-- SECURITY DEFINER para que analytics_writer pueda purgar sin tener DELETE sobre la tabla.
create or replace function purgar_visitas(dias int default 90) returns int
language plpgsql security definer set search_path = public as $$
declare borradas int;
begin
  delete from visitas_sesion where inicio < now() - make_interval(days => greatest(dias, 1));
  get diagnostics borradas = row_count;
  delete from admin_intentos
   where primer_fallo < now() - interval '1 day'
     and (bloqueado_hasta is null or bloqueado_hasta < now());
  return borradas;
end $$;
revoke all on function purgar_visitas(int) from public;

-- ============================================================================
-- Roles (ejecutar una vez a mano, con contraseñas largas y aleatorias).
-- Ninguno de los dos tiene acceso a candidatos, documentos ni chunks.
--
-- create role analytics_writer login password '...';
-- create role analytics_reader login password '...';
-- revoke all on all tables in schema public from analytics_writer, analytics_reader;
-- grant usage on schema public to analytics_writer, analytics_reader;
--
-- Escritura (DATABASE_URL_ANALYTICS): INSERT/UPDATE en visitas_sesion.
-- Postgres exige SELECT sobre las columnas que lee un UPDATE (WHERE y expresiones del SET),
-- por eso se concede SELECT solo en esas tres columnas, no en la tabla.
-- grant insert, update on visitas_sesion to analytics_writer;
-- grant select (sesion_id, inicio, ambitos_visitados) on visitas_sesion to analytics_writer;
-- grant select, insert, update, delete on admin_intentos to analytics_writer;
-- grant execute on function purgar_visitas(int) to analytics_writer;
--
-- Lectura (DATABASE_URL_ANALYTICS_READER): solo el panel.
-- grant select on visitas_sesion to analytics_reader;
--
-- Comprobación: \dp visitas_sesion   y   \dp candidatos   (los roles analytics_* no deben aparecer en candidatos)
-- ============================================================================
