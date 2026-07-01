# Parche requerido: `tesis_role.php` (roles granulares)

> **Cambio externo al repo.** `tesis_role.php` vive en el árbol de Moodle, no en
> este repositorio. El rediseño de autoría por roles (rama
> `feat/lesson-editor-role-workflows`) **depende** de que este archivo devuelva
> las flags granulares. Si el servidor no tiene el parche, el sistema degrada de
> forma segura (ver más abajo), pero admin de curso y técnico IA/RAG **no**
> verán sus vistas avanzadas.

## Rutas

| Entorno | Ruta |
|---|---|
| Dev (XAMPP local) | `C:\Moodle\server\moodle\proyecto_curso\api_persistente\tesis_role.php` |
| Servidor | `<MOODLE_WWWROOT>/proyecto_curso/api_persistente/tesis_role.php` |

En el servidor (deploy full-docker) el archivo está dentro del árbol de Moodle
(`wwwroot`). Recuerda que en ese entorno **el servidor es la fuente de verdad**:
edita ahí y replica el mismo cambio (no lo dejes solo en dev).

## Qué devuelve ahora el endpoint

`GET /api/lms/proyecto_curso/api_persistente/tesis_role.php?token=<TOKEN>&courseid=<SIGNED_COURSE_ID>`

```json
{
  "esProfesor": true,
  "puedeAdministrarCurso": false,
  "esTecnicoRAG": false
}
```

`esProfesor` se conserva por compatibilidad (ya lo consumía `CourseContentView`).
Se añaden `puedeAdministrarCurso` y `esTecnicoRAG`.

## Cómo se derivan (capacidades Moodle, no una tabla de roles paralela)

Dentro del contexto del curso (`context_course::instance($courseid)`), para el
`userid` dueño del token:

| Flag | Derivación | Rol típico |
|---|---|---|
| `esProfesor` | `has_capability('moodle/course:manageactivities', $context, $userid)` | editingteacher+ |
| `puedeAdministrarCurso` | `has_capability('moodle/course:update', $context, $userid)` | manager / admin de curso |
| `esTecnicoRAG` | `is_siteadmin($userid)` | site admin |

Fragmento relevante del archivo (sin secretos):

```php
$userid = $token_record->userid;
$es_profesor = has_capability('moodle/course:manageactivities', $context, $userid);
$puede_admin = has_capability('moodle/course:update', $context, $userid);
$es_tecnico  = is_siteadmin($userid);

echo json_encode(array(
    'esProfesor'            => $es_profesor,
    'puedeAdministrarCurso' => $puede_admin,
    'esTecnicoRAG'          => $es_tecnico,
));
```

> `courseid` llega **firmado** (`kenth_verify_id`), igual que hoy: el endpoint
> valida el token contra `mdl_external_tokens` y exige matrícula (o siteadmin)
> antes de responder. No se cambió esa parte.

## Cómo probarlo

Necesitas un token válido de cada usuario y el `courseid` **firmado** que ya usa
el frontend (puedes copiarlo desde la pestaña Red del navegador al abrir el curso,
o reutilizar la llamada que hace la app). No hace falta ningún secreto adicional.

```bash
# Sustituye <TOKEN> y <SIGNED_COURSE_ID>. En dev, host = http://localhost:5173
curl "https://<host>/api/lms/proyecto_curso/api_persistente/tesis_role.php?token=<TOKEN>&courseid=<SIGNED_COURSE_ID>"
```

Resultado esperado por tipo de usuario (matriculado en el curso):

| Usuario | `esProfesor` | `puedeAdministrarCurso` | `esTecnicoRAG` |
|---|---|---|---|
| **Profesor** (editingteacher) | `true` | `false` | `false` |
| **Admin de curso** (manager) | `true` | `true` | `false` |
| **Técnico / site admin** | `true` | `true` | `true` |

Verificación funcional en la app tras el patch:
- **Profesor** abre "Editar tutor IA" en una clase → ve la **Vista Profesor**
  ("Configuración docente del tutor"), sin editor avanzado.
- **Admin de curso / técnico** → ve el **Editor avanzado** (LessonVideoEditor).
- Solo el **técnico (siteadmin)** puede disparar el reindex
  (`POST /api/ai/documents/rebuild`); cualquier otro recibe **403** del backend.

## Qué ocurre si el servidor NO tiene el parche

El frontend degrada de forma segura: si el endpoint no expone las flags nuevas,
`puedeAdministrarCurso` y `esTecnicoRAG` se leen como `false`
(ver `frontend-tesis/src/shared/services/permissions.js`).

- El **profesor** cae, seguro, a la **Vista Profesor** (pedagogía). No pierde su
  capacidad de configurar el tutor.
- **Admin de curso / técnico NO** verán el **editor avanzado** ni el
  **diagnóstico IA/RAG**, porque el front no puede distinguir su rol.
- Ninguna acción sensible se abre indebidamente: la barrera real está en el
  backend FastAPI (`require_teacher` / `require_course_admin` / `require_rag_admin`),
  que sí consulta los roles/capacidades reales de Moodle de forma independiente.

Por eso el patch es **obligatorio para habilitar** las vistas avanzadas, pero su
ausencia **no** abre huecos de seguridad: solo limita lo que se ve.

## ⚠️ Advertencia de seguridad

**Nunca** uses `localStorage["moodle_rol"]` como control de acceso. Es una
heurística por nombre de usuario (`helperDetermineRole`), es puramente cosmética
(decide ítems del Navbar) y es **trivialmente falsificable** desde el navegador.

- Frontera de UI → `permissions.js` (derivado de `tesis_role.php`).
- Frontera de **seguridad real** → guards de FastAPI
  (`require_teacher` / `require_course_admin` / `require_rag_admin`), que validan
  el token y los roles/capacidades directamente contra Moodle.

Ocultar un botón en el front **no** es seguridad; toda acción sensible se valida
además en el backend.
