// guidanceStore — persistencia local del "pending_guidance" del tutor por
// curso+lección. Resuelve el problema UX: el mensaje automático de orientación
// (H5P learning_signals) no debe perderse si el estudiante cierra el chat,
// recarga la página o vuelve más tarde; el badge "Conviene reforzar · el tutor
// tiene una guía" debe poder RECUPERARLO siempre.
//
// Modelo guardado (JSON en localStorage, clave por curso+lección — la guía de
// SEC2-R59 jamás se cruza con SEC2-R56):
//   { id, message, created_at, notified_at, seen_at }
//   - id          : guidance_id (attempt_id/signal_hash) => dedupe por intento.
//   - message     : texto determinístico completo (recuperable tras recarga).
//   - notified_at : primera notificación (badge/sonido). El sonido NO se repite.
//   - seen_at     : el estudiante ya lo vio en el chat. No se re-notifica.
//
// Lógica pura (sin React/window) para poder testearla por contrato en Node.

const MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; // guía "reciente": 7 días

export const guidanceStorageKey = (courseId, lessonId) => (
  courseId && lessonId ? `kenth:h5p-guidance:${courseId}:${lessonId}` : ''
);

/** Lee la guía guardada. Tolera el formato legado (solo el id como string):
 *  sin mensaje no hay nada que recuperar, se trata como vista para no
 *  re-notificar infinitamente. Guías más viejas que MAX_AGE_MS expiran. */
export function readStoredGuidance(storage, courseId, lessonId, now = Date.now()) {
  const key = guidanceStorageKey(courseId, lessonId);
  if (!key || !storage) return null;
  let raw = null;
  try { raw = storage.getItem(key); } catch { return null; }
  if (!raw) return null;
  let parsed = null;
  try { parsed = JSON.parse(raw); } catch { parsed = null; }
  if (!parsed || typeof parsed !== 'object' || !parsed.id) {
    return { id: String(raw), message: '', created_at: 0, notified_at: 0, seen_at: 1, legacy: true };
  }
  if (parsed.created_at && now - parsed.created_at > MAX_AGE_MS) return null;
  return parsed;
}

export function writeStoredGuidance(storage, courseId, lessonId, entry) {
  const key = guidanceStorageKey(courseId, lessonId);
  if (!key || !storage || !entry) return;
  try { storage.setItem(key, JSON.stringify(entry)); } catch { /* cuota llena: la UI sigue */ }
}

/**
 * Decide qué hacer al RECIBIR una guía nueva del backend.
 * Devuelve { entry, action }:
 *  - 'skip'     : guía inválida (sin id/mensaje) => no hacer nada.
 *  - 'skip_seen': mismo intento ya visto => no re-notificar (dedupe).
 *  - 'renotify' : mismo intento aún no visto (p.ej. tras recarga) =>
 *                 mostrar badge de nuevo pero SIN repetir el sonido.
 *  - 'notify'   : intento nuevo => notificación completa (badge + sonido).
 */
export function registerGuidance(stored, guidance, now = Date.now()) {
  const id = guidance?.id || '';
  const message = guidance?.message || '';
  if (!id || !message) return { entry: stored || null, action: 'skip' };
  if (stored && stored.id === id) {
    if (stored.seen_at) return { entry: stored, action: 'skip_seen' };
    return {
      entry: { ...stored, message: stored.message || message },
      action: stored.notified_at ? 'renotify' : 'notify',
    };
  }
  return {
    entry: { id, message, created_at: now, notified_at: 0, seen_at: 0 },
    action: 'notify',
  };
}

export function markNotified(entry, now = Date.now()) {
  if (!entry) return entry;
  return entry.notified_at ? entry : { ...entry, notified_at: now };
}

export function markSeen(entry, now = Date.now()) {
  if (!entry) return entry;
  return { ...entry, seen_at: entry.seen_at || now };
}

/** Guía recuperable para reinsertar en el chat (aunque ya haya sido vista:
 *  el alumno siempre puede volver a pedirla desde el badge). */
export function recoverableGuidance(stored) {
  if (!stored || !stored.id || !stored.message) return null;
  return { id: stored.id, message: stored.message };
}

/** Guía pendiente de VER (para restaurar el badge tras recargar la página). */
export function pendingGuidance(stored) {
  const rec = recoverableGuidance(stored);
  return rec && !stored.seen_at ? rec : null;
}
