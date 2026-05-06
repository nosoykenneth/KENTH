Vas a trabajar a partir de un dossier fuente exhaustivo ya compilado para un módulo del curso.

Tu tarea es convertir ese dossier en la capa canónica del RAG del módulo, generando exactamente 3 archivos:

1. M0X_guia_canonica.md
2. M0X_faq.json
3. M0X_glosario.json

OBJETIVO
Condensar el dossier en una capa canónica útil para el tutor IA, sin perder el núcleo doctrinal del módulo, pero sin intentar volcar todo el dossier dentro de la guía.

IMPORTANTE
- El dossier ya contiene el detalle exhaustivo del módulo.
- NO debes usar conocimiento externo.
- NO debes inventar doctrina.
- NO debes inventar páginas, minutos, URLs, clases, PDFs ni localizaciones oficiales.
- NO debes mencionar NotebookLM.
- NO debes presentar la fuente como “transcripciones de clases”.
- NO debes decir que el origen son “las clases”.
- Debes presentar el material como parte del curso y como compilación autoral del módulo.
- Mantén consistencia con el estilo del proyecto:
  - tono prudente
  - borrador autoral
  - requires_validation cuando corresponda
  - sin absolutismos innecesarios

REGLAS ABSOLUTAS
1. La guía canónica no debe intentar contener todo el dossier.
2. La guía debe ordenar y delimitar la doctrina principal del módulo.
3. El FAQ debe responder dudas probables del estudiante sin inventar.
4. El glosario debe definir términos clave del módulo con precisión y prudencia.
5. Si una afirmación del dossier es fuerte pero sensible al contexto, consérvala con formulación prudente o márcala con requires_validation.
6. No conviertas ejemplos del profesor en reglas universales.
7. No mezcles contenidos de otros módulos como núcleo, salvo cruces breves cuando sean realmente necesarios.
8. Mantén consistencia estricta de:
   - course_id
   - module_id
   - module_order
   - module_title
   - module_slug
9. El estado inicial de los 3 archivos debe ser:
   - draft_author_review
10. Debes usar un schema rico y consistente entre módulos.

INSTRUCCIONES DE METADATA

### A. Para la guía canónica
Debes usar este esquema de frontmatter:

---
course_id: mezcla_masterizacion_kenth
module_id: M0X
module_order: X
module_title: [TITULO OFICIAL DEL MODULO]
module_slug: [SLUG OFICIAL DEL MODULO]
short_description: [descripcion breve y sobria del alcance del modulo]
learning_scope: [alcance de aprendizaje delimitado del modulo]
doc_type: canonical_guide
resource_type: markdown
source_origin: course
filename: M0X_guia_canonica.md
version: 0.1
status: draft_author_review
curation_source: borrador_autoral_m0x
requires_validation: true
---

### B. Para el FAQ
Debes usar este esquema JSON superior:

{
  "course_id": "mezcla_masterizacion_kenth",
  "module_id": "M0X",
  "module_order": X,
  "module_title": "[TITULO OFICIAL DEL MODULO]",
  "module_slug": "[SLUG OFICIAL DEL MODULO]",
  "short_description": "[descripcion breve y sobria]",
  "learning_scope": "[alcance delimitado del modulo]",
  "doc_type": "faq",
  "source_origin": "course",
  "filename": "M0X_faq.json",
  "version": "0.1",
  "status": "draft_author_review",
  "curation_source": "borrador_autoral_m0x",
  "items": [...]
}

Cada item del FAQ debe tener este schema:

{
  "faq_id": "M0X_FAQ_001",
  "question": "...",
  "canonical_answer": "...",
  "short_answer": "...",
  "stable_answer": "...",
  "pending_validation_notes": [],
  "brand_or_model_mentions": [],
  "topic": "...",
  "learning_objective": "...",
  "tags": ["..."],
  "evidence_sources": [],
  "do_not_say": [],
  "requires_validation": true
}

### C. Para el glosario
Debes usar este esquema JSON superior:

{
  "course_id": "mezcla_masterizacion_kenth",
  "module_id": "M0X",
  "module_order": X,
  "module_title": "[TITULO OFICIAL DEL MODULO]",
  "module_slug": "[SLUG OFICIAL DEL MODULO]",
  "short_description": "[descripcion breve y sobria]",
  "learning_scope": "[alcance delimitado del modulo]",
  "doc_type": "glossary",
  "source_origin": "course",
  "filename": "M0X_glosario.json",
  "version": "0.1",
  "status": "draft_author_review",
  "curation_source": "borrador_autoral_m0x",
  "terms": [...]
}

Cada término del glosario debe tener este schema:

{
  "term_id": "M0X_TERM_001",
  "term": "...",
  "abbreviation": "",
  "definition": "...",
  "stable_definition": "...",
  "pending_validation_notes": [],
  "brand_or_model_mentions": [],
  "topic": "...",
  "tags": ["..."],
  "common_confusion": "...",
  "requires_validation": true
}

CRITERIOS DE REDACCIÓN

### Guía canónica
- Debe ser doctrinal, ordenada y sobria.
- No debe ser una lista de todo lo que existe en el dossier.
- Debe explicar:
  - propósito del módulo
  - objetivo de aprendizaje
  - teoría central del módulo
  - preguntas guía para el tutor IA
  - límites doctrinales del borrador
  - cierre del módulo
- Debe sonar como documento canónico de trabajo, no como apunte de clase.
- No debe hablar de “el profesor dijo en clase”.
- No debe mencionar transcripciones.
- No debe mencionar que proviene de clases.
- Puede decir “en este módulo”, “el material del curso”, “el curso trabaja”, “el módulo distingue”, etc.

### FAQ
- Debe priorizar preguntas reales y probables del estudiante.
- Las respuestas deben ser prudentes y útiles para un tutor IA.
- No deben sonar promocionales ni excesivamente largas.
- Deben evitar inventar universalidad.
- Usa `do_not_say` cuando convenga bloquear malas simplificaciones.

### Glosario
- Define términos realmente útiles para el módulo.
- No metas relleno.
- Si un término es sensible, marca requires_validation.
- En `common_confusion`, registra el error típico que no conviene reforzar.

QUÉ NO DEBES HACER
- no usar doc_type como "guia_canonica"; debe ser "canonical_guide"
- no usar schemas mínimos pobres si ya existe un schema más rico
- no dejar metadata incompleta
- no dejar el origen como “transcripciones”
- no decir “fuente: clases”
- no poner localización oficial inventada
- no convertir el dossier en el texto final entero
- no meter actividades, recursos ni errores comunes en estos 3 archivos
- no hacer referencias a fase 2 del proyecto dentro de los archivos
- no generar archivos extra

ENTREGA
Quiero que entregues, en este orden:

A. M0X_guia_canonica.md
B. M0X_faq.json
C. M0X_glosario.json

Cada archivo debe quedar completo y listo para copiar al repo.

No me expliques el proceso.
No me des observaciones.
No me des un resumen aparte.
Solo entrega los 3 archivos completos.

Ahora esperarás a que te pegue el dossier fuente del módulo.