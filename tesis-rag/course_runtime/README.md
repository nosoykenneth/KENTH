# course_runtime

Capa operativa del curso (Capa 2 del tutor contextual).

**No** contiene el conocimiento pedagógico canónico (eso vive en
`documentos/oficial/ejes/`). Aquí solo viven los manifiestos
estructurales que permiten al backend saber:

- qué ejes existen y qué lecciones pertenecen a cada uno
- qué recursos tiene cada eje / lección (canónico, paquete limpio, derivados, video)
- cómo apuntar a un recurso (id, tipo, URI relativa al repo)
- (si la lección tiene video grabado) la segmentación en bloques con
  `start_time` / `end_time` que permite al tutor saber qué bloque está
  viendo el alumno en cada momento

Esquemas Pydantic en `models/context.py`. Servicio principal en
`services/axis_service.py`. Router REST en `api/routes/axes.py`.

## Estructura

```
course_runtime/
├── README.md                          este archivo
├── manifest.json                      índice global del curso (8 ejes)
├── axes/
│   ├── eje_0/
│   │   ├── manifest.json              metadatos del eje 0
│   │   └── lessons/                   mini-lecciones del eje (E0-L*.json)
│   ├── eje_1/
│   │   ├── manifest.json
│   │   └── lessons/
│   │       ├── E1-L01.json            ... una por subsección canónica
│   │       └── ...
│   ├── eje_2/
│   │   ├── manifest.json
│   │   └── lessons/
│   │       └── E2-L01.json            con bloques de video segmentados
│   └── ...                            eje_3 a eje_7
└── resources/                         catálogo plano de recursos
    ├── res_E0_canonico.json           contenido canónico (mío)
    ├── res_E0_paquete_limpio.json     paquete limpio (atribuible)
    ├── res_E0_glosario.json           derivado (vacío hasta poblarse)
    ├── ...
    └── res_E2-L01_video.json          video de una lección
```

## Convenciones de IDs

- **Ejes**: `Eje 0`, `Eje 1`, ..., `Eje 7` (con espacio, conserva
  legibilidad humana). El slug de carpeta es `eje_N`.
- **Lecciones**: `E<N>-L<NN>` (ej. `E1-L03`). El número de eje viene
  pegado al `E`. Si la lección viene de una subsección canónica
  (ej. 1-B2), el lesson JSON incluye `subsection_code` para trazabilidad.
- **Bloques de video**: `<lesson_id>-B<idx>` (ej. `E2-L01-B4`).
- **Recursos**:
  - `res_E<N>_<tipo>` para recursos a nivel de eje (canónico, paquete
    limpio, glosario, faq, etc.).
  - `res_<lesson_id>_<tipo>` para recursos a nivel de lección
    (ej. `res_E2-L01_video`).

## Capa de documento (`doc_layer`)

Cada recurso lleva en `metadata.doc_layer` una de estas tres etiquetas:

| `doc_layer` | Significado | `attribution_required` |
|-------------|-------------|------------------------|
| `canonico`  | Contenido propio del curso. Indexable en RAG y citable como mío. | `false` |
| `limpio`    | Paquete limpio (extracción forense). Contiene material atribuible (Rabinovich, AES/EBU, Katz K-System, ITU-R BS.1770, etc.). Indexable, pero el tutor debe referenciar la fuente y no presentarlo como contenido propio. | `true` |
| `derivado`  | Glosario, heurísticas, FAQ, errores frecuentes, índices de recursos. Generados a partir del canónico. | `false` |

## Resolución (DB-first, JSON-fallback)

Tanto lecciones como recursos pueden vivir en la BD de Moodle
(`mdl_local_tesisai_*`). Si están ahí, se sirven desde la DB. Si no,
el `axis_service` cae a leer estos JSON del filesystem. Eso permite:

- arrancar el sistema sin DB poblada usando solo los JSON aquí, y
- migrar gradualmente cada eje a la DB sin tocar el código del tutor.

El script `scripts/backfill_moodle_operational.py` lee este árbol y
hace el upsert correspondiente en Moodle.

## Estado actual del contenido

| Eje | Recursos | Lecciones | Notas |
|-----|----------|-----------|-------|
| Eje 0 — Campo de decisión       | 7 (canónico, limpio, 5 derivados) | 0 | Eje documental cargado. Mini-lecciones pendientes de guion. |
| Eje 1 — Lectura de señales      | 7 (canónico, limpio, 5 derivados) | 6 (E1-L01 a E1-L06) | Mini-lecciones derivadas de subsecciones canónicas (sin bloques de video aún). |
| Eje 2 — Integridad de la señal  | 9 videos (E2-L01 a E2-L09) | 9 (E2-L01 a E2-L09) | Eje completo. E2-L01 con video grabado real (8 bloques). E2-L02 a E2-L09 derivadas del guion v2 con bloques segmentados por timestamp como guion de grabación (`pending_capture`): los videos H5P se graban para coincidir con esos bloques y se enlazan igual que E2-L01. |
| Eje 3 — Identidad espectral     | 1 video (E3-L03) | 1 (E3-L03) | Migrada del piloto. Con 8 bloques de video. |
| Eje 4 — Energía y movimiento    | 1 video (E4-L01) | 1 (E4-L01) | Migrada del piloto. Con 9 bloques de video. |
| Eje 5 — Dimensión espacial      | 0 | 0 | Placeholder. |
| Eje 6 — Integración global      | 0 | 0 | Placeholder. |
| Eje 7 — Traducción y entrega    | 0 | 0 | Placeholder. |

## Cómo agregar contenido nuevo a un eje

1. Crea (o actualiza) `axes/eje_N/manifest.json` con los IDs nuevos
   en `lessons[]` y/o `primary_resources[]` / `derived_resources[]`.
2. Si es un recurso: crea `resources/<resource_id>.json` con shape
   de `models.context.Resource` (campos clave: `resource_id`, `type`,
   `axis_id`, `source_uri`, `metadata.doc_layer`).
3. Si es una lección sin video: crea `axes/eje_N/lessons/<lesson_id>.json`
   con `learning_goal`, `expected_action`, `resources[]` y `blocks: []`.
4. Si es una lección con video grabado y segmentado: añade el array
   `blocks` con `block_id`, `start_time`, `end_time`, `block_title`,
   `summary`, `interaction_mode`, `concepts`, `preguntas_probables`,
   `tutor_focus`.
5. Actualiza también `course_runtime/manifest.json` para que la lista
   global refleje el cambio.
6. (Opcional) Corre `python scripts/backfill_moodle_operational.py`
   para volcar el nuevo contenido a la DB de Moodle.
