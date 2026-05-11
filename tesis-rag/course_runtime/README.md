# course_runtime

Capa operativa del curso (Capa 2 del tutor contextual).

NO contiene conocimiento pedagogico canonico (eso vive en
`documentos/oficial/ejes/`). Aqui solo viven los manifiestos
estructurales que permiten al backend saber:

- que lecciones existen
- que recursos tiene cada leccion
- como apuntar a un recurso (id, tipo, ruta/URL)

Esquemas Pydantic en `models/context.py`.

Estructura:

```
course_runtime/
  manifest.json          indice global de lecciones por eje
  lessons/<lesson_id>.json     un archivo por leccion (Lesson)
  resources/<resource_id>.json un archivo por recurso (Resource)
```

Los archivos aqui son esqueletos: se completan a medida que el
curso real se vaya cargando. El backend los lee al vuelo via
`services/context_service.py`.
