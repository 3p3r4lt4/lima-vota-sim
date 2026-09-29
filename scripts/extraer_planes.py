"""Extrae el texto por página de los PDF de planes de gobierno (requiere pdftotext / poppler-utils).
Uso: python scripts/extraer_planes.py public/planes/150114
Genera scripts/planes/<ubigeo>/<clave>.json con la lista de páginas.
"""
import json, pathlib, re, subprocess, sys

def main(carpeta):
    carpeta = pathlib.Path(carpeta)
    ubigeo = carpeta.name
    salida = pathlib.Path(__file__).parent / "planes" / ubigeo
    salida.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(carpeta.glob("*.pdf")):
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        n = int(re.search(r"Pages:\s+(\d+)", info).group(1))
        paginas = []
        for i in range(1, n + 1):
            t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"], capture_output=True, text=True).stdout
            paginas.append(" ".join(t.split()))
        (salida / f"{pdf.stem}.json").write_text(json.dumps(paginas, ensure_ascii=False), encoding="utf-8")
        print(f"{pdf.name}: {n} páginas")

if __name__ == "__main__":
    main(sys.argv[1])
