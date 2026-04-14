import { requestMoodleRestJson } from '@/shared/lib/moodleApi';

/**
 * Obtiene los cursos matriculados de un usuario específico.
 * @param {string} token - Moodle Token
 * @param {string|number} userid - Id del usuario en Moodle
 * @returns {Promise<Array>} Array de objetos curso
 */
export const getEnrolledCourses = async (token, userid) => {
  const data = await requestMoodleRestJson({
    wstoken: token,
    wsfunction: 'core_enrol_get_users_courses',
    moodlewsrestformat: 'json',
    userid: userid,
  });

  if (data.exception) {
    throw new Error(data.message);
  }

  // Moodle retorna un arreglo vacio si no hay cursos, o el arreglo poblado.
  // Es importante asegurarnos de retornar un arreglo.
  return Array.isArray(data) ? data : [];
};

/**
 * Función para crear un nuevo curso (Usado por los Profesores/Admins).
 * @param {string} token - Moodle Token
 * @param {string} fullName - Nombre completo del curso
 * @param {string} shortName - Nombre corto identificativo (único)
 * @param {string} summary - Resumen del curso
 * @returns {Promise<Object>} Resultado de la creación
 */
export const createCourse = async (token, fullName, shortName, summary) => {
  const data = await requestMoodleRestJson({
    wstoken: token,
    wsfunction: 'core_course_create_courses',
    moodlewsrestformat: 'json',
    'courses[0][fullname]': fullName,
    'courses[0][shortname]': shortName,
    'courses[0][categoryid]': 1,
    'courses[0][summary]': summary,
    'courses[0][visible]': 1,
  });

  if (data.exception) {
    throw new Error(data.message);
  }

  // Moodle responde con un array de cursos creados. Nosotros retornamos el primero.
  return data[0] || data;
};

/**
 * Obtiene el contenido de un curso (Secciones y modulos).
 * @param {string} token
 * @param {string|number} courseid
 * @returns {Promise<Array>}
 */
export const getCourseContents = async (token, courseid) => {
  const data = await requestMoodleRestJson({
    wstoken: token,
    wsfunction: 'core_course_get_contents',
    moodlewsrestformat: 'json',
    courseid: courseid,
  });

  if (data.exception) throw new Error(data.message);
  return data;
};

/**
 * Crea una etiqueta (Label) en el curso y seccion indicados
 * @param {string} token
 * @param {string|number} courseid
 * @param {string|number} section
 * @param {string} content
 * @returns {Promise<string>} Mensaje de exito/error de Moodle
 */
export const createCourseLabel = async (token, courseid, section, content) => {
  const data = await requestMoodleRestJson({
    wstoken: token,
    wsfunction: 'local_tesisai_create_label',
    moodlewsrestformat: 'json',
    courseid: courseid,
    section: section,
    content: content,
  });

  if (data.exception) throw new Error(data.message);
  return data;
};

/**
 * Crea una tarea (Assign) híbrida en el curso y seccion indicados
 * @param {string} token
 * @param {string|number} courseid
 * @param {string|number} section
 * @param {string} name
 * @param {string} description
 * @param {number} duedate
 * @returns {Promise<string>} Mensaje de exito/error de Moodle
 */
export const createCourseAssign = async (token, courseid, section, name, description, duedate) => {
  const data = await requestMoodleRestJson({
    wstoken: token,
    wsfunction: 'local_tesisai_create_assign',
    moodlewsrestformat: 'json',
    courseid: courseid,
    section: section,
    name: name,
    description: description,
    duedate: duedate,
  });

  if (data.exception) throw new Error(data.message);
  return data;
};
