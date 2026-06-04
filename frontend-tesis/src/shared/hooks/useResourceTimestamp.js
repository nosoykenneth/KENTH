import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * useResourceTimestamp
 *
 * Adapter / hook preparado para alimentar `current_timestamp` al
 * activity_context cuando el recurso abierto (video/H5P) exponga su
 * tiempo de reproduccion al frontend.
 *
 * Estado actual (fase 1):
 *   - El iframe H5P de Moodle NO retransmite eventos xAPI al window
 *     padre por defecto (mismo origen pero sin bridge). Por eso este
 *     hook permanece "armado pero inactivo": expone `currentTimestamp`
 *     en null y solo escucha mensajes con la forma esperada si llegan.
 *
 * Como activarlo en fase 2 (orden de costo creciente):
 *   1. Bridge ligero: agregar un pequeno snippet al view de Moodle
 *      (tesis_view.php) que, si H5P esta presente, haga
 *      `parent.postMessage({ type: 'kenth:resource_time', seconds }, '*')`
 *      en eventos play/pause/seek. Este hook ya lo recoge.
 *   2. xAPI completo: capturar `H5P.externalDispatcher` (mismo origen) y
 *      mandar al padre los verbos relevantes (played, paused, seeked,
 *      answered) ademas del segundo actual.
 *   3. Backend: cuando el payload incluya `current_timestamp`, el
 *      resolver de bloque ya sabe devolver el bloque activo del video
 *      por timestamp (ver `/axes/lessons/{id}/block?t=...`).
 *
 * Forma de los mensajes que ya quedan soportados:
 *   { type: 'kenth:resource_time', seconds: <number> }
 *   { type: 'kenth:resource_time', timestamp: <number> }
 *
 * @param {object} options
 * @param {boolean} [options.enabled=true]  Si false, no instala listener.
 * @param {string|number} [options.resourceId]  cmid del recurso activo. Usado
 *   para filtrar mensajes si el bridge lo incluye (`resourceId`).
 * @returns {{ currentTimestamp: number|null, reset: () => void }}
 */
export function useResourceTimestamp({ enabled = true, resourceId = null } = {}) {
  const [currentTimestamp, setCurrentTimestamp] = useState(null);

  useEffect(() => {
    if (!enabled) return undefined;

    const onMessage = (event) => {
      const data = event?.data;
      if (!data || typeof data !== 'object') return;
      if (data.type !== 'kenth:resource_time') return;

      // Filtro opcional por recurso (si el bridge lo pasa).
      if (
        resourceId != null &&
        data.resourceId != null &&
        String(data.resourceId) !== String(resourceId)
      ) {
        return;
      }

      const raw = data.seconds ?? data.timestamp;
      const seconds = typeof raw === 'number' ? raw : parseFloat(raw);
      if (Number.isFinite(seconds)) {
        setCurrentTimestamp(Math.max(0, Math.floor(seconds)));
      }
    };

    window.addEventListener('message', onMessage);
    return () => window.removeEventListener('message', onMessage);
  }, [enabled, resourceId]);

  // Reset cuando cambia el recurso (evita arrastrar el ultimo timestamp
  // de un video anterior al abrir otro).
  useEffect(() => {
    setCurrentTimestamp(null);
  }, [resourceId]);

  return {
    currentTimestamp,
    reset: () => setCurrentTimestamp(null),
  };
}

/**
 * useResourceVideoBridge
 *
 * Version "completa" del bridge para el EDITOR de leccion. Ademas del
 * timestamp en vivo (igual que useResourceTimestamp), expone:
 *   - meta: { duration, videoWidth, videoHeight, src, ready } del <video>
 *     real dentro del H5P (lo emite el wrapper de tesis_view.php).
 *   - duration: atajo de meta.duration.
 *   - senders al wrapper (postMessage al iframe por nombre):
 *       seek(seconds), play(), pause(), requestMeta(),
 *       requestThumbnail(time) -> Promise<dataUrl>.
 *
 * El canal es el mismo que ya emite 'kenth:resource_time'; aqui solo se
 * agregan los mensajes nuevos ('kenth:resource_meta' / '..._thumbnail') y
 * el envio de comandos ('kenth:cmd'). El trabajo pesado (acceso al DOM del
 * video, canvas) lo hace el wrapper, que es mismo-origen que el H5P.
 *
 * @param {object} options
 * @param {boolean} [options.enabled=true]
 * @param {string|number} [options.resourceId]  cmid del recurso (filtra mensajes
 *   y se incluye en los comandos para que el wrapper correcto responda).
 * @param {string} [options.iframeName='moodle_view_iframe']  name del iframe destino.
 */
export function useResourceVideoBridge({
  enabled = true,
  resourceId = null,
  iframeName = 'moodle_view_iframe',
} = {}) {
  const [currentTimestamp, setCurrentTimestamp] = useState(null);
  const [meta, setMeta] = useState(null);
  const thumbResolversRef = useRef([]);

  const getWin = useCallback(() => {
    try { return window.frames?.[iframeName] || null; } catch { return null; }
  }, [iframeName]);

  const post = useCallback((payload) => {
    const win = getWin();
    if (!win) return false;
    try {
      win.postMessage(
        { ...payload, ...(resourceId != null ? { resourceId } : {}) },
        '*',
      );
      return true;
    } catch { return false; }
  }, [getWin, resourceId]);

  const seek = useCallback((seconds) => post({ type: 'kenth:cmd', action: 'seek', seconds }), [post]);
  const play = useCallback(() => post({ type: 'kenth:cmd', action: 'play' }), [post]);
  const pause = useCallback(() => post({ type: 'kenth:cmd', action: 'pause' }), [post]);
  const requestMeta = useCallback(() => post({ type: 'kenth:cmd', action: 'meta' }), [post]);
  const requestThumbnail = useCallback((time) => new Promise((resolve) => {
    thumbResolversRef.current.push({ time, resolve });
    const ok = post({ type: 'kenth:cmd', action: 'thumbnail', time });
    if (!ok) {
      // Sin iframe disponible todavia: resolver vacio para no colgar.
      const idx = thumbResolversRef.current.findIndex((r) => r.time === time);
      if (idx >= 0) thumbResolversRef.current.splice(idx, 1);
      resolve('');
    }
  }), [post]);

  useEffect(() => {
    if (!enabled) return undefined;

    const onMessage = (event) => {
      const data = event?.data;
      if (!data || typeof data !== 'object') return;
      if (
        resourceId != null &&
        data.resourceId != null &&
        String(data.resourceId) !== String(resourceId)
      ) {
        return;
      }

      if (data.type === 'kenth:resource_time') {
        const raw = data.seconds ?? data.timestamp;
        const seconds = typeof raw === 'number' ? raw : parseFloat(raw);
        if (Number.isFinite(seconds)) setCurrentTimestamp(Math.max(0, Math.floor(seconds)));
      } else if (data.type === 'kenth:resource_meta') {
        setMeta({
          duration: Number.isFinite(data.duration) ? data.duration : null,
          videoWidth: data.videoWidth || 0,
          videoHeight: data.videoHeight || 0,
          src: data.src || '',
          ready: !!data.ready,
        });
      } else if (data.type === 'kenth:resource_thumbnail') {
        const resolvers = thumbResolversRef.current;
        if (resolvers.length) {
          let idx = resolvers.findIndex((r) => Math.abs(r.time - data.time) < 0.5);
          if (idx < 0) idx = 0;
          const [r] = resolvers.splice(idx, 1);
          r.resolve(data.dataUrl || '');
        }
      }
    };

    window.addEventListener('message', onMessage);
    return () => window.removeEventListener('message', onMessage);
  }, [enabled, resourceId]);

  // Reset al cambiar de recurso.
  useEffect(() => {
    setCurrentTimestamp(null);
    setMeta(null);
    thumbResolversRef.current.forEach((r) => r.resolve(''));
    thumbResolversRef.current = [];
  }, [resourceId]);

  return {
    currentTimestamp,
    meta,
    duration: meta?.duration ?? null,
    seek,
    play,
    pause,
    requestMeta,
    requestThumbnail,
  };
}

export default useResourceTimestamp;
