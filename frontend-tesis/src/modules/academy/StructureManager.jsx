import React, { useCallback, useEffect, useMemo, useState } from 'react';
import {
  listAxes,
  getAxisLessons,
  getLesson,
  upsertAxis,
  deleteAxis,
  upsertLesson,
  deleteLesson,
  reorderLessons,
  listResourceLinks,
} from '../../shared/services/axesService';
import { showNotification } from '../../shared/components/ui/Notification';

/**
 * StructureManager — pestaña "Estructura" de Gestión del Tutor.
 * Administra el temario: ejes → lecciones (crear/editar/borrar/reordenar).
 * El detalle de cada lección (bloques/prompts/transcripción) se edita en el
 * editor sobre el video; aquí es estructura y navegación.
 */

const lessonNumber = (lessonId) => {
  const m = /-L(\d+)/i.exec(lessonId || '');
  return m ? parseInt(m[1], 10) : 0;
};

export default function StructureManager({ courseId }) {
  const [axes, setAxes] = useState([]);
  const [axisId, setAxisId] = useState('');
  const [lessons, setLessons] = useState([]);
  const [linkedIds, setLinkedIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [newAxisTitle, setNewAxisTitle] = useState('');
  const [newLessonTitle, setNewLessonTitle] = useState('');

  const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none';
  const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';

  const loadAxes = useCallback(async (keepAxis) => {
    try {
      const ax = await listAxes(courseId);
      setAxes(ax);
      setAxisId((cur) => keepAxis && cur ? cur : (ax[0]?.axis_id || ''));
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
    // Los vínculos solo alimentan los badges "● video"; si fallan, no bloquean.
    try {
      const links = await listResourceLinks(courseId);
      setLinkedIds(new Set((links || []).map((l) => l.lesson_id)));
    } catch { /* badges opcionales */ }
  }, [courseId]);

  const loadLessons = useCallback(async (aId) => {
    if (!aId) { setLessons([]); return; }
    try { setLessons(await getAxisLessons(aId, courseId)); }
    catch (e) { showNotification('error', e.message); }
  }, [courseId]);

  useEffect(() => { loadAxes(); }, [loadAxes]);
  useEffect(() => { loadLessons(axisId); }, [axisId, loadLessons]);

  const axis = axes.find((a) => a.axis_id === axisId) || null;

  const nextAxisNumber = useMemo(
    () => axes.reduce((mx, a) => Math.max(mx, a.axis_number || 0), 0) + 1,
    [axes],
  );
  const nextLessonId = useMemo(() => {
    const max = lessons.reduce((mx, l) => Math.max(mx, lessonNumber(l.lesson_id)), 0);
    const n = axis?.axis_number || (axisId.match(/\d+/)?.[0]) || (axes.length + 1);
    return `E${n}-L${String(max + 1).padStart(2, '0')}`;
  }, [lessons, axis, axisId, axes.length]);

  // ---- Ejes ----
  const createAxis = async () => {
    const title = newAxisTitle.trim();
    if (!title) return;
    const newId = `Eje ${nextAxisNumber}`;
    setSaving(true);
    try {
      await upsertAxis(courseId, newId, {
        axis_id: newId, axis_number: nextAxisNumber, title, axis_order: nextAxisNumber,
      });
      setNewAxisTitle('');
      showNotification('success', `${newId} creado.`);
      await loadAxes();
      setAxisId(newId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const renameAxis = async (a, title) => {
    setSaving(true);
    try {
      await upsertAxis(courseId, a.axis_id, {
        axis_id: a.axis_id, axis_number: a.axis_number, title,
        pedagogical_role: a.pedagogical_role || '', axis_order: a.axis_order || a.axis_number,
      });
      await loadAxes(true);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const removeAxis = async (a) => {
    if (!window.confirm(`¿Eliminar ${a.axis_id}? (debe estar sin lecciones)`)) return;
    setSaving(true);
    try {
      await deleteAxis(courseId, a.axis_id);
      showNotification('success', `${a.axis_id} eliminado.`);
      await loadAxes();
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  // ---- Lecciones ----
  const createLesson = async () => {
    if (!axisId) return;
    setSaving(true);
    try {
      await upsertLesson(courseId, nextLessonId, {
        lesson_id: nextLessonId, axis_id: axisId,
        title: newLessonTitle.trim() || 'Nueva lección', order: lessons.length + 1,
      });
      setNewLessonTitle('');
      showNotification('success', `${nextLessonId} creada.`);
      loadLessons(axisId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  // Renombra preservando el resto de campos (load-merge-upsert).
  const renameLesson = async (lessonId, title) => {
    setSaving(true);
    try {
      const full = await getLesson(lessonId, courseId);
      await upsertLesson(courseId, lessonId, {
        lesson_id: lessonId,
        axis_id: full.axis_id || axisId,
        title,
        order: Number(full.order) || 0,
        learning_goal: full.learning_goal || '',
        expected_action: full.expected_action || '',
        learning_goals: full.learning_goals || [],
        expected_actions: full.expected_actions || [],
        source_script_file: full.source_script_file || '',
        resources: full.resources || [],
        prerequisites: full.prerequisites || [],
        notes: full.notes || '',
      });
      loadLessons(axisId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const removeLesson = async (lessonId) => {
    if (!window.confirm(`¿Eliminar la lección ${lessonId} y sus bloques/prompts?`)) return;
    setSaving(true);
    try {
      await deleteLesson(courseId, lessonId);
      showNotification('success', 'Lección eliminada.');
      loadLessons(axisId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const moveLesson = async (idx, dir) => {
    const j = idx + dir;
    if (j < 0 || j >= lessons.length) return;
    const next = [...lessons];
    [next[idx], next[j]] = [next[j], next[idx]];
    setLessons(next);
    try {
      await reorderLessons(courseId, next.map((l, i) => ({ lesson_id: l.lesson_id, order: i + 1 })));
    } catch (e) { showNotification('error', e.message); loadLessons(axisId); }
  };

  if (loading) return <p className="text-sm text-kenth-subtext">Cargando estructura…</p>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[300px_1fr] gap-5">
      {/* Ejes */}
      <div className="bg-kenth-card border border-kenth-border rounded-2xl p-4 h-fit">
        <label className={labelCls}>Ejes ({axes.length})</label>
        <div className="flex flex-col gap-1 mt-2 mb-3 max-h-[50vh] overflow-y-auto">
          {axes.map((a) => (
            <div key={a.axis_id} className={`group flex items-center gap-1 px-2 py-2 rounded-lg border text-xs transition ${axisId === a.axis_id ? 'bg-kenth-brightred/10 border-kenth-brightred/50' : 'bg-kenth-surface/5 border-kenth-border hover:border-kenth-brightred/30'}`}>
              <button onClick={() => setAxisId(a.axis_id)} className="flex-1 text-left min-w-0">
                <span className="font-bold text-kenth-text">{a.axis_id}</span>
                <span className="text-kenth-subtext"> · {a.axis_title || a.title}</span>
              </button>
              <button
                onClick={() => { const t = window.prompt('Nuevo título del eje:', a.axis_title || a.title); if (t != null && t.trim()) renameAxis(a, t.trim()); }}
                className="opacity-0 group-hover:opacity-100 text-kenth-subtext hover:text-kenth-text px-1" title="Renombrar">✎</button>
              <button onClick={() => removeAxis(a)} className="opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-300 px-1" title="Eliminar">✕</button>
            </div>
          ))}
          {axes.length === 0 && <p className="text-xs text-kenth-subtext py-2">Aún no hay ejes.</p>}
        </div>
        <div className="border-t border-kenth-border pt-3">
          <label className={labelCls}>Nuevo eje (Eje {nextAxisNumber})</label>
          <input className={`${inputCls} mt-1`} value={newAxisTitle} onChange={(e) => setNewAxisTitle(e.target.value)} placeholder="Título del eje" onKeyDown={(e) => e.key === 'Enter' && createAxis()} />
          <button onClick={createAxis} disabled={saving || !newAxisTitle.trim()} className="mt-2 w-full px-3 py-2 rounded-lg bg-kenth-brightred hover:bg-red-600 text-white text-[11px] font-black uppercase tracking-widest disabled:opacity-40">+ Crear eje</button>
        </div>
      </div>

      {/* Lecciones del eje */}
      <div className="bg-kenth-card border border-kenth-border rounded-2xl p-4 min-w-0">
        {!axis ? (
          <p className="text-sm text-kenth-subtext">Selecciona o crea un eje.</p>
        ) : (
          <>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-sm font-black uppercase tracking-widest text-kenth-text">{axis.axis_id} · Lecciones ({lessons.length})</h3>
                {axis.axis_title && <p className="text-xs text-kenth-subtext">{axis.axis_title}</p>}
              </div>
            </div>

            <div className="flex flex-col gap-1.5 max-h-[55vh] overflow-y-auto pr-1">
              {lessons.map((l, idx) => (
                <div key={l.lesson_id} className="group flex items-center gap-2 px-3 py-2 rounded-lg border border-kenth-border bg-kenth-surface/5">
                  <div className="flex flex-col flex-1 min-w-0">
                    <span className="text-sm text-kenth-text truncate"><span className="font-bold">{l.lesson_id}</span> · {l.lesson_title}</span>
                    <div className="flex items-center gap-1.5 mt-0.5">
                      {l.has_blocks && <span className="text-[9px] uppercase tracking-widest font-black text-emerald-400">● bloques</span>}
                      {linkedIds.has(l.lesson_id) && <span className="text-[9px] uppercase tracking-widest font-black text-sky-300">● video</span>}
                      {!l.has_blocks && !linkedIds.has(l.lesson_id) && <span className="text-[9px] uppercase tracking-widest text-kenth-subtext">vacía</span>}
                    </div>
                  </div>
                  <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100">
                    <button onClick={() => moveLesson(idx, -1)} className="text-kenth-subtext hover:text-kenth-text px-1" title="Subir">▲</button>
                    <button onClick={() => moveLesson(idx, 1)} className="text-kenth-subtext hover:text-kenth-text px-1" title="Bajar">▼</button>
                    <button onClick={() => { const t = window.prompt('Nuevo título de la lección:', l.lesson_title); if (t != null && t.trim()) renameLesson(l.lesson_id, t.trim()); }} className="text-kenth-subtext hover:text-kenth-text px-1" title="Renombrar">✎</button>
                    <button onClick={() => removeLesson(l.lesson_id)} className="text-red-400 hover:text-red-300 px-1" title="Eliminar">✕</button>
                  </div>
                </div>
              ))}
              {lessons.length === 0 && <p className="text-xs text-kenth-subtext py-2">Este eje no tiene lecciones aún.</p>}
            </div>

            <div className="border-t border-kenth-border mt-3 pt-3 flex items-end gap-2">
              <div className="flex-1">
                <label className={labelCls}>Nueva lección ({nextLessonId})</label>
                <input className={`${inputCls} mt-1`} value={newLessonTitle} onChange={(e) => setNewLessonTitle(e.target.value)} placeholder="Título de la lección" onKeyDown={(e) => e.key === 'Enter' && createLesson()} />
              </div>
              <button onClick={createLesson} disabled={saving} className="px-4 py-2 rounded-lg bg-kenth-brightred hover:bg-red-600 text-white text-[11px] font-black uppercase tracking-widest disabled:opacity-40">+ Crear</button>
            </div>
            <p className="text-[11px] text-kenth-subtext mt-2">El detalle (bloques, prompts, transcripción) se edita abriendo el video de la lección y usando <span className="text-kenth-text font-bold">Enlazar lección</span>.</p>
          </>
        )}
      </div>
    </div>
  );
}
