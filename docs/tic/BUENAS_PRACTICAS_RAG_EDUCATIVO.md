# Buenas prácticas de RAG educativo — el flujo docente de TIC-KENTH

> Documento de referencia (académico/profesional) que justifica por qué el tutor de
> IA se alimenta desde un **flujo docente controlado** y no desde archivos ocultos.
> Es también material de sustentación para la tesis (Capítulo IV / discusión).

## 1. Problema: el corpus oculto no validado

Un tutor RAG responde con lo que hay indexado. Si ese índice se llena con archivos
Markdown/YAML que el docente nunca ve ni aprueba (un "corpus oculto"), aparecen tres
riesgos de gobernanza:

1. **Falta de control docente**: el profesor no puede saber —ni corregir— qué sabe el
   tutor sobre su clase, aunque él es el responsable pedagógico.
2. **Falta de trazabilidad**: no queda claro de qué material salió cada respuesta ni
   quién lo aprobó.
3. **Riesgo de alucinación y de fuga**: material interno (guías del tutor, rúbricas,
   atribuciones, manifiestos técnicos) puede filtrarse como si fuera contenido del
   estudiante.

En TIC-KENTH ese corpus oculto existía como semilla técnica: los `.md` canónicos bajo
`tesis-rag/documentos/oficial/curso_2/...`. Sirvieron para arrancar, pero **no son un
flujo defendible** para que un profesor real alimente al tutor.

## 2. Principio rector: human-in-the-loop

La evidencia que usa el tutor debe pasar por una **persona responsable** (el docente)
antes de convertirse en conocimiento activo. No se indexa nada "automágico": se indexa
lo que el profesor aprueba desde la interfaz. Esto alinea el sistema con las buenas
prácticas de IA educativa: **control docente, transparencia, trazabilidad y
evaluación**.

## 3. El flujo docente de alimentación del RAG

El profesor alimenta al tutor **sin tocar Markdown, YAML ni Chroma**, en cuatro gestos:

| Gesto en la interfaz | Qué produce | Naturaleza |
|---|---|---|
| Aprobar la **transcripción** | `transcript` indexado | conocimiento (evidencia) |
| **Preparar tutor con IA** → aceptar | `teacher_approved_context` | conocimiento (evidencia) |
| **Subir recursos** (PDF/imagen/FLP/audio) | `resource_text` / `resource_description` | conocimiento (evidencia) |
| Editar tono/nivel/reglas del tutor | perfil de comportamiento | comportamiento (se **inyecta**) |
| **Publicar cambios del tutor** | reindexa incremental esa lección | operación |

### 3.1 La transcripción se aprueba antes de indexarse

La transcripción cruda de Whisper es un borrador, no evidencia. Con el flag
`INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL` (default en producción) queda en estado
`generated_pending_review` y **no se indexa** hasta que el profesor la aprueba o
edita. Así el tutor nunca cita texto que nadie revisó.

### 3.2 Los recursos se transforman a texto indexable

- **PDF/TXT** → se extrae su texto y se indexa como `resource_text` (el estudiante lo
  descarga; el tutor lo usa como evidencia).
- **Imágenes, plantillas de DAW (.flp/.als), audio, stems** → su **binario NUNCA se
  indexa**. Lo buscable es la **descripción pedagógica** que escribe el profesor,
  indexada como `resource_description`, con un puntero al archivo para poder mostrarlo
  o enlazarlo. El tutor puede explicar "qué contiene el proyecto `0_5_gain_staging_hot.flp`"
  aunque nunca "lea" el binario.

### 3.3 Inject vs. index: comportamiento ≠ evidencia

Dos naturalezas que no deben mezclarse:

- **Comportamiento** (tono, nivel de ayuda, reglas privadas, `tutor_must_not_do`,
  mensajes proactivos, prompts sugeridos) → se **inyecta** en el prompt del tutor. No
  es evidencia; nunca se indexa.
- **Conocimiento** (objetivo, resumen, conceptos, errores comunes, preguntas
  probables, momentos, transcripción, descripciones de recursos) → se **materializa e
  indexa** como evidencia recuperable.

Separarlos evita que reglas internas se recuperen como "contenido" y que el tutor
confunda "cómo debo comportarme" con "qué sé de la clase".

## 4. Trazabilidad por `course_id`, `section_id`, `lesson_id`

Cada chunk lleva `course_id`, `moodle_section_id` y `lesson_id`. Esto permite:

- **Retrieval acotado** por lección (una lección vacía no responde con otra).
- **Auditoría**: contar por lección y por tipo de fuente (`canonical_md`, `transcript`,
  `teacher_approved_context`, `resource_text`, `resource_description`).
- **Supersesión quirúrgica**: retirar una fuente de una sección sin tocar el resto.

## 5. Evaluación de retrieval y de generación

No basta con "responde": se mide.

- **Retrieval**: batería de preguntas por lección; se verifica que las fuentes citadas
  sean de la lección correcta (no de otra) y del tipo correcto.
- **Generación**: se comprueba que la respuesta esté **grounded** en la evidencia y que
  el sistema **rechace fuera de dominio**. La verificación post-generación elimina
  citas/ubicaciones inventadas.

## 6. Por qué se evita el corpus oculto no validado por el docente

El corpus `canonical_md` de la Sección 0 dejó de ser **fuente activa**: quedó como
**semilla/admin** en disco (no se borra), pero no se indexa como evidencia. Su valor
pedagógico no se pierde: el contenido rico de cada lección se convirtió en un
**"Apunte del profesor" (PDF visible)** que el docente sube por el flujo normal, y que
el tutor usa como `resource_text`. Resultado: **nada que el tutor sepa de la Sección 0
escapa al control del docente**.

La política es configurable y no arriesga otras secciones
(`RAG_SECTION0_SOURCE_MODE ∈ {hybrid, teacher_flow, canonical_only}`; default de
producción `teacher_flow` solo para la sección declarada).

## 7. Alineación con buenas prácticas de IA educativa

| Principio | Cómo lo cumple TIC-KENTH |
|---|---|
| **Control docente del material** | Todo lo que sabe el tutor lo aprobó el profesor desde la interfaz. |
| **Privacidad** | El binario del alumno/material sensible no se embebe; se controla `visible_to_student`. |
| **Trazabilidad** | Metadata `course/section/lesson` + tipo de fuente en cada chunk. |
| **Transparencia** | "Gestión del Tutor" muestra conteos por fuente sin exponer Chroma/YAML. |
| **Evaluación** | Batería de retrieval + verificación de grounding y rechazo fuera de dominio. |
| **Reducción de alucinación** | Solo evidencia aprobada; verificación post-generación; sin corpus oculto. |
| **Gobernanza de contenido** | Semilla ≠ evidencia; inject ≠ index; supersesión auditable y reversible. |

## 8. Justificación del cambio de corpus canónico manual a flujo docente de recursos indexables (para la tesis)

**Antes.** El conocimiento de la Sección 0 vivía en 208 chunks `canonical_md`
generados desde archivos Markdown con frontmatter YAML que el docente no manipulaba ni
veía. Era funcional pero **no defendible como flujo real**: mezclaba contenido del
estudiante con material interno (guías del tutor, rúbricas, manifiestos), no era
trazable a una acción del docente y no podía auditarse por tipo de fuente.

**Cambio.** Se adoptó un **flujo docente teacher-driven**: (1) la transcripción se
aprueba y se indexa; (2) "Preparar tutor con IA" materializa un contexto aprobado por
lección; (3) los recursos reales (guías PDF, diagramas, proyectos de DAW, audio,
stems) se suben por el flujo del profesor y se indexan como texto o como descripción;
(4) el contenido canónico rico se transformó en "Apuntes del profesor" (PDF visible)
como un recurso docente más. El Markdown canónico se conservó como semilla y dejó de
ser fuente activa.

**Por qué es mejor (defensa).**
- **Responsabilidad y control**: el docente es dueño y editor de todo el material del
  tutor; no hay conocimiento sin su aprobación.
- **Trazabilidad y auditoría**: cada chunk se ancla a curso/sección/lección y a un tipo
  de fuente, lo que permite medir y superseder con precisión.
- **Reducción de alucinación y de fuga**: se elimina el corpus oculto no validado y se
  separa comportamiento (inyectado) de evidencia (indexada).
- **Evaluabilidad**: el sistema se valida con baterías de retrieval y pruebas de
  grounding, condición del contrato de precisión medible de la tesis (OE4).
- **Reproducibilidad**: la conversión (canónico→apuntes), la subida de recursos y la
  supersesión están versionadas como scripts y datos, no como pasos manuales.

En síntesis: se pasa de "el sistema sabe cosas que el profesor no controla" a "el
profesor gobierna, con trazabilidad y evaluación, todo lo que el tutor sabe de su
clase". Ese es el estándar esperable de una herramienta de IA educativa.
