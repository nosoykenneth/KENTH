#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FASE 1 + FASE 2 — Apuntes del profesor (teacher notes) para la Sección 0.

Este driver toma el contenido canónico (`01_contenido_canonico.md`) de cada
lección de la Sección 0 y produce DOS cosas, de forma reproducible y versionada:

  1) FASE 1 (auditoría de riqueza): compara, por lección, cuántas secciones
     pedagógicas y conceptos aporta el canónico y decide si merece convertirse en
     un "Apunte del profesor" (recurso docente visible) o descartarse.

  2) FASE 2 (materialización): renderiza un PDF LIMPIO de apuntes del profesor
     ("Apuntes del profesor — <título>"), SIN frontmatter YAML, sin course_id,
     lesson_id técnico, source_type, allowed_for_indexing, ingestion_batch_id ni
     ninguna referencia a Chroma/RAG/Markdown. El PDF simula un recurso docente
     normal (lectura de apoyo) que luego se sube por el flujo de recursos del
     profesor y se indexa como resource_text.

El canónico NO se borra: sigue en el repo como semilla/admin. Lo que cambia es la
FUENTE ACTIVA (ver FASE 4/5).

Uso:
    python scripts/section0_teacher_notes.py --out <dir_salida> [--json <ruta>]

No toca la BD ni Chroma. Solo lee .md y escribe PDFs + un JSON de auditoría.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html import escape

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON_ROOT = os.path.join(
    BASE_DIR, "documentos", "oficial", "curso_2", "seccion_00_sistema_decision"
)

# Orden de lecciones y su carpeta canónica (anclado a lesson_id/cmid, no a posición).
LESSONS = [
    ("SEC2-R55", "0.1", "leccion_0_1_mezclar_es_decidir"),
    ("SEC2-R56", "0.2", "leccion_0_2_tu_oido_miente"),
    ("SEC2-R57", "0.3", "leccion_0_3_monitores_y_auriculares"),
    ("SEC2-R58", "0.4", "leccion_0_4_anatomia_universal_mixer_ruteo"),
    ("SEC2-R59", "0.5", "leccion_0_5_gain_staging"),
    ("SEC2-R60", "0.6", "leccion_0_6_nativos_vs_emulaciones"),
    ("SEC2-R61", "0.7", "leccion_0_7_checklist_sesion_lista"),
]

# Secciones del canónico que SÍ son apuntes del profesor (contenido para el
# estudiante). El resto del árbol (guía tutor IA, momentos, rúbrica, manifest,
# atribuciones) es comportamiento/estructura interna y NO va al PDF.
NOTE_SECTIONS = [
    ("Objetivo de aprendizaje", "Objetivo de aprendizaje"),
    ("Idea central", "Idea central"),
    ("Explicación principal", "Explicación"),
    ("Conceptos clave", "Conceptos clave"),
    ("Procedimiento recomendado", "Procedimiento recomendado"),
    ("Criterios de decisión", "Criterios de decisión"),
    ("Errores comunes", "Errores comunes"),
    ("Ejemplo aplicado", "Ejemplo aplicado"),
    ("Qué debe evitar el estudiante", "Qué evitar"),
    ("Resumen final", "Resumen"),
    ("Relación con otras lecciones de la sección", "Conexión con otras lecciones"),
]

# Criterios de riqueza (FASE 1). Convertir si >= 2 presentes.
RICHNESS_KEYS = {
    "objetivo": "Objetivo de aprendizaje",
    "conceptos_clave": "Conceptos clave",
    "procedimiento": "Procedimiento recomendado",
    "criterios_decision": "Criterios de decisión",
    "errores_comunes": "Errores comunes",
    "ejemplo_aplicado": "Ejemplo aplicado",
    "que_evitar": "Qué debe evitar el estudiante",
    "relacion_otras": "Relación con otras lecciones de la sección",
}


def parse_md(path: str):
    raw = open(path, encoding="utf-8").read()
    fm = {}
    body = raw
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        body = m.group(2)
    # Título humano (primera H1) y secciones ## -> texto.
    sections = {}
    cur = None
    buf: list[str] = []
    h1 = ""
    for line in body.splitlines():
        h1m = re.match(r"^#\s+(.*)$", line)
        h2m = re.match(r"^##\s+(.*)$", line)
        if h1m and not h1:
            h1 = h1m.group(1).strip()
            continue
        if h2m:
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            cur = h2m.group(1).strip()
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()
    return fm, h1, sections


def richness(sections: dict):
    present = {k: bool(sections.get(h, "").strip()) for k, h in RICHNESS_KEYS.items()}
    count = sum(1 for v in present.values() if v)
    verdict = "convert_to_teacher_notes_pdf" if count >= 2 else "skip_canonical"
    return present, count, verdict


def _md_inline_to_rl(text: str) -> str:
    """Convierte **negrita** y escapa HTML para Paragraph de reportlab."""
    # Escapamos primero, luego reintroducimos <b>.
    parts = re.split(r"(\*\*.+?\*\*)", text)
    out = []
    for p in parts:
        if p.startswith("**") and p.endswith("**"):
            out.append("<b>" + escape(p[2:-2]) + "</b>")
        else:
            out.append(escape(p))
    return "".join(out)


def build_pdf(out_path: str, lesson_number: str, lesson_title: str, sections: dict):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    base_font, bold_font = "Helvetica", "Helvetica-Bold"
    for reg, bold, fam, fambold in [
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "Arial", "Arial-Bold"),
        ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf", "Segoe", "Segoe-Bold"),
    ]:
        if os.path.exists(reg) and os.path.exists(bold):
            try:
                pdfmetrics.registerFont(TTFont(fam, reg))
                pdfmetrics.registerFont(TTFont(fambold, bold))
                base_font, bold_font = fam, fambold
                break
            except Exception:
                pass

    styles = getSampleStyleSheet()
    h_title = ParagraphStyle("t", parent=styles["Title"], fontName=bold_font, fontSize=18, leading=22, spaceAfter=4)
    h_sub = ParagraphStyle("s", parent=styles["Normal"], fontName=base_font, fontSize=10.5, textColor="#555555", spaceAfter=14)
    h_head = ParagraphStyle("h", parent=styles["Heading2"], fontName=bold_font, fontSize=13, leading=16, spaceBefore=12, spaceAfter=5, textColor="#1a3c5e")
    body = ParagraphStyle("b", parent=styles["Normal"], fontName=base_font, fontSize=10.8, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=7)

    doc = SimpleDocTemplate(
        out_path, pagesize=A4, title=f"Apuntes del profesor — {lesson_title}",
        author="Equipo docente", leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    flow = [
        Paragraph(f"Apuntes del profesor — {escape(lesson_title)}", h_title),
        Paragraph(f"Sección 0 · El sistema de decisión · Lección {lesson_number}", h_sub),
    ]
    for canon_head, note_head in NOTE_SECTIONS:
        txt = sections.get(canon_head, "").strip()
        if not txt:
            continue
        flow.append(Paragraph(escape(note_head), h_head))
        for para in re.split(r"\n\s*\n", txt):
            para = para.strip()
            if para:
                flow.append(Paragraph(_md_inline_to_rl(para), body))
    doc.build(flow)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="dir de salida para los PDFs")
    ap.add_argument("--json", default="", help="ruta del JSON de auditoría (FASE 1)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    audit = []
    for lesson_id, num, folder in LESSONS:
        path = os.path.join(CANON_ROOT, folder, "01_contenido_canonico.md")
        if not os.path.exists(path):
            audit.append({"lesson_id": lesson_id, "error": f"no existe {path}"})
            continue
        fm, h1, sections = parse_md(path)
        lesson_title = fm.get("lesson_title") or re.sub(r"^[0-9.]+\s*[—-]\s*", "", h1)
        present, count, verdict = richness(sections)
        body_words = sum(len(v.split()) for v in sections.values())
        note_words = sum(len(sections.get(h, "").split()) for h, _ in NOTE_SECTIONS)
        pdf_name = f"apuntes_profesor_leccion_{num.replace('.', '_')}.pdf"
        pdf_path = os.path.join(args.out, pdf_name)
        if verdict == "convert_to_teacher_notes_pdf":
            build_pdf(pdf_path, num, lesson_title, sections)
        audit.append({
            "lesson_id": lesson_id,
            "lesson_number": num,
            "lesson_title": lesson_title,
            "canonical_path": os.path.relpath(path, BASE_DIR).replace("\\", "/"),
            "canonical_words": body_words,
            "note_words": note_words,
            "sections_present": [h for h in sections if sections[h].strip()],
            "richness_criteria": present,
            "richness_count": count,
            "verdict": verdict,
            "pdf": pdf_name if verdict == "convert_to_teacher_notes_pdf" else None,
        })
        print(f"[{lesson_id}] {num} '{lesson_title}': {count}/8 criterios -> {verdict}"
              + (f" -> {pdf_name}" if verdict == 'convert_to_teacher_notes_pdf' else ""))

    if args.json:
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        json.dump(audit, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"\nAuditoría FASE 1 -> {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
