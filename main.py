import os
import re
import fitz  # PyMuPDF
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

CARPETA_ENTRADA = "entrada"
CARPETA_SALIDA = "informes"
LOGO_PATH = "gomind_logo.png"

def extraer_texto_pdf(ruta_pdf):
    try:
        with fitz.open(ruta_pdf) as doc:
            return "\n".join(p.get_text() for p in doc)
    except Exception as e:
        print(f"[ERROR] {ruta_pdf}: {e}")
        return None

def extraer_datos(texto):
    def buscar(patron, tipo=str):
        try:
            return tipo(re.search(patron, texto).group(1).strip())
        except:
            return None
    return {
        "nombre_original": buscar(r"Paciente\s*:\s*([A-ZÑÁÉÍÓÚ\s]+)"),
        "edad": buscar(r"Edad\s*:\s*(\d+)", int),
        "sexo": buscar(r"Sexo\s*:\s*(\w+)"),
        "creatinina": buscar(r"Creatinina\s*:\s*([\d,]+)", lambda x: float(x.replace(",", "."))),
        "glucosa": buscar(r"Glicemia Basal\s*:\s*([\d,]+)", lambda x: float(x.replace(",", "."))),
        "colesterol": buscar(r"Colesterol Total\s*:\s*([\d,]+)", lambda x: float(x.replace(",", "."))),
        "proteinas_orina": buscar(r"Proteinas\s*:\s*(\w+)"),
        "glucosa_orina": buscar(r"Glucosa\s*:\s*(\w+)"),
    }

def generar_observaciones(d):
    obs = []
    if d["glucosa"] and d["glucosa"] > 110:
        obs.append("Glucosa elevada (posible prediabetes o diabetes).")
    if d["colesterol"] and d["colesterol"] > 200:
        obs.append("Colesterol total elevado (riesgo cardiovascular).")
    if d["creatinina"] and d["creatinina"] > 1.3:
        obs.append("Creatinina elevada (posible disfunción renal).")
    if d["proteinas_orina"] and "positivo" in d["proteinas_orina"].lower():
        obs.append("Proteínas en orina (posible daño renal).")
    if d["glucosa_orina"] and "positivo" in d["glucosa_orina"].lower():
        obs.append("Glucosa en orina (posible diabetes no controlada).")
    return obs

def generar_recomendaciones(d):
    rec = []
    if d["glucosa"] and d["glucosa"] > 110:
        rec.append("Reducir consumo de azúcares y carbohidratos simples.")
    if d["colesterol"] and d["colesterol"] > 200:
        rec.append("Disminuir grasas saturadas, aumentar fibra y actividad física.")
    if d["creatinina"] and d["creatinina"] > 1.3:
        rec.append("Consultar con nefrólogo para evaluación renal.")
    return rec

def generar_pdf(d, observaciones, recomendaciones, salida_pdf):
    os.makedirs(os.path.dirname(salida_pdf), exist_ok=True)
    c = canvas.Canvas(salida_pdf, pagesize=letter)
    width, height = letter
    y = height - 50

    if os.path.exists(LOGO_PATH):
        try:
            c.drawImage(ImageReader(LOGO_PATH), 40, y - 20, width=80, preserveAspectRatio=True)
        except Exception as e:
            print(f"[LOGO ERROR] {e}")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(140, y, "INFORME CLÍNICO ANÓNIMO")
    y -= 40

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Fecha: {datetime.now().strftime('%d-%m-%Y')}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Datos del paciente:")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"Edad: {d['edad']} años   |   Sexo: {d['sexo']}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Resultados clínicos:")
    y -= 15
    resultados = [
        f"Glucosa: {d['glucosa']} mg/dL",
        f"Colesterol Total: {d['colesterol']} mg/dL",
        f"Creatinina: {d['creatinina']} mg/dL",
        f"Proteínas en orina: {d['proteinas_orina']}",
        f"Glucosa en orina: {d['glucosa_orina']}"
    ]
    for r in resultados:
        c.drawString(60, y, r)
        y -= 15

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Observaciones:")
    y -= 15
    for o in (observaciones or ["Sin observaciones relevantes."]):
        c.drawString(60, y, f"- {o}")
        y -= 15

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Recomendaciones:")
    y -= 15
    for r in (recomendaciones or ["Mantener hábitos saludables."]):
        c.drawString(60, y, f"- {r}")
        y -= 15

    c.save()

def procesar_todos_los_archivos():
    archivos = [f for f in os.listdir(CARPETA_ENTRADA) if f.lower().endswith(".pdf")]
    for i, nombre in enumerate(archivos, 1):
        ruta = os.path.join(CARPETA_ENTRADA, nombre)
        texto = extraer_texto_pdf(ruta)
        if not texto:
            continue
        datos = extraer_datos(texto)
        obs = generar_observaciones(datos)
        recs = generar_recomendaciones(datos)
        nombre_limpio = datos["nombre_original"].strip().lower().replace(" ", "_") if datos["nombre_original"] else f"paciente_{i}"
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        salida = os.path.join(CARPETA_SALIDA, f"{fecha}_{nombre_limpio}_informe.pdf")
        generar_pdf(datos, obs, recs, salida)
        print(f"[{i}] ✅ Generado: {salida}")

if __name__ == "__main__":
    procesar_todos_los_archivos()
