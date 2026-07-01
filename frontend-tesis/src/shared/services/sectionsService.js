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

async function readJson(path, courseId = '') {
  const res = await fetch(`${RAG_API_URL}${path}`, {
    headers: authHeaders(courseId),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Error ${res.status} en ${path}`);
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
    throw new Error(detail.detail || `Error ${res.status} en ${path}`);
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

export function deleteResourceLink(resourceId) {
  return writeJson('DELETE', `/sections/links/${encodeURIComponent(resourceId)}`, '');
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
