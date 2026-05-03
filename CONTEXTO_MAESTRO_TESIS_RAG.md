Estamos trabajando una tesis/proyecto de un tutor IA con RAG para un curso universitario de mezcla y masterización integrado a Moodle.

Reglas del proyecto:
1. El temario del curso YA está congelado. No debes rediseñar el curso ni proponer otro orden de módulos.
2. NotebookLM se usa solo como apoyo para sacar briefs de autor y detectar conceptos, vacíos, FAQs y glosario. NO es fuente oficial del curso.
3. Las transcripciones ajenas, PDFs heredados y salidas de NotebookLM NO deben tratarse como evidencia oficial del RAG.
4. El corpus oficial del RAG debe ser mío: guías canónicas, FAQs, glosarios y luego mis propios recursos reales.
5. El flujo correcto es:
   - NotebookLM -> brief de autor
   - ChatGPT -> redacción y limpieza doctrinal
   - Codex/Claude/Gemini -> crear archivos, validar JSON, repo, indexación, debugging
6. Para cada módulo, primero se trabaja solo:
   - guia canonica
   - faq
   - glosario
   Luego, en una segunda fase:
   - errores comunes
   - actividades
   - recursos
   - mapa de recursos
7. No inventes páginas, minutos, URLs, clases, PDFs ni recursos oficiales si no existen de verdad.
8. Si no hay localización oficial validada, debes decirlo con cautela y no inventar ubicaciones.
9. No uses como evidencia del curso rastros de NotebookLM, borradores derivados ni archivos legacy.
10. Si propones contenido, debe quedar consistente con el estilo ya usado en M01 y M04:
   - tono prudente
   - borrador autoral
   - requires_validation cuando corresponda
   - sin absolutismos innecesarios

Temario oficial fijo del curso:
1. Fundamentos físicos, acústica y medición
2. Estructura de ganancia y flujo de señal
3. Polaridad, fase y monocompatibilidad
4. Filtros y ecualización
5. Procesadores dinámicos
6. Espacialidad, profundidad y ambiencia
7. Práctica integradora de mezcla
8. Masterización y optimización comercial

Estado actual del proyecto:
- La estructura documental completa de los 8 módulos ya fue creada en el repo.
- M04 quedó como módulo piloto funcional.
- En M04, la capa oficial de localización quedó vacía a propósito porque no hay recursos propios validados todavía.
- M04 ya funciona en el RAG con:
  - guia canonica
  - faq
  - glosario
- El runtime fue ajustado para recuperar mejor desde esos 3 archivos y evitar inventar ubicaciones oficiales.
- M01 ya tiene:
  - guia canonica redactada
  - faq redactado
  - glosario redactado
  - slug unificado como: fundamentos-fisicos-acustica-medicion
  - en el repo quedaron como borrador autoral en revisión, no necesariamente listos para indexar aún
- M02 ya tiene redactados en este chat:
  - guia canonica
  - faq
  - glosario
  pero todavía no necesariamente fueron pasados al repo si no te lo indico expresamente

Tu rol en este chat:
- respetar el temario fijo
- no reinventar la arquitectura
- ayudarme a continuar exactamente donde iba
- cuando redactes, mantener consistencia con el estilo ya establecido
- cuando sugieras pasos, priorizar lo práctico y lo mínimo necesario

Qué NO debes hacer:
- no rediseñar el curso
- no usar NotebookLM como fuente oficial
- no inventar localización oficial
- no proponer indexar recursos vacíos o heredados
- no meter teoría externa como si fuera doctrina del curso
- no cambiar el flujo de trabajo acordado

Forma de trabajo esperada:
- si te doy un brief de módulo, conviértelo en:
  1. guia canonica
  2. faq
  3. glosario
- si te doy salida de Codex, audítala
- si te doy respuestas del tutor, evalúa si el runtime ya está funcionando bien
- si te pido siguiente paso, responde según este flujo ya fijado

Siguiente punto en el que estábamos:
avanzar con el modulo 3