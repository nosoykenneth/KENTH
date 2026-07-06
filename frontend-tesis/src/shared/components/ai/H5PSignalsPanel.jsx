import React, { useCallback, useEffect, useState } from 'react';
import { getLessonSignalsSummary, syncLessonSignals } from '../../services/ragService';

/**
 * Panel del PROFESOR: "Evaluaciones interactivas H5P".
 * Muestra el estado de las evaluaciones del video interactivo y el resumen de
 * desempeño del curso. NO edita H5P (eso se hace en Moodle); solo gestiona/muestra
 * estado, sincronización y resultados. No expone Chroma/YAML/metadata técnica.
 *
 * Props: { courseId, lessonId, cmid }
 */
const LEVEL_LABEL = {
  needs_reinforcement: 'Conviene reforzar',
  partial: 'En progreso',
  ready: 'Sólido',
};

export default function H5PSignalsPanel({ courseId, lessonId, cmid = null }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [lastSync, setLastSync] = useState(null);

  // Carga inicial: el estado solo se actualiza dentro del callback async del fetch
  // (evita setState síncrono en el cuerpo del efecto).
  useEffect(() => {
    if (!lessonId) return undefined;
    let alive = true;
    getLessonSignalsSummary(courseId, lessonId).then((data) => {
      if (alive) { setSummary(data); setLoading(false); }
    });
    return () => { alive = false; };
  }, [courseId, lessonId]);

  const onSync = useCallback(async () => {
    setSyncing(true);
    await syncLessonSignals(courseId, lessonId);
    const data = await getLessonSignalsSummary(courseId, lessonId);
    setSummary(data);
    setLastSync(new Date());
    setSyncing(false);
  }, [courseId, lessonId]);

  const moodleUrl = cmid ? `/api/lms/mod/hvp/view.php?id=${cmid}` : null;
  const configured = summary && summary.h5p_configured;
  const dist = (summary && summary.level_distribution) || {};
  const withResults = (summary && summary.students_with_results) || 0;

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-900">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h3 className="text-base font-semibold text-slate-800 dark:text-slate-100">
          🎬 Evaluaciones interactivas H5P
        </h3>
        <span
          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
            configured
              ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300'
              : 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300'
          }`}
        >
          {configured ? 'Configurado' : 'No configurado'}
        </span>
      </div>

      {loading ? (
        <p className="text-sm text-slate-500">Cargando…</p>
      ) : !configured ? (
        <p className="text-sm text-slate-500">
          Esta lección aún no tiene evaluaciones interactivas configuradas para el tutor.
        </p>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Stat label="Interacciones" value={summary.interactions_count} />
            <Stat label="Estudiantes con intento" value={withResults} />
            <Stat label="Promedio" value={withResults ? `${summary.average_percentage}%` : '—'} />
            <Stat label="Completaron" value={summary.completion_count || 0} />
          </div>

          {Array.isArray(summary.concepts) && summary.concepts.length > 0 && (
            <div className="mt-3">
              <p className="text-xs font-medium text-slate-500">Conceptos evaluados</p>
              <div className="mt-1 flex flex-wrap gap-1">
                {summary.concepts.map((c) => (
                  <span key={c} className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                    {c}
                  </span>
                ))}
              </div>
            </div>
          )}

          {withResults > 0 && (
            <div className="mt-3">
              <p className="text-xs font-medium text-slate-500">Distribución</p>
              <div className="mt-1 flex flex-wrap gap-2 text-xs">
                {['needs_reinforcement', 'partial', 'ready'].map((k) => (
                  <span key={k} className="rounded bg-slate-50 px-2 py-1 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                    {LEVEL_LABEL[k]}: <b>{dist[k] || 0}</b>
                  </span>
                ))}
              </div>
            </div>
          )}

          {Array.isArray(summary.most_failed_concepts) && summary.most_failed_concepts.length > 0 && (
            <div className="mt-3">
              <p className="text-xs font-medium text-slate-500">Conceptos más fallados</p>
              <ul className="mt-1 space-y-1 text-sm text-slate-700 dark:text-slate-200">
                {summary.most_failed_concepts.slice(0, 5).map((c) => (
                  <li key={c.concept} className="flex items-center justify-between">
                    <span>{c.label || c.concept}</span>
                    <span className="text-xs text-rose-600 dark:text-rose-400">{c.failures}/{c.answered} fallos</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {withResults === 0 && (
            <p className="mt-3 text-sm text-slate-500">Aún no hay intentos de estudiantes en esta actividad.</p>
          )}
        </>
      )}

      <div className="mt-4 flex flex-wrap items-center gap-2">
        {moodleUrl && (
          <a
            href={moodleUrl}
            target="_blank"
            rel="noreferrer"
            className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            Abrir / editar en Moodle
          </a>
        )}
        <button
          type="button"
          onClick={onSync}
          disabled={syncing || !configured}
          className="rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {syncing ? 'Sincronizando…' : 'Sincronizar resultados'}
        </button>
        {lastSync && (
          <span className="text-xs text-slate-400">
            Últim. sync: {lastSync.toLocaleTimeString()}
          </span>
        )}
      </div>
    </section>
  );
}

function Stat({ label, value }) {
  return (
    <div className="rounded-lg bg-slate-50 p-2 text-center dark:bg-slate-800">
      <div className="text-lg font-semibold text-slate-800 dark:text-slate-100">{value}</div>
      <div className="text-xs text-slate-500">{label}</div>
    </div>
  );
}
