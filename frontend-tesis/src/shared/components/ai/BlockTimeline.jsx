import React, { useCallback, useEffect, useRef, useState } from 'react';
import { fmtTime } from '../../utils/time';

/**
 * BlockTimeline
 *
 * Linea de tiempo del video (estilo YouTube) donde cada BLOQUE de la leccion
 * es un segmento de color entre su start_time y end_time. Permite:
 *   - click en la pista vacia: seek a ese segundo.
 *   - click en un bloque: seleccionarlo + seek a su inicio.
 *   - arrastrar los bordes de un bloque: ajustar start_time / end_time.
 *   - hover: muestra miniatura del frame + timestamp (via requestThumbnail).
 *   - playhead sincronizado a currentTime.
 *
 * Props:
 *   - blocks: [{ start_time, end_time, block_title, interaction_mode }]
 *   - duration: number (segundos). Si null/0, la pista se muestra deshabilitada.
 *   - currentTime: number (segundos) del playhead.
 *   - selectedIndex: number | -1
 *   - onSelectBlock(idx)
 *   - onSeek(seconds)
 *   - onChangeBlockTime(idx, { start_time?, end_time? })
 *   - requestThumbnail(seconds) => Promise<dataUrl>
 */

// Color del bloque por su modo pedagogico (interaction_mode), agrupado por FAMILIA
// para que los modos reales del profe no caigan todos al rojo por defecto.
// Solo afecta el color de la timeline (frontend). No toca BD, backend, enum ni RAG.
const FAMILY = {
  indigo: 'bg-indigo-500/40 border-indigo-400/70',
  emerald: 'bg-emerald-500/40 border-emerald-400/70',
  rose: 'bg-rose-500/40 border-rose-400/70',
  amber: 'bg-amber-500/40 border-amber-400/70',
  sky: 'bg-sky-500/40 border-sky-400/70',
};
const MODE_COLORS = {
  // indigo — teoria
  teoria: FAMILY.indigo,
  teoria_aplicada: FAMILY.indigo,
  // verde — practica
  practica: FAMILY.emerald,
  demostracion_practica: FAMILY.emerald,
  // rosa — diagnostico / troubleshooting
  diagnostico_guiado: FAMILY.rose,
  troubleshooting: FAMILY.rose,
  verificacion: FAMILY.rose,
  // ambar — criterio
  criterio_operativo: FAMILY.amber,
  criterio_de_decision: FAMILY.amber,
  // azul cielo — navegacion / apertura / cierre
  navegacion_de_recurso: FAMILY.sky,
  orientacion_inicial: FAMILY.sky,
  cierre_reflexivo: FAMILY.sky,
  comparacion_contextual: FAMILY.sky,
};
const DEFAULT_COLOR = 'bg-kenth-brightred/40 border-kenth-brightred/70';

// Resuelve el color tolerando mayusculas/espacios; cualquier modo no listado -> rojo.
const colorForMode = (mode) => MODE_COLORS[(mode || '').trim().toLowerCase()] || DEFAULT_COLOR;

export default function BlockTimeline({
  blocks = [],
  duration = 0,
  currentTime = 0,
  selectedIndex = -1,
  onSelectBlock,
  onSeek,
  onChangeBlockTime,
  requestThumbnail,
  transcript = [],
  // Vista Profesor: sin edición de tiempos. Los bloques se pueden seleccionar
  // (click -> seek) pero NO arrastrar; no se muestran los handles de borde.
  readOnly = false,
  // Etiquetas humanas (el profesor ve "Momentos de la clase", no "bloques").
  title = 'Línea de tiempo',
  unitLabel = 'bloque',
  itemPrefix = 'B',
}) {
  const trackRef = useRef(null);
  const scrubRef = useRef(null);
  const [drag, setDrag] = useState(null); // { idx, edge: 'start'|'end' }
  const [scrubbing, setScrubbing] = useState(false);
  const [scrubPreviewTime, setScrubPreviewTime] = useState(null);
  const dragOriginRef = useRef(null); // snapshot de tiempos al iniciar el arrastre
  const dragStateRef = useRef({ startX: 0, moved: false }); // para distinguir clic de arrastre

  const beginDrag = (idx, edge, clientX = 0) => {
    dragOriginRef.current = blocks.map((bb) => ({ s: Number(bb.start_time) || 0, e: Number(bb.end_time) || 0 }));
    dragStateRef.current = { startX: clientX, moved: false };
    setDrag({ idx, edge });
  };
  const [hover, setHover] = useState(null); // { x, time }
  const [thumb, setThumb] = useState(''); // dataUrl
  const [hoverSeg, setHoverSeg] = useState(-1); // segmento de subtítulo bajo el cursor
  const thumbTimerRef = useRef(null);
  const lastThumbTimeRef = useRef(-1);

  const hasDuration = Number.isFinite(duration) && duration > 0;
  const displayTime = scrubPreviewTime ?? currentTime;

  const pct = useCallback((t) => {
    if (!hasDuration) return 0;
    return Math.min(100, Math.max(0, (t / duration) * 100));
  }, [duration, hasDuration]);

  const timeFromClientX = useCallback((clientX) => {
    const el = trackRef.current;
    if (!el || !hasDuration) return 0;
    const rect = el.getBoundingClientRect();
    const ratio = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width));
    return ratio * duration;
  }, [duration, hasDuration]);

  const scrubTimeFromClientX = useCallback((clientX) => {
    const el = scrubRef.current;
    if (!el || !hasDuration) return 0;
    const rect = el.getBoundingClientRect();
    const ratio = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width));
    return ratio * duration;
  }, [duration, hasDuration]);

  const seekFromScrubX = useCallback((clientX) => {
    if (!hasDuration) return;
    const nextTime = scrubTimeFromClientX(clientX);
    setScrubPreviewTime(nextTime);
    onSeek?.(nextTime);
  }, [hasDuration, onSeek, scrubTimeFromClientX]);

  const beginScrub = (e) => {
    if (!hasDuration) return;
    e.preventDefault();
    setScrubbing(true);
    seekFromScrubX(e.clientX);
  };

  useEffect(() => {
    if (!scrubbing) return undefined;
    const onMove = (e) => {
      e.preventDefault();
      seekFromScrubX(e.clientX);
    };
    const onUp = () => setScrubbing(false);
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
    return () => {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
    };
  }, [scrubbing, seekFromScrubX]);

  // Si el tiempo real del video alcanzó el preview de scrub, ocúltalo durante el
  // render (en vez de setState dentro de un efecto, que encadena renders).
  if (
    scrubPreviewTime != null &&
    Math.abs((Number(currentTime) || 0) - scrubPreviewTime) < 0.5
  ) {
    setScrubPreviewTime(null);
  }

  useEffect(() => {
    if (scrubPreviewTime == null) return undefined;
    const timeout = setTimeout(() => setScrubPreviewTime(null), 900);
    return () => clearTimeout(timeout);
  }, [scrubPreviewTime]);

  // ---- Drag de bordes: borde compartido. Al arrastrar, solo el bloque vecino
  // inmediato se achica/crece (su borde lejano queda fijo); el resto no se mueve.
  // Tope = borde lejano del vecino (≈ inicio del bloque siguiente a esos dos).
  useEffect(() => {
    if (!drag) return undefined;
    const MIN = 1; // duración mínima de un bloque (s)
    const orig = dragOriginRef.current;
    if (!orig) return undefined;

    const onMove = (e) => {
      const t = timeFromClientX(e.clientX);
      const i = drag.idx;
      const o = orig[i];
      if (!o) return;
      const trackW = trackRef.current?.clientWidth || 1;
      const snap = duration > 0 ? (7 / trackW) * duration : 0.5; // imán ~7px

      if (drag.edge === 'move') {
        // Mover el bloque completo (conserva duración), topado entre el vecino
        // izquierdo y el derecho. No empuja a nadie.
        const dur = o.e - o.s;
        const dx = e.clientX - dragStateRef.current.startX;
        if (!dragStateRef.current.moved && Math.abs(dx) < 4) return; // umbral clic vs arrastre
        dragStateRef.current.moved = true;
        const deltaSec = duration > 0 ? (dx / trackW) * duration : 0;
        const prev = orig[i - 1];
        const next = orig[i + 1];
        const lower = prev ? prev.e : 0;
        const rightEdge = next ? next.s : duration;
        const upper = rightEdge - dur;
        let ns = Math.max(lower, Math.min(o.s + deltaSec, upper));
        if (Math.abs(ns - lower) <= snap) ns = lower; // imán al vecino izquierdo
        if (Math.abs((ns + dur) - rightEdge) <= snap) ns = rightEdge - dur; // imán al derecho
        onChangeBlockTime?.(i, { start_time: ns, end_time: ns + dur });
      } else if (drag.edge === 'end') {
        const next = orig[i + 1];
        let end = Math.max(t, o.s + MIN);
        if (next) {
          end = Math.min(end, next.e - MIN); // tope: borde lejano del vecino (≈ inicio del 3.º)
          if (Math.abs(end - next.s) <= snap) end = next.s; // imán al punto de unión original
          onChangeBlockTime?.(i, { end_time: end });
          if (end > next.s) {
            // Achicar el vecino desde la izquierda (su fin queda fijo).
            onChangeBlockTime?.(i + 1, { start_time: end, end_time: next.e });
          } else {
            // Antes de unirse: vecino intacto (sin solape).
            onChangeBlockTime?.(i + 1, { start_time: next.s, end_time: next.e });
          }
        } else {
          onChangeBlockTime?.(i, { end_time: Math.min(end, duration) });
        }
      } else {
        const prev = orig[i - 1];
        let start = Math.max(Math.min(t, o.e - MIN), 0);
        if (prev) {
          start = Math.max(start, prev.s + MIN); // tope: borde lejano del vecino
          if (Math.abs(start - prev.e) <= snap) start = prev.e; // imán
          onChangeBlockTime?.(i, { start_time: start });
          if (start < prev.e) {
            // Achicar el vecino desde la derecha (su inicio queda fijo).
            onChangeBlockTime?.(i - 1, { start_time: prev.s, end_time: start });
          } else {
            onChangeBlockTime?.(i - 1, { start_time: prev.s, end_time: prev.e });
          }
        } else {
          onChangeBlockTime?.(i, { start_time: start });
        }
      }
    };
    const onUp = () => {
      // Si fue un clic (no hubo arrastre real) sobre el cuerpo: seleccionar + ir.
      if (drag.edge === 'move' && !dragStateRef.current.moved) {
        onSelectBlock?.(drag.idx);
        onSeek?.(orig[drag.idx]?.s || 0);
      }
      setDrag(null);
    };
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
  }, [drag, duration, timeFromClientX, onChangeBlockTime, onSelectBlock, onSeek]);

  // ---- Hover + miniatura (throttled) ----
  const handleTrackMove = (e) => {
    if (drag || !hasDuration) return;
    const el = trackRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const time = timeFromClientX(e.clientX);
    setHover({ x, time, width: rect.width });

    if (!requestThumbnail) return;
    if (thumbTimerRef.current) return; // throttle
    thumbTimerRef.current = setTimeout(() => {
      thumbTimerRef.current = null;
    }, 140);
    if (Math.abs(time - lastThumbTimeRef.current) < 0.4) return;
    lastThumbTimeRef.current = time;
    Promise.resolve(requestThumbnail(time)).then((url) => {
      if (url) setThumb(url);
    }).catch(() => {});
  };

  const handleTrackLeave = () => {
    setHover(null);
  };

  const handleTrackClick = (e) => {
    if (drag || !hasDuration) return;
    // Si el click cae sobre un bloque, lo maneja el bloque (stopPropagation).
    const t = timeFromClientX(e.clientX);
    onSeek?.(t);
  };

  return (
    <div className="w-full select-none">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-[10px] uppercase tracking-widest text-kenth-subtext font-bold">
          {title} · {blocks.length} {unitLabel}{blocks.length === 1 ? '' : 's'}
        </span>
        <span className="text-[10px] font-mono text-kenth-subtext">
          {fmtTime(displayTime)} {hasDuration ? `/ ${fmtTime(duration)}` : ''}
        </span>
      </div>

      <div className="relative">
        {/* Carril independiente de navegacion: no edita bloques, solo mueve el video. */}
        <div className="mb-2">
          <div
            ref={scrubRef}
            onPointerDown={beginScrub}
            className={`relative h-11 rounded-lg border border-kenth-border bg-kenth-bg/70 overflow-hidden touch-none ${hasDuration ? 'cursor-ew-resize' : 'opacity-50 cursor-not-allowed'}`}
            title="Arrastra o haz clic para mover la marca de tiempo"
          >
            {hasDuration ? (
              <>
                <div className="absolute left-0 right-0 top-5 h-1 rounded-full bg-kenth-surface/40" />
                <div
                  className="absolute left-0 top-5 h-1 rounded-full bg-kenth-brightred"
                  style={{ width: `${pct(displayTime)}%` }}
                />
                {Array.from({ length: 6 }).map((_, i) => {
                  const ratio = i / 5;
                  const time = ratio * duration;
                  return (
                    <div
                      key={i}
                      className="absolute top-0 h-full -translate-x-1/2 pointer-events-none"
                      style={{ left: `${ratio * 100}%` }}
                    >
                      <div className="mx-auto h-3 w-px bg-white/35" />
                      <div className="mt-4 h-3 w-px bg-white/20" />
                      <span className="absolute top-1 left-2 text-[9px] font-mono text-kenth-subtext whitespace-nowrap">
                        {fmtTime(time)}
                      </span>
                    </div>
                  );
                })}
                <div
                  className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 z-20 pointer-events-none"
                  style={{ left: `${pct(displayTime)}%` }}
                >
                  <div className={`h-8 w-0.5 ${scrubbing ? 'bg-kenth-brightred' : 'bg-white'} shadow-[0_0_8px_rgba(255,255,255,0.65)]`} />
                  <div className={`absolute -top-1 left-1/2 -translate-x-1/2 h-3.5 w-3.5 rounded-full border-2 border-kenth-bg ${scrubbing ? 'bg-kenth-brightred' : 'bg-white'}`} />
                </div>
              </>
            ) : (
              <div className="absolute inset-0 flex items-center justify-center text-[10px] text-kenth-subtext uppercase tracking-widest">
                Esperando metadatos del video...
              </div>
            )}
          </div>
        </div>

        {/* Tooltip de miniatura en hover */}
        {hover && (
          <div
            className="absolute -top-2 -translate-y-full -translate-x-1/2 z-30 pointer-events-none"
            style={{ left: `${Math.min(Math.max(hover.x, 60), (hover.width || 0) - 60)}px` }}
          >
            <div className="rounded-lg overflow-hidden border border-kenth-border bg-black shadow-xl">
              {thumb ? (
                <img src={thumb} alt="frame" className="w-40 h-auto block" />
              ) : (
                <div className="w-40 h-[90px] flex items-center justify-center text-[10px] text-kenth-subtext">
                  …
                </div>
              )}
              <div className="text-center text-[10px] font-mono text-white py-0.5 bg-black/80">
                {fmtTime(hover.time)}
              </div>
            </div>
          </div>
        )}

        {/* Pista */}
        <div
          ref={trackRef}
          onMouseMove={handleTrackMove}
          onMouseLeave={handleTrackLeave}
          onClick={handleTrackClick}
          className={`relative h-12 rounded-lg border border-kenth-border bg-kenth-surface/10 overflow-hidden ${hasDuration ? 'cursor-pointer' : 'opacity-50 cursor-not-allowed'}`}
        >
          {!hasDuration && (
            <div className="absolute inset-0 flex items-center justify-center text-[10px] text-kenth-subtext uppercase tracking-widest">
              Esperando metadatos del video…
            </div>
          )}

          {/* Bloques */}
          {hasDuration && blocks.map((b, idx) => {
            const start = Number(b.start_time) || 0;
            const end = Number(b.end_time) || start;
            const left = pct(start);
            const width = Math.max(0.5, pct(end) - left);
            const selected = idx === selectedIndex;
            const color = colorForMode(b.interaction_mode);
            return (
              <div
                key={b.block_id || idx}
                onMouseDown={readOnly ? undefined : (e) => { e.stopPropagation(); beginDrag(idx, 'move', e.clientX); }}
                onClick={readOnly
                  ? (e) => { e.stopPropagation(); onSelectBlock?.(idx); onSeek?.(start); }
                  : (e) => e.stopPropagation()}
                title={b.block_title || `${idx + 1}`}
                className={`absolute top-0 h-full ${readOnly ? 'cursor-pointer' : 'cursor-grab active:cursor-grabbing'} border-l border-r ${color} transition-colors ${selected ? 'ring-2 ring-inset ring-white/80 z-10' : 'hover:brightness-125'}`}
                style={{ left: `${left}%`, width: `${width}%` }}
              >
                <span className="absolute left-1 top-0.5 text-[9px] font-bold text-white/90 truncate max-w-full pr-1 pointer-events-none">
                  {b.block_title || `${itemPrefix}${idx + 1}`}
                </span>
                {/* Handles de borde (solo edición técnica; el profesor no ajusta tiempos) */}
                {!readOnly && (
                  <>
                    <div
                      onMouseDown={(e) => { e.stopPropagation(); beginDrag(idx, 'start'); }}
                      className="absolute left-0 top-0 h-full w-1.5 -ml-0.5 cursor-ew-resize bg-white/0 hover:bg-white/60"
                    />
                    <div
                      onMouseDown={(e) => { e.stopPropagation(); beginDrag(idx, 'end'); }}
                      className="absolute right-0 top-0 h-full w-1.5 -mr-0.5 cursor-ew-resize bg-white/0 hover:bg-white/60"
                    />
                  </>
                )}
              </div>
            );
          })}

          {/* Playhead */}
          {hasDuration && (
            <div
              className="absolute top-0 h-full w-0.5 bg-white shadow-[0_0_6px_rgba(255,255,255,0.8)] z-20 pointer-events-none"
              style={{ left: `${pct(displayTime)}%` }}
            >
              <div className="absolute -top-1 -translate-x-1/2 w-2.5 h-2.5 rounded-full bg-white" />
            </div>
          )}
        </div>

        {/* Carril de subtítulos (transcripción) alineado al mismo tiempo.
            Los chips no llevan texto (serían ilegibles con muchos segmentos);
            el texto del segmento activo/hover se muestra en la línea de caption. */}
        {hasDuration && transcript.length > 0 && (() => {
          let activeSeg = -1;
          for (let i = 0; i < transcript.length; i += 1) {
            const s = transcript[i];
            if (Number(s.start_time) <= displayTime && displayTime < Number(s.end_time)) { activeSeg = i; break; }
          }
          const captionIdx = hoverSeg >= 0 ? hoverSeg : activeSeg;
          const caption = captionIdx >= 0 ? (transcript[captionIdx]?.text || '') : '';
          return (
            <div className="mt-1.5">
              <div className="flex items-baseline gap-2 mb-0.5">
                <span className="text-[9px] uppercase tracking-widest text-indigo-300/70 font-bold flex-shrink-0">Subtítulos</span>
                <span className="text-[11px] text-indigo-100/90 truncate italic">
                  {caption || <span className="text-kenth-subtext not-italic">— pasa el cursor o reproduce para ver el texto —</span>}
                </span>
              </div>
              <div
                className="relative h-3 rounded-md border border-kenth-border bg-kenth-surface/5 overflow-hidden"
                onMouseLeave={() => setHoverSeg(-1)}
              >
                {transcript.map((s, i) => {
                  const start = Number(s.start_time) || 0;
                  const end = Number(s.end_time) || start;
                  const left = pct(start);
                  const width = Math.max(0.25, pct(end) - left);
                  const active = i === activeSeg;
                  const hovered = i === hoverSeg;
                  const shade = active ? 'bg-indigo-400/80' : hovered ? 'bg-indigo-400/60' : (i % 2 ? 'bg-indigo-500/30' : 'bg-indigo-500/20');
                  return (
                    <div
                      key={i}
                      onClick={() => onSeek?.(start)}
                      onMouseEnter={() => setHoverSeg(i)}
                      className={`absolute top-0 h-full cursor-pointer ${shade}`}
                      style={{ left: `${left}%`, width: `${width}%` }}
                    />
                  );
                })}
                <div
                  className="absolute top-0 h-full w-0.5 bg-white/80 z-10 pointer-events-none"
                  style={{ left: `${pct(displayTime)}%` }}
                />
              </div>
            </div>
          );
        })()}
      </div>
    </div>
  );
}
