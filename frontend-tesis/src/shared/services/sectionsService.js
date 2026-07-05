const RAG_API_URL = '/api/ai';

function authHeaders(courseId) {
  const token = localStorage.getItem('moodle_token') || '';
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(courseId ? { 'X-Course-Id': String(courseId) } : {}),
  };
}

function courseQuery(courseId) {
  return courseId ? `?course_id=${encodeURIComponent(courseId)}` : '';
}

// El backend puede devolver `detail` como string o como objeto {code, message,
// errors} (endpoints ai-prepare). Extrae siempre un mensaje legible.
function errMessage(body, status, path) {
  const d = body && body.detail;
  if (typeof d === 'string') return d;
  if (d && typeof d === 'object') return d.message || d.code || JSON.stringify(d);
  return `Error ${status} en ${path}`;
}

async function readJson(path, courseId = '') {
  const res = await fetch(`${RAG_API_URL}${path}`, {
    headers: authHeaders(courseId),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(errMessage(detail, res.status, path));
  }
  return res.json();
}

async function writeJson(method, path, courseId, body) {
  const res = await fetch(`${RAG_API_URL}${path}`, {
    method,
    headers: authHeaders(courseId),
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    const err = new Error(errMessage(detail, res.status, path));
    err.status = res.status;
    err.code = detail && detail.detail && detail.detail.code;
    throw err;
  }
  return res.json();
}

export async function listSections(courseId = '') {
  const data = await readJson(`/sections/list${courseQuery(courseId)}`, courseId);
  return data.sections || [];
}

export async function getSectionLessons(sectionId, courseId = '') {
  const data = await readJson(`/sections/${encodeURIComponent(sectionId)}/lessons${courseQuery(courseId)}`, courseId);
  return data.lessons || [];
}

export async function listAllLessons(courseId = '') {
  const data = await readJson(`/sections/lessons/all${courseQuery(courseId)}`, courseId);
  return data.lessons || [];
}

export function upsertLesson(courseId, lessonId, payload) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}`, courseId, {
    ...payload,
    axis_id: '',
  });
}

export function deleteLesson(courseId, lessonId) {
  return writeJson('DELETE', `/authoring/lessons/${encodeURIComponent(lessonId)}`, courseId);
}

export function reorderLessons(courseId, items) {
  return writeJson('PUT', `/authoring/lessons-reorder`, courseId, { items });
}

export async function listResourceLinks(courseId) {
  const data = await readJson(`/sections/links${courseQuery(courseId)}`, courseId);
  return data.links || [];
}

export async function getResourceLink(resourceId, courseId = '') {
  const qs = courseId ? courseQuery(courseId) : '';
  const res = await fetch(`${RAG_API_URL}/sections/links/${encodeURIComponent(resourceId)}${qs}`, {
    headers: authHeaders(courseId),
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error('Error obteniendo vínculo');
  return res.json();
}

export function upsertResourceLink(resourceId, payload) {
  return writeJson('PUT', `/sections/links/${encodeURIComponent(resourceId)}`, payload.course_id || '', {
    ...payload,
    axis_id: '',
  });
}

export function deleteResourceLink(resourceId, courseId = '') {
  // courseId se envía como X-Course-Id: el backend (require_teacher) valida rol
  // docente en ese curso antes de borrar el vínculo.
  return writeJson('DELETE', `/sections/links/${encodeURIComponent(resourceId)}`, courseId);
}

export async function getLesson(lessonId, courseId = '') {
  return readJson(`/sections/lessons/${encodeURIComponent(lessonId)}${courseQuery(courseId)}`, courseId);
}

export async function resolveLessonBlock(lessonId, timestamp, courseId = '') {
  const sep = courseId ? `&course_id=${encodeURIComponent(courseId)}` : '';
  return readJson(`/sections/lessons/${encodeURIComponent(lessonId)}/block?t=${timestamp}${sep}`, courseId);
}

export function replaceLessonBlocks(courseId, lessonId, blocks) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/blocks`, courseId, { blocks });
}

// Edición PEDAGÓGICA de momentos (bloques) para el profesor: solo campos
// pedagógicos, in-place. El backend (require_teacher) preserva tiempos/estructura
// y rechaza altas/bajas/reorden; los timestamps ni se envían (barrera server-side).
export function updateMoments(courseId, lessonId, moments) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/moments`, courseId, { moments });
}

export function setLessonPrompts(courseId, lessonId, { proactive_message = '', suggested_prompts = [] }) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/prompts`, courseId, {
    proactive_message,
    suggested_prompts,
  });
}

// ---- Perfil pedagógico CANÓNICO (modelo único Profesor/Admin/IA) ----
// Normaliza la respuesta de getLesson a un solo shape que ambos editores leen,
// y lo guarda por PUT /pedagogy (apply_profile). Espejo de services/pedagogy_profile.py.
const _asList = (v) => (Array.isArray(v)
  ? v
  : (typeof v === 'string' ? v.split('\n').map((s) => s.trim()).filter(Boolean) : []));

export function toTutorProfile(lesson = {}) {
  const meta = lesson.metadata || {};
  const ped = meta.pedagogy || {};
  return {
    learning_goal: lesson.learning_goal || '',
    lesson_summary: ped.lesson_summary || '',
    tutor_tone: ped.tutor_tone || '',
    help_level: ped.help_level || '',
    lesson_rules: _asList(ped.lesson_rules),
    key_concepts: _asList(ped.key_concepts),
    common_mistakes: _asList(ped.common_mistakes),
    probable_questions: _asList(ped.probable_questions),
    tutor_focus: _asList(lesson.delegated_to_tutor),
    tutor_must_not_do: _asList(lesson.attribution_constraints),
    proactive_message: lesson.proactive_message || '',
    suggested_prompts: _asList(lesson.suggested_prompts),
    moments: (lesson.blocks || []).map((b) => ({
      block_id: b.block_id,
      title: b.block_title || '',
      summary: b.summary || '',
      pedagogical_intent: b.tutor_focus || '',
      key_concepts: Array.isArray(b.concepts) ? b.concepts : _asList(b.concepts),
      common_mistakes: Array.isArray((b.metadata || {}).common_mistakes) ? b.metadata.common_mistakes : [],
      probable_questions: Array.isArray(b.preguntas_probables) ? b.preguntas_probables : _asList(b.preguntas_probables),
      start_time: b.start_time,
      end_time: b.end_time,
    })),
    ai_prepared: !!meta.ai_prepared,
    requires_review: !!meta.requires_review,
  };
}

// Funde los momentos del borrador IA en los bloques de la lección. Espejo (frontend)
// de services/pedagogy_profile.fuse_moments: si algún momento trae TIEMPOS válidos,
// reconstruye la línea de tiempo desde la segmentación de la IA (distribuida, no
// apilada) preservando el id del bloque existente cuando corresponde; si NINGÚN
// momento trae tiempos, solo funde la pedagogía en los bloques existentes.
const _num = (v) => { const n = Number(v); return Number.isFinite(n) ? n : null; };

export function mergeDraftMomentsIntoBlocks(existingBlocks = [], moments = [], lessonId = '') {
  const blocks = existingBlocks || [];
  const ms = moments || [];
  const byId = {};
  blocks.forEach((b) => { byId[String(b.block_id)] = b; });

  const hasTimes = ms.some((m) => {
    const s = _num(m.start_time); const e = _num(m.end_time);
    return s != null && e != null && e > s;
  });

  if (!hasTimes) {
    // Sin tiempos: funde solo la pedagogía en los bloques existentes (por id).
    const mById = {};
    ms.forEach((m) => { const id = m.existing_block_id || m.block_id; if (id) mById[String(id)] = m; });
    const pick = (a, b) => (Array.isArray(a) && a.length ? a : b);
    return blocks.map((b) => {
      const m = mById[String(b.block_id)];
      if (!m) return b;
      return {
        ...b,
        block_title: m.title || b.block_title,
        summary: m.summary || b.summary,
        interaction_mode: m.interaction_mode || b.interaction_mode,
        tutor_focus: m.pedagogical_intent || b.tutor_focus,
        concepts: pick(m.key_concepts, b.concepts),
        preguntas_probables: pick(m.probable_questions, b.preguntas_probables),
        metadata: { ...(b.metadata || {}), common_mistakes: pick(m.common_mistakes, (b.metadata || {}).common_mistakes || []) },
      };
    });
  }

  // Con tiempos: reconstruye la línea de tiempo desde los momentos de la IA.
  const prefix = (lessonId
    || (blocks[0]?.block_id ? String(blocks[0].block_id).replace(/-B\d+$/, '') : 'L')) || 'L';
  return ms
    .map((m) => ({ m, s: _num(m.start_time), e: _num(m.end_time) }))
    .filter((x) => x.s != null && x.e != null && x.e > x.s)
    .sort((a, b) => a.s - b.s)
    .map(({ m, s, e }, i) => {
      const ex = (m.existing_block_id && byId[String(m.existing_block_id)]) || null;
      // Ids frescos y secuenciales tras reordenar por tiempo (sin colisiones); la
      // identidad del bloque no se referencia fuera de la lección.
      return {
        block_id: `${prefix}-B${i + 1}`,
        block_order: i,
        start_time: s,
        end_time: e,
        block_title: m.title || (ex && ex.block_title) || '',
        summary: m.summary || (ex && ex.summary) || '',
        interaction_mode: m.interaction_mode || (ex && ex.interaction_mode) || '',
        tutor_focus: m.pedagogical_intent || (ex && ex.tutor_focus) || '',
        concepts: (Array.isArray(m.key_concepts) && m.key_concepts.length) ? m.key_concepts : ((ex && ex.concepts) || []),
        preguntas_probables: (Array.isArray(m.probable_questions) && m.probable_questions.length) ? m.probable_questions : ((ex && ex.preguntas_probables) || []),
        metadata: { ...((ex && ex.metadata) || {}), common_mistakes: (Array.isArray(m.common_mistakes) && m.common_mistakes.length) ? m.common_mistakes : (((ex && ex.metadata) || {}).common_mistakes || []) },
      };
    });
}

// Escribe el perfil pedagógico canónico (campos a nivel lección + prompts).
// NO toca estructura técnica ni momentos (esos van por /moments y /blocks).
export function savePedagogy(courseId, lessonId, profile = {}) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/pedagogy`, courseId, {
    learning_goal: profile.learning_goal || '',
    lesson_summary: profile.lesson_summary || '',
    tutor_tone: profile.tutor_tone || '',
    help_level: profile.help_level || '',
    lesson_rules: profile.lesson_rules || [],
    key_concepts: profile.key_concepts || [],
    common_mistakes: profile.common_mistakes || [],
    probable_questions: profile.probable_questions || [],
    tutor_focus: profile.tutor_focus || [],
    tutor_must_not_do: profile.tutor_must_not_do || [],
    proactive_message: profile.proactive_message || '',
    suggested_prompts: profile.suggested_prompts || [],
  });
}

export function importLesson(courseId, json, targetLessonId = '') {
  const qs = targetLessonId ? `?target_lesson_id=${encodeURIComponent(targetLessonId)}` : '';
  return writeJson('POST', `/authoring/lessons/import${qs}`, courseId, { ...json, axis_id: '' });
}

export function upsertResourceMeta(courseId, resourceId, payload) {
  return writeJson('PUT', `/authoring/resources/${encodeURIComponent(resourceId)}`, courseId, {
    ...payload,
    axis_id: '',
  });
}

export async function getTranscript(courseId, lessonId) {
  return readJson(`/authoring/lessons/${encodeURIComponent(lessonId)}/transcript`, courseId);
}

export function replaceTranscript(courseId, lessonId, segments) {
  return writeJson('PUT', `/authoring/lessons/${encodeURIComponent(lessonId)}/transcript`, courseId, { segments });
}

export function autoTranscribe(courseId, lessonId, { resource_id, language = 'es' }) {
  return writeJson('POST', `/authoring/lessons/${encodeURIComponent(lessonId)}/transcript/auto`, courseId, {
    resource_id,
    language,
  });
}

export async function getTranscriptStatus(courseId, lessonId) {
  return readJson(`/authoring/lessons/${encodeURIComponent(lessonId)}/transcript/status`, courseId);
}

// Asistente "Preparar tutor con IA": genera un BORRADOR pedagógico desde la
// transcripción. NO reindexa ni publica; el borrador queda en metadata.ai_prepare.
export function aiPrepare(courseId, lessonId, {
  mode = 'draft', quality = 'balanced', use_existing_transcript = true,
  regenerate_transcript = false, include_resources = true, include_vision = false,
  review_model = null,
} = {}) {
  return writeJson('POST', `/authoring/lessons/${encodeURIComponent(lessonId)}/ai-prepare`, courseId, {
    mode, quality, use_existing_transcript, regenerate_transcript, include_resources, include_vision,
    ...(review_model ? { review_model } : {}),
  });
}

// Acepta el borrador (posiblemente editado por el profesor) y lo promueve a los
// campos vivos del tutor. `draft` opcional; si no viene, promueve el guardado.
export function aiPrepareAccept(courseId, lessonId, { draft = null, apply_moments = true } = {}) {
  return writeJson('POST', `/authoring/lessons/${encodeURIComponent(lessonId)}/ai-prepare/accept`, courseId, {
    ...(draft ? { draft } : {}),
    apply_moments,
  });
}

// "Publicar cambios del tutor": (re)genera e indexa el contexto aprobado de la
// lección desde el perfil vigente. Devuelve el estado que se muestra al profesor
// (tutor_updated, transcript_status, index_status, indexed_at, requires_reindex).
export function publishTutorChanges(courseId, lessonId) {
  return writeJson('POST', `/authoring/lessons/${encodeURIComponent(lessonId)}/publish`, courseId, {});
}
