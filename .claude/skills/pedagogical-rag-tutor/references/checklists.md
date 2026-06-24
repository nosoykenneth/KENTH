# Checklists: routing, retrieval, generación

Listas operativas para auditar o revisar un cambio en cada etapa. La checklist de
**metadata** vive en [metadata-contract.md](metadata-contract.md); la de
**pruebas** en [testing.md](testing.md). Marca cada ítem con evidencia
(archivo:línea o resultado del endpoint), no de memoria.

---

## Checklist de routing / clasificación

El supervisor decide la ruta y la intención. El defecto estructural típico es
decidir **antes** de hidratar la política pedagógica.

- [ ] **Acceso a la política.** ¿El nodo de routing recibe lección/bloque/
      `concepts`/`delegated_to_tutor` (vía la política canónica) o solo
      `pregunta` + string de contexto? Si solo el string → hallazgo estructural.
- [ ] **Gate de dominio.** ¿"Fuera de dominio" se decide con taxonomía/`concepts`/
      delegación, o con keywords/`domain_hint_terms`/título? Lo segundo produce
      falsos "fuera de dominio".
- [ ] **Título genérico.** Un título no-descriptivo ("Clase 3") con conceptos del
      dominio, ¿sigue clasificándose dentro del dominio?
- [ ] **Términos no soportados.** ¿`unsupported_terms` puede rechazar un término
      que `delegated_to_tutor` cubre? Debe poder anularse por delegación.
- [ ] **"Estudiante perdido".** ¿Se dispara por frases sueltas ("no entiendo")
      aunque la pregunta sea una consulta conceptual normal del curso? Debe exigir
      señal real, no cubierta por un concepto del dominio.
- [ ] **Determinismo.** ¿Las decisiones de alto impacto son deterministas y
      reproducibles, con el LLM solo como desempate de baja consecuencia?
- [ ] **Dominio cableado.** ¿El prompt del clasificador menciona el curso concreto
      ("mezcla y masterizacion") o un DAW? Debe venir del Domain Pack.
- [ ] **Saludo / charla básica.** ¿Se enruta sin LLM y sin exigir evidencia?
- [ ] **Forzar internet.** ¿Solo cuando el usuario lo pide explícitamente?
- [ ] **`suggested_prompts` no se rechazan** ni caen a "ambigua"/"fuera de
      dominio".
- [ ] **Traza:** `selected_route`, `intent` y, si bloquea, `blocked_by` con razón.

---

## Checklist de retrieval

El retrieval debe priorizar la lección activa y nunca "rellenar" una lección vacía
con material ajeno.

- [ ] **Pre-filtro por curso.** ¿La búsqueda está acotada al curso (no global
      ciega)?
- [ ] **Prioridad de lección activa.** En modo lección, ¿se prioriza el material
      de la lección/sección/eje activos por encima del resto?
- [ ] **Transcripción garantizada.** Si la lección tiene transcripción propia, ¿se
      incluye y no se colapsa por dedup?
- [ ] **Sin herencia silenciosa.** Lección sin material propio: ¿el retrieval
      evita traer chunks de **otra** lección y se marca evidencia insuficiente?
- [ ] **Alcance del tema delegado.** Para un tema `delegated_to_tutor` sin
      evidencia, ¿el flujo permite responder sin forzar un retrieval vacío que
      degrade a "no hay evidencia"?
- [ ] **Runtime fuera de la query.** El contexto de actividad (Capa 2) se
      **inyecta** pero **no** se añade a la query vectorial (no contamina la
      búsqueda).
- [ ] **Bloque activo.** Con timestamp, ¿el bloque resuelto orienta el retrieval/
      contexto sin borrar el resto?
- [ ] **Visibilidad vs indexación.** Se respeta `allowed_for_indexing` vs
      `visible_to_student`: un recurso indexado-no-visible aporta conocimiento pero
      **no** se muestra/enlaza al alumno.
- [ ] **Traza:** `retrieval_scope` (curso/eje/sección/lección) y `evidence_level`.

---

## Checklist de generación

La respuesta debe servir al objetivo, respetar restricciones, distinguir fuentes y
no inventar.

- [ ] **Ancla en lo correcto.** Modo lección: responde primero desde la lección/
      bloque; el RAG amplía, no reemplaza. Modo general: orienta sin inventar
      bloque/video.
- [ ] **Cuatro fuentes separadas.** Runtime, evidencia documental, reglas y
      conocimiento general llegan rotulados; el modelo no cita runtime como
      evidencia.
- [ ] **Restricciones impuestas.** `attribution_constraints` presentes en el prompt
      **y** verificadas en la salida (no solo informativas).
- [ ] **Tema delegado bien marcado.** Lo `delegated_to_tutor` se responde como
      **adaptación operativa del tutor**, distinguible del contenido oficial.
- [ ] **Sin recetas universales** si la metadata/constraints lo prohíben.
- [ ] **Insuficiencia declarada.** Sin contexto suficiente, el tutor lo dice; no
      rellena con otra lección ni inventa citas/ubicaciones.
- [ ] **Sin invenciones.** La verificación post-gen elimina citas/ubicaciones
      inventadas y no "promete" ejes/temas futuros sin base.
- [ ] **No truncado.** La respuesta no queda cortada a media frase (límite de
      tokens/streaming).
- [ ] **Sin doble inyección.** Objetivo/acción esperada y similares no aparecen
      duplicados en el contexto que se arma.
- [ ] **Idioma.** Respuesta en español, acorde a la persona del Domain Pack.
- [ ] **Traza:** `applied_policies`, `evidence_level`, `warnings`, y `blocked_by`
      si se recortó algo.
