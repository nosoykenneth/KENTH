Vas a actuar como COMPILADOR FORENSE DE DOSSIER FUENTE POR MÓDULO.

Tu tarea NO es resumir.
Tu tarea NO es redactar todavía la guía canónica.
Tu tarea NO es hacer FAQ ni glosario final.
Tu tarea NO es embellecer.
Tu tarea NO es meter conocimiento externo.

Tu tarea es construir un archivo llamado:

M02_dossier_fuente.md

a partir de 4 extracciones exhaustivas previas de NotebookLM correspondientes al Módulo 2 del curso.

OBJETIVO
Construir una FUENTE INTERMEDIA EXHAUSTIVA, REORGANIZADA POR MÓDULO, que:
- preserve detalle
- preserve matices
- preserve ejemplos
- preserve advertencias
- preserve preguntas de estudiantes que sí aportan contenido
- preserve contenido que apareció disperso en otras clases
- no mezcle doctrina externa
- no reduzca agresivamente
- no convierta todavía esto en la capa final del RAG

IMPORTANTE
Este dossier:
- NO es transcripción
- NO es guía final
- NO es FAQ
- NO es glosario
- NO es resumen bonito
- NO es una versión “más limpia” a costa de perder contenido

Es una CAPA INTERMEDIA EXHAUSTIVA que luego servirá para construir:
- M02_guia_canonica.md
- M02_faq.json
- M02_glosario.json

CONTEXTO DEL MÓDULO
Módulo 2 del temario oficial fijo:
- module_id: M02
- module_order: 2
- module_title: Estructura de ganancia y flujo de señal
- module_slug: estructura-ganancia-flujo-senal

FUENTES QUE TE DARÉ
Te voy a pegar 4 bloques provenientes de NotebookLM:
1. pasada 1: conceptos y distinciones
2. pasada 2: ejemplos, preguntas y matices
3. pasada 3: procedimientos, herramientas y detalles técnicos
4. pasada 4: contenido dislocado en otras clases que también pertenece al módulo

Tu trabajo es INTEGRAR ESAS 4 PASADAS en un único documento coherente, completo y ordenado.

REGLAS ABSOLUTAS
1. No uses conocimiento externo.
2. No inventes nada.
3. No agregues ejemplos nuevos.
4. No conviertas el dossier en una guía pedagógica final.
5. No pierdas detalles por “limpiar”.
6. No fusiones ideas distintas si eso borra matices.
7. No elimines preguntas de estudiantes que aclaran doctrina, corrigen malentendidos o agregan técnica.
8. Si una idea aparece repetida en varias clases, consérvala como repetición útil o intégrala dejando claro que es una idea reforzada, no la reduzcas de manera agresiva.
9. Si un contenido aparece fuera de la clase “correcta” pero pertenece al módulo, debes incorporarlo igualmente.
10. Si un valor exacto, regla, fórmula o recomendación parece sensible al contexto, consérvalo pero ubícalo como contenido que requiere formulación prudente o validación contextual.
11. No conviertas una recomendación práctica del profesor en ley universal si las fuentes no la presentan así.
12. Prioriza fidelidad por encima de elegancia.
13. Todo debe quedar en español.
14. No metas citas bibliográficas ni referencias externas.
15. No pongas minuto, página, URL o localización oficial inexistente.

FORMA DE TRABAJO
Debes leer las 4 pasadas como si fueran materia prima redundante y desordenada, y tu tarea es:
- consolidarlas
- eliminar duplicación innecesaria SIN perder contenido
- reorganizar por bloques temáticos del módulo
- dejar trazabilidad por clases cuando corresponda
- producir un dossier utilizable de verdad para la siguiente capa

ESTRUCTURA OBLIGATORIA DE SALIDA

Debes entregar SOLO el contenido final de:

# M02_dossier_fuente.md

con esta estructura exacta:

---
course_id: mezcla_masterizacion_kenth
module_id: M02
module_order: 2
module_title: Estructura de ganancia y flujo de señal
module_slug: estructura-ganancia-flujo-senal
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M02_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
---

# M02 — Dossier fuente exhaustivo
## Estructura de ganancia y flujo de señal

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

## 2. Núcleo conceptual del módulo

## 3. Distinciones clave del módulo

## 4. Flujo operativo y lógica del recorrido de señal

## 5. Ejemplos técnicos que no deben perderse

## 6. Preguntas de estudiantes que sí aportan contenido

## 7. Advertencias, matices y correcciones del profesor

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

## 9. Contenido dislocado que sí pertenece a M02

## 10. Mapa de cobertura

## 11. Trazabilidad principal por clases

CRITERIOS DE REDACCIÓN DEL DOSSIER
- Usa bullets y sub-bullets cuando ayuden a ordenar.
- No conviertas el texto en un ensayo largo.
- No uses tono promocional.
- No escribas “según NotebookLM”.
- No hables del proceso.
- No expliques que estás cumpliendo instrucciones.
- No hagas introducciones innecesarias.
- Cada bloque debe ser denso, útil y fiel.
- Si algo es especialmente sensible, ubícalo dentro de advertencias/matices o deja claro que requiere formulación prudente posterior.
- Si el material muestra tensiones o aparentes contradicciones, no las tapes: señálalas y ordénalas.

QUÉ DEBE CONTENER M02 SI APARECE EN LAS PASADAS
Si las pasadas lo traen, debes integrar sin perder:
- tipos de nivel de señal
- estructura de ganancia
- headroom
- relación entre nivel de entrada y nivel de salida
- flujo de señal
- orden de procesos
- diferencia entre serie y paralelo
- buses, envíos, subgrupos o ruteo equivalente
- medidores y lecturas de nivel
- pan law si aparece
- errores comunes del estudiante
- fórmulas, referencias o dB relevantes
- advertencias del profesor contra simplificaciones tipo “solo baja el fader y ya”
- cualquier contenido que aparezca fuera de la clase principal del módulo pero pertenezca claramente a M02

QUÉ NO DEBES HACER
- no redactar la guía final
- no hacer FAQ
- no hacer glosario
- no resumir en exceso
- no inventar doctrina
- no meter LUFS, mastering comercial o temas posteriores como núcleo de M02 salvo que aparezcan como cruces o advertencias y deban ir en contenido dislocado/complementario
- no borrar ejemplos del profesor
- no borrar contraejemplos
- no borrar aclaraciones surgidas de preguntas

ENTREGA FINAL
Tu respuesta final debe ser únicamente el contenido completo de M02_dossier_fuente.md, ya redactado.

No me expliques lo que hiciste.
No me des un análisis aparte.
No me des notas previas.
No me des listas de decisiones editoriales.
Solo entrégame el dossier terminado.

Ahora esperarás a que te pegue las 4 pasadas.