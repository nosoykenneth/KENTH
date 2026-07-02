import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

import { updateMoments, replaceLessonBlocks, savePedagogy, toTutorProfile } from '../src/shared/services/sectionsService.js';

/**
 * Contrato de la Vista Profesor (FASE 8, sin runner de componentes).
 *
 * Combina:
 *   1. Contrato de wire: updateMoments -> PUT /moments con SOLO campos pedagógicos
 *      (nunca start_time/end_time/block_order); replaceLessonBlocks -> PUT /blocks.
 *   2. Garantías de fuente: la Vista Profesor usa /moments (no /blocks), muestra
 *      "Momentos de la clase", reutiliza video+timeline y no expone jerga técnica;
 *      el Editor avanzado (admin) conserva "Bloques" y /blocks.
 */

globalThis.localStorage = { getItem: (k) => (k === 'moodle_token' ? 'test-token' : '') };

const requests = [];
globalThis.fetch = async (url, options = {}) => {
  requests.push({ url: String(url), method: options.method || 'GET', body: options.body ? JSON.parse(options.body) : null });
  return { ok: true, status: 200, async json() { return { ok: true }; } };
};

// --- 1. Wire: el profesor guarda momentos por /moments, sin campos de tiempo ---
await updateMoments('2', 'S15-L01', [
  { block_id: 'S15-L01-B1', block_title: 'Momento 1', summary: 's', interaction_mode: 'teoria', tutor_focus: 'f', concepts: ['x'], preguntas_probables: ['q'] },
]);
const momentsReq = requests.find((r) => r.url.includes('/authoring/lessons/S15-L01/moments'));
assert.ok(momentsReq, 'updateMoments debe llamar a /authoring/lessons/{id}/moments');
assert.equal(momentsReq.method, 'PUT');
const m0 = momentsReq.body.moments[0];
assert.equal(m0.block_id, 'S15-L01-B1');
for (const forbidden of ['start_time', 'end_time', 'block_order']) {
  assert.ok(!(forbidden in m0), `el payload de momentos NO debe incluir ${forbidden}`);
}

// --- 1b. /blocks es un endpoint DISTINTO (reservado al editor avanzado/admin) ---
await replaceLessonBlocks('2', 'S15-L01', [{ block_id: 'S15-L01-B1', start_time: 0, end_time: 10 }]);
const blocksReq = requests.find((r) => r.url.includes('/authoring/lessons/S15-L01/blocks'));
assert.ok(blocksReq, 'replaceLessonBlocks debe llamar a /authoring/lessons/{id}/blocks');
assert.notEqual(momentsReq.url, blocksReq.url);

// --- 1c. Perfil pedagógico CANÓNICO: savePedagogy -> PUT /pedagogy; toTutorProfile normaliza ---
await savePedagogy('2', 'S15-L01', { learning_goal: 'Objetivo', tutor_focus: ['reforzar X'], key_concepts: ['a'] });
const pedagogyReq = requests.find((r) => r.url.includes('/authoring/lessons/S15-L01/pedagogy'));
assert.ok(pedagogyReq, 'savePedagogy debe llamar a /authoring/lessons/{id}/pedagogy');
assert.equal(pedagogyReq.method, 'PUT');
assert.equal(pedagogyReq.body.learning_goal, 'Objetivo');

const prof0 = toTutorProfile({
  learning_goal: 'G',
  delegated_to_tutor: ['reforzar'],
  attribution_constraints: ['no spoilers'],
  metadata: { pedagogy: { tutor_tone: 'socratico', key_concepts: ['headroom'], lesson_summary: 'resu' } },
  proactive_message: 'Hola',
  suggested_prompts: ['¿qué es X?'],
  blocks: [{ block_id: 'B1', block_title: 'Intro', tutor_focus: 'activar', concepts: ['c'], preguntas_probables: ['q'], metadata: { common_mistakes: ['err'] }, start_time: 0, end_time: 10 }],
});
assert.equal(prof0.tutor_focus[0], 'reforzar', 'delegated_to_tutor -> tutor_focus');
assert.equal(prof0.tutor_must_not_do[0], 'no spoilers', 'attribution_constraints -> tutor_must_not_do');
assert.equal(prof0.tutor_tone, 'socratico');
assert.equal(prof0.lesson_summary, 'resu');
assert.equal(prof0.proactive_message, 'Hola');
assert.equal(prof0.moments[0].pedagogical_intent, 'activar', 'block.tutor_focus -> moment.pedagogical_intent');
assert.equal(prof0.moments[0].common_mistakes[0], 'err', 'block.metadata.common_mistakes -> moment.common_mistakes');

// --- 2. Garantías de fuente ---
const read = (rel) => readFileSync(fileURLToPath(new URL(rel, import.meta.url)), 'utf8');
const prof = read('../src/shared/components/ai/TutorPedagogyView.jsx');
const admin = read('../src/shared/components/ai/LessonVideoEditor.jsx');

// El profesor guarda por /moments, nunca por /blocks.
assert.ok(prof.includes('updateMoments'), 'Vista Profesor debe importar/usar updateMoments');
assert.ok(!prof.includes('replaceLessonBlocks'), 'Vista Profesor NO debe usar replaceLessonBlocks (/blocks)');

// Terminología pedagógica hacia el profesor: "Momentos de la clase", no "Bloques".
assert.ok(prof.includes('Momentos de la clase'), 'Vista Profesor debe decir "Momentos de la clase"');
assert.ok(!prof.includes('Bloques'), 'Vista Profesor NO debe mostrar la etiqueta "Bloques"');

// Video + línea de tiempo reutilizados, timeline en solo lectura (sin mover tiempos).
assert.ok(prof.includes('useResourceVideoBridge'), 'Vista Profesor debe reutilizar el bridge de video');
assert.ok(prof.includes('<BlockTimeline'), 'Vista Profesor debe renderizar la línea de tiempo');
assert.ok(/readOnly\b/.test(prof), 'la línea de tiempo del profesor debe ir en readOnly');
assert.ok(prof.includes('technical={false}'), 'los recursos del profesor deben ir sin jerga técnica (technical={false})');

// El profesor NO ve jerga técnica.
for (const jerga of ['source_hash', 'retrieval_scope', 'index_status', 'chunk_count']) {
  assert.ok(!prof.includes(jerga), `Vista Profesor NO debe exponer "${jerga}"`);
}

// El Editor avanzado (admin) conserva "Bloques" y el reemplazo técnico por /blocks.
assert.ok(admin.includes('replaceLessonBlocks'), 'Editor avanzado debe usar replaceLessonBlocks (/blocks)');
assert.ok(admin.includes('Bloques'), 'Editor avanzado debe seguir mostrando "Bloques"');

// --- 3. UNIFICACIÓN: mismo modelo canónico + misma IA en ambos editores ---
for (const [name, src] of [['Vista Profesor', prof], ['Editor Avanzado', admin]]) {
  assert.ok(src.includes('toTutorProfile'), `${name} debe leer el perfil canónico (toTutorProfile)`);
  assert.ok(src.includes('savePedagogy'), `${name} debe guardar el perfil canónico (savePedagogy)`);
  assert.ok(src.includes('aiPrepare'), `${name} debe usar el MISMO endpoint de IA (aiPrepare)`);
}
// El admin (editor avanzado) usa 4 pestañas: Lección (perfil canónico + estructura/legacy),
// Bloques, Transcripción y Recursos. El perfil canónico y la IA viven en "Lección".
assert.ok(admin.includes("id: 'leccion'"), 'Admin debe tener la pestaña "Lección"');
assert.ok(admin.includes('Perfil del tutor'), 'La pestaña "Lección" debe contener el perfil canónico del tutor');
assert.ok(admin.includes('Generar con IA'), 'Admin debe tener botón "Generar con IA"');
assert.ok(!admin.includes("id: 'avanzado'"), 'Admin ya NO debe tener una pestaña "Avanzado" separada');
assert.ok(!admin.includes("id: 'perfil'"), 'Admin ya NO debe tener una pestaña "Perfil" separada (fusionada en "Lección")');
assert.ok(admin.includes('Orden dentro de la sección'), 'Admin debe conservar "Orden dentro de la sección" en "Lección"');
// Paso 1 del profesor NO edita momentos (solo timeline visual): el modal de momento
// se abre desde el paso 3 (openEditMoment) y el timeline va en readOnly.
assert.ok(prof.includes('openEditMoment'), 'El profesor edita momentos por modal (paso 3)');

console.log('OK - contrato unificación (perfil canónico compartido, IA única, terminología, sin jerga)');
