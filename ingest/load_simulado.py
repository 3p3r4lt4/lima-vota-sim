"""Carga el corpus SIMULADO (public/data/planes/*.json) en Postgres + pgvector.
Activa el modo de recuperación semántica de /api/preguntar sin necesidad de PDFs reales.
Uso: python ingest/load_simulado.py
"""
import hashlib, json, os, pathlib
import psycopg, voyageai
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

load_dotenv()
ROOT = pathlib.Path(__file__).resolve().parents[1]
vo = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])

def main():
    with psycopg.connect(os.environ["DATABASE_URL_ADMIN"]) as conn:
        register_vector(conn)
        cur = conn.cursor()
        for f in sorted((ROOT / "public/data/comparaciones").glob("*.json")):
            comp = json.loads(f.read_text(encoding="utf-8"))
            planes = json.loads((ROOT / "public/data/planes" / f.name).read_text(encoding="utf-8"))
            textos = {c["id"]: c["paginas"] for c in planes["candidatos"]}
            for c in comp["candidatos"]:
                cur.execute("""insert into candidatos (id,nivel,ubigeo,ambito,cargo,nombre,organizacion,plan_url)
                               values (%s,%s,%s,%s,%s,%s,%s,'') on conflict (id) do update set nombre=excluded.nombre""",
                            (c["id"], comp["nivel"], comp["ubigeo"], comp["ambito"], comp["cargo"], c["nombre"], c["organizacion"]))
                paginas = textos[c["id"]]
                sha = hashlib.sha256(json.dumps(paginas, ensure_ascii=False).encode()).hexdigest()
                cur.execute("select 1 from documentos where sha256=%s", (sha,))
                if cur.fetchone():
                    continue
                cur.execute("delete from chunks where candidato_id=%s", (c["id"],))
                cur.execute("""insert into documentos (candidato_id,tipo,url,sha256,paginas)
                               values (%s,'plan_simulado','',%s,%s) returning id""", (c["id"], sha, len(paginas)))
                did = cur.fetchone()[0]
                embs = vo.embed([f"{p['titulo']}. {p['texto']}" for p in paginas], model="voyage-3.5", input_type="document").embeddings
                cur.executemany("insert into chunks (documento_id,candidato_id,pagina,contenido,embedding) values (%s,%s,%s,%s,%s)",
                                [(did, c["id"], p["pagina"], p["texto"], e) for p, e in zip(paginas, embs)])
            conn.commit()
            print(f"ok {comp['ambito']}")
        cur.execute("select setval('candidatos_id_seq', (select max(id) from candidatos))")
        conn.commit()

if __name__ == "__main__":
    main()
