import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { getResourceLink, getLesson, upsertLesson, updateMoments } from '../../services/sectionsService';
import { activityContextFromMoodleModule } from '../../services/activityContext';
import { showNotification } from '../../utils/notify';
import TutorAssistCard from './TutorAssistCard';
import LessonResourcesPanel from './LessonResourcesPanel';

/**
 * TutorPedagogyView — "Panel docente de la lección" (Vista Profesor).
 *
 * Vista PEDAGÓGICA simple para el profesor editor: personaliza cómo se comporta
 * el tutor sin ver nada técnico (block_id, timestamps crudos, Chroma,
 * index_status, retrieval_scope…). Reusa los mismos endpoints de autoría que el
 * editor avanzado, pero:
 *   - la pedagogía se guarda con `upsertLesson` (incl. metadata.pedagogy).
 *   - los "momentos" se guardan con `updateMoments` (NUNCA `/blocks`): el backend
 *     preserva tiempos/estructura y rechaza cambios técnicos.
 *
 * UX (máx. 4 bloques + progressive disclosure):
 *   1. Objetivo de la lección
 *   2. Cómo debe ayudar el tutor  (+ "Opciones avanzadas": reforzar / no hacer)
 *   3. Errores y preguntas frecuentes
 *   4. Vista previa del tutor
 *   · Secundario, colapsado: "Editar momentos de la clase", "Recursos de la lección"
 *
 * El editor avanzado (LessonVideoEditor) queda para admin de curso / técnico.
 *
 * Props: { resource, courseId, sectionContext, onClose(refresh), readOnly }
 *   - readOnly: modo revisión (profesor SIN edición). Deshabilita la edición y
 *     oculta Guardar; solo permite ver y probar el tutor.
 */

const TONE_OPTIONS = [
  { value: '', label: 'Automático (según el curso)' },
  { value: 'directo', label: 'Directo' },
  { value: 'paciente', label: 'Paciente' },
  { value: 'exigente', label: 'Exigente' },
  { value: 'socratico', label: 'Socrático' },
  { value: 'practico', label: 'Práctico' },
];

const HELP_OPTIONS = [
  { value: '', label: 'Automático' },
  { value: 'orientar', label: 'Orientar (pistas, no la respuesta)' },
  { value: 'explicar', label: 'Explicar' },
  { value: 'corregir', label: 'Corregir' },
  { value: 'preguntar', label: 'Hacer preguntas' },
  { value: 'ejemplo_guiado', label: 'Dar ejemplo guiado' },
];

const linesToArr = (s) => (s || '').split('\n').map((x) => x.trim()).filter(Boolean);
const arrToLines = (a) => (Array.isArray(a) ? a.join('\n') : (a || ''));

const secondsToClock = (s) => {
  const n = Math.max(0, Math.floor(Number(s) || 0));
  const mm = String(Math.floor(n / 60)).padStart(2, '0');
  const ss = String(n % 60).padStart(2, '0');
  return `${mm}:${ss}`;
};

export default function TutorPedagogyView({ resource, courseId, sectionContext = null, onClose, readOnly = false }) {
  const [lessonId, setLessonId] = useState('');
  const [lesson, setLesson] = useState(null);
  const [form, setForm] = useState(null);
  const [moments, setMoments] = useState([]);
  const [showTimes, setShowTimes] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [dirtyPed, setDirtyPed] = useState(false);
  const [dirtyMoments, setDirtyMoments] = useState(false);
  const [dirtyChange, setDirtyChange] = useState(false);
  const [probando, setProbando] = useState(false);

  // Progressive disclosure: casi todo arranca colapsado.
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [showMoments, setShowMoments] = useState(false);
  const [showResources, setShowResources] = useState(false);

  const isDirty = dirtyPed || dirtyMoments;

  // --- Carga: vínculo del recurso -> lección -> detalle ---
  useEffect(() => {
    if (!resource?.id) return undefined;
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const link = await getResourceLink(resource.id, courseId);
        const lId = link?.lesson_id || sectionContext?.lesson_id || '';
        if (!alive) return;
        setLessonId(lId);
        if (!lId) { setLesson(null); setForm(null); setMoments([]); return; }
        const data = await getLesson(lId, courseId);
        if (!alive) return;
        const ped = (data.metadata || {}).pedagogy || {};
        setLesson(data);
        setForm({
          learning_goal: data.learning_goal || '',
          learning_goals: arrToLines(data.learning_goals),
          delegated: arrToLines(data.delegated_to_tutor),
          attribution: arrToLines(data.attribution_constraints),
          tutor_tone: ped.tutor_tone || '',
          help_level: ped.help_level || '',
          lesson_rules: ped.lesson_rules || '',
          common_mistakes: arrToLines(ped.common_mistakes),
        });
        setMoments((data.blocks || []).map((b) => ({
          block_id: b.block_id,
          block_title: b.block_title || '',
          summary: b.summary || '',
          tutor_focus: b.tutor_focus || '',
          concepts: Array.isArray(b.concepts) ? b.concepts : linesToArr(b.concepts),
          preguntas_probables: Array.isArray(b.preguntas_probables) ? b.preguntas_probables : linesToArr(b.preguntas_probables),
          start_time: b.start_time,
          end_time: b.end_time,
        })));
        setDirtyPed(false);
        setDirtyMoments(false);
      } catch (e) {
        if (alive) showNotification('error', e.message);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, [resource?.id, courseId, sectionContext?.lesson_id]);

  const setPed = (k, v) => {
    if (readOnly) return;
    setForm((p) => ({ ...p, [k]: v }));
    setDirtyPed(true);
  };
  const setMomentField = (idx, k, v) => {
    if (readOnly) return;
    setMoments((prev) => prev.map((m, i) => (i === idx ? { ...m, [k]: v } : m)));
    setDirtyMoments(true);
  };

  const testCtx = useMemo(() => activityContextFromMoodleModule(resource, sectionContext?.section, {
    courseId,
    moodleSectionId: sectionContext?.moodle_section_id,
    sectionName: sectionContext?.current_section_name,
    sectionOrder: sectionContext?.current_section_order,
    lessonId: lessonId || sectionContext?.lesson_id,
  }), [resource, sectionContext, courseId, lessonId]);

  const saveAll = useCallback(async () => {
    if (readOnly || !lessonId || !isDirty) return true;
    setSaving(true);
    try {
      if (dirtyPed) {
        await upsertLesson(courseId, lessonId, {
          lesson_id: lessonId,
          // preservamos estructura: sección, título, orden, prerequisitos, etc.
          moodle_section_id: lesson.moodle_section_id || sectionContext?.moodle_section_id || '',
          title: lesson.lesson_title || lesson.title || '',
          order: Number(lesson.order) || 0,
          expected_action: lesson.expected_action || '',
          resources: lesson.resources || [],
          prerequisites: lesson.prerequisites || [],
          notes: lesson.notes || '',
          // pedagogía editable por el profesor:
          learning_goal: form.learning_goal,
          learning_goals: linesToArr(form.learning_goals),
          delegated_to_tutor: linesToArr(form.delegated),
          attribution_constraints: linesToArr(form.attribution),
          pedagogy: {
            tutor_tone: form.tutor_tone,
            help_level: form.help_level,
            lesson_rules: form.lesson_rules,
            common_mistakes: linesToArr(form.common_mistakes),
          },
        });
      }
      if (dirtyMoments) {
        // updateMoments NO envía timestamps: el backend preserva la estructura.
        await updateMoments(courseId, lessonId, moments.map((m) => ({
          block_id: m.block_id,
          block_title: m.block_title || '',
          summary: m.summary || '',
          tutor_focus: m.tutor_focus || '',
          concepts: Array.isArray(m.concepts) ? m.concepts : linesToArr(m.concepts),
          preguntas_probables: Array.isArray(m.preguntas_probables) ? m.preguntas_probables : linesToArr(m.preguntas_probables),
        })));
      }
      setDirtyPed(false);
      setDirtyMoments(false);
      setDirtyChange(true);
      showNotification('success', 'Configuración del tutor guardada.');
      return true;
    } catch (e) {
      showNotification('error', e.message);
      return false;
    } finally {
      setSaving(false);
    }
  }, [readOnly, lessonId, isDirty, dirtyPed, dirtyMoments, courseId, lesson, form, moments, sectionContext?.moodle_section_id]);

  const handleClose = () => {
    if (isDirty && !window.confirm('Tienes cambios sin guardar. ¿Salir de todos modos?')) return;
    onClose?.(dirtyChange);
  };

  const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none disabled:opacity-60 disabled:cursor-not-allowed';
  const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';
  const cardCls = 'bg-kenth-card border border-kenth-border rounded-2xl p-5 flex flex-col gap-4';
  const discloseBtnCls = 'w-full flex items-center justify-between text-left text-sm font-black uppercase italic text-kenth-text tracking-tight px-5 py-4 bg-kenth-card border border-kenth-border rounded-2xl hover:border-kenth-brightred/50 transition';

  const configurado = Boolean(
    form && (form.learning_goal || form.tutor_tone || form.help_level || form.lesson_rules
      || linesToArr(form.common_mistakes).length || linesToArr(form.attribution).length),
  );

  const chevron = (open) => (
    <svg className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
    </svg>
  );

  return (
    <div className="fixed inset-0 z-[200] bg-black/80 backdrop-blur-sm flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between gap-4 px-5 py-3 border-b border-kenth-border bg-kenth-card">
        <div className="min-w-0">
          <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">
            {readOnly ? 'Panel docente de la lección · solo lectura' : 'Panel docente de la lección'}
          </p>
          <h3 className="text-base font-black uppercase italic text-kenth-text tracking-tight truncate">
            {resource?.name || 'Lección'}
            {sectionContext?.current_section_name && (
              <span className="ml-2 text-[10px] not-italic font-bold text-kenth-subtext align-middle">
                · {sectionContext.current_section_name}
              </span>
            )}
          </h3>
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          {/* Estados honestos: sin publicación mientras no exista backend real. */}
          <div className="hidden sm:flex items-center gap-2">
            {readOnly ? (
              <StatusChip tone="info">Solo lectura</StatusChip>
            ) : saving ? (
              <StatusChip tone="info">Guardando…</StatusChip>
            ) : isDirty ? (
              <StatusChip tone="warn">Cambios pendientes</StatusChip>
            ) : (
              <StatusChip tone="ok">Guardado</StatusChip>
            )}
            {configurado && !isDirty && <StatusChip tone="ok">Tutor configurado</StatusChip>}
          </div>
          {!readOnly && (
            <button
              onClick={saveAll}
              disabled={saving || !isDirty || !lessonId}
              className="px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40 transition"
            >
              {saving ? 'Guardando…' : (isDirty ? 'Guardar' : 'Guardado')}
            </button>
          )}
          <button onClick={handleClose} className="text-kenth-subtext hover:text-kenth-text" title="Cerrar">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        {loading ? (
          <p className="text-sm text-kenth-subtext">Cargando…</p>
        ) : !lessonId || !form ? (
          <div className="max-w-xl mx-auto text-center mt-16">
            <p className="text-kenth-text font-bold">Esta actividad todavía no es una lección del tutor.</p>
            <p className="text-sm text-kenth-subtext mt-2">
              El tutor se personaliza sobre las clases en video (H5P). Abre una clase en video para configurar su comportamiento.
            </p>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto flex flex-col gap-4">
            {readOnly && (
              <div className="rounded-2xl border border-kenth-border bg-kenth-surface/5 px-5 py-3 text-sm text-kenth-subtext">
                Estás revisando esta lección en <b className="text-kenth-text">modo solo lectura</b>. Puedes ver la
                configuración y probar el tutor, pero no editar. La edición requiere permiso de profesor editor.
              </div>
            )}

            {/* 1 · Objetivo de la lección */}
            <section className={cardCls}>
              <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">1 · Objetivo de la lección</h4>
              <div>
                <label className={labelCls}>Objetivo de aprendizaje</label>
                <textarea rows={2} disabled={readOnly} className={inputCls} value={form.learning_goal} onChange={(e) => setPed('learning_goal', e.target.value)} placeholder="En una frase, qué logra el estudiante en esta clase." />
              </div>
              <div>
                <label className={labelCls}>Criterios de logro (uno por línea)</label>
                <textarea rows={3} disabled={readOnly} className={inputCls} value={form.learning_goals} onChange={(e) => setPed('learning_goals', e.target.value)} placeholder={'Reconoce el concepto X\nAplica la técnica Y'} />
              </div>
            </section>

            {/* 2 · Cómo debe ayudar el tutor */}
            <section className={cardCls}>
              <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">2 · Cómo debe ayudar el tutor</h4>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className={labelCls}>Tono del tutor</label>
                  <select disabled={readOnly} className={inputCls} value={form.tutor_tone} onChange={(e) => setPed('tutor_tone', e.target.value)}>
                    {TONE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                  </select>
                </div>
                <div>
                  <label className={labelCls}>Nivel de ayuda</label>
                  <select disabled={readOnly} className={inputCls} value={form.help_level} onChange={(e) => setPed('help_level', e.target.value)}>
                    {HELP_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                  </select>
                </div>
              </div>
              <div>
                <label className={labelCls}>Reglas de la lección</label>
                <textarea rows={2} disabled={readOnly} className={inputCls} value={form.lesson_rules} onChange={(e) => setPed('lesson_rules', e.target.value)} placeholder="Ej.: No des la respuesta directa; guía con preguntas." />
              </div>

              {/* Progressive disclosure: reforzar / no hacer */}
              <button type="button" onClick={() => setShowAdvanced((v) => !v)} className="flex items-center gap-2 text-[10px] uppercase tracking-widest text-kenth-subtext hover:text-kenth-text self-start">
                {chevron(showAdvanced)} Opciones avanzadas del tutor
              </button>
              {showAdvanced && (
                <div className="flex flex-col gap-4 border-t border-kenth-border/50 pt-4">
                  <div>
                    <label className={labelCls}>Qué debe reforzar el tutor (uno por línea)</label>
                    <textarea rows={2} disabled={readOnly} className={inputCls} value={form.delegated} onChange={(e) => setPed('delegated', e.target.value)} placeholder="Temas que el tutor debe cubrir aunque no estén en el video." />
                  </div>
                  <div>
                    <label className={labelCls}>Qué NO debe hacer el tutor (uno por línea)</label>
                    <textarea rows={2} disabled={readOnly} className={inputCls} value={form.attribution} onChange={(e) => setPed('attribution', e.target.value)} placeholder="Ej.: No recomendar plugins de pago." />
                  </div>
                </div>
              )}
            </section>

            {/* 3 · Errores y preguntas frecuentes */}
            <section className={cardCls}>
              <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">3 · Errores y preguntas frecuentes</h4>
              <div>
                <label className={labelCls}>Errores comunes a vigilar (uno por línea)</label>
                <textarea rows={3} disabled={readOnly} className={inputCls} value={form.common_mistakes} onChange={(e) => setPed('common_mistakes', e.target.value)} placeholder={'Confundir X con Y\nOlvidar el paso Z'} />
              </div>
              <p className="text-[11px] text-kenth-subtext">
                Las preguntas probables por momento se editan en “Editar momentos de la clase”.
              </p>
            </section>

            {/* 4 · Vista previa del tutor */}
            <section className={cardCls}>
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">4 · Vista previa del tutor</h4>
                <button onClick={() => setProbando((v) => !v)} className="px-3 py-1.5 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60">
                  {probando ? 'Cerrar prueba' : 'Abrir tutor'}
                </button>
              </div>
              <p className="text-[11px] text-kenth-subtext">
                Los cambios de comportamiento del tutor se aplican al instante (no requieren reindexación).
                {!readOnly && ' Guarda antes de probar.'}
              </p>
              {probando && (
                <TutorAssistCard
                  variant="lesson"
                  titulo={`Prueba · ${lessonId}`}
                  contexto={`Lección: ${resource?.name}. Tipo: ${resource?.modname}.`}
                  activityContext={testCtx}
                  proactiveMessage={lesson?.proactive_message || ''}
                  suggestedPrompts={lesson?.suggested_prompts || []}
                />
              )}
            </section>

            {/* Secundario · Editar momentos de la clase (colapsado) */}
            <div>
              <button type="button" onClick={() => setShowMoments((v) => !v)} className={discloseBtnCls}>
                <span>Editar momentos de la clase{moments.length ? ` (${moments.length})` : ''}</span>
                {chevron(showMoments)}
              </button>
              {showMoments && (
                <section className={`${cardCls} mt-3`}>
                  <div className="flex items-center justify-end">
                    <button onClick={() => setShowTimes((v) => !v)} className="text-[10px] uppercase tracking-widest text-kenth-subtext hover:text-kenth-text">
                      {showTimes ? 'Ocultar tiempos' : 'Mostrar tiempos (solo lectura)'}
                    </button>
                  </div>
                  {moments.length === 0 ? (
                    <p className="text-sm text-kenth-subtext">Esta clase aún no tiene momentos segmentados. Un administrador puede crearlos en el editor avanzado.</p>
                  ) : (
                    <div className="flex flex-col gap-3">
                      {moments.map((m, idx) => (
                        <div key={m.block_id || idx} className="border border-kenth-border/60 rounded-xl p-4 bg-kenth-surface/5 flex flex-col gap-3">
                          <div className="flex items-center gap-3">
                            <span className="text-[10px] font-black text-kenth-brightred">Momento {idx + 1}</span>
                            {showTimes && (
                              <span className="text-[10px] text-kenth-subtext font-mono">
                                {secondsToClock(m.start_time)} – {secondsToClock(m.end_time)} (solo lectura)
                              </span>
                            )}
                          </div>
                          <input disabled={readOnly} className={inputCls} value={m.block_title} onChange={(e) => setMomentField(idx, 'block_title', e.target.value)} placeholder="Título del momento (ej.: La regla y tu tarea)" />
                          <textarea rows={2} disabled={readOnly} className={inputCls} value={m.summary} onChange={(e) => setMomentField(idx, 'summary', e.target.value)} placeholder="Resumen: qué pasa en este momento." />
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                            <input disabled={readOnly} className={inputCls} value={m.tutor_focus} onChange={(e) => setMomentField(idx, 'tutor_focus', e.target.value)} placeholder="Intención / foco del tutor aquí" />
                            <textarea rows={1} disabled={readOnly} className={inputCls} value={arrToLines(m.concepts)} onChange={(e) => setMomentField(idx, 'concepts', linesToArr(e.target.value))} placeholder="Conceptos (uno por línea)" />
                            <textarea rows={1} disabled={readOnly} className={inputCls} value={arrToLines(m.preguntas_probables)} onChange={(e) => setMomentField(idx, 'preguntas_probables', linesToArr(e.target.value))} placeholder="Preguntas probables (una por línea)" />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </section>
              )}
            </div>

            {/* Secundario · Recursos de la lección (colapsado) */}
            <div>
              <button type="button" onClick={() => setShowResources((v) => !v)} className={discloseBtnCls}>
                <span>Recursos de la lección</span>
                {chevron(showResources)}
              </button>
              {showResources && (
                <section className={`${cardCls} mt-3`}>
                  <LessonResourcesPanel courseId={courseId} lessonId={lessonId} />
                </section>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatusChip({ tone = 'info', children }) {
  const map = {
    ok: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30',
    warn: 'bg-amber-500/10 text-amber-300 border-amber-500/30',
    info: 'bg-kenth-surface/10 text-kenth-subtext border-kenth-border',
  };
  return (
    <span className={`px-2.5 py-1 rounded-full border text-[10px] font-black uppercase tracking-widest ${map[tone] || map.info}`}>
      {children}
    </span>
  );
}
