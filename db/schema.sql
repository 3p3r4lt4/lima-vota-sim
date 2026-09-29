-- Postgres 15+ con pgvector (Neon o Supabase). Ejecutar una vez: psql "$DATABASE_URL_ADMIN" -f db/schema.sql
create extension if not exists vector;

create table if not exists candidatos (
  id            bigserial primary key,
  nivel         text not null check (nivel in ('distrital','provincial','regional','presidencial')),
  ubigeo        text not null,          -- '1501' Lima Metropolitana, '150114' La Molina, etc.
  ambito        text not null,
  cargo         text not null,
  nombre        text not null,
  organizacion  text not null,
  plan_url      text not null default '',  -- PDF oficial del JNE (vacío en modo simulado)
  hoja_vida_url text,
  unique (ubigeo, cargo, organizacion)
);

create table if not exists documentos (
  id            bigserial primary key,
  candidato_id  bigint not null references candidatos(id) on delete cascade,
  tipo          text not null default 'plan_gobierno',
  url           text not null,
  sha256        text not null unique,   -- evita reingestar el mismo PDF
  paginas       int,
  requirio_ocr  boolean default false,
  ingestado_en  timestamptz default now()
);

create table if not exists chunks (
  id            bigserial primary key,
  documento_id  bigint not null references documentos(id) on delete cascade,
  candidato_id  bigint not null references candidatos(id) on delete cascade,
  pagina        int not null,
  contenido     text not null,
  embedding     vector(1024) not null,  -- voyage-3.5 = 1024 dims
  tsv           tsvector generated always as (to_tsvector('spanish', contenido)) stored
);

create index if not exists chunks_embedding_hnsw on chunks using hnsw (embedding vector_cosine_ops);
create index if not exists chunks_tsv_gin on chunks using gin (tsv);
create index if not exists chunks_candidato on chunks (candidato_id);

-- Búsqueda híbrida (vector + texto) con Reciprocal Rank Fusion, filtrada por candidatos
create or replace function buscar_chunks(
  q_embedding vector(1024), q_texto text, candidato_ids bigint[], k int default 12
) returns table (id bigint, candidato_id bigint, pagina int, contenido text, score float)
language sql stable as $$
  with vec as (
    select c.id, row_number() over (order by c.embedding <=> q_embedding) as r
    from chunks c where c.candidato_id = any(candidato_ids)
    order by c.embedding <=> q_embedding limit 60
  ),
  txt as (
    select c.id, row_number() over (order by ts_rank_cd(c.tsv, q) desc) as r
    from chunks c, websearch_to_tsquery('spanish', q_texto) q
    where c.candidato_id = any(candidato_ids) and c.tsv @@ q
    order by ts_rank_cd(c.tsv, q) desc limit 60
  ),
  fused as (
    select coalesce(vec.id, txt.id) as id,
           coalesce(1.0/(60+vec.r),0) + coalesce(1.0/(60+txt.r),0) as score
    from vec full outer join txt on vec.id = txt.id
  )
  select c.id, c.candidato_id, c.pagina, c.contenido, f.score
  from fused f join chunks c on c.id = f.id
  order by f.score desc limit k;
$$;

-- Usuario de solo lectura para las Netlify Functions
-- create role app_lectura login password '...';
-- grant select on all tables in schema public to app_lectura;
-- grant execute on function buscar_chunks to app_lectura;
