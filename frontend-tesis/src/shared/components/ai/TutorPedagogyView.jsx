import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  getResourceLink, getLesson, getTranscript, getTranscriptStatus,
  autoTranscribe, replaceTranscript, aiPrepare, aiPrepareAccept, updateMoments,
} from '../../services/sectionsService';
import { activityContextFromMoodleModule } from '../../services/activityContext';
import { showNotification } from '../../utils/notify';
import { fmtTime } from '../../utils/time';
import { buildMoodleViewUrl, getMoodleToken } from '../../utils/moodleToken';
import { useResourceVideoBridge } from '../../hooks/useResourceTimestamp';
import BlockTimeline from './BlockTimeline';
import TutorAssistCard from './TutorAssistCard';
import LessonResourcesPanel from './LessonResourcesPanel';

/**
 * TutorPedagogyView — asistente "Preparar tutor con IA" (Vista Profesor).
 *
 * Asistente de 3 pasos para que el profesor NO tenga que llenar 20 campos a mano.
 *
 *   Paso 1 · Clase y recursos  -> VIDEO + línea de tiempo + "Momentos de la clase"
 *                                 (editables pedagógicamente) + transcripción + recursos
 *   Paso 2 · Preparación con IA -> calidad + generar borrador + resumen
 *   Paso 3 · Revisión y prueba  -> editar borrador (acordeones), probar tutor, aceptar
 *
 * TERMINOLOGÍA: el profesor ve "Momentos de la clase" (nunca la nomenclatura
 * técnica de bloques); no ve identificadores internos, tiempos crudos, orden, JSON,
 * metadata ni estado de indexación técnico. Guarda los momentos SOLO por
 * `PUT /moments` (updateMoments): el backend preserva tiempos/estructura y rechaza
 * altas/bajas (barrera server-side). Crear/borrar/reordenar momentos o mover tiempos
 * es exclusivo del Editor avanzado (admin/técnico, vía reemplazo de bloques).
 *
 * Props: { resource, courseId, sectionContext, onClose(refresh), readOnly }
 */

const IFRAME_NAME = 'kenth_prof_video';

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
// Términos técnicos que el ASR suele transcribir mal: ayuda al profesor a corregirlos.
const GLOSARIO = ['headroom', 'gain staging', 'LUFS', 'threshold', 'sidechain', 'fase', 'compresión paralela', 'ecualización', 'masterización'];

const linesToArr = (s) => (s || '').split('\n').map((x) => x.trim()).filter(Boolean);
const arrToLines = (a) => (Array.isArray(a) ? a.join('\n') : (a || ''));

const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none disabled:opacity-60 disabled:cursor-not-allowed';
const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';
const cardCls = 'bg-kenth-card border border-kenth-border rounded-2xl p-5 flex flex-col gap-4';

// Rango de minutos humano de un momento (nunca segundos crudos como "start_time = 0").
const momentRange = (b) => {
  const a = fmtTime(Number(b?.start_time) || 0);
  const z = fmtTime(Number(b?.end_time) || 0);
  return `${a}–${z}`;
};

// Deriva el formulario editable del borrador devuelto por la IA.
// NOTA: key_concepts y probable_questions a NIVEL LECCIÓN se conservan como paso a paso
// (no se editan en la UI del profesor: eran campos muertos / duplicados — ver auditoría),
// pero se preservan en el round-trip para no perder lo que produjo la IA.
function draftToForm(d = {}) {
  return {
    learning_goal: d.learning_goal || '',
    lesson_summary: d.lesson_summary || '',
    recommended_tone: d.recommended_tone || '',
    recommended_help_level: d.recommended_help_level || '',
    key_concepts: Array.isArray(d.key_concepts) ? d.key_concepts : [],           // pass-through (no UI)
    common_mistakes: arrToLines(d.common_mistakes),
    probable_questions: Array.isArray(d.probable_questions) ? d.probable_questions : [], // pass-through (no UI)
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
    key_concepts: f.key_concepts || [],
    common_mistakes: linesToArr(f.common_mistakes),
    probable_questions: f.probable_questions || [],
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

  // Momentos de la clase (== lesson_blocks; el profesor NO ve block_id ni tiempos crudos).
  const [moments, setMoments] = useState([]);
  const [selectedMoment, setSelectedMoment] = useState(-1);
  const [editing, setEditing] = useState(null); // borrador de edición de UN momento
  const [savingMoment, setSavingMoment] = useState(false);

  // Transcripción
  const [transcript, setTranscript] = useState([]);
  const [job, setJob] = useState(null);
  const [correcting, setCorrecting] = useState(false);
  const [savingTranscript, setSavingTranscript] = useState(false);

  // IA
  const [quality, setQuality] = useState('balanced');
  const [aiBusy, setAiBusy] = useState(false);
  const [aiPhase, setAiPhase] = useState('');
  const [aiResult, setAiResult] = useState(null);
  const [form, setForm] = useState(null);
  const [accepting, setAccepting] = useState(false);
  const [accepted, setAccepted] = useState(false);
  const [probando, setProbando] = useState(false);
  const [testTimestamp, setTestTimestamp] = useState(null);
  const phaseTimer = useRef(null);

  // Video H5P + puente de tiempo (reutiliza el mismo bridge del Editor avanzado).
  const token = getMoodleToken();
  const isH5P = resource?.modname === 'hvp' || resource?.modname === 'h5pactivity';
  const [iframeLoading, setIframeLoading] = useState(true);
  const [revealFallback, setRevealFallback] = useState(false);
  const {
    currentTimestamp, duration, seek, play, pause, muted, setMuted,
    hideNativeControls, requestMeta, requestThumbnail,
  } = useResourceVideoBridge({ enabled: isH5P, resourceId: resource?.id ?? null, iframeName: IFRAME_NAME });
  const currentTime = currentTimestamp || 0;

  const meta = lesson?.metadata || {};
  const transcriptStatus = meta.transcript_status || (transcript.length ? 'generated' : 'missing');
  const hasTranscript = transcript.length > 0;

  const videoSrc = useMemo(() => buildMoodleViewUrl({
    token, cmid: resource?.id, modname: resource?.modname, extra: { hidefs: 1 },
  }), [resource?.id, resource?.modname, token]);

  // --- Carga: vínculo del recurso -> lección -> detalle + transcripción ---
  const reload = useCallback(async () => {
    if (!resource?.id) return;
    setLoading(true);
    try {
      const link = await getResourceLink(resource.id, courseId);
      const lId = link?.lesson_id || sectionContext?.lesson_id || '';
      setLessonId(lId);
      if (!lId) { setLesson(null); setTranscript([]); setMoments([]); return; }
      const [data, tr] = await Promise.all([
        getLesson(lId, courseId),
        getTranscript(courseId, lId).catch(() => ({ segments: [], job: null })),
      ]);
      setLesson(data);
      setMoments((data.blocks || []).map((b) => ({ ...b })));
      setTranscript(tr.segments || []);
      setJob(tr.job || null);
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

  // --- Video: pedir metadatos hasta tener duración; revelar cuando esté listo ---
  useEffect(() => {
    if (!isH5P || duration) return undefined;
    const iv = setInterval(() => requestMeta(), 1500);
    return () => clearInterval(iv);
  }, [isH5P, duration, requestMeta]);

  useEffect(() => {
    if (iframeLoading || duration) return undefined;
    const t = setTimeout(() => setRevealFallback(true), 12000);
    return () => clearTimeout(t);
  }, [iframeLoading, duration]);
  const videoReady = !iframeLoading && (Boolean(duration) || revealFallback);

  useEffect(() => {
    if (!isH5P || !videoReady) return undefined;
    hideNativeControls();
    const iv = setInterval(() => hideNativeControls(), 1500);
    return () => clearInterval(iv);
  }, [isH5P, videoReady, hideNativeControls]);

  // Momento activo según el tiempo del video (para resaltar la card correspondiente).
  const activeMoment = useMemo(() => {
    for (let i = 0; i < moments.length; i += 1) {
      const b = moments[i];
      if (Number(b.start_time) <= currentTime && currentTime < Number(b.end_time)) return i;
    }
    return -1;
  }, [moments, currentTime]);

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

  // --- Edición pedagógica de UN momento (guarda por /moments preservando tiempos) ---
  const openEditMoment = (idx) => {
    if (readOnly) return;
    const b = moments[idx];
    if (!b) return;
    setEditing({
      idx,
      block_title: b.block_title || '',
      summary: b.summary || '',
      tutor_focus: b.tutor_focus || '',
      concepts: arrToLines(b.concepts),
      preguntas_probables: arrToLines(b.preguntas_probables),
    });
  };

  const saveMoment = async () => {
    if (readOnly || !editing || !lessonId) return;
    setSavingMoment(true);
    // Aplica la edición al momento seleccionado y reenvía TODO el conjunto: el backend
    // exige que el conjunto de block_id coincida (rechaza altas/bajas encubiertas).
    const next = moments.map((b, i) => (i === editing.idx ? {
      ...b,
      block_title: editing.block_title,
      summary: editing.summary,
      tutor_focus: editing.tutor_focus,
      concepts: linesToArr(editing.concepts),
      preguntas_probables: linesToArr(editing.preguntas_probables),
    } : b));
    // Payload = solo campos pedagógicos permitidos por MomentPayload (extra="forbid").
    // NO se envían start_time/end_time/block_order: el profesor no toca tiempos/estructura.
    const payload = next.map((b) => ({
      block_id: b.block_id,
      block_title: b.block_title || '',
      summary: b.summary || '',
      interaction_mode: b.interaction_mode || '',   // se preserva el existente
      tutor_focus: b.tutor_focus || '',
      concepts: Array.isArray(b.concepts) ? b.concepts : linesToArr(b.concepts),
      preguntas_probables: Array.isArray(b.preguntas_probables) ? b.preguntas_probables : linesToArr(b.preguntas_probables),
    }));
    try {
      await updateMoments(courseId, lessonId, payload);
      setMoments(next);
      setEditing(null);
      showNotification('success', 'Momento actualizado.');
      await reload();
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setSavingMoment(false);
    }
  };

  const runAiPrepare = async () => {
    if (readOnly || !lessonId) return;
    setAiBusy(true);
    setAiResult(null);
    const phases = quality === 'max'
      ? ['Transcribiendo…', 'Analizando la clase…', 'Detectando momentos…', 'Generando la guía del tutor…', 'Revisando calidad…']
      : ['Transcribiendo…', 'Analizando la clase…', 'Detectando momentos…', 'Generando la guía del tutor…'];
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

  const testCtxBase = useMemo(() => activityContextFromMoodleModule(resource, sectionContext?.section, {
    courseId,
    moodleSectionId: sectionContext?.moodle_section_id,
    sectionName: sectionContext?.current_section_name,
    sectionOrder: sectionContext?.current_section_order,
    lessonId: lessonId || sectionContext?.lesson_id,
  }), [resource, sectionContext, courseId, lessonId]);
  // "Probar tutor desde aquí": inyecta el timestamp del momento elegido.
  const testCtx = useMemo(() => (
    testTimestamp != null ? { ...testCtxBase, current_timestamp: testTimestamp } : testCtxBase
  ), [testCtxBase, testTimestamp]);

  const probarDesdeMomento = (b) => {
    const t = Math.round(Number(b?.start_time) || 0);
    setTestTimestamp(t);
    if (isH5P) seek(t);
    setProbando(true);
  };

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

            {/* ============ PASO 1: CLASE Y RECURSOS ============ */}
            {step === 1 && (
              <>
                {/* Video + línea de tiempo + momentos */}
                <section className={cardCls}>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">1 · La clase en video</h4>
                    <span className="text-[11px] text-kenth-subtext">Mira la clase y revisa sus <b className="text-kenth-text">momentos</b>.</span>
                  </div>

                  {isH5P && videoSrc ? (
                    <>
                      <div className="relative w-full max-w-[820px] mx-auto rounded-xl overflow-hidden bg-black">
                        <div style={{ paddingTop: '56.25%' }} />
                        {!videoReady && (
                          <div className="absolute inset-0 z-10 flex items-center justify-center bg-kenth-bg text-indigo-400 text-xs uppercase tracking-widest">
                            Cargando video…
                          </div>
                        )}
                        <iframe
                          name={IFRAME_NAME}
                          onLoad={() => setIframeLoading(false)}
                          src={videoSrc}
                          className={`absolute top-0 left-0 w-full border-none bg-transparent transition-opacity duration-500 ${videoReady ? 'opacity-100' : 'opacity-0'}`}
                          style={{ height: 'calc(100% + 56px)' }}
                          allow="autoplay *; encrypted-media *"
                          scrolling="no"
                          title="Video de la clase"
                        />
                      </div>

                      {/* Transporte simple (sin controles técnicos) */}
                      <div className="flex items-center gap-2 flex-wrap">
                        <button onClick={() => play()} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/10 text-xs font-bold text-kenth-text hover:border-kenth-brightred/60">▶ Reproducir</button>
                        <button onClick={() => pause()} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/10 text-xs font-bold text-kenth-text hover:border-kenth-brightred/60">⏸ Pausa</button>
                        <button onClick={() => seek(Math.max(0, currentTime - 5))} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/5 text-[10px] font-black uppercase tracking-widest text-kenth-subtext hover:text-kenth-text">-5s</button>
                        <button onClick={() => seek(currentTime + 5)} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/5 text-[10px] font-black uppercase tracking-widest text-kenth-subtext hover:text-kenth-text">+5s</button>
                        <button onClick={() => setMuted(!muted)} className={`px-3 py-1.5 rounded-lg border text-[10px] font-black uppercase tracking-widest ${muted ? 'border-kenth-brightred/70 bg-kenth-brightred/15 text-kenth-brightred' : 'border-kenth-border bg-kenth-surface/5 text-kenth-subtext hover:text-kenth-text'}`}>{muted ? 'Activar sonido' : 'Silenciar'}</button>
                      </div>

                      {/* Línea de tiempo de momentos (solo lectura: el profesor no mueve tiempos) */}
                      <BlockTimeline
                        blocks={moments}
                        duration={duration}
                        currentTime={currentTime}
                        selectedIndex={selectedMoment}
                        onSelectBlock={(idx) => setSelectedMoment(idx)}
                        onSeek={(s) => seek(s)}
                        requestThumbnail={requestThumbnail}
                        transcript={transcript}
                        readOnly
                        title="Momentos de la clase"
                        unitLabel="momento"
                        itemPrefix="M"
                      />
                    </>
                  ) : isH5P ? (
                    <p className="text-sm text-kenth-subtext">Sesión expirada. Vuelve a iniciar sesión para ver el video.</p>
                  ) : (
                    <p className="text-sm text-kenth-subtext">Esta actividad ({resource?.modname}) no es un video H5P; el timeline y los momentos requieren un video H5P.</p>
                  )}
                </section>

                {/* Momentos de la clase (cards editables) */}
                <section className={cardCls}>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Momentos de la clase ({moments.length})</h4>
                  </div>
                  {moments.length === 0 ? (
                    <p className="text-[12px] text-kenth-subtext">
                      Esta lección aún no tiene momentos marcados sobre el video. Los momentos (con sus minutos)
                      se crean en el <b className="text-kenth-text">editor avanzado</b> (técnico); aquí podrás darles
                      título, resumen e intención pedagógica.
                    </p>
                  ) : (
                    <div className="flex flex-col gap-2">
                      {moments.map((b, idx) => (
                        <div
                          key={b.block_id || idx}
                          className={`border rounded-xl p-3 flex items-start gap-3 transition ${activeMoment === idx ? 'border-kenth-brightred/60 bg-kenth-brightred/5' : 'border-kenth-border/60 bg-kenth-surface/5'}`}
                        >
                          <div className="flex flex-col items-center gap-1 flex-shrink-0 pt-0.5">
                            <span className="text-[10px] font-black text-kenth-brightred">M{idx + 1}</span>
                            <button onClick={() => { setSelectedMoment(idx); if (isH5P) seek(Number(b.start_time) || 0); }}
                              className="text-[10px] font-mono text-kenth-subtext hover:text-kenth-text" title="Ir a este momento">
                              {momentRange(b)}
                            </button>
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold text-kenth-text truncate">{b.block_title || `Momento ${idx + 1}`}</p>
                            {b.summary && <p className="text-[11px] text-kenth-subtext line-clamp-2">{b.summary}</p>}
                          </div>
                          <div className="flex flex-col gap-1 flex-shrink-0">
                            {!readOnly && (
                              <button onClick={() => openEditMoment(idx)} className="px-2.5 py-1 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60">Editar</button>
                            )}
                            <button onClick={() => probarDesdeMomento(b)} className="px-2.5 py-1 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-subtext hover:text-kenth-text">Probar aquí</button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </section>

                {/* Transcripción */}
                <section className={cardCls}>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Transcripción de la clase</h4>
                    <TranscriptChip status={transcriptStatus} count={transcript.length} />
                  </div>
                  <p className="text-[12px] text-kenth-subtext">
                    La IA necesita la transcripción del video para analizar la clase. El modelo no escucha audio: transcribimos primero y luego analiza el texto.
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

                {/* Recursos (sin jerga técnica para el profesor) */}
                <section className={cardCls}>
                  <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Recursos de la lección</h4>
                  <LessonResourcesPanel courseId={courseId} lessonId={lessonId} technical={false} />
                </section>

                {/* Probar tutor (con el momento elegido, si se pulsó "Probar aquí") */}
                {probando && (
                  <section className={cardCls}>
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Probar tutor</h4>
                      <button onClick={() => setProbando(false)} className="px-3 py-1.5 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60">Cerrar prueba</button>
                    </div>
                    <TutorAssistCard variant="lesson" titulo={`Prueba · ${resource?.name || ''}`} contexto={`Lección: ${resource?.name}.`}
                      activityContext={testCtx} proactiveMessage={lesson?.proactive_message || ''} suggestedPrompts={lesson?.suggested_prompts || []} />
                  </section>
                )}

                <div className="flex justify-end">
                  <button onClick={() => setStep(2)} disabled={!hasTranscript}
                    className="px-5 py-2.5 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40 transition">
                    Siguiente: Preparación con IA →
                  </button>
                </div>
                {!hasTranscript && <p className="text-[11px] text-amber-300/80 text-right">Transcribe el video para continuar.</p>}
              </>
            )}

            {/* ============ PASO 2: PREPARACIÓN CON IA ============ */}
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
                        {aiResult.models?.review_model && <StatusChip tone="info">Revisado</StatusChip>}
                      </div>
                      <ResumeLine label="Objetivo" value={aiResult.draft.learning_goal} />
                      <ResumeLine label="Resumen" value={aiResult.draft.lesson_summary} />
                      <ResumeLine label="Momentos detectados" value={`${(aiResult.draft.moments || []).length}`} />
                      {(aiResult.draft.terms_to_review || []).length > 0 && (
                        <ResumeLine label="Términos dudosos" value={(aiResult.draft.terms_to_review || []).join(', ')} tone="warn" />
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

            {/* ============ PASO 3: REVISIÓN Y PRUEBA ============ */}
            {step === 3 && (
              !form ? (
                <section className={cardCls}>
                  <p className="text-sm text-kenth-subtext">Aún no hay borrador. Genera uno en el paso 2.</p>
                  <button onClick={() => setStep(2)} className="self-start px-4 py-2 rounded-xl bg-kenth-brightred text-white text-xs font-black uppercase tracking-widest">Ir a Preparación con IA</button>
                </section>
              ) : (
                <>
                  <Accordion title="Lo esencial" defaultOpen>
                    <div>
                      <label className={labelCls}>Objetivo de aprendizaje</label>
                      <textarea rows={2} disabled={readOnly} className={inputCls} value={form.learning_goal} onChange={(e) => setF('learning_goal', e.target.value)} />
                    </div>
                    <div>
                      <label className={labelCls}>Resumen de la clase</label>
                      <textarea rows={3} disabled={readOnly} className={inputCls} value={form.lesson_summary} onChange={(e) => setF('lesson_summary', e.target.value)} />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className={labelCls}>Estilo del tutor (tono)</label>
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
                  </Accordion>

                  <Accordion title="Preguntas y errores">
                    <div>
                      <label className={labelCls}>Errores comunes a vigilar (uno por línea)</label>
                      <textarea rows={3} disabled={readOnly} className={inputCls} value={form.common_mistakes} onChange={(e) => setF('common_mistakes', e.target.value)} />
                    </div>
                    {/* Las preguntas probables se editan POR MOMENTO (paso 1); aquí solo recap. */}
                    {form.moments.some((m) => (m.probable_questions || '').trim()) && (
                      <div>
                        <label className={labelCls}>Preguntas probables por momento (resumen)</label>
                        <ul className="mt-1 flex flex-col gap-1">
                          {form.moments.map((m, i) => (m.probable_questions || '').trim() && (
                            <li key={i} className="text-[12px] text-kenth-subtext">
                              <span className="text-kenth-text font-bold">{m.title || `Momento ${i + 1}`}: </span>
                              {(m.probable_questions || '').split('\n').filter(Boolean).join(' · ')}
                            </li>
                          ))}
                        </ul>
                        <p className="text-[10px] text-kenth-subtext mt-1">Para editarlas, ve al paso 1 y abre el momento.</p>
                      </div>
                    )}
                  </Accordion>

                  <Accordion title="Opciones del tutor">
                    <div>
                      <label className={labelCls}>Reglas importantes (una por línea)</label>
                      <textarea rows={2} disabled={readOnly} className={inputCls} value={form.lesson_rules} onChange={(e) => setF('lesson_rules', e.target.value)} />
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
                  </Accordion>

                  {form.moments.length > 0 && (
                    <Accordion title={`Momentos de la clase (${form.moments.length})`}>
                      <div className="flex flex-col gap-2">
                        {form.moments.map((m, idx) => (
                          <div key={idx} className="border border-kenth-border/60 rounded-xl p-3 bg-kenth-surface/5">
                            <p className="text-sm font-bold text-kenth-text">{m.title || `Momento ${idx + 1}`}</p>
                            {m.summary && <p className="text-[11px] text-kenth-subtext line-clamp-2">{m.summary}</p>}
                            {m.pedagogical_intent && <p className="text-[11px] text-kenth-subtext mt-0.5"><span className={labelCls}>Intención: </span>{m.pedagogical_intent}</p>}
                          </div>
                        ))}
                      </div>
                      <p className="text-[10px] text-kenth-subtext">Edita título/resumen/intención de cada momento en el paso 1.</p>
                    </Accordion>
                  )}

                  <Accordion title="Transcripción">
                    <p className="text-[12px] text-kenth-subtext">
                      {hasTranscript ? `Transcripción con ${transcript.length} segmentos.` : 'Sin transcripción.'} Corrígela en el paso 1.
                    </p>
                  </Accordion>

                  <section className={cardCls}>
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Probar tutor</h4>
                      <button onClick={() => setProbando((v) => !v)} className="px-3 py-1.5 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60">
                        {probando ? 'Cerrar prueba' : 'Abrir tutor'}
                      </button>
                    </div>
                    <p className="text-[11px] text-kenth-subtext">Acepta el borrador para que el tutor use esta configuración; los cambios de comportamiento se aplican al instante (sin reindexar).</p>
                    {probando && (
                      <TutorAssistCard variant="lesson" titulo={`Prueba · ${resource?.name || ''}`} contexto={`Lección: ${resource?.name}.`}
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

      {/* Modal de edición de UN momento (campos pedagógicos; nunca tiempos/estructura) */}
      {editing && (
        <div className="fixed inset-0 z-[210] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => !savingMoment && setEditing(null)}>
          <div className="w-full max-w-lg bg-kenth-card border border-kenth-border rounded-2xl shadow-2xl p-5 flex flex-col gap-3 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between">
              <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Editar momento · {momentRange(moments[editing.idx])}</p>
              <button onClick={() => !savingMoment && setEditing(null)} className="text-kenth-subtext hover:text-kenth-text">✕</button>
            </div>
            <div>
              <label className={labelCls}>Título</label>
              <input className={inputCls} value={editing.block_title} onChange={(e) => setEditing((p) => ({ ...p, block_title: e.target.value }))} placeholder="Título del momento" />
            </div>
            <div>
              <label className={labelCls}>Resumen (qué pasa en esta parte)</label>
              <textarea rows={2} className={inputCls} value={editing.summary} onChange={(e) => setEditing((p) => ({ ...p, summary: e.target.value }))} />
            </div>
            <div>
              <label className={labelCls}>Intención del tutor (qué reforzar aquí)</label>
              <input className={inputCls} value={editing.tutor_focus} onChange={(e) => setEditing((p) => ({ ...p, tutor_focus: e.target.value }))} />
            </div>
            <div>
              <label className={labelCls}>Conceptos clave (uno por línea)</label>
              <textarea rows={2} className={inputCls} value={editing.concepts} onChange={(e) => setEditing((p) => ({ ...p, concepts: e.target.value }))} />
            </div>
            <div>
              <label className={labelCls}>Preguntas probables (una por línea)</label>
              <textarea rows={2} className={inputCls} value={editing.preguntas_probables} onChange={(e) => setEditing((p) => ({ ...p, preguntas_probables: e.target.value }))} />
            </div>
            <div className="flex justify-end gap-2 pt-1">
              <button onClick={() => setEditing(null)} disabled={savingMoment} className="px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-text text-xs font-bold uppercase tracking-widest disabled:opacity-40">Cancelar</button>
              <button onClick={saveMoment} disabled={savingMoment} className="px-5 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                {savingMoment ? 'Guardando…' : 'Guardar momento'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Accordion({ title, defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <section className="bg-kenth-card border border-kenth-border rounded-2xl overflow-hidden">
      <button onClick={() => setOpen((v) => !v)} className="w-full flex items-center justify-between px-5 py-3 text-left">
        <span className="text-sm font-black uppercase italic text-kenth-text tracking-tight">{title}</span>
        <span className={`text-kenth-subtext transition-transform ${open ? 'rotate-180' : ''}`}>▾</span>
      </button>
      {open && <div className="px-5 pb-5 flex flex-col gap-4 border-t border-kenth-border/50 pt-4">{children}</div>}
    </section>
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
