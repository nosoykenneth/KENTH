import React, { useCallback, useEffect, useMemo, useState } from 'react';
import {
  getLesson,
  getResourceLink,
  replaceLessonBlocks,
  upsertLesson,
  getTranscript,
  replaceTranscript,
  autoTranscribe,
  getTranscriptStatus,
  importLesson,
  savePedagogy,
  toTutorProfile,
  aiPrepare,
} from '../../services/sectionsService';
import { showNotification } from '../../utils/notify';
import { MODOS_PEDAGOGICOS } from '../../types/lesson';
import { useResourceVideoBridge } from '../../hooks/useResourceTimestamp';
import BlockTimeline from './BlockTimeline';
import { fmtTime } from '../../utils/time';
import { buildMoodleViewUrl, getMoodleToken } from '../../utils/moodleToken';
import AssignLessonDialog from './AssignLessonDialog';
import LessonResourcesPanel from './LessonResourcesPanel';

const IFRAME_NAME = 'kenth_editor_video';

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

// Vocabulario único: viene del schema compartido (types/lesson.ts) y debe
// ser idéntico al enum InteractionMode del backend.
const INTERACTION_MODES = MODOS_PEDAGOGICOS;

const linesToArr = (s) => (s || '').split('\n').map((x) => x.trim()).filter(Boolean);
const arrToLines = (a) => (Array.isArray(a) ? a.join('\n') : (a || ''));

// Opciones del perfil pedagógico canónico (idénticas a la Vista Profesor).
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

// Overlay del borrador IA sobre el perfil canónico (solo pisa lo NO vacío).
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

const Icon = ({ children }) => (
  <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {children}
  </svg>
);
const PlayIcon = () => <Icon><path d="M8 5v14l11-7-11-7z" fill="currentColor" stroke="none" /></Icon>;
const PauseIcon = () => <Icon><path d="M9 5v14" /><path d="M15 5v14" /></Icon>;
const VolumeIcon = () => <Icon><path d="M11 5 6 9H3v6h3l5 4V5z" /><path d="M16 9.5a4 4 0 0 1 0 5" /><path d="M19 7a8 8 0 0 1 0 10" /></Icon>;
const MutedIcon = () => <Icon><path d="M11 5 6 9H3v6h3l5 4V5z" /><path d="m16 9 5 6" /><path d="m21 9-5 6" /></Icon>;
const BackIcon = () => <Icon><path d="M11 7 6 12l5 5" /><path d="M18 7l-5 5 5 5" /></Icon>;
const ForwardIcon = () => <Icon><path d="m6 7 5 5-5 5" /><path d="m13 7 5 5-5 5" /></Icon>;
const RefreshIcon = () => <Icon><path d="M21 12a9 9 0 1 1-2.64-6.36" /><path d="M21 4v6h-6" /></Icon>;

const TABS = [
  { id: 'leccion', label: 'Lección' },
  { id: 'bloques', label: 'Bloques' },
  { id: 'transcripcion', label: 'Transcripción' },
  { id: 'recursos', label: 'Recursos' },
];

/**
 * LessonVideoEditor
 *
 * Editor full-screen del tutor sobre el video H5P. Reemplaza al antiguo
 * LinkLessonModal: ademas de elegir la leccion enlazada, edita los bloques
 * (timeline visual sobre el video), metadatos y prompts. Todo se guarda en
 * BD via /authoring (sectionsService).
 *
 * Props:
 *   - resource: modulo Moodle abierto { id, modname, name }.
 *   - courseId: id (firmado) del curso.
 *   - onClose(refresh: boolean)
 */
export default function LessonVideoEditor({ resource, courseId, sectionContext = null, onClose }) {
  const token = getMoodleToken();
  const isH5P = resource?.modname === 'hvp' || resource?.modname === 'h5pactivity';

  const [tab, setTab] = useState('leccion');
  const [iframeLoading, setIframeLoading] = useState(true);
  const [revealFallback, setRevealFallback] = useState(false); // revelar aunque no llegue duración

  const [currentLink, setCurrentLink] = useState(null);
  const [selectedLessonId, setSelectedLessonId] = useState('');
  const [lesson, setLesson] = useState(null);
  // Perfil pedagógico CANÓNICO (mismo modelo que la Vista Profesor y la IA).
  const [profile, setProfile] = useState(null);
  const [selectedBlockIdx, setSelectedBlockIdx] = useState(-1);
  const [showAssign, setShowAssign] = useState(false); // "Corregir vínculo"

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [dirtyChange, setDirtyChange] = useState(false); // hubo cambios persistidos -> refrescar al cerrar
  const [aiBusy, setAiBusy] = useState(false); // botón "Generar con IA" (mismo endpoint que el profesor)

  // Cambios sin guardar, por sección (para el único botón Guardar y el aviso al cerrar).
  const [dirty, setDirty] = useState({ profile: false, lesson: false, blocks: false, transcript: false });
  const [showUnsaved, setShowUnsaved] = useState(false);
  const mark = useCallback((k) => setDirty((d) => (d[k] ? d : { ...d, [k]: true })), []);
  const isDirty = dirty.profile || dirty.lesson || dirty.blocks || dirty.transcript;
  const setPro = (k, v) => { setProfile((p) => (p ? { ...p, [k]: v } : p)); mark('profile'); };

  // Transcripción
  const [transcript, setTranscript] = useState([]);
  const [transcriptLoading, setTranscriptLoading] = useState(false);
  const [job, setJob] = useState(null); // { status, progress, error, segments }
  const [pauseOnType, setPauseOnType] = useState(true);
  const [transcriptView, setTranscriptView] = useState('segments'); // 'segments' | 'text'
  const [textBuffer, setTextBuffer] = useState(''); // edición continua (una línea = un segmento)

  const {
    currentTimestamp,
    duration,
    seek,
    play,
    pause,
    muted,
    setMuted,
    hideNativeControls,
    requestMeta,
    requestThumbnail,
  } = useResourceVideoBridge({ enabled: true, resourceId: resource?.id ?? null, iframeName: IFRAME_NAME });

  const currentTime = currentTimestamp || 0;

  // ---- Carga inicial: lecciones + vinculo actual ----
  useEffect(() => {
    if (!resource?.id) return undefined;
    let alive = true;
    (async () => {
      try {
        setLoading(true);
        const link = await getResourceLink(resource.id, courseId);
        if (!alive) return;
        const fallbackLink = sectionContext?.lesson_id
          ? {
              resource_id: resource.id,
              lesson_id: sectionContext.lesson_id,
              course_id: courseId,
              moodle_section_id: sectionContext.moodle_section_id || '',
            }
          : null;
        const activeLink = link || fallbackLink;
        setCurrentLink(activeLink);
        setSelectedLessonId(activeLink?.lesson_id || '');
        setTab('leccion');
      } catch (e) {
        if (alive) showNotification('error', e.message);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, [resource?.id, courseId, sectionContext?.lesson_id, sectionContext?.moodle_section_id]);

  // ---- Carga del detalle de la leccion seleccionada ----
  const loadLessonDetail = useCallback(async (lId) => {
    if (!lId) { setLesson(null); setSelectedBlockIdx(-1); return; }
    try {
      const data = await getLesson(lId, courseId);
      setLesson({
        ...data,
        // Legacy (solo pestaña "Avanzado"): criterios y prerrequisitos pre-IA.
        _learning_goals: arrToLines(data.learning_goals),
        _prerequisites: (data.prerequisites || []).join(', '),
        blocks: (data.blocks || []).map((b) => ({ ...EMPTY_BLOCK, ...b })),
      });
      // Perfil pedagógico canónico (lo consumen Perfil tab + la IA).
      setProfile(toTutorProfile(data));
      setSelectedBlockIdx((data.blocks || []).length ? 0 : -1);
      setDirty((d) => ({ ...d, profile: false, lesson: false, blocks: false }));
    } catch (e) {
      showNotification('error', e.message);
    }
  }, [courseId]);

  useEffect(() => { loadLessonDetail(selectedLessonId); }, [selectedLessonId, loadLessonDetail]);

  // ---- Transcripción ----
  const loadTranscript = useCallback(async (lId) => {
    if (!lId) { setTranscript([]); setJob(null); return; }
    setTranscriptLoading(true);
    try {
      const data = await getTranscript(courseId, lId);
      setTranscript(data.segments || []);
      setJob(data.job || null);
      setTranscriptView('segments');
      setDirty((d) => ({ ...d, transcript: false }));
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setTranscriptLoading(false);
    }
  }, [courseId]);

  useEffect(() => { loadTranscript(selectedLessonId); }, [selectedLessonId, loadTranscript]);

  // Polling del job de transcripción automática.
  useEffect(() => {
    if (!selectedLessonId || job?.status !== 'running') return undefined;
    const iv = setInterval(async () => {
      try {
        const data = await getTranscriptStatus(courseId, selectedLessonId);
        const st = data.job;
        setJob(st || null);
        if (!st || st.status === 'done') {
          clearInterval(iv);
          if (st?.status === 'done') {
            await loadTranscript(selectedLessonId);
            setDirtyChange(true);
            showNotification('success', 'Transcripción automática lista.');
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
  }, [job?.status, selectedLessonId, courseId, loadTranscript]);

  const startAutoTranscribe = async () => {
    if (!selectedLessonId || !resource?.id) return;
    if (transcript.length && !window.confirm('Esto reemplazará la transcripción actual al terminar. ¿Continuar?')) return;
    try {
      const data = await autoTranscribe(courseId, selectedLessonId, { resource_id: Number(resource.id) });
      setJob(data.job || { status: 'running', progress: 0 });
      showNotification('success', 'Transcripción iniciada. Puede tardar varios minutos…');
    } catch (e) {
      showNotification('error', e.message);
    }
  };

  const setSegText = (idx, text) => {
    setTranscript((p) => p.map((s, i) => (i === idx ? { ...s, text } : s)));
    mark('transcript');
    if (pauseOnType) pause();
  };
  // Edición del inicio como timecode HH:MM:SS.mmm (4 campos). Conserva la
  // precisión real (milisegundos) que ya trae la transcripción de Whisper.
  const setSegStartPart = (idx, part, raw) => {
    const v = Math.max(0, Math.floor(Number(raw) || 0));
    setTranscript((p) => p.map((s, i) => {
      if (i !== idx) return s;
      const cur = Number(s.start_time) || 0;
      let h = Math.floor(cur / 3600);
      let m = Math.floor((cur % 3600) / 60);
      let sec = Math.floor(cur % 60);
      let ms = Math.round((cur - Math.floor(cur)) * 1000);
      if (part === 'h') h = v;
      else if (part === 'm') m = Math.min(59, v);
      else if (part === 's') sec = Math.min(59, v);
      else if (part === 'ms') ms = Math.min(999, v);
      return { ...s, start_time: h * 3600 + m * 60 + sec + ms / 1000 };
    }));
    mark('transcript');
  };
  const addSegment = () => {
    const start = Math.round(currentTime);
    setTranscript((p) => [...p, { seq: p.length, start_time: start, end_time: start + 3, text: '', speaker: '' }]);
    mark('transcript');
  };
  const removeSegment = (idx) => { setTranscript((p) => p.filter((_, i) => i !== idx)); mark('transcript'); };

  // ---- Edición como texto (toggle estilo YouTube): una línea = un segmento ----
  // Rehace la lista de segmentos manteniendo los tiempos por índice; las líneas
  // nuevas heredan un rango corto tras el último segmento.
  const applyTextBuffer = useCallback((buf) => {
    const lines = (buf || '').split('\n');
    setTranscript((prev) => {
      const out = [];
      let lastEnd = 0;
      lines.forEach((line, i) => {
        const base = prev[i];
        if (base) {
          out.push({ ...base, text: line });
          lastEnd = Number(base.end_time) || lastEnd;
        } else {
          const start = lastEnd;
          const end = lastEnd + 3;
          out.push({ start_time: start, end_time: end, text: line, speaker: '' });
          lastEnd = end;
        }
      });
      return out;
    });
  }, []);

  const switchToText = () => {
    setTextBuffer(transcript.map((s) => s.text || '').join('\n'));
    setTranscriptView('text');
  };
  const switchToSegments = () => {
    applyTextBuffer(textBuffer);
    setTranscriptView('segments');
  };
  const onTextBufferChange = (val) => {
    setTextBuffer(val);
    applyTextBuffer(val);
    mark('transcript');
    if (pauseOnType) pause();
  };

  const clearTranscript = () => {
    if (!transcript.length) return;
    if (!window.confirm('¿Borrar TODA la transcripción de esta lección? Se aplicará al Guardar cambios.')) return;
    setTranscript([]);
    setTextBuffer('');
    mark('transcript');
  };

  const activeSegIdx = useMemo(() => {
    for (let i = 0; i < transcript.length; i += 1) {
      const s = transcript[i];
      if (Number(s.start_time) <= currentTime && currentTime < Number(s.end_time)) return i;
    }
    return -1;
  }, [transcript, currentTime]);

  // Pedir metadatos del video hasta recibir la duracion. El iframe hace un
  // redirect interno (_wrap) y el <video> tarda en exponer loadedmetadata,
  // asi que insistimos cada 1.5s; el bridge tambien reemite solo al tenerla.
  useEffect(() => {
    if (!isH5P || duration) return undefined;
    const iv = setInterval(() => requestMeta(), 1500);
    return () => clearInterval(iv);
  }, [isH5P, duration, requestMeta]);

  // Revelar el H5P solo cuando ya llegó la duración (metadatos): así no se ve el
  // frame oscuro/incompleto. Fallback a los 12s por si la duración nunca llega.
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

  // ---- Mutaciones locales de bloques ----
  const setBlockField = (idx, k, v) => {
    setLesson((p) => {
      if (!p) return p;
      const blocks = [...p.blocks];
      blocks[idx] = { ...blocks[idx], [k]: v };
      return { ...p, blocks };
    });
    mark('blocks');
  };

  // Campos del momento que viven en block.metadata (p. ej. common_mistakes).
  const setBlockMeta = (idx, k, v) => {
    setLesson((p) => {
      if (!p) return p;
      const blocks = [...p.blocks];
      blocks[idx] = { ...blocks[idx], metadata: { ...(blocks[idx].metadata || {}), [k]: v } };
      return { ...p, blocks };
    });
    mark('blocks');
  };

  const changeBlockTime = useCallback((idx, patch) => {
    setLesson((p) => {
      if (!p) return p;
      const blocks = [...p.blocks];
      const next = { ...blocks[idx] };
      if (patch.start_time != null) next.start_time = Math.round(patch.start_time);
      if (patch.end_time != null) next.end_time = Math.round(patch.end_time);
      blocks[idx] = next;
      return { ...p, blocks };
    });
    mark('blocks');
  }, [mark]);

  const addBlock = () => {
    if (!lesson) return;
    const start = Math.round(currentTime);
    const end = duration ? Math.min(Math.round(currentTime) + 30, Math.floor(duration)) : Math.round(currentTime) + 30;
    const newIdx = lesson.blocks.length;
    setLesson((p) => (p ? {
      ...p,
      blocks: [...p.blocks, { ...EMPTY_BLOCK, block_id: `${p.lesson_id}-B${p.blocks.length + 1}`, start_time: start, end_time: end }],
    } : p));
    setSelectedBlockIdx(newIdx);
    mark('blocks');
  };

  const removeBlock = (idx) => {
    setLesson((p) => (p ? { ...p, blocks: p.blocks.filter((_, i) => i !== idx) } : p));
    setSelectedBlockIdx((cur) => (cur === idx ? -1 : cur > idx ? cur - 1 : cur));
    mark('blocks');
  };

  // ---- Guardado único de todos los cambios ----
  const saveAll = useCallback(async () => {
    if (!isDirty) return true;
    setSaving(true);
    try {
      if (lesson) {
        // Estructura + legacy (title/order/section/notes/criterios/prereq). NO envía
        // pedagogy: eso lo escribe savePedagogy (perfil canónico) para no duplicar.
        if (dirty.lesson) {
          await upsertLesson(courseId, lesson.lesson_id, {
            lesson_id: lesson.lesson_id,
            axis_id: '',
            moodle_section_id: lesson.moodle_section_id || currentLink?.moodle_section_id || sectionContext?.moodle_section_id || '',
            title: lesson.lesson_title || lesson.title || '',
            order: Number(lesson.order) || 0,
            learning_goal: (profile?.learning_goal) || lesson.learning_goal || '',
            expected_action: lesson.expected_action || '',
            learning_goals: linesToArr(lesson._learning_goals),
            resources: lesson.resources || [],
            prerequisites: (lesson._prerequisites || '').split(',').map((x) => x.trim()).filter(Boolean),
            delegated_to_tutor: profile?.tutor_focus || [],
            attribution_constraints: profile?.tutor_must_not_do || [],
            notes: lesson.notes || '',
          });
        }
        // Perfil pedagógico CANÓNICO (mismo escritor que la Vista Profesor: PUT /pedagogy).
        if (dirty.profile && profile) {
          await savePedagogy(courseId, lesson.lesson_id, profile);
        }
        if (dirty.blocks) {
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
            // errores comunes del momento viven en block.metadata (no es columna técnica).
            metadata: b.metadata || {},
          }));
          await replaceLessonBlocks(courseId, lesson.lesson_id, blocks);
        }
        if (dirty.transcript) {
          const segs = transcript.map((s, i) => ({
            seq: i,
            start_time: Number(s.start_time) || 0,
            end_time: Number(s.end_time) || 0,
            text: s.text || '',
            speaker: s.speaker || '',
          }));
          await replaceTranscript(courseId, lesson.lesson_id, segs);
        }
      }
      setDirty({ profile: false, lesson: false, blocks: false, transcript: false });
      setDirtyChange(true);
      showNotification('success', 'Cambios guardados.');
      return true;
    } catch (e) {
      showNotification('error', e.message);
      return false;
    } finally {
      setSaving(false);
    }
  }, [isDirty, dirty, lesson, profile, transcript, courseId, currentLink?.moodle_section_id, sectionContext?.moodle_section_id]);

  // Botón "Generar con IA" del admin: MISMO endpoint que el profesor (ai-prepare).
  const runAiPrepareAdmin = async () => {
    if (!selectedLessonId) return;
    if (!transcript.length) { showNotification('error', 'Primero transcribe el video (pestaña Transcripción).'); return; }
    setAiBusy(true);
    try {
      const res = await aiPrepare(courseId, selectedLessonId, { mode: 'draft', quality: 'balanced' });
      setProfile((p) => overlayDraft(p || {}, res.draft));
      mark('profile');
      showNotification('success', 'Perfil pedagógico generado. Revísalo y guarda los cambios.');
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setAiBusy(false);
    }
  };

  const handleCloseRequest = () => {
    if (isDirty) setShowUnsaved(true);
    else onClose(dirtyChange);
  };

  // Importar archivo JSON sobre ESTA lección (rellena todos los campos).
  const importFromFile = async (file) => {
    if (!file || !selectedLessonId) return;
    let json;
    try { json = JSON.parse(await file.text()); }
    catch (e) { showNotification('error', 'JSON inválido: ' + e.message); return; }
    if (isDirty && !window.confirm('Tienes cambios sin guardar que se descartarán, y el archivo reemplazará los campos de esta lección. ¿Continuar?')) return;
    if (!isDirty && !window.confirm('El archivo reemplazará todos los campos de esta lección. ¿Continuar?')) return;
    setSaving(true);
    try {
      await importLesson(courseId, json, selectedLessonId); // no toca el vínculo
      await loadLessonDetail(selectedLessonId);
      await loadTranscript(selectedLessonId);
      setDirty({ lesson: false, blocks: false, transcript: false });
      setDirtyChange(true);
      showNotification('success', 'Lección importada.');
    } catch (e) { showNotification('error', e.message); }
    finally { setSaving(false); }
  };

  const setField = (k, v) => { setLesson((p) => (p ? { ...p, [k]: v } : p)); mark('lesson'); };

  const selectedBlock = selectedBlockIdx >= 0 ? lesson?.blocks?.[selectedBlockIdx] : null;

  const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none';
  const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';
  const transportBtnCls = 'inline-flex h-9 min-w-9 items-center justify-center gap-1.5 rounded-lg border border-kenth-border bg-kenth-surface/10 px-2.5 text-xs font-bold text-kenth-text transition hover:border-kenth-brightred/60 hover:bg-kenth-brightred/10 focus:outline-none focus:ring-2 focus:ring-kenth-brightred/40';
  const transportGhostCls = 'inline-flex h-9 items-center justify-center gap-1.5 rounded-lg border border-kenth-border bg-kenth-surface/5 px-3 text-[10px] font-black uppercase tracking-widest text-kenth-subtext transition hover:border-kenth-brightred/60 hover:bg-kenth-surface/10 hover:text-kenth-text focus:outline-none focus:ring-2 focus:ring-kenth-brightred/40';

  const videoSrc = useMemo(() => buildMoodleViewUrl({
    token,
    cmid: resource?.id,
    modname: resource?.modname,
    extra: { hidefs: 1 },
  }), [resource?.id, resource?.modname, token]);

  return (
    <div className="fixed inset-0 z-[200] bg-black/80 backdrop-blur-sm flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between gap-4 px-5 py-3 border-b border-kenth-border bg-kenth-card">
        <div className="min-w-0">
          <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Editor de lección</p>
          <h3 className="text-base font-black uppercase italic text-kenth-text tracking-tight truncate">
            {resource?.name}
            {currentLink?.lesson_id && (
              <span className="ml-2 text-[10px] not-italic font-bold text-emerald-300 align-middle">
                · {currentLink.lesson_id}
              </span>
            )}
          </h3>
          <button onClick={() => setShowAssign(true)} className="text-[10px] uppercase tracking-widest text-kenth-subtext hover:text-kenth-text mt-0.5" title="Reasignar este video a otra lección (solo para corregir errores)">
            Corregir vínculo
          </button>
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          <label className="px-3 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-text text-xs font-bold uppercase tracking-widest hover:border-kenth-brightred/50 cursor-pointer transition" title="Rellenar todos los campos de esta lección desde un JSON">
            Importar archivo
            <input type="file" accept="application/json,.json" className="hidden" onChange={(e) => { importFromFile(e.target.files?.[0]); e.target.value = ''; }} />
          </label>
          <button
            onClick={saveAll}
            disabled={saving || !isDirty}
            className="px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40 transition"
          >
            {saving ? 'Guardando…' : (isDirty ? 'Guardar cambios' : 'Guardado')}
          </button>
          <button onClick={handleCloseRequest} className="text-kenth-subtext hover:text-kenth-text">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Body */}
      <div className="flex-1 min-h-0 flex flex-col lg:flex-row">
        {/* IZQUIERDA: video + timeline */}
        <div className="lg:flex-1 min-w-0 flex flex-col bg-kenth-bg border-r border-kenth-border">
          <div className="relative flex-1 min-h-[240px] flex items-center justify-center p-3">
            {isH5P && !videoSrc ? (
              <div className="text-center text-sm text-kenth-subtext max-w-md">
                Sesion expirada. Vuelve a iniciar sesion para editar este video.
              </div>
            ) : isH5P ? (
              <div className="relative w-full max-w-[820px] rounded-xl overflow-hidden bg-black">
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
                  title="Editor H5P"
                />
              </div>
            ) : (
              <div className="text-center text-sm text-kenth-subtext max-w-md">
                Este recurso ({resource?.modname}) no es un video H5P. Puedes enlazar la lección,
                pero el timeline visual y la transcripción requieren un video H5P.
              </div>
            )}
          </div>

          {/* Transporte + timeline */}
          {isH5P && (
            <div className="px-4 pb-4 pt-2 border-t border-kenth-border bg-kenth-card/40">
              <div className="flex items-center gap-2 mb-3">
                <button onClick={() => play()} className={transportBtnCls} title="Reproducir" aria-label="Reproducir">
                  <PlayIcon />
                </button>
                <button onClick={() => pause()} className={transportBtnCls} title="Pausar" aria-label="Pausar">
                  <PauseIcon />
                </button>
                <button onClick={() => setMuted(!muted)} className={`${transportBtnCls} ${muted ? 'border-kenth-brightred/70 bg-kenth-brightred/15 text-kenth-brightred' : ''}`} title={muted ? 'Desmutear' : 'Mutear'} aria-label={muted ? 'Desmutear' : 'Mutear'}>
                  {muted ? <MutedIcon /> : <VolumeIcon />}
                </button>
                <button onClick={() => seek(Math.max(0, currentTime - 5))} className={transportGhostCls} title="Retroceder 5 segundos" aria-label="Retroceder 5 segundos">
                  <BackIcon />
                  <span>-5s</span>
                </button>
                <button onClick={() => seek(currentTime + 5)} className={transportGhostCls} title="Avanzar 5 segundos" aria-label="Avanzar 5 segundos">
                  <span>+5s</span>
                  <ForwardIcon />
                </button>
                <button onClick={() => { hideNativeControls(); requestMeta(); }} className={`${transportGhostCls} ml-auto`} title="Releer metadatos del video" aria-label="Releer video">
                  <RefreshIcon />
                  <span>Releer video</span>
                </button>
              </div>
              <BlockTimeline
                blocks={lesson?.blocks || []}
                duration={duration}
                currentTime={currentTime}
                selectedIndex={selectedBlockIdx}
                onSelectBlock={(idx) => { setSelectedBlockIdx(idx); setTab('bloques'); }}
                onSeek={(s) => seek(s)}
                onChangeBlockTime={changeBlockTime}
                requestThumbnail={requestThumbnail}
                transcript={transcript}
              />
              {!selectedLessonId && (
                <p className="text-[11px] text-amber-300/80 mt-2">
                  Enlaza una lección en la pestaña <strong>Vínculo</strong> para ver y editar sus bloques.
                </p>
              )}
            </div>
          )}
        </div>

        {/* DERECHA: pestañas */}
        <div className="lg:w-[420px] flex flex-col bg-kenth-card min-h-0">
          <div className="flex border-b border-kenth-border flex-shrink-0">
            {TABS.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`flex-1 px-2 py-2.5 text-[11px] font-black uppercase tracking-widest transition ${
                  tab === t.id ? 'text-kenth-brightred border-b-2 border-kenth-brightred' : 'text-kenth-subtext hover:text-kenth-text'
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          <div className="flex-1 min-h-0 overflow-y-auto p-4">
            {loading ? (
              <p className="text-sm text-kenth-subtext">Cargando…</p>
            ) : (
              <>
                {/* ---------- BLOQUES ---------- */}
                {tab === 'bloques' && (
                  !lesson ? (
                    <p className="text-sm text-kenth-subtext">Enlaza una lección para editar sus bloques.</p>
                  ) : (
                    <div className="flex flex-col gap-3">
                      <div className="flex items-center justify-between">
                        <span className={labelCls}>Bloques ({lesson.blocks.length})</span>
                        <button onClick={addBlock} className="text-[10px] font-black uppercase text-kenth-brightred hover:underline">+ Bloque en {fmtTime(currentTime)}</button>
                      </div>

                      {/* Lista compacta */}
                      <div className="flex flex-wrap gap-1.5">
                        {lesson.blocks.map((b, idx) => (
                          <button
                            key={b.block_id || idx}
                            onClick={() => { setSelectedBlockIdx(idx); seek(Number(b.start_time) || 0); }}
                            className={`px-2 py-1 rounded-md text-[10px] border ${selectedBlockIdx === idx ? 'bg-kenth-brightred/15 border-kenth-brightred/50 text-kenth-text' : 'bg-kenth-surface/5 border-kenth-border text-kenth-subtext hover:border-kenth-brightred/30'}`}
                          >
                            {b.block_title || `B${idx + 1}`} · {fmtTime(b.start_time)}
                          </button>
                        ))}
                      </div>

                      {selectedBlock ? (
                        <div className="border border-kenth-border rounded-xl p-3 bg-kenth-surface/5 flex flex-col gap-2">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold uppercase text-kenth-subtext">{selectedBlock.block_id || `Bloque ${selectedBlockIdx + 1}`}</span>
                            <button onClick={() => removeBlock(selectedBlockIdx)} className="text-red-400 hover:text-red-300 text-xs">✕ Borrar bloque</button>
                          </div>
                          <div className="grid grid-cols-2 gap-2">
                            <div>
                              <label className={labelCls}>Inicio (s)</label>
                              <div className="flex gap-1">
                                <input type="number" className={inputCls} value={selectedBlock.start_time ?? 0} onChange={(e) => setBlockField(selectedBlockIdx, 'start_time', Number(e.target.value))} />
                                <button onClick={() => changeBlockTime(selectedBlockIdx, { start_time: currentTime })} className="px-2 rounded-lg bg-kenth-surface/10 border border-kenth-border text-[10px] text-kenth-subtext whitespace-nowrap" title="Usar tiempo actual">⏱</button>
                              </div>
                            </div>
                            <div>
                              <label className={labelCls}>Fin (s)</label>
                              <div className="flex gap-1">
                                <input type="number" className={inputCls} value={selectedBlock.end_time ?? 0} onChange={(e) => setBlockField(selectedBlockIdx, 'end_time', Number(e.target.value))} />
                                <button onClick={() => changeBlockTime(selectedBlockIdx, { end_time: currentTime })} className="px-2 rounded-lg bg-kenth-surface/10 border border-kenth-border text-[10px] text-kenth-subtext whitespace-nowrap" title="Usar tiempo actual">⏱</button>
                              </div>
                            </div>
                          </div>
                          <div>
                            <label className={labelCls}>Título del bloque</label>
                            <input className={inputCls} value={selectedBlock.block_title || ''} onChange={(e) => setBlockField(selectedBlockIdx, 'block_title', e.target.value)} />
                          </div>
                          <div>
                            <label className={labelCls}>Resumen (qué pasa en pantalla)</label>
                            <textarea rows={2} className={inputCls} value={selectedBlock.summary || ''} onChange={(e) => setBlockField(selectedBlockIdx, 'summary', e.target.value)} />
                          </div>
                          <div className="grid grid-cols-1 gap-2">
                            <div>
                              <label className={labelCls}>Modo pedagógico</label>
                              <select className={inputCls} value={selectedBlock.interaction_mode || ''} onChange={(e) => setBlockField(selectedBlockIdx, 'interaction_mode', e.target.value)}>
                                {INTERACTION_MODES.map((m) => <option key={m} value={m}>{m}</option>)}
                              </select>
                            </div>
                            <div>
                              <label className={labelCls}>Foco del tutor</label>
                              <input className={inputCls} value={selectedBlock.tutor_focus || ''} onChange={(e) => setBlockField(selectedBlockIdx, 'tutor_focus', e.target.value)} />
                            </div>
                          </div>
                          <div>
                            <label className={labelCls}>Conceptos (una por línea)</label>
                            <textarea rows={2} className={inputCls} value={Array.isArray(selectedBlock.concepts) ? arrToLines(selectedBlock.concepts) : selectedBlock.concepts} onChange={(e) => setBlockField(selectedBlockIdx, 'concepts', linesToArr(e.target.value))} />
                          </div>
                          <div>
                            <label className={labelCls}>Preguntas probables (una por línea)</label>
                            <textarea rows={2} className={inputCls} value={Array.isArray(selectedBlock.preguntas_probables) ? arrToLines(selectedBlock.preguntas_probables) : selectedBlock.preguntas_probables} onChange={(e) => setBlockField(selectedBlockIdx, 'preguntas_probables', linesToArr(e.target.value))} />
                          </div>
                          <div>
                            <label className={labelCls}>Errores comunes del momento (una por línea)</label>
                            <textarea rows={2} className={inputCls} value={arrToLines((selectedBlock.metadata || {}).common_mistakes)} onChange={(e) => setBlockMeta(selectedBlockIdx, 'common_mistakes', linesToArr(e.target.value))} />
                          </div>
                        </div>
                      ) : (
                        <p className="text-xs text-kenth-subtext">Selecciona un bloque (en el timeline o arriba) para editarlo, o crea uno nuevo.</p>
                      )}
                    </div>
                  )
                )}

                {/* ---------- LECCIÓN: perfil pedagógico canónico + datos de la lección (legacy) ---------- */}
                {tab === 'leccion' && (
                  !lesson || !profile ? (
                    <p className="text-sm text-kenth-subtext">Enlaza una lección para editar su perfil pedagógico.</p>
                  ) : (
                    <div className="flex flex-col gap-3">
                      <div className="flex items-center justify-between gap-2">
                        <span className={labelCls}>Perfil del tutor</span>
                        <button
                          onClick={runAiPrepareAdmin}
                          disabled={aiBusy || !transcript.length}
                          title={!transcript.length ? 'Transcribe el video primero' : 'Genera el perfil con IA (mismo motor que el profesor)'}
                          className="px-2.5 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-[10px] font-black uppercase tracking-widest disabled:opacity-40"
                        >
                          {aiBusy ? 'Generando…' : '✨ Generar con IA'}
                        </button>
                      </div>
                      <div>
                        <label className={labelCls}>Objetivo de aprendizaje</label>
                        <textarea rows={2} className={inputCls} value={profile.learning_goal} onChange={(e) => setPro('learning_goal', e.target.value)} />
                      </div>
                      <div>
                        <label className={labelCls}>Resumen de la clase</label>
                        <textarea rows={2} className={inputCls} value={profile.lesson_summary} onChange={(e) => setPro('lesson_summary', e.target.value)} />
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <label className={labelCls}>Tono</label>
                          <select className={inputCls} value={profile.tutor_tone} onChange={(e) => setPro('tutor_tone', e.target.value)}>
                            {TONE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                          </select>
                        </div>
                        <div>
                          <label className={labelCls}>Nivel de ayuda</label>
                          <select className={inputCls} value={profile.help_level} onChange={(e) => setPro('help_level', e.target.value)}>
                            {HELP_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                          </select>
                        </div>
                      </div>
                      <div>
                        <label className={labelCls}>Reglas de la lección (una por línea)</label>
                        <textarea rows={2} className={inputCls} value={arrToLines(profile.lesson_rules)} onChange={(e) => setPro('lesson_rules', linesToArr(e.target.value))} />
                      </div>
                      <div>
                        <label className={labelCls}>Conceptos clave (uno por línea)</label>
                        <textarea rows={2} className={inputCls} value={arrToLines(profile.key_concepts)} onChange={(e) => setPro('key_concepts', linesToArr(e.target.value))} />
                      </div>
                      <div>
                        <label className={labelCls}>Errores comunes (uno por línea)</label>
                        <textarea rows={2} className={inputCls} value={arrToLines(profile.common_mistakes)} onChange={(e) => setPro('common_mistakes', linesToArr(e.target.value))} />
                      </div>
                      <div>
                        <label className={labelCls}>Preguntas probables (una por línea)</label>
                        <textarea rows={2} className={inputCls} value={arrToLines(profile.probable_questions)} onChange={(e) => setPro('probable_questions', linesToArr(e.target.value))} />
                      </div>
                      <div>
                        <label className={labelCls}>Qué debe reforzar el tutor (uno por línea)</label>
                        <textarea rows={2} className={inputCls} value={arrToLines(profile.tutor_focus)} onChange={(e) => setPro('tutor_focus', linesToArr(e.target.value))} />
                      </div>
                      <div>
                        <label className={labelCls}>Qué NO debe hacer el tutor (uno por línea)</label>
                        <textarea rows={2} className={inputCls} value={arrToLines(profile.tutor_must_not_do)} onChange={(e) => setPro('tutor_must_not_do', linesToArr(e.target.value))} />
                      </div>

                      <div className="h-px bg-kenth-border my-2" />
                      <span className={labelCls}>Mensajes al alumno</span>
                      <div>
                        <label className={labelCls}>Mensaje de bienvenida</label>
                        <textarea rows={2} className={inputCls} value={profile.proactive_message} onChange={(e) => setPro('proactive_message', e.target.value)} />
                      </div>
                      <div>
                        <label className={labelCls}>Preguntas sugeridas (una por línea)</label>
                        <textarea rows={3} className={inputCls} value={arrToLines(profile.suggested_prompts)} onChange={(e) => setPro('suggested_prompts', linesToArr(e.target.value))} />
                      </div>

                      {/* ---------- Datos de la lección (estructura + legacy) ---------- */}
                      <div className="h-px bg-kenth-border my-2" />
                      <span className={labelCls}>Datos de la lección</span>
                      <div>
                        <label className={labelCls}>Título</label>
                        <input className={inputCls} value={lesson.lesson_title || ''} onChange={(e) => setField('lesson_title', e.target.value)} />
                      </div>
                      <div>
                        <label className={labelCls}>Orden dentro de la sección</label>
                        <input type="number" className={inputCls} value={lesson.order ?? 0} onChange={(e) => setField('order', e.target.value)} />
                        <p className="text-[10px] text-kenth-subtext mt-1">Define la posición de esta lección dentro de la sección.</p>
                      </div>

                      <div className="h-px bg-kenth-border my-2" />

                      {/* Campos pre-IA que el tutor sigue usando como respaldo (context_service los
                          inyecta si están), pero que el perfil/IA ya no genera. Plegados por defecto. */}
                      <details className="rounded-lg border border-kenth-border bg-kenth-surface/5">
                        <summary className="cursor-pointer px-3 py-2 text-[10px] uppercase tracking-widest text-kenth-subtext font-bold">
                          Configuración pedagógica avanzada (legacy)
                        </summary>
                        <div className="px-3 pb-3 pt-1 flex flex-col gap-3">
                          <p className="text-[10px] text-kenth-subtext">
                            Campos heredados (pre-IA). El tutor los usa como respaldo si están presentes;
                            el perfil pedagógico y la IA ya no los generan.
                          </p>
                          <div>
                            <label className={labelCls}>Prerrequisitos (coma)</label>
                            <input className={inputCls} value={lesson._prerequisites} onChange={(e) => setField('_prerequisites', e.target.value)} />
                          </div>
                          <div>
                            <label className={labelCls}>Acción esperada</label>
                            <input className={inputCls} value={lesson.expected_action || ''} onChange={(e) => setField('expected_action', e.target.value)} />
                          </div>
                          <div>
                            <label className={labelCls}>Criterios de logro (una por línea)</label>
                            <textarea rows={2} className={inputCls} value={lesson._learning_goals} onChange={(e) => setField('_learning_goals', e.target.value)} />
                          </div>
                        </div>
                      </details>

                      <div className="h-px bg-kenth-border my-2" />

                      <div>
                        <label className={labelCls}>Notas internas</label>
                        <textarea rows={2} className={inputCls} value={lesson.notes || ''} onChange={(e) => setField('notes', e.target.value)} />
                        <p className="text-[10px] text-kenth-subtext mt-1">Solo visible para ti: el tutor nunca recibe este campo.</p>
                      </div>
                    </div>
                  )
                )}

                {/* ---------- TRANSCRIPCIÓN ---------- */}
                {tab === 'transcripcion' && (
                  !selectedLessonId ? (
                    <p className="text-sm text-kenth-subtext">Enlaza una lección para transcribir su video.</p>
                  ) : (
                    <div className="flex flex-col gap-3">
                      <div className="flex items-center gap-2 flex-wrap">
                        <button
                          onClick={startAutoTranscribe}
                          disabled={job?.status === 'running'}
                          className="px-3 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40"
                        >
                          {job?.status === 'running' ? 'Transcribiendo…' : '✨ Transcribir automático'}
                        </button>
                        {transcript.length > 0 && (
                          <button
                            onClick={clearTranscript}
                            disabled={saving || job?.status === 'running'}
                            className="text-[10px] font-black uppercase text-red-400 hover:text-red-300 disabled:opacity-40"
                          >
                            🗑 Borrar todo
                          </button>
                        )}
                        <label className="ml-auto flex items-center gap-1.5 text-[10px] uppercase tracking-widest text-kenth-subtext cursor-pointer">
                          <input type="checkbox" checked={pauseOnType} onChange={(e) => setPauseOnType(e.target.checked)} className="accent-kenth-brightred" />
                          Pausar al escribir
                        </label>
                      </div>

                      {/* Toggle de vista: Segmentos / Texto */}
                      <div className="flex items-center justify-between gap-2">
                        <div className="inline-flex rounded-lg border border-kenth-border overflow-hidden">
                          <button
                            onClick={switchToSegments}
                            className={`px-3 py-1.5 text-[10px] font-black uppercase tracking-widest transition ${transcriptView === 'segments' ? 'bg-kenth-brightred text-white' : 'text-kenth-subtext hover:text-kenth-text'}`}
                          >
                            Segmentos
                          </button>
                          <button
                            onClick={switchToText}
                            className={`px-3 py-1.5 text-[10px] font-black uppercase tracking-widest transition ${transcriptView === 'text' ? 'bg-kenth-brightred text-white' : 'text-kenth-subtext hover:text-kenth-text'}`}
                          >
                            Texto
                          </button>
                        </div>
                        {transcriptView === 'segments' && (
                          <button onClick={addSegment} className="text-[10px] font-black uppercase text-kenth-brightred hover:underline">
                            + Segmento en {fmtTime(currentTime)}
                          </button>
                        )}
                      </div>

                      {job?.status === 'running' && (
                        <div className="rounded-lg border border-indigo-500/30 bg-indigo-500/10 p-2">
                          <div className="flex items-center justify-between text-[10px] text-indigo-200 mb-1">
                            <span>Transcribiendo con Whisper… ({job.segments || 0} segmentos)</span>
                            <span>{Math.round((job.progress || 0) * 100)}%</span>
                          </div>
                          <div className="h-1.5 rounded-full bg-indigo-900/40 overflow-hidden">
                            <div className="h-full bg-indigo-400 transition-all" style={{ width: `${Math.round((job.progress || 0) * 100)}%` }} />
                          </div>
                        </div>
                      )}
                      {job?.status === 'error' && (
                        <p className="text-[11px] text-red-400">Error: {job.error}</p>
                      )}

                      {transcriptLoading ? (
                        <p className="text-sm text-kenth-subtext">Cargando…</p>
                      ) : transcriptView === 'text' ? (
                        <div className="flex flex-col gap-1.5">
                          <textarea
                            value={textBuffer}
                            onChange={(e) => onTextBufferChange(e.target.value)}
                            rows={16}
                            placeholder="Una línea por segmento…"
                            className="w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text leading-relaxed focus:border-kenth-brightred focus:outline-none resize-y"
                          />
                          <p className="text-[10px] text-kenth-subtext">
                            Una línea = un segmento. Los tiempos se mantienen por orden; las líneas nuevas se ubican tras el último segmento (puedes ajustarlas en la vista <strong>Segmentos</strong>).
                          </p>
                        </div>
                      ) : transcript.length === 0 ? (
                        <p className="text-xs text-kenth-subtext">
                          No hay transcripción todavía. Usa <strong>Transcribir automático</strong> o agrega segmentos a mano.
                        </p>
                      ) : (
                        <div className="flex flex-col gap-1.5 max-h-[42vh] overflow-y-auto pr-1">
                          {transcript.map((s, idx) => (
                            <div
                              key={idx}
                              className={`flex gap-2 p-2 rounded-lg border ${activeSegIdx === idx ? 'bg-kenth-brightred/10 border-kenth-brightred/50' : 'bg-kenth-surface/5 border-kenth-border'}`}
                            >
                              <div className="flex flex-col items-center gap-1 flex-shrink-0">
                                <button onClick={() => seek(Number(s.start_time) || 0)} className="text-[10px] font-mono text-kenth-brightred hover:underline" title="Ir a este punto">
                                  {fmtTime(s.start_time)}
                                </button>
                                <div className="flex items-center gap-0.5" title="Inicio (horas : minutos : segundos . milisegundos)">
                                  {(() => {
                                    const t = Number(s.start_time) || 0;
                                    const h = Math.floor(t / 3600);
                                    const m = Math.floor((t % 3600) / 60);
                                    const sec = Math.floor(t % 60);
                                    const ms = Math.round((t - Math.floor(t)) * 1000);
                                    const cls = 'bg-kenth-surface/10 border border-kenth-border rounded px-0.5 py-0.5 text-[10px] text-kenth-subtext text-center';
                                    return (
                                      <>
                                        <input type="number" min="0" value={h} onChange={(e) => setSegStartPart(idx, 'h', e.target.value)} className={`w-6 ${cls}`} title="horas" />
                                        <span className="text-[10px] text-kenth-subtext">:</span>
                                        <input type="number" min="0" max="59" value={String(m).padStart(2, '0')} onChange={(e) => setSegStartPart(idx, 'm', e.target.value)} className={`w-7 ${cls}`} title="minutos" />
                                        <span className="text-[10px] text-kenth-subtext">:</span>
                                        <input type="number" min="0" max="59" value={String(sec).padStart(2, '0')} onChange={(e) => setSegStartPart(idx, 's', e.target.value)} className={`w-7 ${cls}`} title="segundos" />
                                        <span className="text-[10px] text-kenth-subtext">.</span>
                                        <input type="number" min="0" max="999" value={String(ms).padStart(3, '0')} onChange={(e) => setSegStartPart(idx, 'ms', e.target.value)} className={`w-9 ${cls}`} title="milisegundos" />
                                      </>
                                    );
                                  })()}
                                </div>
                              </div>
                              <textarea
                                rows={2}
                                value={s.text || ''}
                                onChange={(e) => setSegText(idx, e.target.value)}
                                className="flex-1 bg-kenth-surface/10 border border-kenth-border rounded-lg px-2 py-1 text-xs text-kenth-text focus:border-kenth-brightred focus:outline-none resize-none"
                              />
                              <button onClick={() => removeSegment(idx)} className="text-red-400 hover:text-red-300 text-xs flex-shrink-0" title="Borrar segmento">✕</button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )
                )}

                {/* ---------- RECURSOS ---------- */}
                {tab === 'recursos' && (
                  !selectedLessonId ? (
                    <p className="text-sm text-kenth-subtext">Enlaza una lección para añadirle recursos.</p>
                  ) : (
                    <LessonResourcesPanel courseId={courseId} lessonId={selectedLessonId} />
                  )
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Aviso de cambios sin guardar al cerrar (estilo propio, no del navegador) */}
      {showUnsaved && (
        <div
          className="fixed inset-0 z-[210] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
          onClick={() => !saving && setShowUnsaved(false)}
        >
          <div
            className="w-full max-w-md bg-kenth-card border border-kenth-border rounded-2xl shadow-2xl p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Cambios sin guardar</p>
            <h3 className="text-lg font-black uppercase italic text-kenth-text tracking-tight mt-1">¿Salir sin guardar?</h3>
            <p className="text-sm text-kenth-subtext mt-2">
              Tienes cambios que no has guardado. ¿Quieres guardarlos antes de salir?
            </p>
            <div className="flex flex-col gap-2 mt-5">
              <button
                onClick={async () => { const ok = await saveAll(); if (ok) { setShowUnsaved(false); onClose(true); } }}
                disabled={saving}
                className="w-full px-4 py-2.5 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40 transition"
              >
                {saving ? 'Guardando…' : 'Guardar y salir'}
              </button>
              <button
                onClick={() => { setShowUnsaved(false); onClose(dirtyChange); }}
                disabled={saving}
                className="w-full px-4 py-2.5 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-text text-xs font-bold uppercase tracking-widest hover:border-red-400/50 disabled:opacity-40 transition"
              >
                Salir sin guardar
              </button>
              <button
                onClick={() => setShowUnsaved(false)}
                disabled={saving}
                className="w-full px-4 py-2 text-xs font-bold uppercase tracking-widest text-kenth-subtext hover:text-kenth-text disabled:opacity-40"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Corregir vínculo: reasignar este video a otra lección (solo errores) */}
      {showAssign && (
        <AssignLessonDialog
          resource={resource}
          courseId={courseId}
          sectionContext={sectionContext}
          onClose={async (lessonId) => {
            setShowAssign(false);
            if (lessonId) {
              try { setCurrentLink(await getResourceLink(resource.id, courseId)); } catch { /* ignore */ }
              setSelectedLessonId(lessonId);
              setDirtyChange(true);
            }
          }}
        />
      )}
    </div>
  );
}
