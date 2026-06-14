/**
 * activityContext.js
 *
 * Capa 2 del tutor contextual en el frontend.
 *
 * Construye el objeto `activity_context` que se manda al backend en /chat.
 * El contrato corresponde 1 a 1 con `models/context.py::ActivityContext`
 * del backend (tesis-rag). NO se mandan transcripciones ni recursos
 * pesados: solo metadata.
 */

// Tipos de recurso soportados por el backend.
export const RESOURCE_TYPES = Object.freeze({
  VIDEO: 'video',
  PDF: 'pdf',
  WEB_PAGE: 'web_page',
  DOWNLOADABLE_FILE: 'downloadable_file',
  IMAGE_REFERENCE: 'image_reference',
  LESSON_NOTE: 'lesson_note',
});

// Modos de interaccion del tutor.
export const INTERACTION_MODES = Object.freeze({
  TEORIA: 'teoria',
  PRACTICA: 'practica',
  TROUBLESHOOTING: 'troubleshooting',
  REVISION: 'revision',
  NAVEGACION_DE_RECURSO: 'navegacion_de_recurso',
});

// Subtipos para refinar `resource_type = web_page` sin romper el enum
// del backend. Hoy se usan principalmente para H5P (contenedor de
// videos/clases interactivas en el curso).
export const RESOURCE_SUBTYPES = Object.freeze({
  H5P_ACTIVITY: 'h5p_activity',         // generico Moodle h5pactivity
  H5P_VIDEO: 'h5p_video',               // H5P Interactive Video
  H5P_INTERACTIVE: 'h5p_interactive',   // course presentation, quiz, branching, etc.
});

/**
 * Mapea un Moodle modname (page, resource, url, h5pactivity, etc.)
 * al ResourceType del contrato backend.
 */
export function moodleModnameToResourceType(modname, fileExt = '') {
  const m = (modname || '').toLowerCase();
  const ext = (fileExt || '').toLowerCase();

  if (m === 'url') return RESOURCE_TYPES.WEB_PAGE;
  if (m === 'page') return RESOURCE_TYPES.WEB_PAGE;
  if (m === 'label') return RESOURCE_TYPES.LESSON_NOTE;
  if (m === 'h5pactivity' || m === 'hvp') return RESOURCE_TYPES.WEB_PAGE;
  if (m === 'quiz') return RESOURCE_TYPES.LESSON_NOTE;

  if (m === 'resource') {
    if (ext === 'pdf') return RESOURCE_TYPES.PDF;
    if (['mp4', 'webm', 'mov', 'm4v'].includes(ext)) return RESOURCE_TYPES.VIDEO;
    if (['png', 'jpg', 'jpeg', 'webp', 'gif'].includes(ext)) return RESOURCE_TYPES.IMAGE_REFERENCE;
    return RESOURCE_TYPES.DOWNLOADABLE_FILE;
  }

  return RESOURCE_TYPES.LESSON_NOTE;
}

/**
 * Detecta si un modulo Moodle es H5P (h5pactivity moderno o hvp legacy).
 */
export function isH5PModule(mod) {
  if (!mod) return false;
  const m = (mod.modname || '').toLowerCase();
  return m === 'h5pactivity' || m === 'hvp';
}

/**
 * Resuelve el subtipo H5P. Por ahora hace una clasificacion blanda por
 * nombre/descripcion del modulo. Cuando se conecte un listener de
 * eventos H5P (xAPI: video.played, video.paused, slide.viewed, etc.)
 * este helper podra leer el contentType real y devolver el subtipo
 * exacto.
 */
export function detectH5PSubtype(mod) {
  if (!isH5PModule(mod)) return '';
  const haystack = `${mod.name || ''} ${mod.description || ''}`.toLowerCase();
  if (/video|clase|leccion grabada|interactive video/.test(haystack)) {
    return RESOURCE_SUBTYPES.H5P_VIDEO;
  }
  if (/quiz|cuestionario|branching|presentation|presentacion|interact/.test(haystack)) {
    return RESOURCE_SUBTYPES.H5P_INTERACTIVE;
  }
  return RESOURCE_SUBTYPES.H5P_ACTIVITY;
}

/**
 * Default razonable de interaction_mode segun el tipo (y subtipo) de recurso.
 * El componente puede sobreescribirlo si tiene mejor info.
 */
export function defaultInteractionMode(resourceType, resourceSubtype = '') {
  // H5P toma precedencia sobre el tipo base web_page.
  if (resourceSubtype === RESOURCE_SUBTYPES.H5P_VIDEO) {
    return INTERACTION_MODES.NAVEGACION_DE_RECURSO;
  }
  if (
    resourceSubtype === RESOURCE_SUBTYPES.H5P_ACTIVITY ||
    resourceSubtype === RESOURCE_SUBTYPES.H5P_INTERACTIVE
  ) {
    return INTERACTION_MODES.PRACTICA;
  }

  switch (resourceType) {
    case RESOURCE_TYPES.VIDEO:
      return INTERACTION_MODES.NAVEGACION_DE_RECURSO;
    case RESOURCE_TYPES.PDF:
    case RESOURCE_TYPES.DOWNLOADABLE_FILE:
      return INTERACTION_MODES.REVISION;
    case RESOURCE_TYPES.WEB_PAGE:
      return INTERACTION_MODES.TEORIA;
    case RESOURCE_TYPES.IMAGE_REFERENCE:
      return INTERACTION_MODES.TROUBLESHOOTING;
    default:
      return INTERACTION_MODES.TEORIA;
  }
}

/**
 * Builder canonico. Devuelve null si no hay nada util que mandar
 * (asi el aiService puede omitir el campo y el backend degrada limpio).
 *
 * @param {object} input
 * @param {string|number} [input.courseId]
 * @param {string|number} [input.moodleSectionId]
 * @param {string|number} [input.lessonId]
 * @param {string|number} [input.resourceId]
 * @param {string} [input.resourceType]   uno de RESOURCE_TYPES
 * @param {number} [input.timestamp]      segundos (videos)
 * @param {number} [input.page]           pagina (PDFs)
 * @param {string} [input.section]
 * @param {string} [input.sectionName]
 * @param {number} [input.sectionOrder]
 * @param {string} [input.learningGoal]
 * @param {string} [input.expectedAction]
 * @param {string} [input.interactionMode] uno de INTERACTION_MODES
 */
export function buildActivityContext(input = {}) {
  const {
    courseId = '',
    moodleSectionId = '',
    lessonId = '',
    resourceId = '',
    resourceType = null,
    resourceSubtype = '',
    timestamp = null,
    page = null,
    section = '',
    sectionName = '',
    sectionOrder = null,
    learningGoal = '',
    expectedAction = '',
    interactionMode = null,
  } = input;

  const ctx = {
    course_id: courseId ? String(courseId) : '',
    moodle_section_id: moodleSectionId ? String(moodleSectionId) : '',
    current_lesson_id: lessonId ? String(lessonId) : '',
    current_resource_id: resourceId ? String(resourceId) : '',
    current_resource_type: resourceType || null,
    resource_subtype: resourceSubtype || '',
    current_timestamp: typeof timestamp === 'number' ? timestamp : null,
    current_page: typeof page === 'number' ? page : null,
    current_section: section || '',
    current_section_name: sectionName || section || '',
    current_section_order: typeof sectionOrder === 'number' ? sectionOrder : null,
    learning_goal: learningGoal || '',
    expected_action: expectedAction || '',
    interaction_mode:
      interactionMode || defaultInteractionMode(resourceType, resourceSubtype),
  };

  const tieneAlgo =
    ctx.moodle_section_id ||
    ctx.course_id ||
    ctx.current_lesson_id ||
    ctx.current_resource_id ||
    ctx.current_section ||
    ctx.current_section_name ||
    ctx.learning_goal;

  return tieneAlgo ? ctx : null;
}

/**
 * Atajo para construir contexto desde un modulo Moodle estandar
 * (el shape que ya devuelve courseService).
 */
export function activityContextFromMoodleModule(mod, seccion = null, extra = {}) {
  if (!mod) return null;

  const fileExt = (() => {
    const url = mod.url || '';
    const match = url.match(/\.([a-z0-9]+)(?:\?|$)/i);
    return match ? match[1] : '';
  })();

  const resourceType = moodleModnameToResourceType(mod.modname, fileExt);
  // Para H5P (contenedor principal de videos/clases del curso) refinamos
  // el tipo base con un subtype. Permite distinguir "h5p_video" de
  // "h5p_interactive" sin tocar el enum del backend.
  const resourceSubtype = isH5PModule(mod) ? detectH5PSubtype(mod) : '';

  return buildActivityContext({
    courseId: extra.courseId || '',
    moodleSectionId: extra.moodleSectionId || extra.moodle_section_id || seccion?.id || '',
    lessonId: extra.lessonId || extra.lesson_id || mod.id,
    resourceId: mod.id,
    resourceType,
    resourceSubtype,
    section: seccion?.name || '',
    sectionName: extra.sectionName || seccion?.name || '',
    sectionOrder: typeof extra.sectionOrder === 'number'
      ? extra.sectionOrder
      : (typeof seccion?.section === 'number' ? seccion.section : null),
    learningGoal: mod.description || '',
    interactionMode:
      extra.interactionMode || defaultInteractionMode(resourceType, resourceSubtype),
    // TODO: cuando exista listener xAPI/H5P, alimentar timestamp en vivo aqui.
    timestamp: extra.timestamp ?? null,
    page: extra.page ?? null,
    ...extra.overrides,
  });
}
