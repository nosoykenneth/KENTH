import React, { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import {
  listAxes,
  getAxisLessons,
  getLesson,
  upsertLesson,
  deleteLesson,
  replaceLessonBlocks,
  setLessonPrompts,
} from '../../shared/services/axesService';
import { showNotification } from '../../shared/components/ui/Notification';
import PageContainer from '../../shared/components/layout/PageContainer';
import DocumentManager from './DocumentManager';

const EMPTY_BLOCK = {
  block_id: '',
  start_time: 0,
  end_time: 0,
  block_title: '',
  summary: '',
  interaction_mode: 'navegacion_de_recurso',
  tutor_focus: '',
  concepts: [],
  preguntas_probables: [],
};

const INTERACTION_MODES = [
  'navegacion_de_recurso',
  'criterio_operativo',
  'practica',
  'teoria',
  'troubleshooting',
];

const linesToArr = (s) => (s || '').split('\n').map((x) => x.trim()).filter(Boolean);
const arrToLines = (a) => (Array.isArray(a) ? a.join('\n') : '');

export default function CourseAuthoringView() {
  const { courseId } = useParams(); // id firmado del curso (X-Course-Id)
  const [axes, setAxes] = useState([]);
  const [axisId, setAxisId] = useState('');
  const [lessons, setLessons] = useState([]);
  const [lessonId, setLessonId] = useState('');
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // ------- carga -------
  const loadAxes = useCallback(async () => {
    try {
      const data = await listAxes(courseId);
      setAxes(data);
      if (data.length && !axisId) setAxisId(data[0].axis_id);
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
  }, [courseId, axisId]);

  const loadLessons = useCallback(async (aId) => {
    if (!aId) return;
    try {
      const data = await getAxisLessons(aId, courseId);
      setLessons(data);
    } catch (e) {
      showNotification('error', e.message);
    }
  }, [courseId]);

  const loadLesson = useCallback(async (lId) => {
    if (!lId) { setLesson(null); return; }
    try {
      const data = await getLesson(lId, courseId);
      setLesson({
        ...data,
        _learning_goals: arrToLines(data.learning_goals),
        _prerequisites: (data.prerequisites || []).join(', '),
        _suggested: arrToLines(data.suggested_prompts),
        blocks: (data.blocks || []).map((b) => ({ ...EMPTY_BLOCK, ...b })),
      });
    } catch (e) {
      showNotification('error', e.message);
    }
  }, [courseId]);

  useEffect(() => { loadAxes(); }, [loadAxes]);
  useEffect(() => { if (axisId) { setLessonId(''); setLesson(null); loadLessons(axisId); } }, [axisId, loadLessons]);
  useEffect(() => { loadLesson(lessonId); }, [lessonId, loadLesson]);

  // ------- mutaciones de estado local -------
  const setField = (k, v) => setLesson((p) => ({ ...p, [k]: v }));
  const setBlock = (idx, k, v) => setLesson((p) => {
    const blocks = [...p.blocks];
    blocks[idx] = { ...blocks[idx], [k]: v };
    return { ...p, blocks };
  });
  const moveBlock = (idx, dir) => setLesson((p) => {
    const blocks = [...p.blocks];
    const j = idx + dir;
    if (j < 0 || j >= blocks.length) return p;
    [blocks[idx], blocks[j]] = [blocks[j], blocks[idx]];
    return { ...p, blocks };
  });
  const addBlock = () => setLesson((p) => ({
    ...p,
    blocks: [...p.blocks, { ...EMPTY_BLOCK, block_id: `${p.lesson_id}-B${p.blocks.length + 1}` }],
  }));
  const removeBlock = (idx) => setLesson((p) => ({ ...p, blocks: p.blocks.filter((_, i) => i !== idx) }));

  // ------- guardado -------
  const saveMeta = async () => {
    if (!lesson) return;
    setSaving(true);
    try {
      await upsertLesson(courseId, lesson.lesson_id, {
        lesson_id: lesson.lesson_id,
        axis_id: lesson.axis_id || axisId,
        title: lesson.lesson_title || lesson.title || '',
        order: Number(lesson.order) || 0,
        learning_goal: lesson.learning_goal || '',
        expected_action: lesson.expected_action || '',
        learning_goals: linesToArr(lesson._learning_goals),
        expected_actions: lesson.expected_actions || [],
        source_script_file: lesson.source_script_file || '',
        resources: lesson.resources || [],
        prerequisites: (lesson._prerequisites || '').split(',').map((x) => x.trim()).filter(Boolean),
        notes: lesson.notes || '',
      });
      showNotification('success', 'Lección guardada.');
      loadLessons(axisId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const savePrompts = async () => {
    if (!lesson) return;
    setSaving(true);
    try {
      await setLessonPrompts(courseId, lesson.lesson_id, {
        proactive_message: lesson.proactive_message || '',
        suggested_prompts: linesToArr(lesson._suggested),
      });
      showNotification('success', 'Prompts guardados.');
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const saveBlocks = async () => {
    if (!lesson) return;
    setSaving(true);
    try {
      const blocks = lesson.blocks.map((b) => ({
        block_id: b.block_id || '',
        start_time: Number(b.start_time) || 0,
        end_time: Number(b.end_time) || 0,
        block_title: b.block_title || '',
        summary: b.summary || '',
        interaction_mode: b.interaction_mode || '',
        tutor_focus: b.tutor_focus || '',
        concepts: Array.isArray(b.concepts) ? b.concepts : linesToArr(b.concepts),
        preguntas_probables: Array.isArray(b.preguntas_probables) ? b.preguntas_probables : linesToArr(b.preguntas_probables),
      }));
      await replaceLessonBlocks(courseId, lesson.lesson_id, blocks);
      showNotification('success', `${blocks.length} bloques guardados.`);
      loadLessons(axisId);
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const createLesson = async () => {
    const id = window.prompt('ID de la nueva lección (ej. E2-L10):');
    if (!id) return;
    try {
      await upsertLesson(courseId, id, {
        lesson_id: id,
        axis_id: axisId,
        title: 'Nueva lección',
        order: (lessons.length || 0) + 1,
      });
      showNotification('success', 'Lección creada.');
      await loadLessons(axisId);
      setLessonId(id);
    } catch (e) { showNotification('error', e.message); }
  };

  const removeLesson = async () => {
    if (!lesson) return;
    if (!window.confirm(`¿Eliminar la lección ${lesson.lesson_id} y sus bloques?`)) return;
    try {
      await deleteLesson(courseId, lesson.lesson_id);
      showNotification('success', 'Lección eliminada.');
      setLessonId(''); setLesson(null);
      loadLessons(axisId);
    } catch (e) { showNotification('error', e.message); }
  };

  const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none';
  const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';

  return (
    <PageContainer>
      <div className="mb-5">
        <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Autoría del curso</p>
        <h1 className="text-2xl font-black uppercase italic text-kenth-text tracking-tight">Gestión del tutor</h1>
        <p className="text-xs text-kenth-subtext mt-1">
          Edita ejes, lecciones, bloques de video y prompts del tutor. Los cambios son inmediatos: no requieren tocar código.
        </p>
      </div>

      {loading ? (
        <p className="text-sm text-kenth-subtext">Cargando…</p>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-[320px_1fr] gap-5">
          {/* Columna izquierda: ejes + lecciones */}
          <div className="bg-kenth-card border border-kenth-border rounded-2xl p-4 h-fit">
            <label className={labelCls}>Eje</label>
            <select className={`${inputCls} mt-1 mb-4`} value={axisId} onChange={(e) => setAxisId(e.target.value)}>
              {axes.map((a) => (
                <option key={a.axis_id} value={a.axis_id}>{a.axis_id} — {a.axis_title}</option>
              ))}
            </select>

            <div className="flex items-center justify-between mb-2">
              <label className={labelCls}>Lecciones ({lessons.length})</label>
              <button onClick={createLesson} className="text-[10px] font-black uppercase text-kenth-brightred hover:underline">+ Nueva</button>
            </div>
            <div className="flex flex-col gap-1 max-h-[60vh] overflow-y-auto">
              {lessons.map((l) => (
                <button
                  key={l.lesson_id}
                  onClick={() => setLessonId(l.lesson_id)}
                  className={`text-left px-3 py-2 rounded-lg border text-xs transition ${
                    lessonId === l.lesson_id
                      ? 'bg-kenth-brightred/10 border-kenth-brightred/50 text-kenth-text'
                      : 'bg-kenth-surface/5 border-kenth-border text-kenth-subtext hover:border-kenth-brightred/30'
                  }`}
                >
                  <span className="font-bold">{l.lesson_id}</span> · {l.lesson_title}
                  {l.has_blocks ? <span className="ml-1 text-emerald-400">●</span> : null}
                </button>
              ))}
              {lessons.length === 0 && <p className="text-xs text-kenth-subtext py-2">Este eje no tiene lecciones aún.</p>}
            </div>
          </div>

          {/* Columna derecha: editor */}
          <div className="min-w-0">
            <div className="mb-5">
              <DocumentManager courseId={courseId} axes={axes} />
            </div>
            {!lesson ? (
              <div className="bg-kenth-card border border-kenth-border rounded-2xl p-8 text-center text-sm text-kenth-subtext">
                Selecciona una lección para editarla, o crea una nueva.
              </div>
            ) : (
              <div className="flex flex-col gap-5">
                {/* Metadata */}
                <section className="bg-kenth-card border border-kenth-border rounded-2xl p-5">
                  <div className="flex items-center justify-between mb-3">
                    <h2 className="text-sm font-black uppercase tracking-widest text-kenth-text">{lesson.lesson_id} · Datos</h2>
                    <button onClick={removeLesson} className="text-[10px] font-bold uppercase text-red-400 hover:underline">Eliminar lección</button>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="md:col-span-2">
                      <label className={labelCls}>Título</label>
                      <input className={inputCls} value={lesson.lesson_title || ''} onChange={(e) => setField('lesson_title', e.target.value)} />
                    </div>
                    <div>
                      <label className={labelCls}>Orden</label>
                      <input type="number" className={inputCls} value={lesson.order ?? 0} onChange={(e) => setField('order', e.target.value)} />
                    </div>
                    <div>
                      <label className={labelCls}>Prerrequisitos (coma)</label>
                      <input className={inputCls} value={lesson._prerequisites} onChange={(e) => setField('_prerequisites', e.target.value)} />
                    </div>
                    <div className="md:col-span-2">
                      <label className={labelCls}>Objetivo de aprendizaje</label>
                      <input className={inputCls} value={lesson.learning_goal || ''} onChange={(e) => setField('learning_goal', e.target.value)} />
                    </div>
                    <div className="md:col-span-2">
                      <label className={labelCls}>Acción esperada</label>
                      <input className={inputCls} value={lesson.expected_action || ''} onChange={(e) => setField('expected_action', e.target.value)} />
                    </div>
                    <div className="md:col-span-2">
                      <label className={labelCls}>Metas (una por línea)</label>
                      <textarea rows={2} className={inputCls} value={lesson._learning_goals} onChange={(e) => setField('_learning_goals', e.target.value)} />
                    </div>
                  </div>
                  <button onClick={saveMeta} disabled={saving} className="mt-3 px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                    {saving ? 'Guardando…' : 'Guardar datos'}
                  </button>
                </section>

                {/* Prompts */}
                <section className="bg-kenth-card border border-kenth-border rounded-2xl p-5">
                  <h2 className="text-sm font-black uppercase tracking-widest text-kenth-text mb-3">Prompts del tutor</h2>
                  <label className={labelCls}>Mensaje proactivo</label>
                  <textarea rows={2} className={`${inputCls} mb-3`} value={lesson.proactive_message || ''} onChange={(e) => setField('proactive_message', e.target.value)} />
                  <label className={labelCls}>Preguntas sugeridas (una por línea)</label>
                  <textarea rows={4} className={inputCls} value={lesson._suggested} onChange={(e) => setField('_suggested', e.target.value)} />
                  <button onClick={savePrompts} disabled={saving} className="mt-3 px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                    {saving ? 'Guardando…' : 'Guardar prompts'}
                  </button>
                </section>

                {/* Bloques */}
                <section className="bg-kenth-card border border-kenth-border rounded-2xl p-5">
                  <div className="flex items-center justify-between mb-3">
                    <h2 className="text-sm font-black uppercase tracking-widest text-kenth-text">Bloques de video ({lesson.blocks.length})</h2>
                    <button onClick={addBlock} className="text-[10px] font-black uppercase text-kenth-brightred hover:underline">+ Bloque</button>
                  </div>
                  <div className="flex flex-col gap-4">
                    {lesson.blocks.map((b, idx) => (
                      <div key={idx} className="border border-kenth-border rounded-xl p-3 bg-kenth-surface/5">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-[10px] font-bold uppercase text-kenth-subtext">{b.block_id || `bloque ${idx + 1}`}</span>
                          <div className="flex items-center gap-2">
                            <button onClick={() => moveBlock(idx, -1)} className="text-kenth-subtext hover:text-kenth-text text-xs">▲</button>
                            <button onClick={() => moveBlock(idx, 1)} className="text-kenth-subtext hover:text-kenth-text text-xs">▼</button>
                            <button onClick={() => removeBlock(idx)} className="text-red-400 hover:text-red-300 text-xs">✕</button>
                          </div>
                        </div>
                        <div className="grid grid-cols-2 gap-2 mb-2">
                          <div>
                            <label className={labelCls}>Inicio (s)</label>
                            <input type="number" className={inputCls} value={b.start_time ?? 0} onChange={(e) => setBlock(idx, 'start_time', e.target.value)} />
                          </div>
                          <div>
                            <label className={labelCls}>Fin (s)</label>
                            <input type="number" className={inputCls} value={b.end_time ?? 0} onChange={(e) => setBlock(idx, 'end_time', e.target.value)} />
                          </div>
                        </div>
                        <label className={labelCls}>Título del bloque</label>
                        <input className={`${inputCls} mb-2`} value={b.block_title || ''} onChange={(e) => setBlock(idx, 'block_title', e.target.value)} />
                        <label className={labelCls}>Resumen (qué pasa en pantalla)</label>
                        <textarea rows={2} className={`${inputCls} mb-2`} value={b.summary || ''} onChange={(e) => setBlock(idx, 'summary', e.target.value)} />
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-2">
                          <div>
                            <label className={labelCls}>Modo pedagógico</label>
                            <select className={inputCls} value={b.interaction_mode || ''} onChange={(e) => setBlock(idx, 'interaction_mode', e.target.value)}>
                              {INTERACTION_MODES.map((m) => <option key={m} value={m}>{m}</option>)}
                            </select>
                          </div>
                          <div>
                            <label className={labelCls}>Foco del tutor</label>
                            <input className={inputCls} value={b.tutor_focus || ''} onChange={(e) => setBlock(idx, 'tutor_focus', e.target.value)} />
                          </div>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          <div>
                            <label className={labelCls}>Conceptos (una por línea)</label>
                            <textarea rows={2} className={inputCls}
                              value={Array.isArray(b.concepts) ? arrToLines(b.concepts) : b.concepts}
                              onChange={(e) => setBlock(idx, 'concepts', linesToArr(e.target.value))} />
                          </div>
                          <div>
                            <label className={labelCls}>Preguntas probables (una por línea)</label>
                            <textarea rows={2} className={inputCls}
                              value={Array.isArray(b.preguntas_probables) ? arrToLines(b.preguntas_probables) : b.preguntas_probables}
                              onChange={(e) => setBlock(idx, 'preguntas_probables', linesToArr(e.target.value))} />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <button onClick={saveBlocks} disabled={saving} className="mt-4 px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                    {saving ? 'Guardando…' : 'Guardar bloques'}
                  </button>
                </section>
              </div>
            )}
          </div>
        </div>
      )}
    </PageContainer>
  );
}
