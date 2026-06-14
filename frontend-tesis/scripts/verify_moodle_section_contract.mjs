import assert from 'node:assert/strict';

import {
  activityContextFromMoodleModule,
} from '../src/shared/services/activityContext.js';
import {
  upsertLesson,
  upsertResourceLink,
} from '../src/shared/services/sectionsService.js';
import {
  resolveLessonByMoodleOrder,
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

assert.equal(
  resolveLessonByMoodleOrder({ resource: { id: 987 }, secciones, lessons }).lesson_id,
  'SEC15-L01',
);
assert.equal(
  resolveLessonByMoodleOrder({
    resource: { id: 987 },
    secciones: [{ ...secciones[0], modules: [...secciones[0].modules].reverse() }],
    lessons,
  }).lesson_id,
  'SEC15-L02',
);

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
