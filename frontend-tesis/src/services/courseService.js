/**
 * courseService.js
 * Servicio para gestionar la comunicación con la API de Moodle de Kenth Courses.
 */

// ==========================================
// 1. OBTENER EL CONTENIDO COMPLETO DE UN CURSO
// ==========================================
export const getCourseContents = async (token, courseId) => {
  if (!token) throw new Error('No hay sesión activa (token ausente).');
  
  // ¡CORREGIDO! Ahora tiene el prefijo /moodle_api para que el proxy de Vite lo deje pasar
  const url = `/moodle_api/webservice/rest/server.php?wstoken=${token}&wsfunction=core_course_get_contents&moodlewsrestformat=json&courseid=${courseId}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.exception) {
      throw new Error(data.message || 'Error al obtener el contenido del curso.');
    }

    return data;
  } catch (error) {
    console.error('Error en getCourseContents:', error);
    throw error;
  }
};

// ==========================================
// 2. OBTENER EL PERFIL DEL USUARIO
// ==========================================
export const getUserProfile = async (token) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/tesis_profile.php?token=${token}&action=get`;

  try {
    const response = await fetch(url);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'No se pudo cargar el perfil.');
    }

    return result.data;
  } catch (error) {
    console.error('Error en getUserProfile:', error);
    throw error;
  }
};

// ==========================================
// 3. ACTUALIZAR EL PERFIL DEL USUARIO
// ==========================================
export const updateUserProfile = async (token, profileData) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/tesis_profile.php?token=${token}&action=update`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profileData)
    });

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Hubo un error al guardar el perfil.');
    }

    return result;
  } catch (error) {
    console.error('Error en updateUserProfile:', error);
    throw error;
  }
};

// ==========================================
// 4. EJECUTAR ACCIÓN SOBRE UN MÓDULO (Ocultar, Mostrar, Borrar, Duplicar)
// ==========================================
export const executeModuleAction = async (token, action, cmid) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/tesis_actions.php?token=${token}&action=${action}&cmid=${cmid}`;

  try {
    const response = await fetch(url);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || `Error al ejecutar la acción: ${action}`);
    }

    return true;
  } catch (error) {
    console.error(`Error en executeModuleAction (${action}):`, error);
    throw error;
  }
};

// ==========================================
// 5. OBTENER MIS CURSOS (CATÁLOGO)
// ==========================================
export const getMyCourses = async (token, userid) => {
  if (!token || !userid) throw new Error('Se requiere sesión y ID de usuario activo.');

  // Usamos el Web Service nativo de Moodle para traer los cursos del usuario
  const url = `/moodle_api/webservice/rest/server.php?wstoken=${token}&wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json&userid=${userid}`;

  try {
    const response = await fetch(url, { method: 'POST' });
    const data = await response.json();

    if (data.exception) {
      throw new Error(data.message || 'Error al obtener tus cursos.');
    }

    // Moodle devuelve un array de objetos con id, fullname, shortname, etc.
    return data;
  } catch (error) {
    console.error('Error en getMyCourses:', error);
    throw error;
  }
};