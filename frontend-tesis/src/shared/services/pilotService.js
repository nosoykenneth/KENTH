/**
 * pilotService.js
 *
 * Cliente del API de lecciones piloto del tutor contextual KENTH.
 * Vertical slice fase 1.
 */

const RAG_API_URL = '/rag_api';

export async function listPilotLessons() {
  const res = await fetch(`${RAG_API_URL}/pilot/lessons`);
  if (!res.ok) throw new Error('No se pudo listar las lecciones piloto');
  const data = await res.json();
  return data.lessons || [];
}

export async function getPilotLesson(lessonId) {
  const res = await fetch(`${RAG_API_URL}/pilot/lessons/${encodeURIComponent(lessonId)}`);
  if (!res.ok) throw new Error('Leccion piloto no encontrada');
  return res.json();
}

export async function resolvePilotBlock(lessonId, timestamp) {
  const url = `${RAG_API_URL}/pilot/lessons/${encodeURIComponent(lessonId)}/block?t=${timestamp}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('No se pudo resolver el bloque del piloto');
  return res.json();
}

// ==========================================
// VINCULOS RECURSO <-> LECCION
// ==========================================

export async function listResourceLinks(courseId) {
  const qs = courseId ? `?course_id=${encodeURIComponent(courseId)}` : '';
  const res = await fetch(`${RAG_API_URL}/pilot/links${qs}`);
  if (!res.ok) throw new Error('No se pudieron cargar los vinculos');
  const data = await res.json();
  return data.links || [];
}

export async function getResourceLink(resourceId) {
  const res = await fetch(`${RAG_API_URL}/pilot/links/${encodeURIComponent(resourceId)}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error('Error obteniendo vinculo');
  return res.json();
}

export async function upsertResourceLink(resourceId, payload) {
  const res = await fetch(`${RAG_API_URL}/pilot/links/${encodeURIComponent(resourceId)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || 'No se pudo guardar el vinculo');
  }
  return res.json();
}

export async function deleteResourceLink(resourceId) {
  const res = await fetch(`${RAG_API_URL}/pilot/links/${encodeURIComponent(resourceId)}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('No se pudo quitar el vinculo');
  return res.json();
}

/**
 * Construye el activity_context que se manda al backend para una
 * leccion piloto seleccionada y un timestamp del slider de prueba.
 */
export function buildPilotActivityContext(lesson, timestamp) {
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
