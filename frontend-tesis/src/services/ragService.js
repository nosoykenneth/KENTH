/**
 * ragService.js
 * Servicio para gestionar la comunicación con FastAPI (tesis-rag)
 */

const API_BASE_URL = '/rag_api/documents';

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
