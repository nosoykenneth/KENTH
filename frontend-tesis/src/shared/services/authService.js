const API_BASE_URL = '/moodle_api/webservice/rest/server.php';
const LOGIN_URL = '/moodle_api/proyecto_curso/api_persistente/tesis_login.php';
const ONBOARDING_URL = '/moodle_api/proyecto_curso/api_persistente/api_onboarding_process.php';
const SERVICE_NAME = 'api_tesis';

/**
 * Autentica un usuario contra el interceptor personalizado que detecta Onboarding.
 * @param {string} username - Nombre de usuario
 * @param {string} password - Contraseña
 * @returns {Promise<Object>} Retorna {token, requiresOnboarding} o arroja un error
 */
export const login = async (username, password) => {
  const params = new URLSearchParams({
    username: username,
    password: password,
    service: SERVICE_NAME
  });

  const response = await fetch(`${LOGIN_URL}?${params.toString()}`, {
    method: 'POST'
  });

  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || "Error de autenticación");
  }
  
  return {
    token: data.token,
    requiresOnboarding: data.requiresOnboarding,
    fullname: data.fullname,
    userid: data.userid
  };
};

/**
 * Envía los datos de personalización del perfil al finalizar el Wizard.
 */
export const completeOnboarding = async (token, userData) => {
  const params = new URLSearchParams({
    token: token,
    firstname: userData.firstname,
    lastname: userData.lastname,
    password: userData.password,
    pictureData: userData.pictureData || ''
  });

  const response = await fetch(`${ONBOARDING_URL}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString()
  });

  const raw = await response.text();
  let data;

  try {
    data = JSON.parse(raw);
  } catch {
    throw new Error(`Respuesta inválida del servidor: ${raw}`);
  }

  if (!data.success) {
    throw new Error(data.error || 'Error al completar onboarding');
  }

  return data;
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