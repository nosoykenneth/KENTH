const RAG_API_URL = '/api/ai';

function authHeaders(courseId) {
  const token = localStorage.getItem('moodle_token') || '';
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(courseId ? { 'X-Course-Id': String(courseId) } : {}),
  };
}

function courseQuery(courseId) {
  return courseId ? `?course_id=${encodeURIComponent(courseId)}` : '';
}

// El backend puede devolver `detail` como string o como objeto {code, message,
// errors} (endpoints ai-prepare). Extrae siempre un mensaje legible.
function errMessage(body, status, path) {
  const d = body && body.detail;
  if (typeof d === 'string') return d;
  if (d && typeof d === 'object') return d.message || d.code || JSON.stringify(d);
  return `Error ${status} en ${path}`;
}

async function readJson(path, courseId = '') {
  const res = await fetch(`${RAG_API_URL}${path}`, {
    headers: authHeaders(courseId),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(errMessage(detail, res.status, path));
  }
  return res.json();
}

async function writeJson(method, path, courseId, body) {
  const res = await fetch(`${RAG_API_URL}${path}`, {
    method,
    headers: authHeaders(courseId),
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    const err = new Error(errMessage(detail, res.status, path));
    err.status = res.status;
    err.code = detail && detail.detail && detail.detail.code;
    throw err;
  }
  return res.json();
}

export async function listSections(courseId = '') {
  const data = await readJson(`/sections/list${courseQuery(courseId)}`, courseId);
  return data.sections || [];
}

export async function getSectionLessons(sectionId, courseId = '') {
  const data = await readJson(`/sections/${encodeURIComponent(sectionId)}/lessons${courseQuery(courseId)}`, courseId);
  return data.lessons || [];
}

export async function listAllLessons(courseId = '') {
  const data = await readJson(`/sections/lessons/all${courseQuery(courseId)}`, courseId);
  return data.lessons || [];
}

export function upsertLesson(courseId, lessonId, payload) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}`, courseId, {
    ...payload,
    axis_id: '',
  });
}

export function deleteLesson(courseId, lessonId) {
  return writeJson('DELETE', `/authoring/lessons/${encodeURIComponent(lessonId)}`, courseId);
}

export function reorderLessons(courseId, items) {
  return writeJson('PUT', `/authoring/lessons-reorder`, courseId, { items });
}

export async function listResourceLinks(courseId) {
  const data = await readJson(`/sections/links${courseQuery(courseId)}`, courseId);
  return data.links || [];
}

export async function getResourceLink(resourceId, courseId = '') {
  const qs = courseId ? courseQuery(courseId) : '';
  const res = await fetch(`${RAG_API_URL}/sections/links/${encodeURIComponent(resourceId)}${qs}`, {
    headers: authHeaders(courseId),
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error('Error obteniendo vínculo');
  return res.json();
}

export function upsertResourceLink(resourceId, payload) {
  return writeJson('PUT', `/sections/links/${encodeURIComponent(resourceId)}`, payload.course_id || '', {
    ...payload,
    axis_id: '',
  });
}

export function deleteResourceLink(resourceId, courseId = '') {
  // courseId se envía como X-Course-Id: el backend (require_teacher) valida rol
  // docente en ese curso antes de borrar el vínculo.
  return writeJson('DELETE', `/sections/links/${encodeURIComponent(resourceId)}`, courseId);
}

export async function getLesson(lessonId, courseId = '') {
  return readJson(`/sections/lessons/${encodeURIComponent(lessonId)}${courseQuery(courseId)}`, courseId);
}

export async function resolveLessonBlock(lessonId, timestamp, courseId = '') {
  const sep = courseId ? `&course_id=${encodeURIComponent(courseId)}` : '';
  return readJson(`/sections/lessons/${encodeURIComponent(lessonId)}/block?t=${timestamp}${sep}`, courseId);
}

export function replaceLessonBlocks(courseId, lessonId, blocks) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/blocks`, courseId, { blocks });
}

// Edición PEDAGÓGICA de momentos (bloques) para el profesor: solo campos
// pedagógicos, in-place. El backend (require_teacher) preserva tiempos/estructura
// y rechaza altas/bajas/reorden; los timestamps ni se envían (barrera server-side).
export function updateMoments(courseId, lessonId, moments) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/moments`, courseId, { moments });
}

export function setLessonPrompts(courseId, lessonId, { proactive_message = '', suggested_prompts = [] }) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/prompts`, courseId, {
    proactive_message,
    suggested_prompts,
  });
}

export function importLesson(courseId, json, targetLessonId = '') {
  const qs = targetLessonId ? `?target_lesson_id=${encodeURIComponent(targetLessonId)}` : '';
  return writeJson('POST', `/authoring/lessons/import${qs}`, courseId, { ...json, axis_id: '' });
}

export function upsertResourceMeta(courseId, resourceId, payload) {
  return writeJson('PUT', `/authoring/resources/${encodeURIComponent(resourceId)}`, courseId, {
    ...payload,
    axis_id: '',
  });
}

export async function getTranscript(courseId, lessonId) {
  return readJson(`/authoring/lessons/${encodeURIComponent(lessonId)}/transcript`, courseId);
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
  return readJson(`/authoring/lessons/${encodeURIComponent(lessonId)}/transcript/status`, courseId);
}

// Asistente "Preparar tutor con IA": genera un BORRADOR pedagógico desde la
// transcripción. NO reindexa ni publica; el borrador queda en metadata.ai_prepare.
export function aiPrepare(courseId, lessonId, {
  mode = 'draft', quality = 'balanced', use_existing_transcript = true,
  regenerate_transcript = false, include_resources = true, include_vision = false,
  review_model = null,
} = {}) {
  return writeJson('POST', `/authoring/lessons/${encodeURIComponent(lessonId)}/ai-prepare`, courseId, {
    mode, quality, use_existing_transcript, regenerate_transcript, include_resources, include_vision,
    ...(review_model ? { review_model } : {}),
  });
}

// Acepta el borrador (posiblemente editado por el profesor) y lo promueve a los
// campos vivos del tutor. `draft` opcional; si no viene, promueve el guardado.
export function aiPrepareAccept(courseId, lessonId, { draft = null, apply_moments = true } = {}) {
  return writeJson('POST', `/authoring/lessons/${encodeURIComponent(lessonId)}/ai-prepare/accept`, courseId, {
    ...(draft ? { draft } : {}),
    apply_moments,
  });
}
