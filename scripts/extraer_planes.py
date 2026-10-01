"""Extrae el texto por página de los PDF de planes de gobierno (requiere Poppler: pdfinfo, pdftotext, pdftoppm).
Uso: python scripts/extraer_planes.py public/planes/150114
     python scripts/extraer_planes.py scripts/.cache/planes/150130
Genera scripts/planes/<ubigeo>/<clave>.json con la lista de páginas.

Si un PDF es escaneado (páginas sin texto), aplica OCR en español con Tesseract (`tesseract -l spa`) sobre la
imagen de cada página y lo marca en el manifiesto ("ocr": true). Sin Tesseract instalado, lo marca como
"requiere_ocr" y no inventa texto.
"""
import json, os, pathlib, re, shutil, subprocess, sys, tempfile

MIN_CARACTERES = 40  # una página con menos texto se considera sin capa de texto
TESSDATA = pathlib.Path(__file__).parent / ".cache/tessdata"  # spa.traineddata local (no requiere instalar idiomas)


def buscar_tesseract():
    return shutil.which("tesseract") or next(
        (str(p) for p in [pathlib.Path("C:/Program Files/Tesseract-OCR/tesseract.exe"),
                               pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Tesseract-OCR/tesseract.exe"] if p.exists()), None)


def correr(*args):
    return subprocess.run(list(args), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def ocr(pdf, pagina, tesseract):
    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp) / "p"
        subprocess.run(["pdftoppm", "-f", str(pagina), "-l", str(pagina), "-r", "300", "-png", "-singlefile", str(pdf), str(base)], check=True)
        extra = ["--tessdata-dir", str(TESSDATA)] if (TESSDATA / "spa.traineddata").exists() else []
        return correr(tesseract, str(base) + ".png", "-", "-l", "spa", *extra)


def main(carpeta):
    carpeta = pathlib.Path(carpeta)
    ubigeo = carpeta.name
    salida = pathlib.Path(__file__).parent / "planes" / ubigeo
    salida.mkdir(parents=True, exist_ok=True)
    tesseract = buscar_tesseract()
    f_manifiesto = salida / "manifiesto.json"
    manifiesto = json.loads(f_manifiesto.read_text(encoding="utf-8")) if f_manifiesto.exists() else None
    for pdf in sorted(carpeta.glob("*.pdf")):
        n = int(re.search(r"Pages:\s+(\d+)", correr("pdfinfo", str(pdf))).group(1))
        paginas, con_ocr, sin_texto = [], [], []
        for i in range(1, n + 1):
            t = " ".join(correr("pdftotext", "-enc", "UTF-8", "-f", str(i), "-l", str(i), str(pdf), "-").split())
            if len(t) < MIN_CARACTERES:
                if tesseract:
                    t = " ".join(ocr(pdf, i, tesseract).split())
                    con_ocr.append(i)
                else:
                    sin_texto.append(i)
            paginas.append(t)
        (salida / f"{pdf.stem}.json").write_text(json.dumps(paginas, ensure_ascii=False), encoding="utf-8", newline="\n")
        nota = f", OCR en {len(con_ocr)}" if con_ocr else ""
        nota += f", {len(sin_texto)} SIN TEXTO (requiere OCR)" if sin_texto else ""
        print(f"{pdf.name}: {n} páginas{nota}")
        if manifiesto:
            for m in manifiesto["planes"]:
                if m["clave"] == pdf.stem:
                    m.update(paginas=n, ocr=bool(con_ocr), paginas_ocr=con_ocr, requiere_ocr=sin_texto)
    if manifiesto:
        f_manifiesto.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main(sys.argv[1])
