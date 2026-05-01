/**
 * aiService.js
 * Servicio para gestionar la comunicación con Ollama a través de Moodle.
 */

const API_BASE_URL = '/moodle_api/webservice/rest/server.php';

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
 */
const RAG_API_URL = '/rag_api';

export const askOllamaDirect = async (prompt, courseContext = '', imageBase64 = '', usarInternet = false, sessionId = '') => {
  try {
    const payload = {
      pregunta: prompt,
      contexto_leccion: courseContext,
      imagen: imageBase64,
      usar_internet: usarInternet,
      session_id: sessionId
    };

    const response = await fetch(`${RAG_API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
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

export const getChatSessions = async (userId) => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/user/${userId}`);
  if (!response.ok) throw new Error('Error fetching sessions');
  const data = await response.json();
  return data.chats;
};

export const createChatSession = async (userId, title) => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, title })
  });
  if (!response.ok) throw new Error('Error creating session');
  const data = await response.json();
  return data.chat;
};

export const getChatMessages = async (sessionId) => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/${sessionId}/messages`);
  if (!response.ok) throw new Error('Error fetching messages');
  const data = await response.json();
  return data.messages;
};

export const deleteChatSession = async (sessionId) => {
  const response = await fetch(`${RAG_API_URL}/chat-sessions/${sessionId}`, { method: 'DELETE' });
  if (!response.ok) throw new Error('Error deleting session');
  return response.json();
};