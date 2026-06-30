import React, { useEffect, useMemo, useState } from 'react';
import {
  listSections,
  listAllLessons,
  listResourceLinks,
  upsertLesson,
  upsertResourceLink,
  importLesson,
} from '../../services/sectionsService';
import { showNotification } from '../../utils/notify';

/**
 * AssignLessonDialog
 *
 * Diálogo de asignación recurso H5P → lección. El vínculo se crea aquí (una vez)
 * y queda fijo. Tres caminos de igual peso:
 *   - Elegir lección existente (del eje, que aún no tenga video).
 *   - Crear lección nueva vacía (número auto en el eje).
 *   - Importar lección desde JSON (formato semilla) con validación + preview.
 *
 * Props:
 *   - resource: módulo Moodle { id, modname, name }.
 *   - courseId: id firmado del curso.
 *   - onClose(lessonId | null): lessonId si se asignó; null si se canceló.
 */

const MODES = [
  { id: 'existente', label: 'Existente' },
  { id: 'nueva', label: 'Nueva' },
  { id: 'importar', label: 'Importar JSON' },
];

const lessonNumber = (lessonId) => {
  const m = /-L(\d+)/i.exec(lessonId || '');
  return m ? parseInt(m[1], 10) : 0;
};

export default function AssignLessonDialog({ resource, courseId, sectionContext = null, onClose }) {
  const isH5P = resource?.modname === 'hvp' || resource?.modname === 'h5pactivity';
  const linkPayloadBase = useMemo(() => ({
    course_id: String(courseId || ''),
    moodle_section_id: sectionContext?.moodle_section_id || '',
    resource_type: isH5P ? 'web_page' : (resource?.modname || ''),
    resource_subtype: isH5P ? 'h5p_video' : '',
  }), [courseId, isH5P, resource?.modname, sectionContext?.moodle_section_id]);

  const [mode, setMode] = useState('existente');
  const [sections, setSections] = useState([]);
  const [selectedSectionId, setSelectedSectionId] = useState(sectionContext?.moodle_section_id || '');
  const [lessons, setLessons] = useState([]);
  const [linkedIds, setLinkedIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Existente
  const [selectedLessonId, setSelectedLessonId] = useState('');
  // Nueva
  const [newTitle, setNewTitle] = useState('');
  // Importar
  const [jsonText, setJsonText] = useState('');
  const [parsed, setParsed] = useState(null);
  const [parseError, setParseError] = useState('');

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        setLoading(true);
        const [sx, all] = await Promise.all([
          listSections(courseId),
          listAllLessons(courseId),
        ]);
        if (!alive) return;
        setSections(sx);
        setLessons(all);
        setSelectedSectionId(sectionContext?.moodle_section_id || sx[0]?.moodle_section_id || '');
        // Vínculos best-effort (solo para filtrar lecciones con video).
        try {
          const links = await listResourceLinks(courseId);
          if (alive) setLinkedIds(new Set((links || []).map((l) => l.lesson_id)));
        } catch { /* opcional */ }
      } catch (e) {
        if (alive) showNotification('error', e.message);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, [courseId, sectionContext?.moodle_section_id]);

  const lessonsOfSection = lessons.filter((l) => String(l.moodle_section_id || '') === String(selectedSectionId || ''));
  const freeLessons = lessonsOfSection.filter((l) => !linkedIds.has(l.lesson_id));
  const sectionOptions = sections.map((s, idx) => ({
    id: s.moodle_section_id,
    label: `Tema ${idx + 1} - ${s.section_name}`,
  }));

  const nextLessonId = useMemo(() => {
    const max = lessonsOfSection.reduce((mx, l) => Math.max(mx, lessonNumber(l.lesson_id)), 0);
    const num = String(max + 1).padStart(2, '0');
    const n = Math.max(1, sections.findIndex((s) => String(s.moodle_section_id) === String(selectedSectionId)) + 1);
    return `S${n}-L${num}`;
  }, [lessonsOfSection, sections, selectedSectionId]);

  const onJsonChange = (text) => {
    setJsonText(text);
    setParseError('');
    setParsed(null);
    if (!text.trim()) return;
    try {
      const obj = JSON.parse(text);
      setParsed(obj);
    } catch (e) {
      setParseError('JSON inválido: ' + e.message);
    }
  };

  const onFile = async (file) => {
    if (!file) return;
    const text = await file.text();
    onJsonChange(text);
  };

  const linkAndClose = async (lessonId) => {
    await upsertResourceLink(resource.id, { ...linkPayloadBase, lesson_id: lessonId });
    showNotification('success', `Recurso enlazado a ${lessonId}.`);
    onClose(lessonId);
  };

  const confirmExistente = async () => {
    if (!selectedLessonId) return;
    setSaving(true);
    try { await linkAndClose(selectedLessonId); }
    catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const confirmNueva = async () => {
    if (!selectedSectionId) return;
    setSaving(true);
    try {
      await upsertLesson(courseId, nextLessonId, {
        lesson_id: nextLessonId,
        axis_id: '',
        moodle_section_id: selectedSectionId,
        title: newTitle.trim() || 'Nueva lección',
        order: lessonsOfSection.length + 1,
      });
      await linkAndClose(nextLessonId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const confirmImportar = async () => {
    if (!parsed) { setParseError('Pega o sube un JSON válido primero.'); return; }
    setSaving(true);
    try {
      const created = await importLesson(courseId, {
        ...parsed,
        moodle_section_id: parsed.moodle_section_id || selectedSectionId || '',
      }); // crea la lección
      const lessonId = created?.lesson_id || parsed.lesson_id;
      if (!lessonId) throw new Error('El backend no devolvió lesson_id.');
      await linkAndClose(lessonId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const confirm = () => {
    if (mode === 'existente') return confirmExistente();
    if (mode === 'nueva') return confirmNueva();
    return confirmImportar();
  };

  const confirmDisabled = saving
    || (mode === 'existente' && !selectedLessonId)
    || (mode === 'nueva' && !selectedSectionId)
    || (mode === 'importar' && !parsed);

  const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none';
  const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';

  return (
    <div className="fixed inset-0 z-[205] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => !saving && onClose(null)}>
      <div className="w-full max-w-lg bg-kenth-card border border-kenth-border rounded-2xl shadow-2xl p-6" onClick={(e) => e.stopPropagation()}>
        <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Tutor contextual</p>
        <h3 className="text-lg font-black uppercase italic text-kenth-text tracking-tight">¿A qué lección pertenece este video?</h3>
        <p className="text-xs text-kenth-subtext mt-1 truncate">Recurso: <span className="text-kenth-text font-bold">{resource?.name}</span></p>

        {loading ? (
          <p className="text-sm text-kenth-subtext py-6">Cargando…</p>
        ) : (
          <>
            <div className="flex border border-kenth-border rounded-lg overflow-hidden my-4">
              {MODES.map((m) => (
                <button
                  key={m.id}
                  onClick={() => setMode(m.id)}
                  className={`flex-1 px-2 py-2 text-[11px] font-black uppercase tracking-widest transition ${mode === m.id ? 'bg-kenth-brightred text-white' : 'text-kenth-subtext hover:text-kenth-text'}`}
                >
                  {m.label}
                </button>
              ))}
            </div>

            {/* Selector de eje (existente / nueva) */}
            {mode !== 'importar' && (
              <div className="mb-3">
                <label className={labelCls}>Sección Moodle</label>
                <select className={inputCls} value={selectedSectionId} onChange={(e) => setSelectedSectionId(e.target.value)}>
                  {sectionOptions.map((a) => <option key={a.id} value={a.id}>{a.id} — {a.label}</option>)}
                </select>
              </div>
            )}

            {mode === 'existente' && (
              freeLessons.length === 0 ? (
                <p className="text-xs text-kenth-subtext py-2">Esta sección no tiene lecciones libres (sin video). Crea una nueva o importa.</p>
              ) : (
                <div className="flex flex-col gap-2 max-h-[40vh] overflow-y-auto pr-1">
                  {freeLessons.map((l) => {
                    const checked = selectedLessonId === l.lesson_id;
                    return (
                      <label key={l.lesson_id} className={`flex items-start gap-3 p-3 rounded-xl border cursor-pointer transition ${checked ? 'bg-kenth-brightred/10 border-kenth-brightred/50' : 'bg-kenth-surface/5 border-kenth-border hover:border-kenth-brightred/30'}`}>
                        <input type="radio" name="assign-lesson" checked={checked} onChange={() => setSelectedLessonId(l.lesson_id)} className="mt-1 accent-kenth-brightred" />
                        <span className="text-sm font-bold text-kenth-text">{l.lesson_id} · {l.lesson_title}</span>
                      </label>
                    );
                  })}
                </div>
              )
            )}

            {mode === 'nueva' && (
              <div className="flex flex-col gap-3">
                <div>
                  <label className={labelCls}>ID asignado (automático)</label>
                  <input className={`${inputCls} opacity-70`} value={nextLessonId} readOnly />
                </div>
                <div>
                  <label className={labelCls}>Título</label>
                  <input className={inputCls} value={newTitle} onChange={(e) => setNewTitle(e.target.value)} placeholder="Título de la lección" />
                </div>
                <p className="text-[11px] text-kenth-subtext">La lección se crea vacía; la llenarás en el editor (bloques, prompts, transcripción).</p>
              </div>
            )}

            {mode === 'importar' && (
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <label className={labelCls}>JSON de la lección</label>
                  <label className="text-[10px] font-black uppercase text-kenth-brightred hover:underline cursor-pointer">
                    Subir archivo
                    <input type="file" accept="application/json,.json" className="hidden" onChange={(e) => onFile(e.target.files?.[0])} />
                  </label>
                </div>
                <textarea
                  rows={6}
                  className={`${inputCls} font-mono text-[11px] resize-y`}
                  value={jsonText}
                  onChange={(e) => onJsonChange(e.target.value)}
                  placeholder='Pega aquí el JSON (formato E2-L03.json) o usa "Subir archivo"…'
                />
                {parseError && <p className="text-[11px] text-red-400">{parseError}</p>}
                {parsed && (
                  <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 text-[11px] text-emerald-100">
                    <p className="font-bold text-emerald-300 mb-1">Vista previa</p>
                    <div><span className="text-kenth-subtext">Lección:</span> {parsed.lesson_id || '—'} · {parsed.lesson_title || parsed.title || '—'}</div>
                    <div><span className="text-kenth-subtext">Sección Moodle:</span> {parsed.moodle_section_id || selectedSectionId || '—'}</div>
                    <div><span className="text-kenth-subtext">SecciÃ³n Moodle:</span> {parsed.moodle_section_id || sectionContext?.moodle_section_id || 'â€”'}</div>
                    <div><span className="text-kenth-subtext">Bloques:</span> {(parsed.blocks || []).length}</div>
                    <div><span className="text-kenth-subtext">Prompts sugeridos:</span> {(parsed.suggested_prompts || []).length}</div>
                    {parsed.learning_goal && <div className="mt-1 line-clamp-2"><span className="text-kenth-subtext">Objetivo:</span> {parsed.learning_goal}</div>}
                  </div>
                )}
              </div>
            )}

            <div className="flex items-center justify-end gap-2 mt-5">
              <button onClick={() => onClose(null)} disabled={saving} className="px-4 py-2 text-xs font-bold uppercase tracking-widest text-kenth-subtext hover:text-kenth-text disabled:opacity-40">Cancelar</button>
              <button onClick={confirm} disabled={confirmDisabled} className="px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                {saving ? 'Guardando…' : 'Asignar'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
