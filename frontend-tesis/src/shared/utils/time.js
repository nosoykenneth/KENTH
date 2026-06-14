/**
 * Formatea segundos a `m:ss` (o `h:mm:ss` si supera la hora).
 *
 * Compartido por BlockTimeline y LessonVideoEditor; vive aquí para no romper
 * React Fast Refresh (no exportar utilidades desde archivos de componente).
 *
 * @param {number} s segundos
 * @returns {string}
 */
export function fmtTime(s) {
  if (!Number.isFinite(s) || s < 0) return '0:00';
  const total = Math.floor(s);
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const sec = total % 60;
  const mm = h > 0 ? String(m).padStart(2, '0') : String(m);
  const ss = String(sec).padStart(2, '0');
  return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
}
