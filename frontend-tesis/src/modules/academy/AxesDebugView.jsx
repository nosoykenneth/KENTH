import React, { useEffect, useMemo, useState } from 'react';
import OllamaChat from '../../shared/components/ai/OllamaChat';
import {
  listAllLessons,
  getLesson,
  buildLessonActivityContext,
} from '../../shared/services/axesService';
import { createChatSession } from '../../shared/services/aiService';

/**
 * Panel de debug del tutor contextual sobre la estructura formal por ejes.
 *
 * Permite:
 *  1. Elegir una lección del curso (de cualquier eje cargado).
 *  2. Fijar un timestamp con un slider (si la lección tiene bloques de video).
 *  3. Ver el bloque resuelto en el cliente (mismo criterio que el backend).
 *  4. Lanzar preguntas al tutor con activity_context completo.
 *
 * No reemplaza la UI principal: vive como ruta /dashboard/debug-tutor.
 */

function findBlockAt(lesson, t) {
  if (!lesson || typeof t !== 'number') return null;
  const blocks = lesson.blocks || [];
  for (const b of blocks) {
    if (t >= b.start_time && t <= b.end_time) return b;
  }
  if (!blocks.length) return null;
  return blocks.reduce((best, b) => {
    const dist = t < b.start_time ? b.start_time - t : t > b.end_time ? t - b.end_time : 0;
    const bestDist = best
      ? t < best.start_time ? best.start_time - t : t > best.end_time ? t - best.end_time : 0
      : Infinity;
    return dist < bestDist ? b : best;
  }, null);
}

export default function AxesDebugView() {
  const [lessonsIndex, setLessonsIndex] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [lesson, setLesson] = useState(null);
  const [timestamp, setTimestamp] = useState(0);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listAllLessons()
      .then((items) => {
        setLessonsIndex(items);
        if (items.length && !selectedId) {
          setSelectedId(items[0].lesson_id);
        }
      })
      .catch((e) => console.error('[AXES]', e))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    getLesson(selectedId)
      .then((data) => {
        setLesson(data);
        setTimestamp(0);
      })
      .catch((e) => console.error('[AXES]', e));
  }, [selectedId]);

  const duration = useMemo(() => {
    if (!lesson?.blocks?.length) return 0;
    return lesson.blocks[lesson.blocks.length - 1].end_time;
  }, [lesson]);

  const hasVideoBlocks = duration > 0;

  const currentBlock = useMemo(
    () => (hasVideoBlocks ? findBlockAt(lesson, timestamp) : null),
    [lesson, timestamp, hasVideoBlocks],
  );

  const activityContext = useMemo(
    () => buildLessonActivityContext(lesson, hasVideoBlocks ? timestamp : null),
    [lesson, timestamp, hasVideoBlocks],
  );

  const ensureSession = async () => {
    if (sessionId) return sessionId;
    try {
      const created = await createChatSession(
        `Debug ${selectedId} ${new Date().toLocaleTimeString()}`,
      );
      setSessionId(created.id);
      return created.id;
    } catch (e) {
      console.error('[AXES] No se pudo crear sesion, usando id anonimo', e);
      const fallback = `debug-${Date.now()}`;
      setSessionId(fallback);
      return fallback;
    }
  };

  useEffect(() => {
    ensureSession();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (loading) {
    return (
      <div className="p-6 text-sm text-kenth-subtext">Cargando lecciones del curso...</div>
    );
  }

  if (!lessonsIndex.length) {
    return (
      <div className="p-6 text-sm text-red-400">
        No hay lecciones registradas en course_runtime/axes/.
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-80px)] w-full flex bg-kenth-bg overflow-hidden">
      {/* PANEL IZQUIERDO: CONTROLES */}
      <div className="w-[420px] border-r border-kenth-border flex flex-col gap-4 p-5 overflow-y-auto">
        <div>
          <p className="text-[10px] uppercase tracking-widest font-black text-kenth-brightred mb-2">
            Tutor contextual
          </p>
          <h2 className="text-lg font-black uppercase italic tracking-tight text-kenth-text">
            Debug por ejes
          </h2>
          <p className="text-xs text-kenth-subtext mt-1">
            Selecciona una lección, fija un timestamp (si hay video) y pregunta al tutor.
          </p>
        </div>

        <div>
          <label className="text-[10px] uppercase font-black tracking-widest text-kenth-subtext">
            Lección
          </label>
          <select
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
            className="mt-1 w-full bg-kenth-card border border-kenth-border rounded-xl px-3 py-2 text-sm text-kenth-text"
          >
            {lessonsIndex.map((p) => (
              <option key={p.lesson_id} value={p.lesson_id}>
                {p.lesson_id} — {p.lesson_title} ({p.axis_id})
              </option>
            ))}
          </select>
        </div>

        {lesson && (
          <>
            <div className="bg-kenth-card border border-kenth-border rounded-xl p-3 text-xs text-kenth-subtext">
              <p>
                <span className="font-bold text-kenth-text">Eje:</span> {lesson.axis_id}
              </p>
              <p className="mt-1">
                <span className="font-bold text-kenth-text">Goal:</span> {lesson.learning_goal}
              </p>
              <p className="mt-1">
                <span className="font-bold text-kenth-text">Action:</span>{' '}
                {lesson.expected_action}
              </p>
            </div>

            {hasVideoBlocks ? (
              <div>
                <label className="text-[10px] uppercase font-black tracking-widest text-kenth-subtext">
                  Timestamp ({Math.round(timestamp)}s / {duration}s)
                </label>
                <input
                  type="range"
                  min={0}
                  max={duration}
                  step={1}
                  value={timestamp}
                  onChange={(e) => setTimestamp(Number(e.target.value))}
                  className="w-full mt-2"
                />
                <div className="flex flex-wrap gap-1 mt-2">
                  {(lesson.blocks || []).map((b) => (
                    <button
                      key={b.block_id}
                      onClick={() => setTimestamp(b.start_time)}
                      className={`text-[10px] px-2 py-1 rounded-lg border transition ${
                        currentBlock?.block_id === b.block_id
                          ? 'bg-kenth-brightred text-white border-kenth-brightred'
                          : 'bg-kenth-card text-kenth-subtext border-kenth-border hover:border-kenth-brightred'
                      }`}
                      title={`${b.start_time}s - ${b.end_time}s`}
                    >
                      {b.block_title}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="bg-kenth-card border border-kenth-border rounded-xl p-3 text-[11px] text-kenth-subtext">
                Esta lección aún no tiene bloques de video segmentados.
                El tutor responderá con el contexto pedagógico de la lección
                (learning_goal, expected_action) y los recursos del eje.
              </div>
            )}

            {currentBlock && (
              <div className="bg-kenth-card border border-kenth-brightred/40 rounded-xl p-3 text-xs">
                <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">
                  Bloque activo
                </p>
                <p className="mt-1 font-bold text-kenth-text">
                  {currentBlock.block_id} — {currentBlock.block_title}
                </p>
                <p className="mt-1 text-kenth-subtext">{currentBlock.summary}</p>
                <p className="mt-2 text-[10px] uppercase tracking-widest text-kenth-subtext">
                  Modo: {currentBlock.interaction_mode}
                </p>
                {currentBlock.preguntas_probables?.length > 0 && (
                  <div className="mt-2">
                    <p className="text-[10px] uppercase tracking-widest text-kenth-subtext">
                      Preguntas probables
                    </p>
                    <ul className="list-disc list-inside text-kenth-text mt-1">
                      {currentBlock.preguntas_probables.map((q, i) => (
                        <li key={i}>{q}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <details className="bg-kenth-card border border-kenth-border rounded-xl p-3 text-[10px] text-kenth-subtext">
              <summary className="cursor-pointer font-bold uppercase tracking-widest">
                activity_context enviado
              </summary>
              <pre className="mt-2 whitespace-pre-wrap break-all">
                {JSON.stringify(activityContext, null, 2)}
              </pre>
            </details>
          </>
        )}
      </div>

      {/* PANEL DERECHO: CHAT */}
      <div className="flex-1 relative overflow-hidden">
        {sessionId ? (
          <OllamaChat
            sessionId={sessionId}
            contextoLeccion=""
            activityContext={activityContext}
          />
        ) : (
          <div className="p-6 text-sm text-kenth-subtext">Inicializando sesion...</div>
        )}
      </div>
    </div>
  );
}
