/**
 * permissions.js — Capa central de permisos por rol (capabilities Moodle).
 *
 * Fuente de verdad: Moodle vía `has_capability`, expuesto por la WS
 * `local_tesisai_get_permissions` y/o el endpoint `tesis_role.php`. Ambos
 * devuelven el MISMO contrato de flags (la WS en snake_case, tesis_role.php en
 * camelCase); esta capa normaliza a camelCase y tolera ambas fuentes.
 *
 * Contrato de flags:
 *   esProfesor            -> moodle/course:manageactivities (pedagogía)
 *   puedeAdministrarCurso -> ROL manager/coursecreator (estructura/editor avanzado)
 *   esTecnicoRAG          -> is_siteadmin (diagnóstico / reindex global)
 *   puedeVerCurso         -> moodle/course:view / matriculado
 *   puedeRevisar          -> moodle/grade:viewall (profesor sin edición: analítica)
 *   esInvitado            -> ve el curso pero no matriculado ni docente
 *   rolEfectivo           -> etiqueta derivada (solo UI)
 *
 * IMPORTANTE: esto NO es una frontera de seguridad; solo decide qué ve el front.
 * La barrera real vive en FastAPI (require_teacher / require_course_admin /
 * require_course_reviewer / require_course_view / require_rag_admin), que resuelve
 * las MISMAS capabilities vía la WS. Nunca uses `localStorage.moodle_rol`
 * (heurística por username, spoofeable) para gatear acciones sensibles.
 */
import { useEffect, useState } from 'react';
import { getMoodleToken } from '../utils/moodleToken';

const EMPTY_PERMS = Object.freeze({
  esProfesor: false,
  puedeAdministrarCurso: false,
  esTecnicoRAG: false,
  puedeVerCurso: false,
  puedeRevisar: false,
  esInvitado: false,
  rolEfectivo: '',
});

// Lee un flag tolerando camelCase (tesis_role.php) o snake_case (WS Moodle).
const flag = (data, camel, snake) => Boolean(data?.[camel] ?? data?.[snake]);

function normalizePerms(data) {
  if (!data || typeof data !== 'object') return { ...EMPTY_PERMS };
  return {
    esProfesor: flag(data, 'esProfesor', 'es_profesor'),
    puedeAdministrarCurso: flag(data, 'puedeAdministrarCurso', 'puede_administrar_curso'),
    esTecnicoRAG: flag(data, 'esTecnicoRAG', 'es_tecnico_rag'),
    puedeVerCurso: flag(data, 'puedeVerCurso', 'puede_ver_curso'),
    puedeRevisar: flag(data, 'puedeRevisar', 'puede_revisar'),
    esInvitado: flag(data, 'esInvitado', 'es_invitado'),
    rolEfectivo: String(data.rolEfectivo ?? data.rol_efectivo ?? ''),
  };
}

// Cache por (token + courseId): evita golpear la fuente en cada montaje, pero
// AISLA por usuario. Cachear solo por courseId hacía que, al cambiar de usuario
// en la misma pestaña (admin -> profesor), se reutilizaran los permisos previos.
const _cache = new Map();

export async function fetchCoursePermissions(courseId) {
  const token = getMoodleToken();
  if (!token || !courseId) return { ...EMPTY_PERMS };
  const key = `${token}::${courseId}`;
  if (_cache.has(key)) return _cache.get(key);
  try {
    const res = await fetch(
      `/api/lms/proyecto_curso/api_persistente/tesis_role.php?token=${encodeURIComponent(token)}&courseid=${encodeURIComponent(courseId)}`,
    );
    const data = await res.json();
    // Compat: si el backend aún no expone las flags granulares (server sin
    // actualizar), degradan a false -> mínimo privilegio (solo vista estudiante).
    const perms = normalizePerms(data);
    _cache.set(key, perms);
    return perms;
  } catch {
    return { ...EMPTY_PERMS };
  }
}

// Permisos a NIVEL DE SITIO (sin curso), para la barra lateral y las entradas de
// administración de sitio (Gestor IA / Precios). Solo aporta esTecnicoRAG real.
const _siteCache = new Map();

export async function fetchSitePermissions() {
  const token = getMoodleToken();
  if (!token) return { ...EMPTY_PERMS };
  if (_siteCache.has(token)) return _siteCache.get(token);
  try {
    const res = await fetch(
      `/api/lms/proyecto_curso/api_persistente/tesis_role.php?token=${encodeURIComponent(token)}&site=1`,
    );
    const data = await res.json();
    const perms = normalizePerms(data);
    _siteCache.set(token, perms);
    return perms;
  } catch {
    return { ...EMPTY_PERMS };
  }
}

export function clearPermissionsCache(courseId) {
  if (courseId === undefined) { _cache.clear(); _siteCache.clear(); return; }
  const suffix = `::${String(courseId)}`;
  for (const k of _cache.keys()) { if (k.endsWith(suffix)) _cache.delete(k); }
}

// --- Reglas de capacidad (derivadas de flags REALES, no de moodle_rol) ---
export const canViewCourse = (p) => Boolean(p?.puedeVerCurso);
// El invitado ve contenido permitido pero NO usa el tutor IA (sin trazas).
export const canUseTutor = (p) => Boolean(p?.puedeVerCurso && !p?.esInvitado);
// Revisar clase / probar tutor como docente: incluye al profesor SIN edición.
export const canReviewStudents = (p) => Boolean(p?.puedeRevisar || p?.esProfesor || p?.puedeAdministrarCurso);
export const canEditPedagogy = (p) => Boolean(p?.esProfesor);
// OBLIGATORIO: el profesor editor NO entra al editor avanzado (solo gestor/técnico).
export const canEditAdvancedLesson = (p) => Boolean(p?.puedeAdministrarCurso || p?.esTecnicoRAG);
export const canPublishLesson = (p) => Boolean(p?.puedeAdministrarCurso);
// Reindex por curso: gestor o superior. Reindex global/diagnóstico: solo técnico.
export const canReindexCourse = (p) => Boolean(p?.puedeAdministrarCurso || p?.esTecnicoRAG);
export const canViewRagDebug = (p) => Boolean(p?.esTecnicoRAG);
export const canReindex = (p) => Boolean(p?.esTecnicoRAG);

export function deriveCapabilities(perms) {
  return {
    canViewCourse: canViewCourse(perms),
    canUseTutor: canUseTutor(perms),
    canReviewStudents: canReviewStudents(perms),
    canEditPedagogy: canEditPedagogy(perms),
    canEditAdvancedLesson: canEditAdvancedLesson(perms),
    canPublishLesson: canPublishLesson(perms),
    canReindexCourse: canReindexCourse(perms),
    canViewRagDebug: canViewRagDebug(perms),
    canReindex: canReindex(perms),
  };
}

/**
 * Hook React: resuelve permisos del curso y expone las capacidades derivadas.
 * @returns {{ perms, loading, canEditPedagogy, canEditAdvancedLesson, ... }}
 */
export function usePermissions(courseId) {
  // Un solo estado: evita el setState síncrono dentro del efecto (cascading
  // renders). loading arranca en true y se resuelve en el callback asíncrono.
  const [state, setState] = useState({ perms: EMPTY_PERMS, loading: true });

  useEffect(() => {
    let alive = true;
    fetchCoursePermissions(courseId).then((p) => {
      if (alive) setState({ perms: p, loading: false });
    });
    return () => { alive = false; };
  }, [courseId]);

  return { perms: state.perms, loading: state.loading, ...deriveCapabilities(state.perms) };
}

/**
 * Hook React: permisos a nivel de SITIO (sin curso). Úsalo para gatear entradas
 * de administración de sitio (Gestor IA / Precios) por esTecnicoRAG real.
 */
export function useSitePermissions() {
  const [state, setState] = useState({ perms: EMPTY_PERMS, loading: true });
  useEffect(() => {
    let alive = true;
    fetchSitePermissions().then((p) => {
      if (alive) setState({ perms: p, loading: false });
    });
    return () => { alive = false; };
  }, []);
  return { perms: state.perms, loading: state.loading, ...deriveCapabilities(state.perms) };
}
