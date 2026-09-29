"""Descarga planes de gobierno (PDF), los trocea por página y guarda embeddings en pgvector.
Uso: python ingest.py candidatos.csv
"""
import csv, hashlib, os, sys, time
import fitz, psycopg, requests, voyageai
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

load_dotenv()
vo = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
MODEL = os.getenv("VOYAGE_MODEL", "voyage-3.5")
CHUNK_CHARS, OVERLAP = 2400, 300

def trocear(texto):
    texto = " ".join(texto.split())
    i = 0
    while i < len(texto):
        yield texto[i:i + CHUNK_CHARS]
        i += CHUNK_CHARS - OVERLAP

def paginas_pdf(data):
    doc = fitz.open(stream=data, filetype="pdf")
    out, sin_texto = [], 0
    for n, page in enumerate(doc, start=1):
        t = page.get_text()
        if len(t.strip()) < 40:
            sin_texto += 1   # página escaneada: requiere OCR (ver README)
            continue
        out.append((n, t))
    return out, len(doc), sin_texto > len(doc) * 0.5

def upsert_candidato(cur, r):
    cur.execute("""
      insert into candidatos (nivel, ubigeo, ambito, cargo, nombre, organizacion, plan_url, hoja_vida_url)
      values (%(nivel)s,%(ubigeo)s,%(ambito)s,%(cargo)s,%(nombre)s,%(organizacion)s,%(plan_url)s,nullif(%(hoja_vida_url)s,''))
      on conflict (ubigeo, cargo, organizacion) do update
        set nombre=excluded.nombre, plan_url=excluded.plan_url
      returning id""", r)
    return cur.fetchone()[0]

def main(csv_path):
    with psycopg.connect(os.environ["DATABASE_URL_ADMIN"]) as conn:
        register_vector(conn)
        for r in csv.DictReader(open(csv_path, encoding="utf-8")):
            with conn.cursor() as cur:
                cid = upsert_candidato(cur, r)
                pdf = requests.get(r["plan_url"], timeout=60).content
                sha = hashlib.sha256(pdf).hexdigest()
                cur.execute("select 1 from documentos where sha256=%s", (sha,))
                if cur.fetchone():
                    print(f"= {r['nombre']}: sin cambios"); continue
                pags, total, ocr = paginas_pdf(pdf)
                cur.execute("""insert into documentos (candidato_id,url,sha256,paginas,requirio_ocr)
                               values (%s,%s,%s,%s,%s) returning id""", (cid, r["plan_url"], sha, total, ocr))
                did = cur.fetchone()[0]
                cur.execute("delete from chunks where candidato_id=%s and documento_id<>%s", (cid, did))
                piezas = [(p, c) for p, t in pags for c in trocear(t)]
                for i in range(0, len(piezas), 64):
                    lote = piezas[i:i + 64]
                    embs = vo.embed([c for _, c in lote], model=MODEL, input_type="document").embeddings
                    cur.executemany(
                        "insert into chunks (documento_id,candidato_id,pagina,contenido,embedding) values (%s,%s,%s,%s,%s)",
                        [(did, cid, p, c, e) for (p, c), e in zip(lote, embs)])
                    time.sleep(0.2)
                conn.commit()
                aviso = "  (mayormente escaneado: pasar por OCR)" if ocr else ""
                print(f"+ {r['nombre']} ({r['ambito']}): {len(piezas)} chunks{aviso}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "candidatos.csv")
