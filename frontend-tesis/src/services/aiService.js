/**
 * aiService.js
 * Servicio para gestionar la comunicación con Ollama a través de Moodle.
 */

const API_BASE_URL = '/moodle_api/webservice/rest/server.php';

/**
 * Envía un prompt a la IA local usando el plugin local_tesisai de Moodle
 * @param {string} token - Token de sesión del usuario en Moodle
 * @param {string} prompt - La pregunta del usuario
 * @returns {Promise<string>} La respuesta generada por Ollama
 */
export const askOllama = async (token, prompt) => {
  if (!token) throw new Error('No hay sesión activa.');

  // Preparamos los parámetros para el Web Service nativo de Moodle
  const params = new URLSearchParams({
    wstoken: token,
    wsfunction: 'local_tesisai_ask_ollama',
    moodlewsrestformat: 'json',
    prompt: prompt
  });

  try {
    // Usamos POST para enviar textos largos de forma segura
    const response = await fetch(`${API_BASE_URL}?${params.toString()}`, {
      method: 'POST'
    });

    // Como tú definiste en PHP que devuelve un valor RAW simple, 
    // Moodle devolverá directamente el string o un objeto de excepción.
    const data = await response.json();

    // Moodle devuelve un objeto con "exception" si la función falla o no tienes permisos
    if (data.exception) {
      throw new Error(data.message || 'Error al contactar con el Web Service de IA.');
    }

    // Retornamos el texto de la respuesta
    return data;
    
  } catch (error) {
    console.error('Error en askOllama:', error);
    throw error;
  }
};