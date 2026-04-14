const API_BASE_URL = '/moodle_api/webservice/rest/server.php';
const LOGIN_URL = '/moodle_api/login/token.php';
const SERVICE_NAME = 'api_tesis';

/**
 * Autentica un usuario contra el endpoint login/token.php de Moodle.
 * @param {string} username - Nombre de usuario
 * @param {string} password - Contraseña
 * @returns {Promise<Object>} Retorna el token o arroja un error con el mensaje de Moodle
 */
export const login = async (username, password) => {
  const params = new URLSearchParams({
    username: username,
    password: password,
    service: SERVICE_NAME
  });

  const response = await fetch(`${LOGIN_URL}?${params.toString()}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });

  const data = await response.json();
  
  if (data.error) {
    throw new Error(data.error);
  }
  
  return data.token;
};

/**
 * Obtiene la información general del sitio y del usuario autenticado actual
 * usando la funcion core_webservice_get_site_info
 * @param {string} token - Token de Moodle
 * @returns {Promise<Object>} Datos del usuario (userid, fullname, etc)
 */
export const getSiteInfo = async (token) => {
  const params = new URLSearchParams({
    wstoken: token,
    wsfunction: 'core_webservice_get_site_info',
    moodlewsrestformat: 'json',
  });

  const res = await fetch(`${API_BASE_URL}?${params.toString()}`, { method: 'POST' });
  const data = await res.json();
  
  if (data.exception) {
    throw new Error(data.message);
  }

  return data;
};

/**
 * Determina el rol visual simulado para probar la interfaz basado en el username actual
 * (Temporal hasta integraciones completas)
 * @param {string} username - Username de moodle
 * @returns {string} rol ('admin', 'teacher', 'student')
 */
export const helperDetermineRole = (username) => {
  if (username === 'admin' || username === 'superadmin') return 'admin';
  if (username.toLowerCase().includes('prof')) return 'teacher';
  return 'student';
};