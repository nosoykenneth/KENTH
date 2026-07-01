import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  getResourceLink, getLesson, getTranscript, getTranscriptStatus,
  autoTranscribe, replaceTranscript, aiPrepare, aiPrepareAccept,
} from '../../services/sectionsService';
import { activityContextFromMoodleModule } from '../../services/activityContext';
import { showNotification } from '../../utils/notify';
import TutorAssistCard from './TutorAssistCard';
import LessonResourcesPanel from './LessonResourcesPanel';

/**
 * TutorPedagogyView — asistente "Preparar tutor con IA" (Vista Profesor).
 *
 * Rediseñado como asistente de 3 pasos para que el profesor NO tenga que llenar
 * 20 campos a mano. La IA (Ollama local, vía backend) analiza la transcripción y
 * propone un BORRADOR pedagógico; el profesor lo revisa, edita y ACEPTA. Nada se
 * publica ni indexa automáticamente; el borrador queda aislado hasta aceptar.
 *
 *   Paso 1 · Clase y recursos     -> transcripción (estado, transcribir, corregir) + recursos
 *   Paso 2 · Preparación con IA    -> calidad + generar borrador + resumen
 *   Paso 3 · Revisión y prueba     -> editar borrador, probar tutor, aceptar
 *
 * Oculta todo lo técnico (block_id, timestamps, source_hash, Chroma, retrieval,
 * index_status, JSON crudo). El editor avanzado (LessonVideoEditor) sigue siendo
 * para admin de curso / técnico.
 *
 * Props: { resource, courseId, sectionContext, onClose(refresh), readOnly }
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
const QUALITY_OPTIONS = [
  { value: 'fast', label: 'Rápido', hint: 'Borrador veloz.' },
  { value: 'balanced', label: 'Equilibrado', hint: 'Recomendado.' },
  { value: 'max', label: 'Máximo', hint: 'Añade revisión de calidad (más lento).' },
];
// Términos técnicos que el ASR suele transcribir mal (Fase 3): ayuda al profesor
// a corregirlos. Es solo una guía visual del dominio de mezcla/masterización.
const GLOSARIO = ['headroom', 'gain staging', 'LUFS', 'threshold', 'sidechain', 'fase', 'compresión paralela', 'ecualización', 'masterización'];

const linesToArr = (s) => (s || '').split('\n').map((x) => x.trim()).filter(Boolean);
const arrToLines = (a) => (Array.isArray(a) ? a.join('\n') : (a || ''));

const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none disabled:opacity-60 disabled:cursor-not-allowed';
const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';
const cardCls = 'bg-kenth-card border border-kenth-border rounded-2xl p-5 flex flex-col gap-4';

// Deriva el formulario editable del borrador devuelto por la IA.
function draftToForm(d = {}) {
  return {
    learning_goal: d.learning_goal || '',
    lesson_summary: d.lesson_summary || '',
    recommended_tone: d.recommended_tone || '',
    recommended_help_level: d.recommended_help_level || '',
    key_concepts: arrToLines(d.key_concepts),
    common_mistakes: arrToLines(d.common_mistakes),
    probable_questions: arrToLines(d.probable_questions),
    tutor_focus: arrToLines(d.tutor_focus),
    tutor_must_not_do: arrToLines(d.tutor_must_not_do),
    lesson_rules: arrToLines(d.lesson_rules),
    terms_to_review: Array.isArray(d.terms_to_review) ? d.terms_to_review : [],
    transcript_quality_notes: Array.isArray(d.transcript_quality_notes) ? d.transcript_quality_notes : [],
    confidence: d.confidence || 'low',
    moments: (d.moments || []).map((m) => ({
      existing_block_id: m.existing_block_id || null,
      title: m.title || '',
      summary: m.summary || '',
      pedagogical_intent: m.pedagogical_intent || '',
      key_concepts: arrToLines(m.key_concepts),
      probable_questions: arrToLines(m.probable_questions),
      common_mistakes: arrToLines(m.common_mistakes),
    })),
  };
}

// Reconstruye el objeto draft (esquema del backend) desde el formulario.
function formToDraft(f) {
  return {
    learning_goal: f.learning_goal,
    lesson_summary: f.lesson_summary,
    recommended_tone: f.recommended_tone,
    recommended_help_level: f.recommended_help_level,
    key_concepts: linesToArr(f.key_concepts),
    common_mistakes: linesToArr(f.common_mistakes),
    probable_questions: linesToArr(f.probable_questions),
    tutor_focus: linesToArr(f.tutor_focus),
    tutor_must_not_do: linesToArr(f.tutor_must_not_do),
    lesson_rules: linesToArr(f.lesson_rules),
    terms_to_review: f.terms_to_review || [],
    transcript_quality_notes: f.transcript_quality_notes || [],
    confidence: f.confidence || 'low',
    moments: (f.moments || []).map((m) => ({
      existing_block_id: m.existing_block_id || null,
      title: m.title,
      summary: m.summary,
      pedagogical_intent: m.pedagogical_intent,
      key_concepts: linesToArr(m.key_concepts),
      probable_questions: linesToArr(m.probable_questions),
      common_mistakes: linesToArr(m.common_mistakes),
    })),
  };
}

export default function TutorPedagogyView({ resource, courseId, sectionContext = null, onClose, readOnly = false }) {
  const [step, setStep] = useState(1);
  const [lessonId, setLessonId] = useState('');
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);

  // Transcripción
  const [transcript, setTranscript] = useState([]);
  const [job, setJob] = useState(null);
  const [correcting, setCorrecting] = useState(false);
  const [savingTranscript, setSavingTranscript] = useState(false);

  // IA
  const [quality, setQuality] = useState('balanced');
  const [aiBusy, setAiBusy] = useState(false);
  const [aiPhase, setAiPhase] = useState('');
  const [aiResult, setAiResult] = useState(null); // { draft, review, models, confidence, ... }
  const [form, setForm] = useState(null);
  const [accepting, setAccepting] = useState(false);
  const [accepted, setAccepted] = useState(false);
  const [probando, setProbando] = useState(false);
  const phaseTimer = useRef(null);

  const meta = lesson?.metadata || {};
  const transcriptStatus = meta.transcript_status || (transcript.length ? 'generated' : 'missing');
  const hasTranscript = transcript.length > 0;

  // --- Carga: vínculo del recurso -> lección -> detalle + transcripción ---
  const reload = useCallback(async () => {
    if (!resource?.id) return;
    setLoading(true);
    try {
      const link = await getResourceLink(resource.id, courseId);
      const lId = link?.lesson_id || sectionContext?.lesson_id || '';
      setLessonId(lId);
      if (!lId) { setLesson(null); setTranscript([]); return; }
      const [data, tr] = await Promise.all([
        getLesson(lId, courseId),
        getTranscript(courseId, lId).catch(() => ({ segments: [], job: null })),
      ]);
      setLesson(data);
      setTranscript(tr.segments || []);
      setJob(tr.job || null);
      // Si ya hay un borrador guardado, precargarlo (permite volver al paso 3).
      const savedDraft = (data.metadata || {}).ai_prepare?.draft;
      if (savedDraft) {
        setForm(draftToForm(savedDraft));
        setAiResult({ draft: savedDraft, review: (data.metadata || {}).ai_prepare?.review || null });
        setAccepted((data.metadata || {}).ai_prepare_status === 'accepted');
      }
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
  }, [resource?.id, courseId, sectionContext?.lesson_id]);

  useEffect(() => { reload(); }, [reload]);

  // --- Polling del job de transcripción automática ---
  useEffect(() => {
    if (!lessonId || job?.status !== 'running') return undefined;
    const iv = setInterval(async () => {
      try {
        const data = await getTranscriptStatus(courseId, lessonId);
        const st = data.job;
        setJob(st || null);
        if (!st || st.status === 'done') {
          clearInterval(iv);
          if (st?.status === 'done') {
            const tr = await getTranscript(courseId, lessonId);
            setTranscript(tr.segments || []);
            showNotification('success', 'Transcripción lista.');
            await reload();
          }
        } else if (st.status === 'error') {
          clearInterval(iv);
          showNotification('error', st.error || 'Falló la transcripción.');
        }
      } catch (e) {
        clearInterval(iv);
        showNotification('error', e.message);
      }
    }, 3000);
    return () => clearInterval(iv);
  }, [job?.status, lessonId, courseId, reload]);

  useEffect(() => () => { if (phaseTimer.current) clearInterval(phaseTimer.current); }, []);

  const startTranscribe = async () => {
    if (readOnly || !lessonId || !resource?.id) return;
    if (hasTranscript && !window.confirm('Esto reemplazará la transcripción actual al terminar. ¿Continuar?')) return;
    try {
      const data = await autoTranscribe(courseId, lessonId, { resource_id: Number(resource.id) });
      setJob(data.job || { status: 'running', progress: 0 });
      showNotification('success', 'Transcripción iniciada. Puede tardar varios minutos…');
    } catch (e) {
      showNotification('error', e.message);
    }
  };

  const setSegText = (idx, text) => setTranscript((p) => p.map((s, i) => (i === idx ? { ...s, text } : s)));

  const saveTranscript = async () => {
    if (readOnly || !lessonId) return;
    setSavingTranscript(true);
    try {
      const segs = transcript.map((s, i) => ({ seq: i, start_time: Number(s.start_time) || 0, end_time: Number(s.end_time) || 0, text: s.text || '', speaker: s.speaker || '' }));
      await replaceTranscript(courseId, lessonId, segs);
      showNotification('success', 'Transcripción corregida y guardada.');
      setCorrecting(false);
      await reload();
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setSavingTranscript(false);
    }
  };

  const runAiPrepare = async () => {
    if (readOnly || !lessonId) return;
    setAiBusy(true);
    setAiResult(null);
    const phases = quality === 'max'
      ? ['Analizando la clase…', 'Detectando momentos…', 'Generando la guía del tutor…', 'Revisando calidad…']
      : ['Analizando la clase…', 'Detectando momentos…', 'Generando la guía del tutor…'];
    let i = 0;
    setAiPhase(phases[0]);
    phaseTimer.current = setInterval(() => { i = Math.min(i + 1, phases.length - 1); setAiPhase(phases[i]); }, 4000);
    try {
      const res = await aiPrepare(courseId, lessonId, { mode: 'draft', quality });
      setAiResult(res);
      setForm(draftToForm(res.draft));
      setAccepted(false);
      showNotification('success', 'Borrador del tutor generado. Revísalo antes de aceptar.');
      setStep(3);
    } catch (e) {
      if (e.code === 'no_transcript') {
        showNotification('error', 'Primero transcribe el video (paso 1).');
        setStep(1);
      } else {
        showNotification('error', e.message);
      }
    } finally {
      if (phaseTimer.current) clearInterval(phaseTimer.current);
      setAiPhase('');
      setAiBusy(false);
    }
  };

  const setF = (k, v) => { if (!readOnly) setForm((p) => ({ ...p, [k]: v })); };
  const setMoment = (idx, k, v) => { if (!readOnly) setForm((p) => ({ ...p, moments: p.moments.map((m, i) => (i === idx ? { ...m, [k]: v } : m)) })); };

  const acceptDraft = async () => {
    if (readOnly || !lessonId || !form) return;
    setAccepting(true);
    try {
      const res = await aiPrepareAccept(courseId, lessonId, { draft: formToDraft(form), apply_moments: true });
      setAccepted(true);
      const changed = (res.changed || []).length;
      showNotification('success', `Tutor actualizado (${changed} campos${res.moments_applied ? `, ${res.moments_applied} momentos` : ''}).`);
      await reload();
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setAccepting(false);
    }
  };

  const testCtx = useMemo(() => activityContextFromMoodleModule(resource, sectionContext?.section, {
    courseId,
    moodleSectionId: sectionContext?.moodle_section_id,
    sectionName: sectionContext?.current_section_name,
    sectionOrder: sectionContext?.current_section_order,
    lessonId: lessonId || sectionContext?.lesson_id,
  }), [resource, sectionContext, courseId, lessonId]);

  const handleClose = () => onClose?.(accepted);

  const STEPS = [
    { n: 1, label: 'Clase y recursos' },
    { n: 2, label: 'Preparación con IA' },
    { n: 3, label: 'Revisión y prueba' },
  ];

  return (
    <div className="fixed inset-0 z-[200] bg-black/80 backdrop-blur-sm flex flex-col">
      {/* Header + stepper */}
      <div className="flex items-center justify-between gap-4 px-5 py-3 border-b border-kenth-border bg-kenth-card">
        <div className="min-w-0">
          <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">
            Preparar tutor con IA{readOnly ? ' · solo lectura' : ''}
          </p>
          <h3 className="text-base font-black uppercase italic text-kenth-text tracking-tight truncate">
            {resource?.name || 'Lección'}
            {sectionContext?.current_section_name && (
              <span className="ml-2 text-[10px] not-italic font-bold text-kenth-subtext align-middle">· {sectionContext.current_section_name}</span>
            )}
          </h3>
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          {accepted && <StatusChip tone="ok">Tutor configurado</StatusChip>}
          <button onClick={handleClose} className="text-kenth-subtext hover:text-kenth-text" title="Cerrar">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
      </div>

      {/* Stepper */}
      {lessonId && (
        <div className="flex items-center justify-center gap-2 px-5 py-3 border-b border-kenth-border bg-kenth-card/40">
          {STEPS.map((s, i) => (
            <React.Fragment key={s.n}>
              <button
                onClick={() => setStep(s.n)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-[11px] font-black uppercase tracking-widest transition ${
                  step === s.n ? 'bg-kenth-brightred text-white border-kenth-brightred'
                  : 'bg-kenth-surface/5 text-kenth-subtext border-kenth-border hover:text-kenth-text'}`}
              >
                <span className={`inline-flex h-5 w-5 items-center justify-center rounded-full text-[10px] ${step === s.n ? 'bg-white/20' : 'bg-kenth-surface/20'}`}>{s.n}</span>
                <span className="hidden sm:inline">{s.label}</span>
              </button>
              {i < STEPS.length - 1 && <div className="h-px w-4 bg-kenth-border" />}
            </React.Fragment>
          ))}
        </div>
      )}

      {/* Body */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        {loading ? (
          <p className="text-sm text-kenth-subtext">Cargando…</p>
        ) : !lessonId ? (
          <div className="max-w-xl mx-auto text-center mt-16">
            <p className="text-kenth-text font-bold">Esta actividad todavía no es una lección del tutor.</p>
            <p className="text-sm text-kenth-subtext mt-2">El tutor se prepara sobre las clases en video (H5P). Abre una clase en video para configurarlo.</p>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto flex flex-col gap-4">
            {readOnly && (
              <div className="rounded-2xl border border-kenth-border bg-kenth-surface/5 px-5 py-3 text-sm text-kenth-subtext">
                Estás en <b className="text-kenth-text">modo solo lectura</b>. Puedes ver la preparación y probar el tutor, pero no editar ni aceptar.
              </div>
            )}

            {/* ============ PASO 1 ============ */}
            {step === 1 && (
              <>
                <section className={cardCls}>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">1 · Transcripción de la clase</h4>
                    <TranscriptChip status={transcriptStatus} count={transcript.length} />
                  </div>
                  <p className="text-[12px] text-kenth-subtext">
                    La IA necesita la transcripción del video para analizar la clase. El modelo de IA no escucha audio: transcribimos primero y luego analiza el texto.
                  </p>
                  {job?.status === 'running' && (
                    <div className="rounded-lg border border-indigo-500/30 bg-indigo-500/10 p-2">
                      <div className="flex items-center justify-between text-[10px] text-indigo-200 mb-1">
                        <span>Transcribiendo… ({job.segments || 0} segmentos)</span>
                        <span>{Math.round((job.progress || 0) * 100)}%</span>
                      </div>
                      <div className="h-1.5 rounded-full bg-indigo-900/40 overflow-hidden">
                        <div className="h-full bg-indigo-400 transition-all" style={{ width: `${Math.round((job.progress || 0) * 100)}%` }} />
                      </div>
                    </div>
                  )}
                  <div className="flex items-center gap-2 flex-wrap">
                    <button onClick={startTranscribe} disabled={readOnly || job?.status === 'running'}
                      className="px-3 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                      {job?.status === 'running' ? 'Transcribiendo…' : (hasTranscript ? '✨ Regenerar transcripción' : '✨ Transcribir con IA')}
                    </button>
                    {hasTranscript && (
                      <button onClick={() => setCorrecting((v) => !v)} disabled={readOnly}
                        className="px-3 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-text text-xs font-black uppercase tracking-widest hover:border-kenth-brightred/50 disabled:opacity-40">
                        {correcting ? 'Cerrar corrección' : 'Corregir transcripción'}
                      </button>
                    )}
                  </div>

                  {correcting && (
                    <div className="flex flex-col gap-2 border-t border-kenth-border/50 pt-3">
                      <p className="text-[11px] text-kenth-subtext">
                        Corrige los términos técnicos mal transcritos. Referencia:{' '}
                        {GLOSARIO.map((g) => <span key={g} className="inline-block bg-kenth-surface/10 border border-kenth-border rounded px-1.5 py-0.5 text-[10px] text-kenth-subtext mr-1 mb-1">{g}</span>)}
                      </p>
                      <div className="flex flex-col gap-1.5 max-h-[38vh] overflow-y-auto pr-1">
                        {transcript.map((s, idx) => (
                          <textarea key={idx} rows={2} disabled={readOnly} value={s.text || ''} onChange={(e) => setSegText(idx, e.target.value)}
                            className="w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-2 py-1 text-xs text-kenth-text focus:border-kenth-brightred focus:outline-none resize-none" />
                        ))}
                      </div>
                      <button onClick={saveTranscript} disabled={readOnly || savingTranscript}
                        className="self-start px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                        {savingTranscript ? 'Guardando…' : 'Guardar corrección'}
                      </button>
                    </div>
                  )}
                </section>

                <section className={cardCls}>
                  <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Recursos de la lección</h4>
                  <LessonResourcesPanel courseId={courseId} lessonId={lessonId} />
                </section>

                <div className="flex justify-end">
                  <button onClick={() => setStep(2)} disabled={!hasTranscript}
                    className="px-5 py-2.5 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40 transition">
                    Siguiente: Preparación con IA →
                  </button>
                </div>
                {!hasTranscript && <p className="text-[11px] text-amber-300/80 text-right">Transcribe el video para continuar.</p>}
              </>
            )}

            {/* ============ PASO 2 ============ */}
            {step === 2 && (
              <>
                <section className={cardCls}>
                  <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">2 · Genera el borrador del tutor</h4>
                  <p className="text-[12px] text-kenth-subtext">
                    La IA analiza la transcripción y propone objetivo, resumen, momentos, conceptos, errores comunes, preguntas probables y reglas. Es un borrador: tú lo revisas y decides.
                  </p>
                  <div>
                    <label className={labelCls}>Calidad</label>
                    <div className="grid grid-cols-3 gap-2 mt-1">
                      {QUALITY_OPTIONS.map((q) => (
                        <button key={q.value} onClick={() => setQuality(q.value)} disabled={readOnly}
                          className={`rounded-xl border px-3 py-2 text-left transition ${quality === q.value ? 'border-kenth-brightred bg-kenth-brightred/10' : 'border-kenth-border bg-kenth-surface/5 hover:border-kenth-brightred/40'} disabled:opacity-40`}>
                          <div className="text-xs font-black uppercase tracking-widest text-kenth-text">{q.label}</div>
                          <div className="text-[10px] text-kenth-subtext mt-0.5">{q.hint}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {aiBusy ? (
                    <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/10 p-4 flex items-center gap-3">
                      <span className="inline-block h-4 w-4 rounded-full border-2 border-indigo-300 border-t-transparent animate-spin" />
                      <span className="text-sm text-indigo-100">{aiPhase || 'Preparando…'}</span>
                    </div>
                  ) : (
                    <button onClick={runAiPrepare} disabled={readOnly || !hasTranscript}
                      className="self-start px-5 py-3 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-sm font-black uppercase tracking-widest disabled:opacity-40">
                      Generar borrador del tutor
                    </button>
                  )}

                  {aiResult?.draft && !aiBusy && (
                    <div className="border-t border-kenth-border/50 pt-3 flex flex-col gap-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <StatusChip tone="ok">Borrador listo</StatusChip>
                        <ConfidenceChip value={aiResult.draft.confidence} />
                        {aiResult.models?.review_model && <StatusChip tone="info">Revisado · {aiResult.models.review_model}</StatusChip>}
                      </div>
                      <ResumeLine label="Objetivo" value={aiResult.draft.learning_goal} />
                      <ResumeLine label="Resumen" value={aiResult.draft.lesson_summary} />
                      <ResumeLine label="Momentos" value={`${(aiResult.draft.moments || []).length}`} />
                      {(aiResult.draft.terms_to_review || []).length > 0 && (
                        <ResumeLine label="Términos a revisar" value={(aiResult.draft.terms_to_review || []).join(', ')} tone="warn" />
                      )}
                      <button onClick={() => setStep(3)} className="self-start mt-1 px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-text text-xs font-black uppercase tracking-widest hover:border-kenth-brightred/50">
                        Revisar y probar →
                      </button>
                    </div>
                  )}
                </section>
                <div className="flex justify-between">
                  <button onClick={() => setStep(1)} className="px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-subtext text-xs font-black uppercase tracking-widest hover:text-kenth-text">← Atrás</button>
                </div>
              </>
            )}

            {/* ============ PASO 3 ============ */}
            {step === 3 && (
              !form ? (
                <section className={cardCls}>
                  <p className="text-sm text-kenth-subtext">Aún no hay borrador. Genera uno en el paso 2.</p>
                  <button onClick={() => setStep(2)} className="self-start px-4 py-2 rounded-xl bg-kenth-brightred text-white text-xs font-black uppercase tracking-widest">Ir a Preparación con IA</button>
                </section>
              ) : (
                <>
                  <section className={cardCls}>
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Objetivo y resumen</h4>
                    <div>
                      <label className={labelCls}>Objetivo de aprendizaje</label>
                      <textarea rows={2} disabled={readOnly} className={inputCls} value={form.learning_goal} onChange={(e) => setF('learning_goal', e.target.value)} />
                    </div>
                    <div>
                      <label className={labelCls}>Resumen de la clase</label>
                      <textarea rows={3} disabled={readOnly} className={inputCls} value={form.lesson_summary} onChange={(e) => setF('lesson_summary', e.target.value)} />
                    </div>
                  </section>

                  <section className={cardCls}>
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Estilo del tutor</h4>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className={labelCls}>Tono</label>
                        <select disabled={readOnly} className={inputCls} value={form.recommended_tone} onChange={(e) => setF('recommended_tone', e.target.value)}>
                          {TONE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                        </select>
                      </div>
                      <div>
                        <label className={labelCls}>Nivel de ayuda</label>
                        <select disabled={readOnly} className={inputCls} value={form.recommended_help_level} onChange={(e) => setF('recommended_help_level', e.target.value)}>
                          {HELP_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                        </select>
                      </div>
                    </div>
                    <div>
                      <label className={labelCls}>Reglas importantes (una por línea)</label>
                      <textarea rows={2} disabled={readOnly} className={inputCls} value={form.lesson_rules} onChange={(e) => setF('lesson_rules', e.target.value)} />
                    </div>
                  </section>

                  <section className={cardCls}>
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Errores, preguntas y foco</h4>
                    <div>
                      <label className={labelCls}>Errores comunes a vigilar (uno por línea)</label>
                      <textarea rows={3} disabled={readOnly} className={inputCls} value={form.common_mistakes} onChange={(e) => setF('common_mistakes', e.target.value)} />
                    </div>
                    <div>
                      <label className={labelCls}>Preguntas probables (una por línea)</label>
                      <textarea rows={3} disabled={readOnly} className={inputCls} value={form.probable_questions} onChange={(e) => setF('probable_questions', e.target.value)} />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div>
                        <label className={labelCls}>Qué debe reforzar el tutor (uno por línea)</label>
                        <textarea rows={2} disabled={readOnly} className={inputCls} value={form.tutor_focus} onChange={(e) => setF('tutor_focus', e.target.value)} />
                      </div>
                      <div>
                        <label className={labelCls}>Qué NO debe hacer el tutor (uno por línea)</label>
                        <textarea rows={2} disabled={readOnly} className={inputCls} value={form.tutor_must_not_do} onChange={(e) => setF('tutor_must_not_do', e.target.value)} />
                      </div>
                    </div>
                  </section>

                  {form.moments.length > 0 && (
                    <section className={cardCls}>
                      <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Momentos de la clase ({form.moments.length})</h4>
                      <div className="flex flex-col gap-3">
                        {form.moments.map((m, idx) => (
                          <div key={idx} className="border border-kenth-border/60 rounded-xl p-4 bg-kenth-surface/5 flex flex-col gap-2">
                            <div className="flex items-center gap-2">
                              <span className="text-[10px] font-black text-kenth-brightred">Momento {idx + 1}</span>
                              {!m.existing_block_id && <span className="text-[10px] text-amber-300/80">nuevo (se creará en el editor avanzado)</span>}
                            </div>
                            <input disabled={readOnly} className={inputCls} value={m.title} onChange={(e) => setMoment(idx, 'title', e.target.value)} placeholder="Título del momento" />
                            <textarea rows={2} disabled={readOnly} className={inputCls} value={m.summary} onChange={(e) => setMoment(idx, 'summary', e.target.value)} placeholder="Resumen del momento" />
                            <input disabled={readOnly} className={inputCls} value={m.pedagogical_intent} onChange={(e) => setMoment(idx, 'pedagogical_intent', e.target.value)} placeholder="Intención pedagógica / foco del tutor" />
                          </div>
                        ))}
                      </div>
                    </section>
                  )}

                  <section className={cardCls}>
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Probar tutor</h4>
                      <button onClick={() => setProbando((v) => !v)} className="px-3 py-1.5 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60">
                        {probando ? 'Cerrar prueba' : 'Abrir tutor'}
                      </button>
                    </div>
                    <p className="text-[11px] text-kenth-subtext">Acepta el borrador para que el tutor use esta configuración; los cambios de comportamiento se aplican al instante (sin reindexar).</p>
                    {probando && (
                      <TutorAssistCard variant="lesson" titulo={`Prueba · ${lessonId}`} contexto={`Lección: ${resource?.name}.`}
                        activityContext={testCtx} proactiveMessage={lesson?.proactive_message || ''} suggestedPrompts={lesson?.suggested_prompts || []} />
                    )}
                  </section>

                  {!readOnly && (
                    <div className="flex items-center justify-between gap-3 sticky bottom-0 bg-gradient-to-t from-black/60 to-transparent py-3">
                      <button onClick={() => setStep(2)} className="px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-subtext text-xs font-black uppercase tracking-widest hover:text-kenth-text">← Regenerar</button>
                      <button onClick={acceptDraft} disabled={accepting}
                        className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-black uppercase tracking-widest disabled:opacity-40 transition">
                        {accepting ? 'Aplicando…' : (accepted ? 'Guardar revisión' : 'Aceptar y aplicar al tutor')}
                      </button>
                    </div>
                  )}
                </>
              )
            )}
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
  return <span className={`px-2.5 py-1 rounded-full border text-[10px] font-black uppercase tracking-widest ${map[tone] || map.info}`}>{children}</span>;
}

function TranscriptChip({ status, count }) {
  if (status === 'missing' || !count) return <StatusChip tone="warn">Sin transcripción</StatusChip>;
  const label = status === 'edited' ? 'Transcripción corregida' : 'Transcripción lista';
  return <StatusChip tone="ok">{label} · {count} seg.</StatusChip>;
}

function ConfidenceChip({ value }) {
  const map = { high: ['ok', 'Confianza alta'], medium: ['info', 'Confianza media'], low: ['warn', 'Confianza baja'] };
  const [tone, label] = map[value] || map.low;
  return <StatusChip tone={tone}>{label}</StatusChip>;
}

function ResumeLine({ label, value, tone }) {
  if (!value) return null;
  return (
    <p className="text-[12px]">
      <span className={labelCls}>{label}: </span>
      <span className={tone === 'warn' ? 'text-amber-300' : 'text-kenth-text'}>{value}</span>
    </p>
  );
}
