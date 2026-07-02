import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  getResourceLink, getLesson, getTranscript, getTranscriptStatus,
  autoTranscribe, replaceTranscript, aiPrepare,
  replaceLessonBlocks, mergeDraftMomentsIntoBlocks,
  savePedagogy, toTutorProfile,
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
 * Edita el PERFIL PEDAGÓGICO CANÓNICO (el MISMO modelo que el Editor Avanzado y la
 * IA; ver services/pedagogy_profile.py + sectionsService.toTutorProfile). La única
 * diferencia con el admin es la presentación: aquí es una revisión simple, no una
 * pared de campos.
 *
 *   Paso 1 · Clase y recursos  -> VIDEO + línea de tiempo VISUAL (sin editar momentos)
 *                                 + transcripción + recursos
 *   Paso 2 · Preparación con IA -> generar borrador (rellena el mismo perfil)
 *   Paso 3 · Revisión y prueba  -> tarjetas resumidas; se editan SOLO al pulsar "Editar"
 *
 * Guarda el perfil con savePedagogy (PUT /pedagogy = apply_profile) y los momentos
 * (bloques) con replaceLessonBlocks (PUT /blocks): el profesor edita la línea de
 * tiempo igual que el admin (arrastrar tiempos, crear/borrar, fijar el "tipo de
 * momento"). No ve block_id crudo, JSON, metadata, Chroma ni estado técnico.
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
const TONE_LABEL = Object.fromEntries(TONE_OPTIONS.map((o) => [o.value, o.label]));
const HELP_LABEL = Object.fromEntries(HELP_OPTIONS.map((o) => [o.value, o.label]));
const QUALITY_OPTIONS = [
  { value: 'fast', label: 'Rápido', hint: 'Borrador veloz.' },
  { value: 'balanced', label: 'Equilibrado', hint: 'Recomendado.' },
  { value: 'max', label: 'Máximo', hint: 'Añade revisión de calidad (más lento).' },
];
const GLOSARIO = ['headroom', 'gain staging', 'LUFS', 'threshold', 'sidechain', 'fase', 'compresión paralela', 'ecualización', 'masterización'];

// "Tipo de momento" = interaction_mode, con etiquetas simples para el profesor.
// El valor es el mismo enum del backend (InteractionMode / MODOS_PEDAGOGICOS).
const MODE_OPTIONS = [
  { value: '', label: 'Sin definir' },
  { value: 'teoria', label: 'Teoría / explicación' },
  { value: 'practica', label: 'Práctica / demostración' },
  { value: 'criterio_operativo', label: 'Criterio / decisión' },
  { value: 'troubleshooting', label: 'Diagnóstico / resolución' },
  { value: 'revision', label: 'Verificación / repaso' },
  { value: 'navegacion_de_recurso', label: 'Recorrido del recurso' },
];
const MODE_LABEL = Object.fromEntries(MODE_OPTIONS.map((o) => [o.value, o.label]));
// Punto de color por tipo (mismas familias que BlockTimeline) para la leyenda.
const MODE_DOT = {
  teoria: 'bg-indigo-400', practica: 'bg-emerald-400', criterio_operativo: 'bg-amber-400',
  troubleshooting: 'bg-rose-400', revision: 'bg-violet-400', navegacion_de_recurso: 'bg-sky-400',
};
const colorDotForMode = (mode) => MODE_DOT[(mode || '').trim().toLowerCase()] || 'bg-kenth-brightred';

const linesToArr = (s) => (s || '').split('\n').map((x) => x.trim()).filter(Boolean);
const arrToLines = (a) => (Array.isArray(a) ? a.join('\n') : (a || ''));

const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none disabled:opacity-60 disabled:cursor-not-allowed';
const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';
const cardCls = 'bg-kenth-card border border-kenth-border rounded-2xl p-5 flex flex-col gap-4';

const momentRange = (b) => `${fmtTime(Number(b?.start_time) || 0)}–${fmtTime(Number(b?.end_time) || 0)}`;

// Overlay del borrador IA sobre el perfil canónico (solo pisa lo NO vacío). Los
// momentos NO se tratan aquí: van por `blocks` (mergeDraftMomentsIntoBlocks).
function overlayDraft(profile, d = {}) {
  const merged = { ...profile };
  const set = (k, v) => { if (v && (!Array.isArray(v) || v.length)) merged[k] = v; };
  set('learning_goal', d.learning_goal);
  set('lesson_summary', d.lesson_summary);
  set('tutor_tone', d.recommended_tone);
  set('help_level', d.recommended_help_level);
  set('lesson_rules', d.lesson_rules);
  set('key_concepts', d.key_concepts);
  set('common_mistakes', d.common_mistakes);
  set('probable_questions', d.probable_questions);
  set('tutor_focus', d.tutor_focus);
  set('tutor_must_not_do', d.tutor_must_not_do);
  set('proactive_message', d.proactive_message);
  set('suggested_prompts', d.suggested_prompts);
  return merged;
}

// Un "momento" es un bloque del video, con etiqueta amable. El profesor edita el
// mismo objeto `blocks` que persiste el admin, así puede mover tiempos y tipo.
const blockToMoment = (b, idx) => ({
  block_id: b.block_id,
  order: idx,
  title: b.block_title || '',
  summary: b.summary || '',
  pedagogical_intent: b.tutor_focus || '',
  interaction_mode: b.interaction_mode || '',
  key_concepts: Array.isArray(b.concepts) ? b.concepts : linesToArr(b.concepts),
  common_mistakes: Array.isArray((b.metadata || {}).common_mistakes) ? b.metadata.common_mistakes : [],
  probable_questions: Array.isArray(b.preguntas_probables) ? b.preguntas_probables : linesToArr(b.preguntas_probables),
  start_time: b.start_time,
  end_time: b.end_time,
});

// Payload de bloques para PUT /blocks (estructura completa: tiempos + modo + pedagogía).
const blocksPayload = (blocks) => (blocks || []).map((b, i) => ({
  block_id: b.block_id || '',
  block_order: i,
  start_time: Number(b.start_time) || 0,
  end_time: Number(b.end_time) || 0,
  block_title: b.block_title || '',
  summary: b.summary || '',
  interaction_mode: b.interaction_mode || '',
  tutor_focus: b.tutor_focus || '',
  concepts: Array.isArray(b.concepts) ? b.concepts : linesToArr(b.concepts),
  preguntas_probables: Array.isArray(b.preguntas_probables) ? b.preguntas_probables : linesToArr(b.preguntas_probables),
  metadata: b.metadata || {},
}));

export default function TutorPedagogyView({ resource, courseId, sectionContext = null, onClose, readOnly = false }) {
  const [step, setStep] = useState(1);
  const [lessonId, setLessonId] = useState('');
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);

  // Perfil canónico (nivel lección) + bloques (momentos, con tiempos y tipo).
  const [profile, setProfile] = useState(null);
  const [blocks, setBlocks] = useState([]);
  const [blocksDirty, setBlocksDirty] = useState(false); // hay cambios de momentos sin guardar
  const [selectedMoment, setSelectedMoment] = useState(-1);
  const [editing, setEditing] = useState(null); // edición de UN momento (modal)
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  // Muta la lista de bloques y marca cambios sin guardar.
  const mutateBlocks = useCallback((fn) => {
    setBlocks((prev) => fn(prev));
    setBlocksDirty(true);
    setSaved(false);
  }, []);

  // Transcripción
  const [transcript, setTranscript] = useState([]);
  const [job, setJob] = useState(null);
  const [correcting, setCorrecting] = useState(false);
  const [savingTranscript, setSavingTranscript] = useState(false);

  // IA
  const [quality, setQuality] = useState('balanced');
  const [retranscribe, setRetranscribe] = useState(false); // rehacer transcripción aunque exista
  const [aiBusy, setAiBusy] = useState(false);
  const [aiPhase, setAiPhase] = useState('');
  const [aiResult, setAiResult] = useState(null);
  const [probando, setProbando] = useState(false);
  const phaseTimer = useRef(null);

  // Video H5P
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

  const reload = useCallback(async () => {
    if (!resource?.id) return;
    setLoading(true);
    try {
      const link = await getResourceLink(resource.id, courseId);
      const lId = link?.lesson_id || sectionContext?.lesson_id || '';
      setLessonId(lId);
      if (!lId) { setLesson(null); setTranscript([]); setBlocks([]); setProfile(null); return; }
      const [data, tr] = await Promise.all([
        getLesson(lId, courseId),
        getTranscript(courseId, lId).catch(() => ({ segments: [], job: null })),
      ]);
      setLesson(data);
      setProfile(toTutorProfile(data));
      setBlocks((data.blocks || []).map((b) => ({ ...b })));
      setBlocksDirty(false);
      setTranscript(tr.segments || []);
      setJob(tr.job || null);
      setSaved((data.metadata || {}).ai_prepare_status === 'accepted');
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
  }, [resource?.id, courseId, sectionContext?.lesson_id]);

  useEffect(() => { reload(); }, [reload]);

  useEffect(() => () => { if (phaseTimer.current) clearInterval(phaseTimer.current); }, []);

  // Video: metadatos + reveal
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

  // Espera activa (await) a que termine un job de transcripción; devuelve los segmentos.
  // La usa el paso 2: "Generar borrador" transcribe primero y luego analiza.
  const waitForTranscription = async () => {
    for (;;) {
      await new Promise((r) => setTimeout(r, 3000));
      const data = await getTranscriptStatus(courseId, lessonId);
      const st = data.job;
      setJob(st || null);
      if (!st || st.status === 'done') break;
      if (st.status === 'error') throw new Error(st.error || 'Falló la transcripción del video.');
    }
    const tr = await getTranscript(courseId, lessonId);
    return tr.segments || [];
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

  // Momentos derivados de los bloques (para la lista + timeline + modal).
  const moments = useMemo(() => blocks.map(blockToMoment), [blocks]);

  // --- Edición de UN momento (modal) sobre `blocks` (local; persiste al Guardar) ---
  const openEditMoment = (idx) => {
    if (readOnly) return;
    const b = blocks[idx];
    if (!b) return;
    setEditing({
      idx,
      title: b.block_title || '',
      summary: b.summary || '',
      pedagogical_intent: b.tutor_focus || '',
      interaction_mode: b.interaction_mode || '',
      start_time: Math.round(Number(b.start_time) || 0),
      end_time: Math.round(Number(b.end_time) || 0),
      key_concepts: arrToLines(Array.isArray(b.concepts) ? b.concepts : linesToArr(b.concepts)),
      common_mistakes: arrToLines((b.metadata || {}).common_mistakes),
      probable_questions: arrToLines(Array.isArray(b.preguntas_probables) ? b.preguntas_probables : linesToArr(b.preguntas_probables)),
    });
  };

  const saveMoment = () => {
    if (readOnly || !editing) return;
    const e = editing;
    const st = Math.max(0, Math.round(Number(e.start_time) || 0));
    const et = Math.max(st + 1, Math.round(Number(e.end_time) || 0));
    mutateBlocks((prev) => prev.map((b, i) => (i === e.idx ? {
      ...b,
      block_title: e.title,
      summary: e.summary,
      tutor_focus: e.pedagogical_intent,
      interaction_mode: e.interaction_mode || '',
      start_time: st,
      end_time: et,
      concepts: linesToArr(e.key_concepts),
      preguntas_probables: linesToArr(e.probable_questions),
      metadata: { ...(b.metadata || {}), common_mistakes: linesToArr(e.common_mistakes) },
    } : b)));
    setEditing(null);
  };

  // Añadir un momento en el tiempo actual del video (bloque nuevo). Como el admin.
  const addMoment = () => {
    if (readOnly) return;
    const start = Math.round(currentTime);
    const end = duration ? Math.min(start + 30, Math.floor(duration)) : start + 30;
    mutateBlocks((prev) => {
      const next = [...prev, {
        block_id: `${lessonId}-B${prev.length + 1}`,
        block_order: prev.length,
        start_time: start,
        end_time: Math.max(start + 1, end),
        block_title: '', summary: '', interaction_mode: '', tutor_focus: '',
        concepts: [], preguntas_probables: [], metadata: {},
      }];
      next.sort((a, b) => (Number(a.start_time) || 0) - (Number(b.start_time) || 0));
      return next.map((b, i) => ({ ...b, block_order: i }));
    });
  };

  const removeMoment = (idx) => {
    if (readOnly) return;
    mutateBlocks((prev) => prev.filter((_, i) => i !== idx).map((b, i) => ({ ...b, block_order: i })));
    setEditing(null);
  };

  // Arrastre de tiempos en la línea de tiempo (idéntico al admin).
  const changeBlockTime = useCallback((idx, patch) => {
    mutateBlocks((prev) => {
      const next = [...prev];
      const b = { ...next[idx] };
      if (patch.start_time != null) b.start_time = Math.round(patch.start_time);
      if (patch.end_time != null) b.end_time = Math.round(patch.end_time);
      next[idx] = b;
      return next;
    });
  }, [mutateBlocks]);

  // Paso 2: un solo botón. Transcribe el video (si hace falta) y luego genera el borrador.
  const runAiPrepare = async () => {
    if (readOnly || !lessonId) return;
    setAiBusy(true);
    setAiResult(null);
    try {
      // 1) Transcripción: si no existe (o el profesor pide rehacerla), la generamos aquí.
      const needsTx = retranscribe || !hasTranscript;
      if (needsTx) {
        if (!resource?.id) throw new Error('Esta clase no tiene un video asociado para transcribir.');
        setAiPhase('Transcribiendo el video…');
        const started = await autoTranscribe(courseId, lessonId, { resource_id: Number(resource.id) });
        setJob(started.job || { status: 'running', progress: 0 });
        const segs = await waitForTranscription();
        setTranscript(segs);
        setJob(null);
      }
      // 2) Análisis + generación del borrador pedagógico (temporizador visual de fases).
      const phases = quality === 'max'
        ? ['Analizando la clase…', 'Detectando momentos…', 'Generando la guía del tutor…', 'Revisando calidad…']
        : ['Analizando la clase…', 'Detectando momentos…', 'Generando la guía del tutor…'];
      let i = 0;
      setAiPhase(phases[0]);
      phaseTimer.current = setInterval(() => { i = Math.min(i + 1, phases.length - 1); setAiPhase(phases[i]); }, 4000);
      const res = await aiPrepare(courseId, lessonId, { mode: 'draft', quality });
      if (phaseTimer.current) { clearInterval(phaseTimer.current); phaseTimer.current = null; }
      setAiResult(res);
      setProfile((p) => overlayDraft(p || toTutorProfile(lesson || {}), res.draft));
      // Momentos: la IA propone la segmentación con tiempos y tipo -> reconstruye la
      // línea de tiempo (distribuida, no apilada). Se guarda con el resto al aplicar.
      setBlocks((prev) => mergeDraftMomentsIntoBlocks(prev, res.draft?.moments || [], lessonId));
      setBlocksDirty(true);
      setRetranscribe(false);
      setSaved(false);
      showNotification('success', 'Borrador del tutor generado. Revísalo y guárdalo.');
      setStep(3);
    } catch (e) {
      showNotification('error', e.message || 'No se pudo preparar el tutor.');
    } finally {
      if (phaseTimer.current) { clearInterval(phaseTimer.current); phaseTimer.current = null; }
      setAiPhase('');
      setAiBusy(false);
      setJob(null);
    }
  };

  const setP = (k, v) => { if (!readOnly) setProfile((p) => ({ ...p, [k]: v })); };

  // Guardar TODO: perfil canónico (nivel lección) + momentos/bloques (tiempos + tipo).
  const saveProfile = async () => {
    if (readOnly || !lessonId || !profile) return;
    setSaving(true);
    try {
      await savePedagogy(courseId, lessonId, profile);
      // Momentos = bloques del video (PUT /blocks), igual que el admin: persiste
      // tiempos, tipo y pedagogía. Solo si hubo cambios en la línea de tiempo.
      if (blocksDirty) {
        await replaceLessonBlocks(courseId, lessonId, blocksPayload(blocks));
      }
      setSaved(true);
      setBlocksDirty(false);
      showNotification('success', 'Tutor actualizado.');
      await reload();
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setSaving(false);
    }
  };

  const testCtx = useMemo(() => activityContextFromMoodleModule(resource, sectionContext?.section, {
    courseId,
    moodleSectionId: sectionContext?.moodle_section_id,
    sectionName: sectionContext?.current_section_name,
    sectionOrder: sectionContext?.current_section_order,
    lessonId: lessonId || sectionContext?.lesson_id,
  }), [resource, sectionContext, courseId, lessonId]);

  const handleClose = () => onClose?.(saved);

  const STEPS = [
    { n: 1, label: 'Recursos' },
    { n: 2, label: 'Preparación con IA' },
    { n: 3, label: 'Revisión y prueba' },
  ];

  // Video H5P reutilizable (se muestra en el paso 3). Extraído para no duplicar markup.
  const videoPanel = isH5P && videoSrc ? (
    <>
      <div className="relative w-full rounded-xl overflow-hidden bg-black">
        <div style={{ paddingTop: '56.25%' }} />
        {!videoReady && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-kenth-bg text-indigo-400 text-xs uppercase tracking-widest">Cargando video…</div>
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
      <div className="flex items-center gap-2 flex-wrap">
        <button onClick={() => play()} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/10 text-xs font-bold text-kenth-text hover:border-kenth-brightred/60">▶ Reproducir</button>
        <button onClick={() => pause()} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/10 text-xs font-bold text-kenth-text hover:border-kenth-brightred/60">⏸ Pausa</button>
        <button onClick={() => seek(Math.max(0, currentTime - 5))} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/5 text-[10px] font-black uppercase tracking-widest text-kenth-subtext hover:text-kenth-text">-5s</button>
        <button onClick={() => seek(currentTime + 5)} className="px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/5 text-[10px] font-black uppercase tracking-widest text-kenth-subtext hover:text-kenth-text">+5s</button>
        <button onClick={() => setMuted(!muted)} className={`px-3 py-1.5 rounded-lg border text-[10px] font-black uppercase tracking-widest ${muted ? 'border-kenth-brightred/70 bg-kenth-brightred/15 text-kenth-brightred' : 'border-kenth-border bg-kenth-surface/5 text-kenth-subtext hover:text-kenth-text'}`}>{muted ? 'Activar sonido' : 'Silenciar'}</button>
        {!readOnly && (
          <button onClick={addMoment} className="ml-auto px-3 py-1.5 rounded-lg border border-kenth-brightred/50 bg-kenth-brightred/10 text-[10px] font-black uppercase tracking-widest text-kenth-brightred hover:bg-kenth-brightred/20">
            + Momento en {fmtTime(currentTime)}
          </button>
        )}
      </div>
      {/* Línea de tiempo EDITABLE (como el admin): arrastra los bordes para mover
          los tiempos de cada momento; el color = tipo de momento. */}
      <BlockTimeline
        blocks={blocks}
        duration={duration}
        currentTime={currentTime}
        selectedIndex={selectedMoment}
        onSelectBlock={(idx) => setSelectedMoment(idx)}
        onSeek={(s) => seek(s)}
        onChangeBlockTime={readOnly ? undefined : changeBlockTime}
        requestThumbnail={requestThumbnail}
        transcript={transcript}
        readOnly={readOnly}
        title="Momentos de la clase"
        unitLabel="momento"
        itemPrefix="M"
      />
      {/* Leyenda de colores por tipo de momento. */}
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {MODE_OPTIONS.filter((o) => o.value).map((o) => (
          <span key={o.value} className="inline-flex items-center gap-1 text-[10px] text-kenth-subtext">
            <span className={`inline-block h-2 w-2 rounded-sm ${colorDotForMode(o.value)}`} />
            {o.label}
          </span>
        ))}
      </div>
      {!readOnly && (
        <p className="text-[10px] text-kenth-subtext">Arrastra los bordes de un momento en la línea de tiempo para ajustar su inicio y fin. Pulsa <b className="text-kenth-text">Revisar</b> para editar su contenido y tipo.</p>
      )}
    </>
  ) : isH5P ? (
    <p className="text-sm text-kenth-subtext">Sesión expirada. Vuelve a iniciar sesión para ver el video.</p>
  ) : (
    <p className="text-sm text-kenth-subtext">Esta actividad ({resource?.modname}) no es un video H5P; el timeline requiere un video H5P.</p>
  );

  const p = profile || {};

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
          {saved && <StatusChip tone="ok">Tutor configurado</StatusChip>}
          <button onClick={handleClose} className="text-kenth-subtext hover:text-kenth-text" title="Cerrar">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
      </div>

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

      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        {loading ? (
          <p className="text-sm text-kenth-subtext">Cargando…</p>
        ) : !lessonId ? (
          <div className="max-w-xl mx-auto text-center mt-16">
            <p className="text-kenth-text font-bold">Esta actividad todavía no es una lección del tutor.</p>
            <p className="text-sm text-kenth-subtext mt-2">El tutor se prepara sobre las clases en video (H5P). Abre una clase en video para configurarlo.</p>
          </div>
        ) : (
          <div className="w-full flex flex-col gap-4">
            {readOnly && (
              <div className="max-w-3xl mx-auto w-full rounded-2xl border border-kenth-border bg-kenth-surface/5 px-5 py-3 text-sm text-kenth-subtext">
                Estás en <b className="text-kenth-text">modo solo lectura</b>. Puedes ver la preparación y probar el tutor, pero no editar ni guardar.
              </div>
            )}

            {/* ============ PASO 1 · SOLO RECURSOS ============ */}
            {step === 1 && (
              <div className="max-w-3xl mx-auto w-full flex flex-col gap-4">
                <section className={cardCls}>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">1 · Recursos de la clase</h4>
                    <span className="text-[11px] text-kenth-subtext">Sube el material; el video se prepara en el paso 2.</span>
                  </div>
                  <p className="text-[12px] text-kenth-subtext">
                    Material de esta lección: imágenes, plantillas (.flp/.als), audios, PDF.{' '}
                    <b className="text-kenth-text">Indexar</b> = el tutor lo conoce · <b className="text-kenth-text">Visible</b> = el alumno lo ve/descarga.
                  </p>
                  <LessonResourcesPanel courseId={courseId} lessonId={lessonId} technical={false} />
                </section>

                <div className="flex justify-end">
                  <button onClick={() => setStep(2)}
                    className="px-5 py-2.5 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest transition">
                    Siguiente: Preparación con IA →
                  </button>
                </div>
              </div>
            )}

            {/* ============ PASO 2 · TRANSCRIBE + GENERA BORRADOR ============ */}
            {step === 2 && (
              <div className="max-w-3xl mx-auto w-full flex flex-col gap-4">
                <section className={cardCls}>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">2 · Genera el borrador del tutor</h4>
                    <TranscriptChip status={transcriptStatus} count={transcript.length} />
                  </div>
                  <p className="text-[12px] text-kenth-subtext">
                    Al pulsar <b className="text-kenth-text">Generar borrador</b>, la IA transcribe el video (si aún no lo está) y luego
                    propone objetivo, resumen, momentos, conceptos, errores comunes, preguntas probables, reglas y mensajes al alumno.
                    Es un borrador: tú lo revisas y decides.
                  </p>
                  <div>
                    <label className={labelCls}>Calidad</label>
                    <div className="grid grid-cols-3 gap-2 mt-1">
                      {QUALITY_OPTIONS.map((q) => (
                        <button key={q.value} onClick={() => setQuality(q.value)} disabled={readOnly || aiBusy}
                          className={`rounded-xl border px-3 py-2 text-left transition ${quality === q.value ? 'border-kenth-brightred bg-kenth-brightred/10' : 'border-kenth-border bg-kenth-surface/5 hover:border-kenth-brightred/40'} disabled:opacity-40`}>
                          <div className="text-xs font-black uppercase tracking-widest text-kenth-text">{q.label}</div>
                          <div className="text-[10px] text-kenth-subtext mt-0.5">{q.hint}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                  {hasTranscript && !aiBusy && (
                    <label className="flex items-center gap-2 text-[11px] text-kenth-subtext cursor-pointer">
                      <input type="checkbox" checked={retranscribe} disabled={readOnly} onChange={(e) => setRetranscribe(e.target.checked)} className="accent-kenth-brightred" />
                      Rehacer la transcripción del video (ya existe una; por defecto se reutiliza).
                    </label>
                  )}
                  {aiBusy ? (
                    <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/10 p-4 flex flex-col gap-2">
                      <div className="flex items-center gap-3">
                        <span className="inline-block h-4 w-4 rounded-full border-2 border-indigo-300 border-t-transparent animate-spin" />
                        <span className="text-sm text-indigo-100">{aiPhase || 'Preparando…'}</span>
                      </div>
                      {job?.status === 'running' && (
                        <div>
                          <div className="flex items-center justify-between text-[10px] text-indigo-200 mb-1">
                            <span>{job.segments || 0} segmentos</span>
                            <span>{Math.round((job.progress || 0) * 100)}%</span>
                          </div>
                          <div className="h-1.5 rounded-full bg-indigo-900/40 overflow-hidden">
                            <div className="h-full bg-indigo-400 transition-all" style={{ width: `${Math.round((job.progress || 0) * 100)}%` }} />
                          </div>
                        </div>
                      )}
                      <p className="text-[10px] text-indigo-200/70">Transcribir un video puede tardar varios minutos. No cierres esta ventana.</p>
                    </div>
                  ) : (
                    <button onClick={runAiPrepare} disabled={readOnly}
                      className="self-start px-5 py-3 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-sm font-black uppercase tracking-widest disabled:opacity-40">
                      Generar borrador del tutor
                    </button>
                  )}
                  {aiResult?.draft && !aiBusy && (
                    <div className="border-t border-kenth-border/50 pt-3 flex flex-col gap-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <StatusChip tone="ok">Borrador listo</StatusChip>
                        <ConfidenceChip value={aiResult.draft.confidence} />
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
                  <button onClick={() => setStep(1)} disabled={aiBusy} className="px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-subtext text-xs font-black uppercase tracking-widest hover:text-kenth-text disabled:opacity-40">← Atrás</button>
                </div>
              </div>
            )}

            {/* ============ PASO 3 · VIDEO (izq.) + REVISIÓN (der.) ============ */}
            {step === 3 && !profile ? (
              <section className={`${cardCls} max-w-3xl mx-auto w-full`}><p className="text-sm text-kenth-subtext">Cargando…</p></section>
            ) : step === 3 && (
              <div className="max-w-6xl mx-auto w-full flex flex-col gap-4">
                <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_minmax(0,440px)] gap-4 items-start">
                {/* IZQUIERDA: video + línea de tiempo (momentos) + subtítulos + corrección */}
                <div className="flex flex-col gap-4 lg:sticky lg:top-0 min-w-0">
                  <section className={cardCls}>
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">La clase en video</h4>
                      <span className="text-[11px] text-kenth-subtext">Momentos y subtítulos sobre la línea de tiempo.</span>
                    </div>
                    {videoPanel}
                  </section>

                  <section className={cardCls}>
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Transcripción</h4>
                      <div className="flex items-center gap-2">
                        <TranscriptChip status={transcriptStatus} count={transcript.length} />
                        {hasTranscript && !readOnly && (
                          <button onClick={() => setCorrecting((v) => !v)}
                            className="px-2.5 py-1 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60">
                            {correcting ? 'Cerrar' : 'Corregir'}
                          </button>
                        )}
                      </div>
                    </div>
                    {!hasTranscript ? (
                      <p className="text-[12px] text-kenth-subtext">Aún no hay transcripción. Genera el borrador en el paso 2 para transcribir el video.</p>
                    ) : !correcting ? (
                      <p className="text-[12px] text-kenth-subtext">Los subtítulos se muestran bajo la línea de tiempo. Pulsa <b className="text-kenth-text">Corregir</b> para arreglar términos técnicos mal transcritos.</p>
                    ) : (
                      <div className="flex flex-col gap-2">
                        <p className="text-[11px] text-kenth-subtext">
                          Corrige los términos técnicos mal transcritos. Referencia:{' '}
                          {GLOSARIO.map((g) => <span key={g} className="inline-block bg-kenth-surface/10 border border-kenth-border rounded px-1.5 py-0.5 text-[10px] text-kenth-subtext mr-1 mb-1">{g}</span>)}
                        </p>
                        <div className="flex flex-col gap-1.5 max-h-[38vh] overflow-y-auto pr-1">
                          {transcript.map((s, idx) => (
                            <div key={idx} className="flex gap-2 items-start">
                              <button onClick={() => seek(Number(s.start_time) || 0)} className="text-[10px] font-mono text-kenth-brightred hover:underline flex-shrink-0 pt-1.5" title="Ir a este punto">{fmtTime(s.start_time)}</button>
                              <textarea rows={2} disabled={readOnly} value={s.text || ''} onChange={(e) => setSegText(idx, e.target.value)}
                                className="flex-1 bg-kenth-surface/10 border border-kenth-border rounded-lg px-2 py-1 text-xs text-kenth-text focus:border-kenth-brightred focus:outline-none resize-none" />
                            </div>
                          ))}
                        </div>
                        <button onClick={saveTranscript} disabled={readOnly || savingTranscript}
                          className="self-start px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
                          {savingTranscript ? 'Guardando…' : 'Guardar corrección'}
                        </button>
                      </div>
                    )}
                  </section>
                </div>

                {/* DERECHA: revisión pedagógica (tarjetas edit-on-demand) */}
                <div className="flex flex-col gap-4 min-w-0">
                <EditableCard
                  title="Lo esencial"
                  readOnly={readOnly}
                  summary={p.learning_goal ? p.learning_goal : 'Sin objetivo definido'}
                >
                  <div>
                    <label className={labelCls}>Objetivo de aprendizaje</label>
                    <textarea rows={2} disabled={readOnly} className={inputCls} value={p.learning_goal} onChange={(e) => setP('learning_goal', e.target.value)} />
                  </div>
                  <div>
                    <label className={labelCls}>Resumen de la clase</label>
                    <textarea rows={3} disabled={readOnly} className={inputCls} value={p.lesson_summary} onChange={(e) => setP('lesson_summary', e.target.value)} />
                  </div>
                </EditableCard>

                <EditableCard
                  title="Cómo debe ayudar el tutor"
                  readOnly={readOnly}
                  summary={`${TONE_LABEL[p.tutor_tone] || 'Tono automático'} · ${HELP_LABEL[p.help_level] || 'Ayuda automática'}`}
                >
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className={labelCls}>Tono</label>
                      <select disabled={readOnly} className={inputCls} value={p.tutor_tone} onChange={(e) => setP('tutor_tone', e.target.value)}>
                        {TONE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                      </select>
                    </div>
                    <div>
                      <label className={labelCls}>Nivel de ayuda</label>
                      <select disabled={readOnly} className={inputCls} value={p.help_level} onChange={(e) => setP('help_level', e.target.value)}>
                        {HELP_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                      </select>
                    </div>
                  </div>
                  <ListField label="Reglas principales (una por línea)" readOnly={readOnly} value={p.lesson_rules} onChange={(v) => setP('lesson_rules', v)} />
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <ListField label="Qué debe reforzar" readOnly={readOnly} value={p.tutor_focus} onChange={(v) => setP('tutor_focus', v)} />
                    <ListField label="Qué debe evitar" readOnly={readOnly} value={p.tutor_must_not_do} onChange={(v) => setP('tutor_must_not_do', v)} />
                  </div>
                </EditableCard>

                <EditableCard
                  title="Preguntas y errores"
                  readOnly={readOnly}
                  summary={`${(p.common_mistakes || []).length} errores · ${(p.probable_questions || []).length} preguntas · ${(p.key_concepts || []).length} conceptos`}
                >
                  <ListField label="Conceptos clave (uno por línea)" readOnly={readOnly} value={p.key_concepts} onChange={(v) => setP('key_concepts', v)} />
                  <ListField label="Errores comunes a vigilar (uno por línea)" readOnly={readOnly} value={p.common_mistakes} onChange={(v) => setP('common_mistakes', v)} />
                  <ListField label="Preguntas probables (una por línea)" readOnly={readOnly} value={p.probable_questions} onChange={(v) => setP('probable_questions', v)} />
                </EditableCard>

                <EditableCard
                  title="Mensajes al alumno"
                  readOnly={readOnly}
                  summary={p.proactive_message ? p.proactive_message : `${(p.suggested_prompts || []).length} preguntas sugeridas`}
                >
                  <div>
                    <label className={labelCls}>Mensaje de bienvenida (lo ve el alumno al abrir el tutor)</label>
                    <textarea rows={2} disabled={readOnly} className={inputCls} value={p.proactive_message} onChange={(e) => setP('proactive_message', e.target.value)} />
                  </div>
                  <ListField label="Preguntas sugeridas al alumno (una por línea)" readOnly={readOnly} value={p.suggested_prompts} onChange={(v) => setP('suggested_prompts', v)} />
                </EditableCard>

                {/* Momentos: lista + revisar (modal). Editables: tiempos, tipo y pedagogía. */}
                <section className={cardCls}>
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Momentos de la clase ({moments.length})</h4>
                    {!readOnly && (
                      <button onClick={addMoment} className="px-2.5 py-1 rounded-lg border border-kenth-brightred/50 bg-kenth-brightred/10 text-[10px] font-black uppercase tracking-widest text-kenth-brightred hover:bg-kenth-brightred/20">+ Momento</button>
                    )}
                  </div>
                  {moments.length === 0 ? (
                    <p className="text-[12px] text-kenth-subtext">Esta lección aún no tiene momentos. Genera el borrador con IA (paso 2) o crea uno con <b className="text-kenth-text">+ Momento</b>; luego ajusta sus tiempos arrastrando en la línea de tiempo.</p>
                  ) : (
                    <div className="flex flex-col gap-2">
                      {moments.map((m, idx) => (
                        <div key={m.block_id || idx} className="border border-kenth-border/60 rounded-xl p-3 flex items-start gap-3 bg-kenth-surface/5">
                          <div className="flex flex-col items-center gap-1 flex-shrink-0 pt-0.5">
                            <span className="text-[10px] font-black text-kenth-brightred">M{idx + 1}</span>
                            <span className="text-[10px] font-mono text-kenth-subtext">{momentRange(m)}</span>
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold text-kenth-text truncate">{m.title || `Momento ${idx + 1}`}</p>
                            {m.interaction_mode && (
                              <span className="inline-flex items-center gap-1 text-[10px] text-kenth-subtext mt-0.5">
                                <span className={`inline-block h-2 w-2 rounded-sm ${colorDotForMode(m.interaction_mode)}`} />
                                {MODE_LABEL[m.interaction_mode] || m.interaction_mode}
                              </span>
                            )}
                            {m.summary && <p className="text-[11px] text-kenth-subtext line-clamp-2">{m.summary}</p>}
                          </div>
                          {!readOnly && (
                            <button onClick={() => openEditMoment(idx)} className="px-2.5 py-1 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60 flex-shrink-0">Revisar</button>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </section>

                <section className={cardCls}>
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">Probar tutor</h4>
                    <button onClick={() => setProbando((v) => !v)} className="px-3 py-1.5 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60">
                      {probando ? 'Cerrar prueba' : 'Abrir tutor'}
                    </button>
                  </div>
                  <p className="text-[11px] text-kenth-subtext">Guarda para que el tutor use esta configuración; los cambios de comportamiento se aplican al instante (sin reindexar).</p>
                  {probando && (
                    <TutorAssistCard variant="lesson" titulo={`Prueba · ${resource?.name || ''}`} contexto={`Lección: ${resource?.name}.`}
                      activityContext={testCtx} proactiveMessage={p.proactive_message || ''} suggestedPrompts={p.suggested_prompts || []} />
                  )}
                </section>

                </div>
                </div>

                {/* Barra de acciones a lo ancho de las dos columnas: Regenerar al borde
                    izquierdo (columna del video/transcripción), Guardar al borde derecho. */}
                {!readOnly && (
                  <div className="flex items-center justify-between gap-3 sticky bottom-0 bg-gradient-to-t from-black/85 via-black/60 to-transparent pt-4 pb-2 -mx-1 px-1">
                    <button onClick={() => setStep(2)} className="px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-subtext text-xs font-black uppercase tracking-widest hover:text-kenth-text">← Regenerar</button>
                    <button onClick={saveProfile} disabled={saving}
                      className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-black uppercase tracking-widest disabled:opacity-40 transition">
                      {saving ? 'Aplicando…' : 'Guardar y aplicar al tutor'}
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Modal de edición de UN momento (tiempos + tipo + pedagogía) */}
      {editing && (
        <div className="fixed inset-0 z-[210] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => setEditing(null)}>
          <div className="w-full max-w-lg bg-kenth-card border border-kenth-border rounded-2xl shadow-2xl p-5 flex flex-col gap-3 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between">
              <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Momento M{editing.idx + 1}</p>
              <button onClick={() => setEditing(null)} className="text-kenth-subtext hover:text-kenth-text">✕</button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className={labelCls}>Inicio (segundos)</label>
                <div className="flex gap-1">
                  <input type="number" min="0" className={inputCls} value={editing.start_time} onChange={(e) => setEditing((x) => ({ ...x, start_time: Number(e.target.value) }))} />
                  <button onClick={() => setEditing((x) => ({ ...x, start_time: Math.round(currentTime) }))} className="px-2 rounded-lg bg-kenth-surface/10 border border-kenth-border text-[10px] text-kenth-subtext whitespace-nowrap" title="Usar el tiempo actual del video">⏱</button>
                </div>
              </div>
              <div>
                <label className={labelCls}>Fin (segundos)</label>
                <div className="flex gap-1">
                  <input type="number" min="0" className={inputCls} value={editing.end_time} onChange={(e) => setEditing((x) => ({ ...x, end_time: Number(e.target.value) }))} />
                  <button onClick={() => setEditing((x) => ({ ...x, end_time: Math.round(currentTime) }))} className="px-2 rounded-lg bg-kenth-surface/10 border border-kenth-border text-[10px] text-kenth-subtext whitespace-nowrap" title="Usar el tiempo actual del video">⏱</button>
                </div>
              </div>
            </div>
            <div>
              <label className={labelCls}>Tipo de momento (color en la línea de tiempo)</label>
              <select className={inputCls} value={editing.interaction_mode} onChange={(e) => setEditing((x) => ({ ...x, interaction_mode: e.target.value }))}>
                {MODE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
              </select>
            </div>
            <div>
              <label className={labelCls}>Título</label>
              <input className={inputCls} value={editing.title} onChange={(e) => setEditing((x) => ({ ...x, title: e.target.value }))} placeholder="Título del momento" />
            </div>
            <div>
              <label className={labelCls}>Resumen (qué pasa en esta parte)</label>
              <textarea rows={2} className={inputCls} value={editing.summary} onChange={(e) => setEditing((x) => ({ ...x, summary: e.target.value }))} />
            </div>
            <div>
              <label className={labelCls}>Intención del tutor (qué reforzar aquí)</label>
              <input className={inputCls} value={editing.pedagogical_intent} onChange={(e) => setEditing((x) => ({ ...x, pedagogical_intent: e.target.value }))} />
            </div>
            <div>
              <label className={labelCls}>Conceptos clave (uno por línea)</label>
              <textarea rows={2} className={inputCls} value={editing.key_concepts} onChange={(e) => setEditing((x) => ({ ...x, key_concepts: e.target.value }))} />
            </div>
            <div>
              <label className={labelCls}>Errores comunes (uno por línea)</label>
              <textarea rows={2} className={inputCls} value={editing.common_mistakes} onChange={(e) => setEditing((x) => ({ ...x, common_mistakes: e.target.value }))} />
            </div>
            <div>
              <label className={labelCls}>Preguntas probables (una por línea)</label>
              <textarea rows={2} className={inputCls} value={editing.probable_questions} onChange={(e) => setEditing((x) => ({ ...x, probable_questions: e.target.value }))} />
            </div>
            <div className="flex items-center justify-between gap-2 pt-1">
              <button onClick={() => removeMoment(editing.idx)} className="px-3 py-2 rounded-xl border border-red-500/40 text-red-400 text-[10px] font-black uppercase tracking-widest hover:bg-red-500/10">🗑 Borrar momento</button>
              <div className="flex gap-2">
                <button onClick={() => setEditing(null)} className="px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-text text-xs font-bold uppercase tracking-widest">Cancelar</button>
                <button onClick={saveMoment} className="px-5 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest">Aplicar</button>
              </div>
            </div>
            <p className="text-[10px] text-kenth-subtext text-right">Se guarda al pulsar <b className="text-kenth-text">Guardar y aplicar al tutor</b>.</p>
          </div>
        </div>
      )}
    </div>
  );
}

// Tarjeta con edición bajo demanda: cerrada muestra un resumen; "Editar" abre los campos.
function EditableCard({ title, summary, readOnly, children }) {
  const [open, setOpen] = useState(false);
  return (
    <section className={cardCls}>
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0">
          <h4 className="text-sm font-black uppercase italic text-kenth-text tracking-tight">{title}</h4>
          {!open && <p className="text-[12px] text-kenth-subtext truncate mt-0.5">{summary}</p>}
        </div>
        {!readOnly && (
          <button onClick={() => setOpen((v) => !v)} className="px-3 py-1.5 rounded-lg border border-kenth-border text-[10px] font-black uppercase tracking-widest text-kenth-text hover:border-kenth-brightred/60 flex-shrink-0">
            {open ? 'Cerrar' : 'Editar'}
          </button>
        )}
      </div>
      {open && <div className="flex flex-col gap-3 border-t border-kenth-border/50 pt-3">{children}</div>}
    </section>
  );
}

function ListField({ label, value, onChange, readOnly }) {
  return (
    <div>
      <label className={labelCls}>{label}</label>
      <textarea
        rows={2}
        disabled={readOnly}
        className={inputCls}
        value={arrToLines(value)}
        onChange={(e) => onChange(linesToArr(e.target.value))}
      />
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
