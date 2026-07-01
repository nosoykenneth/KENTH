/**
 * permissions.js — Capa central de permisos por rol (rediseño por roles).
 *
 * Fuente de verdad: el backend Moodle vía `tesis_role.php`, que deriva 3 flags
 * de capacidades REALES del contexto del curso:
 *   - esProfesor            -> moodle/course:manageactivities (pedagogía)
 *   - puedeAdministrarCurso -> moodle/course:update (estructura del curso)
 *   - esTecnicoRAG          -> is_siteadmin (diagnóstico / reindex)
 *
 * IMPORTANTE: esto NO es una frontera de seguridad; solo decide qué ve el front.
 * La barrera real vive en FastAPI (require_teacher / require_course_admin /
 * require_rag_admin). Nunca uses `localStorage.moodle_rol` (heurística por
 * username, spoofeable) para gatear acciones sensibles.
 */
import { useEffect, useState } from 'react';
import { getMoodleToken } from '../utils/moodleToken';

const EMPTY_PERMS = Object.freeze({
  esProfesor: false,
  puedeAdministrarCurso: false,
  esTecnicoRAG: false,
});

// Cache por courseId: evita golpear tesis_role.php en cada montaje.
const _cache = new Map();

export async function fetchCoursePermissions(courseId) {
  const token = getMoodleToken();
  if (!token || !courseId) return { ...EMPTY_PERMS };
  const key = String(courseId);
  if (_cache.has(key)) return _cache.get(key);
  try {
    const res = await fetch(
      `/api/lms/proyecto_curso/api_persistente/tesis_role.php?token=${encodeURIComponent(token)}&courseid=${encodeURIComponent(courseId)}`,
    );
    const data = await res.json();
    const perms = {
      esProfesor: Boolean(data.esProfesor),
      // Compat: si el backend aún no expone las flags granulares (server sin
      // actualizar), degradan a false -> el profesor solo ve la vista pedagógica.
      puedeAdministrarCurso: Boolean(data.puedeAdministrarCurso),
      esTecnicoRAG: Boolean(data.esTecnicoRAG),
    };
    _cache.set(key, perms);
    return perms;
  } catch {
    return { ...EMPTY_PERMS };
  }
}

export function clearPermissionsCache(courseId) {
  if (courseId === undefined) _cache.clear();
  else _cache.delete(String(courseId));
}

// --- Reglas de capacidad (derivadas de flags REALES, no de moodle_rol) ---
export const canViewStudentLesson = () => true; // cualquier usuario autenticado
export const canEditPedagogy = (p) => Boolean(p?.esProfesor);
// OBLIGATORIO #1: el profesor NO entra al editor avanzado.
export const canEditAdvancedLesson = (p) => Boolean(p?.puedeAdministrarCurso || p?.esTecnicoRAG);
export const canPublishLesson = (p) => Boolean(p?.puedeAdministrarCurso);
export const canViewRagDebug = (p) => Boolean(p?.esTecnicoRAG);
export const canReindex = (p) => Boolean(p?.esTecnicoRAG);

export function deriveCapabilities(perms) {
  return {
    canViewStudentLesson: canViewStudentLesson(perms),
    canEditPedagogy: canEditPedagogy(perms),
    canEditAdvancedLesson: canEditAdvancedLesson(perms),
    canPublishLesson: canPublishLesson(perms),
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
