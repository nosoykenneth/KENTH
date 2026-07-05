// Contrato: el cliente NUNCA debe listar como fuente citable el material interno
// del tutor (visible_to_student=false: guías del tutor, QA, manifiestos, prompts de
// evaluación). Verifica el helper puro filterVisibleSources / isSourceVisibleToStudent.
import assert from 'node:assert/strict';

import {
  filterVisibleSources,
  isSourceVisibleToStudent,
} from '../src/shared/utils/sources.js';

// --- isSourceVisibleToStudent: robusto ante bool, número, string y ausencia ---
assert.equal(isSourceVisibleToStudent({ visible_to_student: true }), true);
assert.equal(isSourceVisibleToStudent({ visible_to_student: false }), false);
assert.equal(isSourceVisibleToStudent({ visible_to_student: 'true' }), true);
assert.equal(isSourceVisibleToStudent({ visible_to_student: 'false' }), false); // string
assert.equal(isSourceVisibleToStudent({ visible_to_student: 'False' }), false);
assert.equal(isSourceVisibleToStudent({ visible_to_student: '0' }), false);
assert.equal(isSourceVisibleToStudent({ visible_to_student: 1 }), true);
assert.equal(isSourceVisibleToStudent({ visible_to_student: 0 }), false);
assert.equal(isSourceVisibleToStudent({ visible_to_student: 'no' }), false);
assert.equal(isSourceVisibleToStudent({ filename: 'x.md' }), true); // sin flag -> visible (legacy)
assert.equal(isSourceVisibleToStudent(null), false);
assert.equal(isSourceVisibleToStudent('nope'), false);

// --- filterVisibleSources: oculta material interno, conserva lo visible ---
const fuentes = [
  { filename: '01_contenido_canonico.md', visible_to_student: true },
  { filename: '02_guia_tutor_ia.md', visible_to_student: false },   // guía interna
  { filename: '03_momentos_clase.md', visible_to_student: false },  // interno
  { filename: '00_QA_CORPUS_SECCION_0.md', visible_to_student: 'false' }, // QA (string)
  { filename: '00_manifest_indexacion_seccion.md', visible_to_student: false }, // manifest
  { filename: '10_prompt_evaluacion.md', visible_to_student: false }, // evaluación
  { filename: '05_preguntas_frecuentes.md', visible_to_student: true },
  { filename: 'transcript_legacy.md' }, // sin flag -> visible
];

const visibles = filterVisibleSources(fuentes);
const nombres = visibles.map((f) => f.filename);

const prohibidos = [
  '02_guia_tutor_ia.md',
  '03_momentos_clase.md',
  '00_QA_CORPUS_SECCION_0.md',
  '00_manifest_indexacion_seccion.md',
  '10_prompt_evaluacion.md',
];
for (const p of prohibidos) {
  assert.ok(!nombres.includes(p), `Fuente interna NO debe exponerse: ${p}`);
}
assert.ok(nombres.includes('01_contenido_canonico.md'));
assert.ok(nombres.includes('05_preguntas_frecuentes.md'));
assert.ok(nombres.includes('transcript_legacy.md'));
assert.equal(visibles.length, 3);

// --- entradas raras no rompen ---
assert.deepEqual(filterVisibleSources(null), []);
assert.deepEqual(filterVisibleSources(undefined), []);

console.log('OK - chat source visibility contract (fuentes internas ocultas al alumno)');
