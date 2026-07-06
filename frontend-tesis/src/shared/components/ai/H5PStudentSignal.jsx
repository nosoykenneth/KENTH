import React, { useEffect, useState } from 'react';
import { getMyLessonSignals } from '../../services/ragService';

/**
 * Indicador compacto para el ESTUDIANTE: estado de la actividad interactiva H5P.
 * Puede recibir una señal externa para actualizarse en tiempo real sin cerrar la lección.
 * Si hay una guía del tutor (hasGuidance) el badge se vuelve BOTÓN: al hacer clic
 * abre el chat y recupera/enfoca el mensaje de orientación (onOpenGuidance).
 */
export default function H5PStudentSignal({
  courseId,
  lessonId,
  signal = null,
  refreshKey = 0,
  onSignal = null,
  hasGuidance = false,
  onOpenGuidance = null,
}) {
  const [sig, setSig] = useState(signal);

  useEffect(() => {
    let alive = true;
    if (!lessonId) return undefined;
    getMyLessonSignals(courseId, lessonId).then((data) => {
      if (!alive) return;
      setSig(data);
      onSignal?.(data);
    }).catch(() => {
      if (alive) setSig({ status: 'error' });
    });
    return () => { alive = false; };
  }, [courseId, lessonId, refreshKey, onSignal]);

  const displaySig = signal || sig;

  if (!displaySig || !displaySig.h5p_configured) return null;

  if (displaySig.status === 'not_attempted' || displaySig.status === 'empty') {
    return (
      <span className="rounded-full bg-indigo-400/10 px-3 py-1 text-[10px] font-black uppercase tracking-widest text-indigo-300 border border-indigo-400/20">
        ✨ Realiza el video interactivo
      </span>
    );
  }

  if (displaySig.status !== 'available') return null;

  const reinforce = displaySig.level === 'needs_reinforcement' || displaySig.level === 'partial';
  const label = reinforce ? 'Conviene reforzar · el tutor tiene una guía' : 'Actividad completada ✓';
  const cls = reinforce
    ? 'bg-amber-400/10 text-amber-300 border-amber-400/20'
    : 'bg-emerald-400/10 text-emerald-300 border-emerald-400/20';

  // Con guía disponible el badge es un botón: recupera el mensaje del tutor
  // (aunque el chat esté cerrado o el mensaje se haya perdido de vista).
  const clickable = reinforce && hasGuidance && typeof onOpenGuidance === 'function';

  if (clickable) {
    return (
      <button
        type="button"
        onClick={onOpenGuidance}
        title="Ver guía del tutor"
        aria-label="Ver guía del tutor"
        className={`rounded-full px-3 py-1 text-[10px] font-black uppercase tracking-widest border ${cls} inline-flex items-center gap-1.5 cursor-pointer transition-all hover:bg-amber-400/25 hover:border-amber-300/50 hover:scale-[1.03] active:scale-95 focus:outline-none focus:ring-2 focus:ring-amber-300/50`}
      >
        <span>{label}</span>
        <span className="rounded-md bg-amber-300/20 border border-amber-300/30 px-1.5 py-0.5 text-[8px] normal-case tracking-normal font-black">
          Ver guía
        </span>
      </button>
    );
  }

  return (
    <span
      title={reinforce ? 'El tutor tiene una recomendación para ti' : 'Actividad interactiva completada'}
      className={`rounded-full px-3 py-1 text-[10px] font-black uppercase tracking-widest border ${cls}`}
    >
      {label}
    </span>
  );
}
