import { requestMoodleRestText } from '@/shared/lib/moodleApi';

/**
 * Envía un prompt a la función personalizada en Moodle (local_tesisai_ask_ollama) 
 * que conecta con Ollama
 * @param {string} token - Moodle Token
 * @param {string} promptText - Pregunta del alumno
 * @returns {Promise<string>} La respuesta en texto devuelta por la IA
 */
export const askOllama = async (token, promptText) => {
  const textResponse = await requestMoodleRestText({
    wstoken: token,
    wsfunction: 'local_tesisai_ask_ollama',
    moodlewsrestformat: 'json',
    prompt: promptText,
  });
  let data = null;

  try {
    data = textResponse ? JSON.parse(textResponse) : null;
  } catch (e) {
    console.warn("Respuesta de Ollama no es en formato JSON puro. Asumiendo como texto plano.");
  }

  if (data && data.exception) {
    throw new Error(data.message);
  }

  // Si data no es un objeto con excepcion, Moodle probablemente devolvió strings directamente.
  if (data === null) {
      if (textResponse) return textResponse;
      throw new Error("Moodle no devolvió ninguna respuesta (vacío).");
  }

  return typeof data === 'string' ? data : JSON.stringify(data);
};
