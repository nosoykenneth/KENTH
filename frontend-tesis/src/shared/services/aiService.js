/**
 * aiService.js
 * Servicio para gestionar la comunicación con Ollama a través de Moodle.
 */

const API_BASE_URL = '/api/lms/webservice/rest/server.php';

/**
 * Envía un prompt a la IA local usando el plugin local_tesisai de Moodle
 * @param {string} token - Token de sesión del usuario en Moodle
 * @param {string} prompt - La pregunta del usuario
 * @param {string} courseContext - El texto de la lección actual
 * @param {string} imageBase64 - Imagen subida por el usuario
 * @param {boolean} usarInternet - Bandera para activar la búsqueda web (DuckDuckGo)
 * @returns {Promise<string>} La respuesta generada por Ollama
 */
export const askOllama = async (token, prompt, courseContext = '', imageBase64 = '', usarInternet = false) => {
  if (!token) throw new Error('No hay sesión activa.');

  // El token y la función deben ir obligatoriamente en la URL para que Moodle los reconozca
  const urlParams = new URLSearchParams({
    wstoken: token,
    wsfunction: 'local_tesisai_ask_ollama',
    moodlewsrestformat: 'json'
  });

  // Los datos pesados (Pregunta, Contexto y la Imagen) van en el cuerpo de la petición
  const formData = new FormData();
  formData.append('prompt', prompt);
  formData.append('course_context', courseContext);
  formData.append('image_base64', imageBase64);
  
  // EL TRUCO PARA MOODLE: Convertimos el booleano (true/false) a número (1/0)
  formData.append('usar_internet', usarInternet ? 1 : 0);

  try {
    const response = await fetch(`${API_BASE_URL}?${urlParams.toString()}`, {
      method: 'POST',
      body: formData // Usamos formData en lugar de JSON para soportar archivos grandes
    });

    const data = await response.json();

    if (data.exception) {
      throw new Error(data.message || 'Error al contactar con el Web Service de IA.');
    }

    return data;
    
  } catch (error) {
    console.error('Error en askOllama:', error);
    throw error;
  }
};

/**
 * API DIRECTA A FASTAPI (Para soportar sesiones sin modificar Moodle PHP)
 *
 * PRIVACIDAD: el user_id se envía en la cabecera X-User-Id.
 * El backend lo usa como identidad autoritativa para ownership checks.
 */
const RAG_API_URL = '/api/ai';

/**
 * Helper: devuelve cabeceras estándar con autenticación.
 * ENVÍA TOKEN MOODLE COMO BEARER PARA VALIDACIÓN SEGURA EN PRODUCCIÓN.
 * Solo envía X-User-Id como fallback para desarrollo aislado.
 */
function _authHeaders(extra = {}) {
  const token = localStorage.getItem('moodle_token') || '';
  const userId = localStorage.getItem('moodle_userid') || '';
  
  const headers = {
    'Content-Type': 'application/json',
    ...extra,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  // En dev aislado (SQLite) se acepta esto, en prod FastAPI lo ignora
  if (userId) {
    headers['X-User-Id'] = userId;
  }
  
  return headers;
}

export const askOllamaDirect = async (
  prompt,
  courseContext = '',
  imageBase64 = '',
  usarInternet = false,
  sessionId = '',
  historial = [],
  activityContext = null
) => {
  try {
    console.log('[AI DEBUG] Enviando consulta RAG', {
      hasImage: Boolean(imageBase64),
      imageLength: imageBase64 ? imageBase64.length : 0,
      hasSession: Boolean(sessionId),
      hasActivityContext: Boolean(activityContext)
    });

    const payload = {
      pregunta: prompt,
      contexto_leccion: courseContext,
      imagen: imageBase64,
      usar_internet: usarInternet,
      session_id: sessionId,
      historial,
      source_client: 'frontend',
      // user_id en payload es hint; el header X-User-Id es autoritativo.
      user_id: localStorage.getItem('moodle_userid') || ''
    };

    // Capa 2/3: solo se incluye si hay contexto util. Asi el backend
    // degrada limpio cuando el chat se usa fuera de una vista de curso.
    if (activityContext) {
      payload.activity_context = activityContext;
      payload.course_id = activityContext.course_id || '';
      payload.lesson_id = activityContext.current_lesson_id || '';
    }

    const response = await fetch(`${RAG_API_URL}/chat`, {
      method: 'POST',
      headers: _authHeaders(),
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error('Error al contactar con FastAPI directamente');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error en askOllamaDirect:', error);
    throw error;
  }
};

export const getChatSessions = async () => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/`, {
    headers: _authHeaders(),
  });
  if (!response.ok) throw new Error('Error fetching sessions');
  const data = await response.json();
  return data.chats;
};

export const createChatSession = async (title) => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/`, {
    method: 'POST',
    headers: _authHeaders(),
    body: JSON.stringify({ title })
  });
  if (!response.ok) throw new Error('Error creating session');
  const data = await response.json();
  return data.chat;
};

export const getChatMessages = async (sessionId) => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/${sessionId}/messages`, {
    headers: _authHeaders(),
  });
  if (!response.ok) throw new Error('Error fetching messages');
  const data = await response.json();
  return data.messages;
};

export const deleteChatSession = async (sessionId) => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/${sessionId}`, {
    method: 'DELETE',
    headers: _authHeaders(),
  });
  if (!response.ok) throw new Error('Error deleting session');
  return response.json();
};
