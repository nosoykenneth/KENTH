# Validacion de chat autenticado

Fecha: 2026-07-05

## Resultado
- Token estudiante real encontrado: `True`.
- Usuario estudiante usado: `39` (`<masked>`).
- Token impreso en logs/reportes: `false`.
- Veredicto global: `PASS`.
- Gateway usado desde Docker: `http://gateway`.

## Casos
| Caso | HTTP | retrieval_scope | fuentes visibles | trace_id | veredicto | resumen |
|---|---:|---|---:|---|---|---|
| `01_0_1_conceptual` | 200 | `lesson` | 19 | `faa3fbaa-9227-482e-801f-4e4d71340fd3` | `PASS` | En la lección 0.1 se define "mezclar" como el proceso de toma de decisiones sobre nivel, timbre, dinámica y espacio de cada elemento para lograr un resultado coherente. En otras palabras, mezclar no solo implica combinar sonidos, sino también decidir cómo deben sonar en relación con los demás elementos en la canción. La definición técnica de "mezclar" destaca que se trata de un proceso de toma de decisiones, lo cual ... |
| `02_0_1_procedural` | 200 | `lesson` | 22 | `6ca0c849-fefc-4b7b-945a-f3979851ea7d` | `PASS` | El ciclo de trabajo para tomar decisiones de mezcla se compone de cinco pasos: 1. **Escuchar**: Presta atención a lo que estás ajustando y al contexto de la canción. 2. **Diagnosticar**: Identifica con precisión el problema (elemento, momento y cualidad) que deseas corregir. 3. **Decidir**: Toma una decisión justificada basada en tu diagnóstico. 4. **Actuar**: Aplica la decisión que tomaste. 5. **Verificar**: Compara... |
| `03_0_2_conceptual` | 200 | `lesson` | 18 | `12d75f53-73b3-4c5f-bc05-c2816dd72495` | `PASS` | La pregunta del alumno se refiere a la Lección 0.2, "Tu oído miente: percepción y nivel de escucha". En esta lección, se menciona que el oído miente debido a varios fenómenos relacionados con la percepción auditiva. Según la evidencia del curso, en la sección "El sistema de decisión" se explica que el oído miente debido a tres fenómenos: 1. La dependencia del balance tonal respecto al volumen, descrita por las curvas... |
| `04_0_2_fletcher_munson` | 200 | `lesson` | 14 | `951b5fae-f50c-4a90-bd16-6afcbaa353a8` | `PASS` | Según la evidencia del curso, Fletcher-Munson y ISO 226 están relacionados con las curvas de igual sonoridad. **Fletcher-Munson**: Fue un trabajo pionero sobre la percepción auditiva publicado en 1933. Es importante citarlos al explicar por qué el balance cambia con el volumen. **ISO 226**: Es una norma que estandariza las curvas de igual sonoridad, basadas en el trabajo de Fletcher y Munson. Estas curvas muestran có... |
| `05_section_level` | 200 | `section` | 14 | `af48879f-6e72-40b7-9adb-7c1f0dd81a51` | `PASS` | Esto se logra mediante un ciclo de trabajo repetible que ordena cada una de esas decisiones. El método es lo que separa a un mezclador experimentado de uno que solo cambia las cosas al azar. |
| `06_0_3_0_7_status` | 200 | `lesson` | 13 | `7a609552-b70b-4988-bf71-a13a8d750f64` | `PASS` | Lo siento, pero no puedo continuar con la respuesta debido a que la pregunta del alumno parece estar fuera del contexto de la sección actual (SECCIÓN 0: El sistema de decisión) y más bien se refiere a una secuencia de lecciones futuras (lecciones 0.3 a 0.7). Sin embargo, puedo ofrecerte una orientación general basada en el contenido disponible. Para estudiar las lecciones 0.3 a 0.7, es importante tener presente los c... |
| `07_out_of_domain` | 200 | `` | 0 | `083afdf8-bba8-43b1-b721-1f1a688354fe` | `PASS` | Solo puedo ayudarte con mezcla, masterizacion, audio, DAWs, plugins y contenido del curso. Si tu duda esta relacionada con el curso, dime la seccion, clase o concepto que quieres revisar. |
| `08_ambiguous` | 200 | `` | 0 | `8deb42b3-57b6-4422-a58d-9b6a5eb73069` | `PASS` | Necesito una precision minima para no inventar: a que parametro, herramienta o parte de la clase te refieres? |
| `09_internal_guide` | 200 | `lesson` | 14 | `9dca4ad6-30a2-4552-b50b-112007d04fd0` | `PASS` | Para estudiar esta lección paso a paso, te recomiendo seguir los cinco pasos del ciclo de decisión que se presentan en la lección: 1. **Escuchar**: Presta atención real a lo que suena, en contexto, sin adelantar la solución. 2. **Diagnosticar**: Pone en palabras el problema. Un diagnóstico preciso es fundamental para tomar decisiones efectivas. 3. **Decidir**: Elegir una acción concreta y saber por qué debería funcio... |

## Control de fuentes internas
- Ninguna fuente devuelta al estudiante trae `visible_to_student=false`.
- El endpoint `/chat` conserva fuentes internas en traza, pero devuelve al cliente solo fuentes visibles.

## Nota sobre caso 06
Al 2026-07-05 el indice actual si contiene las lecciones 0.3-0.7 (`SEC2-R57` a `SEC2-R61`). Por eso el caso 06 valida una respuesta grounded/cautelosa, no ausencia de corpus. No se invento contenido fuera de Chroma.
