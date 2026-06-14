export function findMoodleModuleLocation(secciones = [], moduleId = '') {
  const target = String(moduleId || '');
  if (!target) return null;
  for (let sectionIndex = 0; sectionIndex < secciones.length; sectionIndex += 1) {
    const section = secciones[sectionIndex];
    const modules = Array.isArray(section?.modules) ? section.modules : [];
    const moduleIndex = modules.findIndex((mod) => String(mod?.id || '') === target);
    if (moduleIndex >= 0) {
      return { section, sectionIndex, moduleIndex };
    }
  }
  return null;
}

// Identidad ESTABLE de la leccion: se ancla al cmid del modulo Moodle, no a su
// posicion. Asi, si el profe reordena los videos dentro de la seccion, la
// metadata/transcripcion/bloques (que se guardan por lesson_id) viajan con el
// video y nunca se intercambian con el de al lado.
export function lessonIdForResource(moodleSectionId, resourceId) {
  const cleanSectionId = String(moodleSectionId || 'section').replace(/[^a-zA-Z0-9_-]/g, '');
  const cleanResourceId = String(resourceId || '').replace(/[^a-zA-Z0-9_-]/g, '');
  return `SEC${cleanSectionId}-R${cleanResourceId}`;
}

export function resolveLessonForResource({ resource, secciones = [], lessons = [], resourceLinks = {} } = {}) {
  const location = findMoodleModuleLocation(secciones, resource?.id);
  if (!location) return null;

  const { section, sectionIndex, moduleIndex } = location;
  const moodleSectionId = String(section?.id || section?.moodle_section_id || '');
  // El numero "Leccion N" es solo presentacion: se calcula en vivo por la
  // posicion actual en Moodle. NO forma parte de la identidad de la leccion.
  const lessonOrder = moduleIndex + 1;

  // La identidad sale del vinculo explicito si existe; si no, se deriva del
  // cmid. Nunca se reutiliza una leccion por coincidir en posicion.
  const link = resourceLinks[String(resource?.id)];
  const targetLessonId = link?.lesson_id || lessonIdForResource(moodleSectionId, resource?.id);
  const existingLesson = (lessons || []).find((l) => String(l.lesson_id) === targetLessonId) || null;

  return {
    lesson_id: targetLessonId,
    lesson_title: existingLesson?.lesson_title || existingLesson?.title || resource?.name || `Leccion ${lessonOrder}`,
    moodle_section_id: moodleSectionId,
    current_section_name: section?.name || section?.section_name || `Tema ${sectionIndex + 1}`,
    current_section_order: sectionIndex + 1,
    lesson_order: lessonOrder,
    module_index: moduleIndex,
    section,
    existing_lesson: existingLesson,
  };
}
