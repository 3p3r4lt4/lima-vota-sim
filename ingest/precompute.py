"""Genera la matriz comparativa candidato x tema como JSON estático
(public/data/comparaciones/<ubigeo>.json) que se revisa en un Pull Request antes de publicar.
Uso: python precompute.py [ubigeo ...]
"""
import json, os, pathlib, sys
import anthropic, psycopg, voyageai
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

load_dotenv()
vo = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
cl = anthropic.Anthropic()
MODEL = os.getenv("CLAUDE_MODEL_BATCH", "claude-sonnet-5-5")
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public/data/comparaciones"

TEMAS = {
  "seguridad": "seguridad ciudadana, serenazgo, cámaras, patrullaje, delincuencia",
  "transporte": "tránsito, transporte público, movilidad, ciclovías, vías",
  "residuos": "limpieza pública, recojo de basura, residuos sólidos, reciclaje",
  "areas_verdes": "parques, áreas verdes, agua de riego, medio ambiente",
  "desarrollo_urbano": "catastro, licencias, zonificación, obras, infraestructura",
  "social": "programas sociales, adulto mayor, niñez, salud, vaso de leche",
  "economia": "emprendimiento, comercio, empleo, formalización, turismo",
  "gestion": "transparencia, gobierno digital, anticorrupción, participación vecinal",
}

SISTEMA = """Eres un analista neutral que resume planes de gobierno municipales de Lima, Perú.
Reglas: usa SOLO los fragmentos entregados; no opines, no califiques, no compares calidad
entre candidatos; cada propuesta cita su página; si el plan no aborda el tema,
sin_informacion=true. Responde solo JSON válido, sin markdown."""

def resumir(cand, tema, fragmentos):
    ctx = "\n\n".join(f"[p.{f[1]}] {f[2]}" for f in fragmentos)
    msg = cl.messages.create(model=MODEL, max_tokens=900, system=SISTEMA, messages=[{"role": "user", "content":
        f"Candidato: {cand}\nTema: {tema}\nFragmentos:\n{ctx}\n\n"
        'Formato: {"sin_informacion":bool,"resumen":"máx 40 palabras","propuestas":'
        '[{"texto":"...","meta":"cifra o plazo si existe, si no null","pagina":n}]} (máx 4 propuestas)'}])
    txt = msg.content[0].text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(txt)

def main(ubigeos):
    OUT.mkdir(parents=True, exist_ok=True)
    with psycopg.connect(os.environ["DATABASE_URL_ADMIN"]) as conn:
        register_vector(conn)
        cur = conn.cursor()
        if not ubigeos:
            cur.execute("select distinct ubigeo from candidatos"); ubigeos = [r[0] for r in cur]
        indice = []
        for ub in ubigeos:
            cur.execute("select id,nombre,organizacion,plan_url,ambito,nivel,cargo from candidatos where ubigeo=%s", (ub,))
            cands = cur.fetchall()
            data = {"ubigeo": ub, "ambito": cands[0][4], "nivel": cands[0][5], "cargo": cands[0][6],
                    "temas": list(TEMAS), "candidatos": []}
            for cid, nombre, org, url, *_ in cands:
                fila = {"id": cid, "nombre": nombre, "organizacion": org, "plan_url": url, "temas": {}}
                for tema, consulta in TEMAS.items():
                    emb = vo.embed([consulta], model="voyage-3.5", input_type="query").embeddings[0]
                    cur.execute("select id,pagina,contenido from buscar_chunks(%s::vector,%s,%s,8)", (emb, consulta, [cid]))
                    frs = cur.fetchall()
                    fila["temas"][tema] = resumir(nombre, tema, frs) if frs else \
                        {"sin_informacion": True, "resumen": "", "propuestas": []}
                data["candidatos"].append(fila)
                print(f"  {nombre} listo")
            (OUT / f"{ub}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            planes = {"ubigeo": ub, "ambito": data["ambito"], "simulado": False, "candidatos": []}
            for c in data["candidatos"]:
                cur.execute("""select pagina, string_agg(contenido, ' ' order by id) from chunks
                               where candidato_id=%s group by pagina order by pagina""", (c["id"],))
                planes["candidatos"].append({"id": c["id"], "nombre": c["nombre"], "plan_url": c["plan_url"],
                    "paginas": [{"pagina": p, "titulo": f"Página {p}", "texto": t} for p, t in cur.fetchall()]})
            (ROOT / "public/data/planes").mkdir(parents=True, exist_ok=True)
            (ROOT / f"public/data/planes/{ub}.json").write_text(json.dumps(planes, ensure_ascii=False), encoding="utf-8")
            indice.append({"ubigeo": ub, "ambito": data["ambito"], "nivel": data["nivel"], "candidatos": len(cands)})
            print(f"ok {ub} {data['ambito']}")
        ruta = ROOT / "public/data/ambitos.json"
        previo = {a["ubigeo"]: a for a in json.loads(ruta.read_text(encoding="utf-8"))} if ruta.exists() else {}
        previo.update({a["ubigeo"]: a for a in indice})
        previo.pop("demo", None)
        ruta.write_text(json.dumps(sorted(previo.values(), key=lambda a: a["ambito"]),
                                   ensure_ascii=False, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main(sys.argv[1:])
