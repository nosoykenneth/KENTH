import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

import { updateMoments, replaceLessonBlocks } from '../src/shared/services/sectionsService.js';

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

console.log('OK - contrato Vista Profesor (momentos/blocks, terminología, video/timeline, sin jerga)');
