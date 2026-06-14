import React, { useCallback, useEffect, useState } from 'react';
import {
  listSections,
  getSectionLessons,
  getLesson,
  upsertLesson,
  deleteLesson,
  reorderLessons,
  listResourceLinks,
} from '../../shared/services/sectionsService';
import { showNotification } from '../../shared/utils/notify';

export default function StructureManager({ courseId }) {
  const [sections, setSections] = useState([]);
  const [sectionId, setSectionId] = useState('');
  const [lessons, setLessons] = useState([]);
  const [linkedIds, setLinkedIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [, setSaving] = useState(false);

  const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';

  const loadSections = useCallback(async (keepSection) => {
    try {
      const data = await listSections(courseId);
      setSections(data);
      setSectionId((cur) => keepSection && cur ? cur : (data[0]?.moodle_section_id || ''));
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
    try {
      const links = await listResourceLinks(courseId);
      setLinkedIds(new Set((links || []).map((l) => l.lesson_id)));
    } catch { /* badges opcionales */ }
  }, [courseId]);

  const loadLessons = useCallback(async (id) => {
    if (!id) { setLessons([]); return; }
    try { setLessons(await getSectionLessons(id, courseId)); }
    catch (e) { showNotification('error', e.message); }
  }, [courseId]);

  useEffect(() => { loadSections(); }, [loadSections]);
  useEffect(() => { loadLessons(sectionId); }, [sectionId, loadLessons]);

  const section = sections.find((s) => String(s.moodle_section_id) === String(sectionId)) || null;
  const sectionIndex = Math.max(0, sections.findIndex((s) => String(s.moodle_section_id) === String(sectionId)));

  const renameLesson = async (lessonId, title) => {
    setSaving(true);
    try {
      const full = await getLesson(lessonId, courseId);
      await upsertLesson(courseId, lessonId, {
        lesson_id: lessonId,
        moodle_section_id: full.moodle_section_id || sectionId,
        title,
        order: Number(full.order) || 0,
        learning_goal: full.learning_goal || '',
        expected_action: full.expected_action || '',
        learning_goals: full.learning_goals || [],
        resources: full.resources || [],
        prerequisites: full.prerequisites || [],
        delegated_to_tutor: full.delegated_to_tutor || [],
        attribution_constraints: full.attribution_constraints || [],
        notes: full.notes || '',
      });
      loadLessons(sectionId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const removeLesson = async (lessonId) => {
    if (!window.confirm(`¿Eliminar la lección ${lessonId} y sus bloques/prompts?`)) return;
    setSaving(true);
    try {
      await deleteLesson(courseId, lessonId);
      showNotification('success', 'Lección eliminada.');
      loadLessons(sectionId);
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
    } catch (e) { showNotification('error', e.message); loadLessons(sectionId); }
  };

  if (loading) return <p className="text-sm text-kenth-subtext">Cargando estructura...</p>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[300px_1fr] gap-5">
      <div className="bg-kenth-card border border-kenth-border rounded-2xl p-4 h-fit">
        <label className={labelCls}>Secciones Moodle ({sections.length})</label>
        <div className="flex flex-col gap-1 mt-2 mb-3 max-h-[60vh] overflow-y-auto">
          {sections.map((s, idx) => (
            <button
              key={s.moodle_section_id}
              onClick={() => setSectionId(s.moodle_section_id)}
              className={`px-2 py-2 rounded-lg border text-xs text-left transition ${sectionId === s.moodle_section_id ? 'bg-kenth-brightred/10 border-kenth-brightred/50' : 'bg-kenth-surface/5 border-kenth-border hover:border-kenth-brightred/30'}`}
            >
              <span className="font-bold text-kenth-text">Tema {idx + 1}</span>
              <span className="text-kenth-subtext"> · {s.section_name}</span>
            </button>
          ))}
          {sections.length === 0 && <p className="text-xs text-kenth-subtext py-2">No hay secciones Moodle disponibles.</p>}
        </div>
      </div>

      <div className="bg-kenth-card border border-kenth-border rounded-2xl p-4 min-w-0">
        {!section ? (
          <p className="text-sm text-kenth-subtext">Selecciona una sección Moodle.</p>
        ) : (
          <>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-sm font-black uppercase tracking-widest text-kenth-text">Tema {sectionIndex + 1} · Lecciones ({lessons.length})</h3>
                <p className="text-xs text-kenth-subtext">{section.section_name}</p>
              </div>
            </div>

            <div className="flex flex-col gap-1.5 max-h-[55vh] overflow-y-auto pr-1">
              {lessons.map((l, idx) => (
                <div key={l.lesson_id} className="group flex items-center gap-2 px-3 py-2 rounded-lg border border-kenth-border bg-kenth-surface/5">
                  <div className="flex flex-col flex-1 min-w-0">
                    <span className="text-sm text-kenth-text truncate"><span className="font-bold">{l.lesson_id}</span> · {l.lesson_title}</span>
                    <div className="flex items-center gap-1.5 mt-0.5">
                      {l.has_blocks && <span className="text-[9px] uppercase tracking-widest font-black text-emerald-400">bloques</span>}
                      {linkedIds.has(l.lesson_id) && <span className="text-[9px] uppercase tracking-widest font-black text-sky-300">video</span>}
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
              {lessons.length === 0 && <p className="text-xs text-kenth-subtext py-2">Esta sección no tiene lecciones aún.</p>}
            </div>

            <p className="text-[11px] text-kenth-subtext border-t border-kenth-border mt-3 pt-3 leading-relaxed">
              Las lecciones se crean solas al añadir un video <span className="font-bold text-kenth-text">H5P</span> a esta sección desde la vista del curso. Aquí solo las corriges (renombrar, reordenar o eliminar).
            </p>
          </>
        )}
      </div>
    </div>
  );
}
