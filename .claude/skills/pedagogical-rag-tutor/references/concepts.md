# Conceptos y reglas de diseño

Modelo mental durable y **agnóstico al curso**. Léelo antes de auditar o
implementar. Define la jerarquía de contexto, los dos modos del tutor, las
representaciones canónicas que evitan duplicar lógica, y las reglas de diseño que
mantienen el sistema reutilizable.

## Tabla de contenido
1. La jerarquía de contexto como autoridad
2. Las cuatro fuentes (no las mezcles)
3. Los dos modos del tutor
4. Representaciones canónicas (contexto del alumno, política pedagógica)
5. Niveles de evidencia y la diferencia "ausencia ≠ fuera de dominio"
6. Determinismo vs LLM en compuertas
7. Observabilidad como contrato
8. Reglas de diseño (catálogo completo)

---

## 1. La jerarquía de contexto como autoridad

El tutor recibe información de siete capas. La regla no es solo "concaténalas en
el prompt": es que cada capa tiene **autoridad** sobre la de menor número cuando
hay conflicto, y que las decisiones (rutas, gates) deben poder mirar las capas
altas antes de ejecutarse.

1. **Reglas del sistema** — seguridad, integridad académica, anti-trampa. Única
   capa que puede vetar una capacidad delegada por la lección.
2. **Configuración del curso** (Domain Pack) — persona, taxonomía, léxico,
   listas allow/deny, FAQ controladas. Es *datos*, no código.
3. **Metadata de la lección activa** — objetivo, criterios, prerrequisitos,
   delegaciones, restricciones, prompts sugeridos.
4. **Metadata del bloque activo** — foco, conceptos, preguntas probables, modo,
   resumen de lo que ocurre en pantalla (resuelto por timestamp).
5. **Evidencia RAG** — chunks recuperados del corpus aprobado.
6. **Conocimiento general autorizado** — lo que el tutor puede aportar como
   adaptación operativa cuando la lección lo delega, marcándolo como tal.
7. **Historial y progreso** — turnos recientes, conceptos vistos, señales
   blandas (parece perdido/frustrado).

**Implicación operativa #1:** una compuerta global (capa 1/2) no puede tumbar
algo que la capa 3/4 habilitó, salvo veto de seguridad. Si el código bloquea una
pregunta sobre un término que `delegated_to_tutor` cubre, la jerarquía está
invertida.

**Implicación operativa #2:** las decisiones tempranas (routing, clasificación,
gate de dominio) que solo ven la pregunta cruda + un string de contexto están
*ciegas* a las capas 3-4. Eso es un anti-patrón estructural: el orden correcto es
**hidratar contexto → decidir**, no **decidir → hidratar**.

## 2. Las cuatro fuentes (no las mezcles)

El modelo recibe texto de cuatro orígenes con semántica distinta. Conviértelos en
secciones rotuladas y nunca disfraces una de otra:

| Fuente | Qué es | Qué NO es |
|---|---|---|
| **Reglas del sistema** | Constitución del tutor, persona, prohibiciones | Evidencia factual del curso |
| **Contexto runtime** | Dónde está el alumno ahora: lección/bloque/sección/timestamp, señales | Evidencia documental citable |
| **Evidencia documental (RAG)** | Chunks del corpus aprobado | Política de comportamiento |
| **Conocimiento general autorizado** | Adaptación operativa que la lección delega | Contenido oficial del curso |

El error clásico: inyectar `probable_questions` o `proactive_message` (runtime) y
que el modelo los cite como si fueran contenido del curso. El render debe
etiquetar explícitamente "NO ES EVIDENCIA RAG" / "pistas runtime" y la
verificación final debe impedir que se conviertan en afirmaciones citadas.

## 3. Los dos modos del tutor

### Modo A — Tutor general del curso
- **Contexto:** dentro del curso, fuera de una lección. No hay `lesson_id`
  activo (o no hay bloque/timestamp).
- **Comportamiento:** orienta, navega ("¿por dónde empiezo?"), explica conceptos
  generales del dominio, considera progreso del alumno.
- **Prohibición:** no inventar bloque/timestamp/"lo que se ve en pantalla". Si no
  hay lección activa, no debe fabricar una.

### Modo B — Tutor dentro de una lección
- **Contexto:** llega `course_id`, sección, `lesson_id`, recurso, metadata de la
  lección y opcionalmente `timestamp`.
- **Comportamiento:** responde **primero desde la lección activa**; usa el RAG del
  eje/curso para fundamentar o ampliar, no para reemplazar el punto actual.
- **Con timestamp:** resuelve el **bloque activo** y lo prioriza.
- **Sin timestamp:** sigue operando **a nivel de lección** sin degradarse.

**Regla anti-duplicación:** A y B comparten la mayoría de la lógica (cómo se
arma el contexto del alumno, cómo se aplica la política). Lo único que cambia es
*qué capas están presentes*. Implementa la diferencia como **presencia/ausencia
de capas en una representación canónica**, no como dos rutas paralelas con código
copiado. Si encuentras dos caminos que repiten la misma lógica de política,
propón unificarlos.

## 4. Representaciones canónicas

Para que A y B no diverjan y para que el dominio no se filtre, define (o
reconoce, si ya existen) dos objetos canónicos:

### 4.1 Contexto del alumno (`StudentContext`)
Una sola estructura que captura *todo* lo runtime: curso, sección, lección
activa (o ninguna), recurso, timestamp, bloque resuelto (o ninguno), modo de
interacción, señales blandas, conceptos recientes, progreso. Modo A = esta
estructura con lección/bloque vacíos; Modo B = la misma estructura poblada. Hoy
el proyecto se acerca a esto con `TutorContextEnvelope` + `ActivityContext` +
`StudentSessionState` (ver [architecture-map.md](architecture-map.md)); audita si
las decisiones realmente consumen ese objeto o si lo ignoran.

### 4.2 Política pedagógica (`PedagogicalPolicy`)
Una vista derivada de las capas 2-4 que expone, ya resuelto, qué puede/no puede
hacer el tutor **para este turno**: temas delegados (`delegated_to_tutor`),
restricciones de atribución (`attribution_constraints`), foco
(`tutor_focus`), conceptos en juego (`concepts`), modo (`interaction_mode`),
prompts y preguntas esperadas. El routing, los gates, el retrieval, la generación
y la verificación deben leer **esta política**, no re-derivar cada uno su propia
interpretación de los campos crudos. Si no existe, su ausencia es un hallazgo:
proponer crearla es el "arreglo arquitectónico mínimo correcto" más común.

## 5. Niveles de evidencia y "ausencia ≠ fuera de dominio"

Distingue tres cosas que se confunden:
- **Dentro/fuera de dominio** — ¿la pregunta pertenece al curso? Se decide con
  taxonomía, `concepts`, `delegated_to_tutor`, título y sección — **no** solo con
  "¿hay chunks?".
- **Nivel de evidencia** — cuánta evidencia documental respalda la respuesta
  (alta / parcial / nula). Una pregunta puede ser **del dominio** con evidencia
  **nula** (p. ej. tema delegado al tutor).
- **Suficiencia de contexto** — ¿tengo lo necesario para responder sin inventar?
  Si no, el tutor lo **declara**; no rellena con otra lección.

La matriz que importa:

| ¿Del dominio? | ¿Evidencia? | Conducta correcta |
|---|---|---|
| Sí | Alta | Responder anclado a evidencia |
| Sí | Nula, pero `delegated_to_tutor` lo cubre | Responder como **adaptación operativa**, distinguiéndola del contenido oficial |
| Sí | Nula y no delegado | Declarar insuficiencia / remitir a recurso, sin inventar |
| No | — | Bloquear con `blocked_by` explicando por qué |

El gate de dominio nunca debe depender de que el **título** de la lección
contenga una palabra del dominio: un título genérico ("Clase 3") con conceptos
del dominio sigue siendo del dominio.

## 6. Determinismo vs LLM en compuertas

Las compuertas críticas (dominio, bloqueo, "estudiante perdido", forzar
internet) tienen consecuencias fuertes y deben ser **predecibles y testeables**.
Prefiere reglas deterministas que consulten la política pedagógica; reserva el
LLM pequeño para desempates de baja consecuencia. Un clasificador LLM no debe ser
el único que decide si una pregunta es "fuera de dominio" o "estudiante
perdido": eso produce falsos positivos no reproducibles. Si un gate determinista
existe pero ignora la política (p. ej. detecta "no entiendo" como frustración sin
mirar si es "no entiendo *este concepto del curso*"), trátalo como bug.

## 7. Observabilidad como contrato

Cada turno debe poder explicarse. Mantén (y completa donde falten) estos campos
de diagnóstico, con estos nombres canónicos:

- `selected_route` — ruta elegida por el supervisor.
- `intent` — intención clasificada.
- `active_lesson` / `active_block` — qué lección/bloque se resolvió (o vacío).
- `applied_policies` — qué políticas/fuentes se aplicaron.
- `retrieval_scope` — alcance del retrieval (curso/eje/sección/lección).
- `evidence_level` — nivel de evidencia documental.
- `warnings` — alertas no fatales.
- `blocked_by` — **por qué** se bloqueó/recortó, si aplica.

Cuando alguno no exista en el sistema real, su ausencia es un hallazgo de
observabilidad: un fix barato y de alto valor para auditar todo lo demás.

## 8. Reglas de diseño (catálogo)

Estas son las reglas que la skill defiende. Cítalas por nombre en los hallazgos.

1. **Dominio en datos, no en código.** Sin nombres de curso ni DAWs concretos en
   la lógica central; todo viene del Domain Pack / metadata.
2. **Hidratar antes de decidir.** Ninguna compuerta crítica decide sobre la
   pregunta cruda sin acceso a la política pedagógica.
3. **Una regla global no veta una delegación de lección** (salvo seguridad/
   integridad).
4. **Ausencia de evidencia ≠ fuera de dominio.** Revisar delegación, prompts,
   preguntas probables, conceptos, objetivo, título y sección antes de bloquear.
5. **Sin herencia silenciosa.** Lección vacía no hereda el contenido de otra;
   declarar insuficiencia.
6. **Timestamp mejora, no condiciona.** Nivel de lección debe funcionar sin él.
7. **No duplicar A vs B.** Lógica común en representación canónica.
8. **Cuatro fuentes separadas y rotuladas.** Runtime ≠ evidencia documental ≠
   reglas ≠ conocimiento general.
9. **Determinismo en gates críticos.** LLM pequeño solo para desempates de baja
   consecuencia.
10. **Restricciones aplicadas pre y post generación.** `attribution_constraints`
    se imponen al construir el prompt y se verifican en la salida.
11. **Trazabilidad obligatoria.** Los nueve campos de §7, y gates que explican el
    porqué.
12. **No inyección redundante.** Un mismo dato (objetivo, acción esperada) no se
    inyecta dos veces con etiquetas distintas.
13. **Implementar solo cuando se solicita.** Auditoría propone; el usuario
    aprueba; luego se cambia código.
