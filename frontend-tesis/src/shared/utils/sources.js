// Utilidades de visibilidad de fuentes del tutor.
//
// El backend /chat puede incluir en `fuentes` chunks internos (guías del tutor,
// QA, manifiestos, prompts de evaluación) que el tutor usa como CONOCIMIENTO pero
// que NO deben mostrarse al estudiante como fuente citable. Estos vienen marcados
// con visible_to_student=false. Aquí los filtramos en el cliente (defensa en
// profundidad; el backend ya filtra en el borde del API).

const FALSY = new Set(['0', 'false', 'no', 'off', 'null', 'none', 'nil', '']);

/**
 * ¿La fuente es visible para el estudiante? Robusto ante bool, número o string
 * ('false'). Si no trae el flag, se asume visible (fuentes legacy sin marca).
 * @param {any} f
 * @returns {boolean}
 */
export function isSourceVisibleToStudent(f) {
  if (!f || typeof f !== 'object') return false;
  const v = f.visible_to_student;
  if (v === undefined || v === null) return true; // legacy sin flag -> visible
  if (typeof v === 'boolean') return v;
  if (typeof v === 'number') return v !== 0;
  return !FALSY.has(String(v).trim().toLowerCase());
}

/**
 * Devuelve solo las fuentes visibles al estudiante (oculta el material interno).
 * @param {any[]} fuentes
 * @returns {any[]}
 */
export function filterVisibleSources(fuentes) {
  if (!Array.isArray(fuentes)) return [];
  return fuentes.filter(isSourceVisibleToStudent);
}
