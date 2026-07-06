import React, { useEffect, useState } from 'react';
import { getMyLessonSignals } from '../../services/ragService';

/**
 * Indicador compacto para el ESTUDIANTE: estado de la actividad interactiva H5P
 * de la lección. No muestra Chroma/YAML/metadata; tono no punitivo. Invita a
 * consultar al tutor cuando conviene reforzar.
 *
 * Props: { courseId, lessonId }
 */
export default function H5PStudentSignal({ courseId, lessonId }) {
  const [sig, setSig] = useState(null);

  useEffect(() => {
    let alive = true;
    if (!lessonId) return undefined;
    getMyLessonSignals(courseId, lessonId).then((d) => { if (alive) setSig(d); });
    return () => { alive = false; };
  }, [courseId, lessonId]);

  if (!sig || !sig.h5p_configured) return null;

  if (sig.status === 'not_attempted' || sig.status === 'empty') {
    return (
      <span className="rounded-full bg-indigo-400/10 px-3 py-1 text-[10px] font-black uppercase tracking-widest text-indigo-300 border border-indigo-400/20">
        ✨ Realiza el video interactivo
      </span>
    );
  }

  if (sig.status !== 'available') return null;

  const reinforce = sig.level === 'needs_reinforcement' || sig.level === 'partial';
  const label = reinforce ? 'Conviene reforzar · pregunta al tutor' : 'Actividad completada ✓';
  const cls = reinforce
    ? 'bg-amber-400/10 text-amber-300 border-amber-400/20'
    : 'bg-emerald-400/10 text-emerald-300 border-emerald-400/20';

  return (
    <span
      title="Tu tutor puede orientarte según tu desempeño en esta actividad"
      className={`rounded-full px-3 py-1 text-[10px] font-black uppercase tracking-widest border ${cls}`}
    >
      {label}
    </span>
  );
}
