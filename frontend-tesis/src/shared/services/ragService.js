/**
 * ragService.js
 * Servicio para gestionar la comunicación con FastAPI (tesis-rag)
 */

const API_BASE_URL = '/api/ai/documents';
const AUTHORING_DOCS_URL = '/api/ai/authoring/documents';

function authHeaders(courseId) {
  const token = localStorage.getItem('moodle_token') || '';
  return {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(courseId ? { 'X-Course-Id': String(courseId) } : {}),
  };
}

async function readAuthoringResponse(response, fallback) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail;
    if (typeof detail === 'string') throw new Error(detail);
    if (detail?.message) throw new Error(detail.message);
    throw new Error(fallback);
  }
  return data;
}

export const getDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) throw new Error('Error al obtener documentos');
    return await response.json();
  } catch (error) {
    console.error('Error en getDocuments:', error);
    throw error;
  }
};

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Error al subir archivo');
    return data;
  } catch (error) {
    console.error('Error en uploadDocument:', error);
    throw error;
  }
};

export const deleteDocument = async (filename) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${filename}`, {
      method: 'DELETE',
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Error al eliminar archivo');
    return data;
  } catch (error) {
    console.error('Error en deleteDocument:', error);
    throw error;
  }
};

export const indexKnowledgeBase = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/index`, {
      method: 'POST',
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Error al iniciar indexación');
    return data;
  } catch (error) {
    console.error('Error en indexKnowledgeBase:', error);
    throw error;
  }
};

export const rebuildKnowledgeBase = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/rebuild`, {
      method: 'POST',
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Error al iniciar rebuild');
    return data;
  } catch (error) {
    console.error('Error en rebuildKnowledgeBase:', error);
    throw error;
  }
};

export const getCourseDocuments = async (courseId) => {
  const response = await fetch(AUTHORING_DOCS_URL, {
    headers: authHeaders(courseId),
  });
  const data = await readAuthoringResponse(response, 'Error al obtener documentos del curso');
  return data.documents || [];
};

export const uploadCourseDocument = async (courseId, payload) => {
  const formData = new FormData();
  formData.append('file', payload.file);
  formData.append('title', payload.title || payload.file?.name || '');
  formData.append('axis_id', payload.axis_id || '');
  formData.append('doc_layer', payload.doc_layer || 'canonico');
  formData.append('attribution_required', payload.attribution_required ? 'true' : 'false');
  formData.append('ownership', payload.ownership || 'kenth_academy');
  formData.append('notes', payload.notes || '');

  const response = await fetch(AUTHORING_DOCS_URL, {
    method: 'POST',
    headers: authHeaders(courseId),
    body: formData,
  });
  return readAuthoringResponse(response, 'Error al subir documento del curso');
};

export const deleteCourseDocument = async (courseId, docId) => {
  const response = await fetch(`${AUTHORING_DOCS_URL}/${encodeURIComponent(docId)}`, {
    method: 'DELETE',
    headers: authHeaders(courseId),
  });
  return readAuthoringResponse(response, 'Error al eliminar documento del curso');
};

export const reindexCourseDocuments = async (courseId) => {
  const response = await fetch(`${AUTHORING_DOCS_URL}/reindex`, {
    method: 'POST',
    headers: authHeaders(courseId),
  });
  return readAuthoringResponse(response, 'Error al reindexar documentos del curso');
};
