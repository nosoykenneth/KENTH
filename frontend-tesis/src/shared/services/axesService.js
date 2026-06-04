/**
 * axesService.js
 *
 * Cliente del API de ejes, lecciones y recursos del tutor contextual KENTH.
 * Reemplaza al antiguo pilotService: la capa operativa ya no se llama
 * "piloto" sino que es la estructura formal por ejes (axes/eje_N/).
 */

const RAG_API_URL = '/api/ai';

// ==========================================
// AUTORÍA (escritura) — requiere rol docente
// ==========================================
// Las rutas /authoring exigen token Moodle + X-Course-Id (id firmado del curso,
// el mismo que usa la ruta de React y tesis_role.php).

function authHeaders(courseId) {
  const token = localStorage.getItem('moodle_token') || '';
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(courseId ? { 'X-Course-Id': String(courseId) } : {}),
  };
}

async function writeJson(method, path, courseId, body) {
  const res = await fetch(`${RAG_API_URL}${path}`, {
    method,
    headers: authHeaders(courseId),
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Error ${res.status} en ${path}`);
  }
  return res.json();
}

function courseQuery(courseId) {
  return courseId ? `?course_id=${encodeURIComponent(courseId)}` : '';
}

export function upsertAxis(courseId, axisId, payload) {
  return writeJson('PUT', `/authoring/axes/${encodeURIComponent(axisId)}`, courseId, payload);
}
export function deleteAxis(courseId, axisId) {
  return writeJson('DELETE', `/authoring/axes/${encodeURIComponent(axisId)}`, courseId);
}
export function upsertLesson(courseId, lessonId, payload) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}`, courseId, payload);
}
export function deleteLesson(courseId, lessonId) {
  return writeJson('DELETE', `/authoring/lessons/${encodeURIComponent(lessonId)}`, courseId);
}
export function replaceLessonBlocks(courseId, lessonId, blocks) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/blocks`, courseId, { blocks });
}
export function setLessonPrompts(courseId, lessonId, { proactive_message = '', suggested_prompts = [] }) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/prompts`, courseId, {
    proactive_message,
    suggested_prompts,
  });
}
export function reorderLessons(courseId, items) {
  return writeJson('PUT', `/authoring/lessons-reorder`, courseId, { items });
}

// ---- Transcripción (segmentos por lección) ----
export async function getTranscript(courseId, lessonId) {
  const res = await fetch(`${RAG_API_URL}/authoring/lessons/${encodeURIComponent(lessonId)}/transcript`, {
    headers: authHeaders(courseId),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Error ${res.status} cargando transcripción`);
  }
  return res.json(); // { lesson_id, segments, job }
}
export function replaceTranscript(courseId, lessonId, segments) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/transcript`, courseId, { segments });
}
export function autoTranscribe(courseId, lessonId, { resource_id, language = 'es' }) {
  return writeJson('POST', `/authoring/lessons/${encodeURIComponent(lessonId)}/transcript/auto`, courseId, {
    resource_id,
    language,
  });
}
export async function getTranscriptStatus(courseId, lessonId) {
  const res = await fetch(`${RAG_API_URL}/authoring/lessons/${encodeURIComponent(lessonId)}/transcript/status`, {
    headers: authHeaders(courseId),
  });
  if (!res.ok) throw new Error(`Error ${res.status} consultando estado`);
  return res.json(); // { lesson_id, job }
}
export function upsertResourceMeta(courseId, resourceId, payload) {
  return writeJson('PUT', `/authoring/resources/${encodeURIComponent(resourceId)}`, courseId, payload);
}
export function deleteResourceMeta(courseId, resourceId) {
  return writeJson('DELETE', `/authoring/resources/${encodeURIComponent(resourceId)}`, courseId);
}

// ==========================================
// MANIFEST GLOBAL Y EJES
// ==========================================

export async function getCourseManifest() {
  const res = await fetch(`${RAG_API_URL}/axes`);
  if (!res.ok) throw new Error('No se pudo cargar el manifest del curso');
  return res.json();
}

export async function listAxes(courseId = '') {
  const res = await fetch(`${RAG_API_URL}/axes/list${courseQuery(courseId)}`);
  if (!res.ok) throw new Error('No se pudieron listar los ejes');
  const data = await res.json();
  return data.axes || [];
}

export async function getAxis(axisId, courseId = '') {
  const res = await fetch(`${RAG_API_URL}/axes/${encodeURIComponent(axisId)}${courseQuery(courseId)}`);
  if (!res.ok) throw new Error('Eje no encontrado');
  return res.json();
}

export async function getAxisLessons(axisId, courseId = '') {
  const res = await fetch(`${RAG_API_URL}/axes/${encodeURIComponent(axisId)}/lessons${courseQuery(courseId)}`);
  if (!res.ok) throw new Error('No se pudieron cargar las lecciones del eje');
  const data = await res.json();
  return data.lessons || [];
}

export async function getAxisResources(axisId, courseId = '') {
  const res = await fetch(`${RAG_API_URL}/axes/${encodeURIComponent(axisId)}/resources${courseQuery(courseId)}`);
  if (!res.ok) throw new Error('No se pudieron cargar los recursos del eje');
  const data = await res.json();
  return data.resources || [];
}

// ==========================================
// LECCIONES (acceso plano por lesson_id)
// ==========================================

export async function listAllLessons(courseId = '') {
  const res = await fetch(`${RAG_API_URL}/axes/lessons/all${courseQuery(courseId)}`);
  if (!res.ok) throw new Error('No se pudieron listar las lecciones');
  const data = await res.json();
  return data.lessons || [];
}

export async function getLesson(lessonId, courseId = '') {
  const res = await fetch(`${RAG_API_URL}/axes/lessons/${encodeURIComponent(lessonId)}${courseQuery(courseId)}`);
  if (!res.ok) throw new Error('Lección no encontrada');
  return res.json();
}

export async function resolveLessonBlock(lessonId, timestamp, courseId = '') {
  const sep = courseId ? `&course_id=${encodeURIComponent(courseId)}` : '';
  const url = `${RAG_API_URL}/axes/lessons/${encodeURIComponent(lessonId)}/block?t=${timestamp}${sep}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('No se pudo resolver el bloque de la lección');
  return res.json();
}

// ==========================================
// RECURSOS
// ==========================================

export async function getResource(resourceId) {
  const res = await fetch(`${RAG_API_URL}/axes/resources/${encodeURIComponent(resourceId)}`);
  if (!res.ok) throw new Error('Recurso no encontrado');
  return res.json();
}

// ==========================================
// VINCULOS RECURSO MOODLE <-> LECCION FORMAL
// ==========================================

export async function listResourceLinks(courseId) {
  const qs = courseId ? `?course_id=${encodeURIComponent(courseId)}` : '';
  const res = await fetch(`${RAG_API_URL}/axes/links${qs}`);
  if (!res.ok) throw new Error('No se pudieron cargar los vínculos');
  const data = await res.json();
  return data.links || [];
}

export async function getResourceLink(resourceId) {
  const res = await fetch(`${RAG_API_URL}/axes/links/${encodeURIComponent(resourceId)}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error('Error obteniendo vínculo');
  return res.json();
}

export async function upsertResourceLink(resourceId, payload) {
  const res = await fetch(`${RAG_API_URL}/axes/links/${encodeURIComponent(resourceId)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || 'No se pudo guardar el vínculo');
  }
  return res.json();
}

export async function deleteResourceLink(resourceId) {
  const res = await fetch(`${RAG_API_URL}/axes/links/${encodeURIComponent(resourceId)}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('No se pudo quitar el vínculo');
  return res.json();
}

// ==========================================
// HELPERS PARA EL TUTOR
// ==========================================

/**
 * Construye el activity_context que se manda al backend para una
 * lección seleccionada y un timestamp (opcional) del slider de video.
 */
export function buildLessonActivityContext(lesson, timestamp) {
  if (!lesson) return null;
  return {
    current_axis: lesson.axis_id || '',
    current_lesson_id: lesson.lesson_id || '',
    current_resource_id: lesson.resource_id || '',
    current_resource_type: lesson.resource_type || 'video',
    resource_subtype: '',
    current_timestamp: typeof timestamp === 'number' ? timestamp : null,
    current_page: null,
    current_section: '',
    learning_goal: lesson.learning_goal || '',
    expected_action: lesson.expected_action || '',
    interaction_mode: 'navegacion_de_recurso',
  };
}
