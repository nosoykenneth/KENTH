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

export const getCourseDocuments = async (courseId, scope = '') => {
  const qs = scope ? `?scope=${encodeURIComponent(scope)}` : '';
  const response = await fetch(`${AUTHORING_DOCS_URL}${qs}`, {
    headers: authHeaders(courseId),
  });
  const data = await readAuthoringResponse(response, 'Error al obtener documentos del curso');
  return data.documents || [];
};

// Jerarquía real desde la BD: { course:[], axes:{axis_id:{axis_resources:[],lessons:{}}}, global_docs:[] }
export const getStructuredDocuments = async (courseId) => {
  const response = await fetch(`${AUTHORING_DOCS_URL}/structured`, {
    headers: authHeaders(courseId),
  });
  return readAuthoringResponse(response, 'Error al obtener la estructura de recursos');
};

export const getKnowledgeSummary = async (courseId) => {
  const response = await fetch(`${AUTHORING_DOCS_URL}/knowledge/summary`, {
    headers: authHeaders(courseId),
  });
  return readAuthoringResponse(response, 'Error al obtener el resumen de conocimiento');
};

// Ver el texto indexado de una fuente (teoría base / transcripción / doc).
export const getKnowledgeItem = async (courseId, source, scope = '') => {
  const qs = new URLSearchParams({ source });
  if (scope) qs.set('scope', scope);
  const response = await fetch(`${AUTHORING_DOCS_URL}/knowledge/item?${qs.toString()}`, {
    headers: authHeaders(courseId),
  });
  return readAuthoringResponse(response, 'No se pudo cargar el contenido indexado');
};

// Object-URL del archivo real de una fuente (pdf/audio/imagen) para el visor.
export const fetchKnowledgeFile = async (courseId, source, scope = '') => {
  const qs = new URLSearchParams({ source });
  if (scope) qs.set('scope', scope);
  const response = await fetch(`${AUTHORING_DOCS_URL}/knowledge/file?${qs.toString()}`, {
    headers: authHeaders(courseId),
  });
  if (!response.ok) throw new Error('No se pudo cargar el archivo');
  const blob = await response.blob();
  return URL.createObjectURL(blob);
};

// Borrar del índice una fuente cualquiera (mueve el archivo a no_indexar si aplica).
export const deleteKnowledgeItem = async (courseId, source, scope = '') => {
  const qs = new URLSearchParams({ source });
  if (scope) qs.set('scope', scope);
  const response = await fetch(`${AUTHORING_DOCS_URL}/knowledge/item?${qs.toString()}`, {
    method: 'DELETE',
    headers: authHeaders(courseId),
  });
  return readAuthoringResponse(response, 'No se pudo borrar del índice');
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
  if (payload.scope) formData.append('scope', payload.scope);
  if (payload.description) formData.append('description', payload.description);
  if (payload.concepts) formData.append('concepts', payload.concepts);
  if (payload.resource_type) formData.append('resource_type', payload.resource_type);

  const response = await fetch(AUTHORING_DOCS_URL, {
    method: 'POST',
    headers: authHeaders(courseId),
    body: formData,
  });
  return readAuthoringResponse(response, 'Error al subir documento del curso');
};

// "Sugerir con IA": borrador de descripción de una imagen (modelo de visión).
export const suggestImageCaption = async (courseId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await fetch(`${AUTHORING_DOCS_URL}/caption`, {
    method: 'POST',
    headers: authHeaders(courseId),
    body: formData,
  });
  const data = await readAuthoringResponse(response, 'No se pudo sugerir la descripción');
  return data.description || '';
};

// Devuelve un object-URL de la imagen de un doc (fetch con auth → blob).
export const fetchMediaUrl = async (courseId, docId, scope = '') => {
  const qs = scope ? `?scope=${encodeURIComponent(scope)}` : '';
  const response = await fetch(`${AUTHORING_DOCS_URL}/media/${encodeURIComponent(docId)}${qs}`, {
    headers: authHeaders(courseId),
  });
  if (!response.ok) throw new Error('No se pudo cargar la imagen');
  const blob = await response.blob();
  return URL.createObjectURL(blob);
};

export const deleteCourseDocument = async (courseId, docId, scope = '') => {
  const qs = scope ? `?scope=${encodeURIComponent(scope)}` : '';
  const response = await fetch(`${AUTHORING_DOCS_URL}/${encodeURIComponent(docId)}${qs}`, {
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

// ============================================================
// RECURSOS POR LECCIÓN (imagen / plantilla / audio / pdf…)
// ============================================================

const AUTHORING_LESSONS_URL = '/api/ai/authoring/lessons';
const LESSONS_URL = '/api/ai/lessons';

// includeAxis=true añade data.inherited_axis_resources (recursos del eje, solo lectura).
export const listLessonResources = async (courseId, lessonId, includeAxis = false) => {
  const qs = includeAxis ? '?include_axis=true' : '';
  const response = await fetch(`${AUTHORING_LESSONS_URL}/${encodeURIComponent(lessonId)}/resources${qs}`, {
    headers: authHeaders(courseId),
  });
  const data = await readAuthoringResponse(response, 'Error al obtener los recursos de la lección');
  if (includeAxis) return data; // { resources, inherited_axis_resources, axis_id }
  return data.resources || [];
};

function appendResourceForm(payload) {
  const formData = new FormData();
  formData.append('file', payload.file);
  formData.append('title', payload.title || payload.file?.name || '');
  formData.append('description', payload.description || '');
  formData.append('concepts', payload.concepts || '');
  formData.append('index_to_tutor', payload.index_to_tutor ? 'true' : 'false');
  if (payload.visible_to_student !== undefined && payload.visible_to_student !== null) {
    formData.append('visible_to_student', payload.visible_to_student ? 'true' : 'false');
  }
  if (payload.resource_type) formData.append('resource_type', payload.resource_type);
  return formData;
}

export const uploadLessonResource = async (courseId, lessonId, payload) => {
  const response = await fetch(`${AUTHORING_LESSONS_URL}/${encodeURIComponent(lessonId)}/resources`, {
    method: 'POST',
    headers: authHeaders(courseId),
    body: appendResourceForm(payload),
  });
  return readAuthoringResponse(response, 'Error al subir el recurso');
};

export const deleteLessonResource = async (courseId, lessonId, docId) => {
  const response = await fetch(
    `${AUTHORING_LESSONS_URL}/${encodeURIComponent(lessonId)}/resources/${encodeURIComponent(docId)}`,
    { method: 'DELETE', headers: authHeaders(courseId) },
  );
  return readAuthoringResponse(response, 'Error al eliminar el recurso');
};

// ============================================================
// RECURSOS DE EJE (scope='axis', pertenecen a todo el eje)
// ============================================================

const AUTHORING_AXES_URL = '/api/ai/authoring/axes';

export const listAxisResources = async (courseId, axisId) => {
  const response = await fetch(`${AUTHORING_AXES_URL}/${encodeURIComponent(axisId)}/resources`, {
    headers: authHeaders(courseId),
  });
  const data = await readAuthoringResponse(response, 'Error al obtener los recursos del eje');
  return data.resources || [];
};

export const uploadAxisResource = async (courseId, axisId, payload) => {
  const response = await fetch(`${AUTHORING_AXES_URL}/${encodeURIComponent(axisId)}/resources`, {
    method: 'POST',
    headers: authHeaders(courseId),
    body: appendResourceForm(payload),
  });
  return readAuthoringResponse(response, 'Error al subir el recurso del eje');
};

export const deleteAxisResource = async (courseId, axisId, docId) => {
  const response = await fetch(
    `${AUTHORING_AXES_URL}/${encodeURIComponent(axisId)}/resources/${encodeURIComponent(docId)}`,
    { method: 'DELETE', headers: authHeaders(courseId) },
  );
  return readAuthoringResponse(response, 'Error al eliminar el recurso del eje');
};

// Borrador de descripción de una imagen de recurso (reusa el endpoint de visión).
export const suggestResourceCaption = suggestImageCaption;

// Panel del alumno: recursos VISIBLES de una lección.
export const getStudentLessonResources = async (courseId, lessonId) => {
  const qs = courseId ? `?course_id=${encodeURIComponent(courseId)}` : '';
  const response = await fetch(`${LESSONS_URL}/${encodeURIComponent(lessonId)}/resources${qs}`);
  if (!response.ok) return [];
  const data = await response.json().catch(() => ({}));
  return data.resources || [];
};
