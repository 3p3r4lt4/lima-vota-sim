-- Eventos por sesión, catálogo de ubigeos INEI y registro de accesos al panel /admin.
-- Requiere db/analytics.sql (no lo modifica). Idempotente.
-- Ejecutar con un usuario administrador: psql "$DATABASE_URL_ADMIN" -f db/analytics_eventos.sql
-- Después: node scripts/cargar-ref-ubigeo.mjs   (llena ref_ubigeo)

alter table visitas_sesion
  add column if not exists preguntas_count int not null default 0,   -- solo el conteo, nunca el texto
  add column if not exists eventos_count   int not null default 0,   -- tope de eventos por sesión
  add column if not exists utm_source      text,
  add column if not exists utm_medium      text,
  add column if not exists utm_campaign    text;

create index if not exists visitas_sesion_ubigeo_geo on visitas_sesion (ubigeo_geo);

-- Una fila por vista, cambio de ámbito, pregunta o salida. Los latidos no se guardan aquí:
-- solo actualizan visitas_sesion.ultima_senal.
create table if not exists analytics_eventos (
  id             bigint generated always as identity primary key,
  sesion_id      uuid not null references visitas_sesion (sesion_id) on delete cascade,
  tipo           text not null check (tipo in ('vista','cambio_ambito','pregunta','latido','salida')),
  ruta           text,
  vista          text check (vista in ('fichas','comparar')),
  ambito_ubigeo  varchar(6),
  creado_en      timestamptz not null default now()
);

create index if not exists analytics_eventos_sesion on analytics_eventos (sesion_id);
create index if not exists analytics_eventos_creado on analytics_eventos (creado_en);
create index if not exists analytics_eventos_ambito on analytics_eventos (ambito_ubigeo);

-- Catálogo INEI: departamentos (2 dígitos), provincias (4) y distritos (6)
create table if not exists ref_ubigeo (
  ubigeo        varchar(6) primary key check (ubigeo ~ '^([0-9]{2}|[0-9]{4}|[0-9]{6})$'),
  departamento  text not null,
  provincia     text,
  distrito      text,
  check (
    (length(ubigeo) = 2 and provincia is null and distrito is null) or
    (length(ubigeo) = 4 and provincia is not null and distrito is null) or
    (length(ubigeo) = 6 and provincia is not null and distrito is not null))
);

-- Auditoría de accesos al panel. No guarda la contraseña, el código ni el usuario escrito.
create table if not exists admin_login_log (
  id         bigint generated always as identity primary key,
  creado_en  timestamptz not null default now(),
  ip_hash    char(64) not null,
  resultado  text not null check (resultado in ('ok','fallo','bloqueado'))
);

create index if not exists admin_login_log_creado on admin_login_log (creado_en);

-- Misma firma que en analytics.sql; ahora también purga el registro de accesos.
-- Los eventos se borran en cascada con su sesión.
create or replace function purgar_visitas(dias int default 90) returns int
language plpgsql security definer set search_path = public as $$
declare borradas int;
begin
  delete from visitas_sesion where inicio < now() - make_interval(days => greatest(dias, 1));
  get diagnostics borradas = row_count;
  delete from admin_login_log where creado_en < now() - make_interval(days => greatest(dias, 1));
  delete from admin_intentos
   where primer_fallo < now() - interval '1 day'
     and (bloqueado_hasta is null or bloqueado_hasta < now());
  return borradas;
end $$;
revoke all on function purgar_visitas(int) from public;

-- Permisos: se aplican solo si los roles ya existen (se crean a mano, ver analytics.sql).
-- Ninguno toca candidatos, documentos ni chunks.
do $$
begin
  if exists (select 1 from pg_roles where rolname = 'analytics_writer') then
    grant insert on analytics_eventos to analytics_writer;
    -- El UPDATE … RETURNING de /api/visita lee estas columnas
    grant select (eventos_count, preguntas_count) on visitas_sesion to analytics_writer;
    grant select on ref_ubigeo to analytics_writer;
    grant insert on admin_login_log to analytics_writer;
    grant execute on function purgar_visitas(int) to analytics_writer;
  end if;
  if exists (select 1 from pg_roles where rolname = 'analytics_reader') then
    grant select on analytics_eventos, ref_ubigeo, admin_login_log to analytics_reader;
  end if;
end $$;
