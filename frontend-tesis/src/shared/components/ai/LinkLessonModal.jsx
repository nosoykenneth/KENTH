import React, { useEffect, useState } from 'react';
import {
  listAllLessons,
  getLesson,
  getResourceLink,
  upsertResourceLink,
  deleteResourceLink,
} from '../../services/sectionsService';

/**
 * Modal de vinculación recurso Moodle <-> lección formal del curso.
 *
 * Props:
 *   - resource:  modulo Moodle abierto. Espera al menos { id, modname, name }.
 *   - courseId:  id del curso (para hidratar el campo course_id del vinculo).
 *   - onClose(refresh: boolean): cierra el modal. refresh=true si hubo cambio.
 */
export default function LinkLessonModal({ resource, courseId, sectionContext = null, onClose }) {
  const [lessons, setLessons] = useState([]);
  const [details, setDetails] = useState({}); // lesson_id -> manifest detail
  const [currentLink, setCurrentLink] = useState(null);
  const [selectedId, setSelectedId] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!resource?.id) return;
    let alive = true;
    (async () => {
      try {
        setLoading(true);
        const [all, link] = await Promise.all([
          listAllLessons(courseId),
          getResourceLink(resource.id, courseId),
        ]);
        if (!alive) return;
        setLessons(all);
        setCurrentLink(link);
        setSelectedId(link?.lesson_id || all[0]?.lesson_id || '');

        // Trae detalle para mostrar learning_goal en cada opción.
        const fulls = await Promise.all(
          all.map((p) => getLesson(p.lesson_id, courseId).catch(() => null)),
        );
        if (!alive) return;
        const map = {};
        fulls.forEach((d) => { if (d) map[d.lesson_id] = d; });
        setDetails(map);
      } catch (e) {
        if (alive) setError(e.message);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, [resource?.id, courseId]);

  const handleSave = async () => {
    if (!selectedId) return;
    setSaving(true);
    setError('');
    try {
      await upsertResourceLink(resource.id, {
        lesson_id: selectedId,
        course_id: String(courseId || ''),
        moodle_section_id: sectionContext?.moodle_section_id || details[selectedId]?.moodle_section_id || '',
        resource_type: resource.modname === 'hvp' || resource.modname === 'h5pactivity'
          ? 'web_page'
          : (resource.modname || ''),
        resource_subtype: (resource.modname === 'hvp' || resource.modname === 'h5pactivity')
          ? 'h5p_video'
          : '',
      });
      onClose(true);
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  const handleRemove = async () => {
    if (!currentLink) return;
    if (!window.confirm('Quitar el vinculo de este recurso con la leccion?')) return;
    setSaving(true);
    setError('');
    try {
      await deleteResourceLink(resource.id, courseId);
      onClose(true);
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-[200] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={() => onClose(false)}
    >
      <div
        className="w-full max-w-lg bg-kenth-card border border-kenth-border rounded-2xl shadow-2xl p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">
              Tutor contextual
            </p>
            <h3 className="text-lg font-black uppercase italic text-kenth-text tracking-tight">
              Enlazar leccion
            </h3>
            <p className="text-xs text-kenth-subtext mt-1 truncate max-w-[28rem]">
              Recurso: <span className="text-kenth-text font-bold">{resource?.name}</span>
            </p>
          </div>
          <button
            onClick={() => onClose(false)}
            className="text-kenth-subtext hover:text-kenth-text"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {currentLink && (
          <div className="mb-3 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-[11px] text-emerald-300">
            Vinculado actualmente a <strong>{currentLink.lesson_id}</strong>
            {currentLink.moodle_section_id ? ` (sección ${currentLink.moodle_section_id})` : ''}.
            {currentLink.moodle_section_id ? ` SecciÃ³n Moodle: ${currentLink.moodle_section_id}.` : ''}
          </div>
        )}

        {loading ? (
          <p className="text-sm text-kenth-subtext py-6">Cargando lecciones del curso...</p>
        ) : lessons.length === 0 ? (
          <p className="text-sm text-red-400 py-6">
            No hay lecciones registradas en el backend.
          </p>
        ) : (
          <div className="flex flex-col gap-2 max-h-[55vh] overflow-y-auto pr-1">
            {lessons.map((p) => {
              const det = details[p.lesson_id];
              const checked = selectedId === p.lesson_id;
              return (
                <label
                  key={p.lesson_id}
                  className={`flex items-start gap-3 p-3 rounded-xl border cursor-pointer transition ${
                    checked
                      ? 'bg-kenth-brightred/10 border-kenth-brightred/50'
                      : 'bg-kenth-surface/5 border-kenth-border hover:border-kenth-brightred/30'
                  }`}
                >
                  <input
                    type="radio"
                    name="course-lesson"
                    value={p.lesson_id}
                    checked={checked}
                    onChange={() => setSelectedId(p.lesson_id)}
                    className="mt-1 accent-kenth-brightred"
                  />
                  <div className="flex flex-col flex-1 min-w-0">
                    <span className="text-sm font-bold text-kenth-text">
                      {p.lesson_id} - {p.lesson_title}
                    </span>
                    <span className="text-[10px] uppercase tracking-widest text-kenth-subtext">
                      {p.moodle_section_id ? `Sección ${p.moodle_section_id}` : ''}
                    </span>
                    {det?.learning_goal && (
                      <span className="text-xs text-kenth-subtext mt-1 line-clamp-3">
                        {det.learning_goal}
                      </span>
                    )}
                  </div>
                </label>
              );
            })}
          </div>
        )}

        {error && (
          <p className="mt-3 text-xs text-red-400">{error}</p>
        )}

        <div className="flex items-center justify-between gap-3 mt-5">
          {currentLink ? (
            <button
              onClick={handleRemove}
              disabled={saving}
              className="text-xs text-red-400 hover:text-red-300 font-bold uppercase tracking-widest disabled:opacity-40"
            >
              Quitar vinculo
            </button>
          ) : <span />}
          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={() => onClose(false)}
              disabled={saving}
              className="px-4 py-2 text-xs font-bold uppercase tracking-widest text-kenth-subtext hover:text-kenth-text disabled:opacity-40"
            >
              Cancelar
            </button>
            <button
              onClick={handleSave}
              disabled={saving || !selectedId}
              className="px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40"
            >
              {saving ? 'Guardando...' : 'Guardar vinculo'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
