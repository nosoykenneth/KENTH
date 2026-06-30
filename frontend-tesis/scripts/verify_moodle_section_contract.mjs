import assert from 'node:assert/strict';

import {
  activityContextFromMoodleModule,
} from '../src/shared/services/activityContext.js';
import {
  upsertLesson,
  upsertResourceLink,
} from '../src/shared/services/sectionsService.js';
import {
  resolveLessonForResource,
} from '../src/shared/services/lessonAutoAssignment.js';

globalThis.localStorage = {
  getItem(key) {
    if (key === 'moodle_token') return 'test-token';
    return '';
  },
};

const requests = [];
globalThis.fetch = async (url, options = {}) => {
  requests.push({
    url: String(url),
    method: options.method || 'GET',
    headers: options.headers || {},
    body: options.body ? JSON.parse(options.body) : null,
  });
  return {
    ok: true,
    status: 200,
    async json() {
      return { ok: true };
    },
  };
};

const ctx = activityContextFromMoodleModule(
  { id: 987, modname: 'h5pactivity', name: 'H5P filtros', description: 'Clase interactiva' },
  { id: 15, name: 'Tema filtros', section: 7 },
  { courseId: '2', sectionOrder: 3, lessonId: 'SEC15-L01' },
);

assert.equal(ctx.moodle_section_id, '15');
assert.equal(ctx.current_lesson_id, 'SEC15-L01');
assert.equal(ctx.current_section_name, 'Tema filtros');
assert.equal(ctx.current_section_order, 3);

const secciones = [{
  id: 15,
  name: 'Tema filtros',
  modules: [
    { id: 987, name: 'Leccion A' },
    { id: 988, name: 'Leccion B' },
  ],
}];
const lessons = [
  { lesson_id: 'SEC15-L01', moodle_section_id: '15', order: 1 },
  { lesson_id: 'SEC15-L02', moodle_section_id: '15', order: 2 },
];

// La identidad de la leccion se ancla al cmid del modulo (lessonIdForResource),
// NO a su posicion: reordenar los modulos de la seccion NO debe cambiar el
// lesson_id resuelto (invariante anti-swap; reemplaza al antiguo resolver por
// orden de Moodle). Tambien se verifica que el moodle_section_id viaja correcto.
const resolved = resolveLessonForResource({ resource: { id: 987 }, secciones, lessons });
assert.equal(resolved.lesson_id, 'SEC15-R987');
assert.equal(resolved.moodle_section_id, '15');

const resolvedReordered = resolveLessonForResource({
  resource: { id: 987 },
  secciones: [{ ...secciones[0], modules: [...secciones[0].modules].reverse() }],
  lessons,
});
assert.equal(resolvedReordered.lesson_id, 'SEC15-R987'); // estable pese al reorden
assert.equal(resolvedReordered.moodle_section_id, '15');

// Un vinculo explicito (resourceLinks) gana sobre la identidad derivada del cmid.
const resolvedLinked = resolveLessonForResource({
  resource: { id: 987 },
  secciones,
  lessons,
  resourceLinks: { 987: { lesson_id: 'SEC15-L01' } },
});
assert.equal(resolvedLinked.lesson_id, 'SEC15-L01');
assert.equal(resolvedLinked.moodle_section_id, '15');

await upsertLesson('2', 'S15-L01', {
  lesson_id: 'S15-L01',
  axis_id: '',
  moodle_section_id: '15',
  title: 'Leccion nueva',
});

await upsertResourceLink('987', {
  lesson_id: 'S15-L01',
  course_id: '2',
  moodle_section_id: '15',
  resource_type: 'web_page',
  resource_subtype: 'h5p_video',
});

const lessonRequest = requests.find((r) => r.url.includes('/authoring/lessons/S15-L01'));
const linkRequest = requests.find((r) => r.url.includes('/sections/links/987'));

assert.equal(lessonRequest.method, 'PUT');
assert.equal(lessonRequest.body.moodle_section_id, '15');
assert.equal(linkRequest.method, 'PUT');
assert.equal(linkRequest.body.moodle_section_id, '15');

console.log('OK - frontend moodle_section_id contract');
