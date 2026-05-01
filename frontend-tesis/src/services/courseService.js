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

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=get`;

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

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=update`;

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

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=${action}&cmid=${cmid}`;

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
// 5.1 OBTENER TODAS LAS CATEGORÍAS DISPONIBLES
// ==========================================
export const getCategories = async (token) => {
  if (!token) throw new Error('Se requiere token para obtener categorías.');
  const url = `/moodle_api/webservice/rest/server.php?wstoken=${token}&wsfunction=core_course_get_categories&moodlewsrestformat=json`;
  
  try {
    const response = await fetch(url, { method: 'POST' });
    const data = await response.json();
    if (data.exception) throw new Error(data.message);
    return data;
  } catch (err) {
    console.error('Error en getCategories:', err);
    throw err;
  }
};

// ==========================================
// 5. OBTENER MIS CURSOS (CATÁLOGO) Y SUS CATEGORÍAS
// ==========================================
export const getMyCourses = async (token, userid) => {
  if (!token || !userid) throw new Error('Se requiere sesión y ID de usuario activo.');

  const urlCursos = `/moodle_api/webservice/rest/server.php?wstoken=${token}&wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json&userid=${userid}`;
  const urlCategorias = `/moodle_api/webservice/rest/server.php?wstoken=${token}&wsfunction=core_course_get_categories&moodlewsrestformat=json`;

  try {
    // 1. Obtener los cursos
    const responseCursos = await fetch(urlCursos, { method: 'POST' });
    const cursos = await responseCursos.json();

    if (cursos.exception) throw new Error(cursos.message || 'Error al obtener tus cursos.');

    // 2. Obtener las categorías (sin detener el flujo si falla)
    let categorias = [];
    try {
       const resCategorias = await fetch(urlCategorias, { method: 'POST' });
       const dataCategorias = await resCategorias.json();
       if (!dataCategorias.exception) {
           categorias = dataCategorias;
       }
    } catch (catErr) {
       console.warn('No se pudieron cargar las categorías, usando fallback.');
    }

    // 3. Cruzar los datos: Inyectar el nombre de la categoría en cada curso
    return cursos.map(curso => {
      const categoria = categorias.find(cat => cat.id === curso.category);
      return {
        ...curso,
        categoryname: categoria ? categoria.name : 'CURSO' // Fallback si no encuentra la categoría
      };
    });
  } catch (error) {
    console.error('Error en getMyCourses:', error);
    throw error;
  }
};

// ==========================================
// 6. OBTENER AJUSTES DE UN CURSO (API PERSISTENTE)
// ==========================================
export const getCourseSettings = async (token, courseId) => {
  if (!token) throw new Error('No hay sesión activa.');

  // EL SECRETO: Añadir &t=${Date.now()} al final para destruir el caché del navegador
  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_course_settings.php?token=${token}&courseid=${courseId}&action=get&t=${Date.now()}`;

  try {
    const response = await fetch(url);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'No se pudieron cargar los ajustes del curso.');
    }

    return result.data;
  } catch (error) {
    console.error('Error en getCourseSettings:', error);
    throw error;
  }
};

// ==========================================
// 7. ACTUALIZAR AJUSTES DE UN CURSO
// ==========================================
export const updateCourseSettings = async (token, courseId, settingsData) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_course_settings.php?token=${token}&courseid=${courseId}&action=update`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(settingsData)
    });

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Hubo un error al guardar los ajustes del curso.');
    }

    return result;
  } catch (error) {
    console.error('Error en updateCourseSettings:', error);
    throw error;
  }
};