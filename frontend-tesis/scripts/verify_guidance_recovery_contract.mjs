// Contrato: la guía del tutor (H5P learning_signals) NO debe perderse.
// - se persiste con mensaje por curso+lección (recuperable tras recarga);
// - dedupe por intento (mismo id no re-notifica si ya fue vista);
// - el sonido solo suena la PRIMERA vez (renotify tras recarga = sin sonido);
// - "Ver guía del tutor" recupera el mensaje aunque ya haya sido visto;
// - la guía de una lección jamás se cruza a otra (clave por lección);
// - las guías viejas (>7 días) expiran; el formato legado (solo id) no revive.
import assert from 'node:assert/strict';

import {
  guidanceStorageKey,
  readStoredGuidance,
  writeStoredGuidance,
  registerGuidance,
  markNotified,
  markSeen,
  recoverableGuidance,
  pendingGuidance,
} from '../src/shared/utils/guidanceStore.js';

// localStorage simulado
const makeStorage = () => {
  const m = new Map();
  return {
    getItem: (k) => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
    removeItem: (k) => m.delete(k),
  };
};

const NOW = 1_800_000_000_000;

// --- clave por curso+lección (no cruza lecciones) ---
assert.equal(guidanceStorageKey('2', 'SEC2-R59'), 'kenth:h5p-guidance:2:SEC2-R59');
assert.notEqual(guidanceStorageKey('2', 'SEC2-R59'), guidanceStorageKey('2', 'SEC2-R56'));
assert.equal(guidanceStorageKey('', 'SEC2-R59'), '');
assert.equal(guidanceStorageKey('2', ''), '');

// --- flujo: llega guía nueva con chat cerrado -> notify (badge + sonido) ---
const storage = makeStorage();
const g1 = { id: 'hvp:25:u:40:t:111', message: 'Conviene reforzar gain staging. Vuelve al minuto 3:45.' };
let stored = readStoredGuidance(storage, '2', 'SEC2-R59', NOW);
assert.equal(stored, null);
let r = registerGuidance(stored, g1, NOW);
assert.equal(r.action, 'notify');
writeStoredGuidance(storage, '2', 'SEC2-R59', markNotified(r.entry, NOW));

// --- recarga de página: misma guía sin ver -> renotify (badge SÍ, sonido NO) ---
stored = readStoredGuidance(storage, '2', 'SEC2-R59', NOW + 1000);
assert.ok(stored && stored.notified_at === NOW && !stored.seen_at);
assert.deepEqual(pendingGuidance(stored), { id: g1.id, message: g1.message }, 'tras recarga el badge debe restaurarse');
r = registerGuidance(stored, g1, NOW + 1000);
assert.equal(r.action, 'renotify', 'mismo intento notificado pero no visto -> re-badge sin sonido');

// --- el estudiante abre el chat: se marca vista; ya no re-notifica ---
writeStoredGuidance(storage, '2', 'SEC2-R59', markSeen(stored, NOW + 2000));
stored = readStoredGuidance(storage, '2', 'SEC2-R59', NOW + 3000);
assert.ok(stored.seen_at);
assert.equal(pendingGuidance(stored), null, 'vista -> sin badge pendiente');
r = registerGuidance(stored, g1, NOW + 3000);
assert.equal(r.action, 'skip_seen', 'mismo intento ya visto -> dedupe total');

// --- pero "Ver guía del tutor" SÍ puede recuperarla (aunque esté vista) ---
assert.deepEqual(recoverableGuidance(stored), { id: g1.id, message: g1.message });

// --- intento NUEVO (otro attempt_id) -> vuelve a notificar con sonido ---
const g2 = { id: 'hvp:25:u:40:t:222', message: 'Nueva guía: ahora conviene reforzar buses.' };
r = registerGuidance(stored, g2, NOW + 4000);
assert.equal(r.action, 'notify');
assert.equal(r.entry.seen_at, 0);
assert.equal(r.entry.notified_at, 0);

// --- no cruza lecciones: R56 no ve nada de R59 ---
assert.equal(readStoredGuidance(storage, '2', 'SEC2-R56', NOW), null);

// --- guía inválida no rompe ni pisa nada ---
r = registerGuidance(stored, { id: '', message: '' }, NOW);
assert.equal(r.action, 'skip');
r = registerGuidance(stored, null, NOW);
assert.equal(r.action, 'skip');

// --- expiración: guía de hace 8 días ya no revive el badge ---
const oldStorage = makeStorage();
writeStoredGuidance(oldStorage, '2', 'SEC2-R59', {
  id: 'x', message: 'vieja', created_at: NOW - 8 * 24 * 3600 * 1000, notified_at: 1, seen_at: 0,
});
assert.equal(readStoredGuidance(oldStorage, '2', 'SEC2-R59', NOW), null, 'guías viejas expiran');

// --- formato legado (solo id string): sin mensaje -> se trata como vista ---
const legacyStorage = makeStorage();
legacyStorage.setItem(guidanceStorageKey('2', 'SEC2-R59'), g1.id);
const legacy = readStoredGuidance(legacyStorage, '2', 'SEC2-R59', NOW);
assert.ok(legacy.legacy && legacy.seen_at, 'legado sin mensaje no debe re-notificar');
assert.equal(pendingGuidance(legacy), null);
assert.equal(recoverableGuidance(legacy), null);
r = registerGuidance(legacy, g1, NOW);
assert.equal(r.action, 'skip_seen', 'mismo id legado ya notificado -> no duplicar');

// --- storage roto no lanza ---
assert.equal(readStoredGuidance({ getItem() { throw new Error('boom'); } }, '2', 'L', NOW), null);
writeStoredGuidance({ setItem() { throw new Error('boom'); } }, '2', 'L', { id: 'a', message: 'b' });

console.log('OK - guidance recovery contract (la guía del tutor no se pierde, no se duplica y es recuperable)');
