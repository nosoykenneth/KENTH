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
 *      por timestamp (ver `/sections/lessons/{id}/block?t=...`).
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

  // Reset al cambiar de recurso DURANTE el render (patrón recomendado de React),
  // en vez de un useEffect con setState que dispara renders en cascada.
  const [prevResourceId, setPrevResourceId] = useState(resourceId);
  if (resourceId !== prevResourceId) {
    setPrevResourceId(resourceId);
    setCurrentTimestamp(null);
  }

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
  const [muted, setMutedState] = useState(false);
  const thumbResolversRef = useRef([]);

  const getWin = useCallback(() => {
    try {
      return window.frames?.[iframeName]
        || document.querySelector(`iframe[name="${iframeName}"]`)?.contentWindow
        || null;
    } catch { return null; }
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

  const getMediaElements = useCallback(() => {
    const findMedia = (root) => {
      if (!root?.querySelector) return [];
      const direct = Array.from(root.querySelectorAll('video, audio') || []);
      const nodes = Array.from(root.querySelectorAll('*') || []);
      const nested = [];
      for (const node of nodes) {
        if (node.shadowRoot) nested.push(...findMedia(node.shadowRoot));
      }
      return [...direct, ...nested];
    };
    const walk = (win, depth = 0) => {
      if (!win || depth > 4) return [];
      try {
        const doc = win.document;
        const media = findMedia(doc);
        const frames = Array.from(doc?.querySelectorAll?.('iframe') || []);
        for (const frame of frames) {
          media.push(...walk(frame.contentWindow, depth + 1));
        }
        return media;
      } catch {
        return [];
      }
    };
    return walk(getWin());
  }, [getWin]);

  const withMedia = useCallback((fn) => {
    const media = getMediaElements();
    if (!media.length) return false;
    try {
      media.forEach(fn);
      return true;
    } catch {
      return false;
    }
  }, [getMediaElements]);

  const hideNativeControls = useCallback(() => {
    post({ type: 'kenth:cmd', action: 'hideControls' });
    return withMedia((media) => {
      media.controls = false;
      media.removeAttribute('controls');
      media.setAttribute('controlsList', 'nodownload nofullscreen noremoteplayback');
    });
  }, [post, withMedia]);

  const seek = useCallback((seconds) => {
    const next = Number(seconds);
    const ok = post({ type: 'kenth:cmd', action: 'seek', seconds: next });
    if (Number.isFinite(next)) {
      setCurrentTimestamp(Math.max(0, next));
      withMedia((media) => { media.currentTime = Math.max(0, next); });
    }
    return ok;
  }, [post, withMedia]);

  const play = useCallback(() => {
    const ok = post({ type: 'kenth:cmd', action: 'play' });
    withMedia((media) => {
      const result = media.play?.();
      if (result?.catch) result.catch(() => {});
    });
    return ok;
  }, [post, withMedia]);

  const pause = useCallback(() => {
    const ok = post({ type: 'kenth:cmd', action: 'pause' });
    withMedia((media) => { media.pause?.(); });
    return ok;
  }, [post, withMedia]);

  const setMuted = useCallback((nextMuted) => {
    const next = Boolean(nextMuted);
    setMutedState(next);
    const ok = post({ type: 'kenth:cmd', action: 'setMuted', muted: next });
    const applyMuted = (media) => {
      media.muted = next;
      media.defaultMuted = next;
      if (!next && media.volume === 0) media.volume = 0.8;
      if (next) media.setAttribute('muted', '');
      else media.removeAttribute('muted');
    };
    const directOk = withMedia(applyMuted);
    return ok || directOk;
  }, [post, withMedia]);
  const toggleMute = useCallback(() => setMuted(!muted), [muted, setMuted]);
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
        // Fracción (no floor): el resaltado de subtítulos necesita seguir el
        // audio con precisión; el bridge ya emite ~4 veces/seg con decimales.
        if (Number.isFinite(seconds)) setCurrentTimestamp(Math.max(0, seconds));
        if (typeof data.muted === 'boolean') setMutedState(data.muted);
      } else if (data.type === 'kenth:resource_meta') {
        setMeta({
          duration: Number.isFinite(data.duration) ? data.duration : null,
          videoWidth: data.videoWidth || 0,
          videoHeight: data.videoHeight || 0,
          src: data.src || '',
          ready: !!data.ready,
        });
        if (typeof data.muted === 'boolean') setMutedState(data.muted);
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

  // Reset de estado al cambiar de recurso DURANTE el render (evita setState en
  // cascada dentro de un efecto). La limpieza de promesas pendientes va en el
  // cleanup de un efecto aparte, porque es un side-effect (no setState).
  const [prevResourceId, setPrevResourceId] = useState(resourceId);
  if (resourceId !== prevResourceId) {
    setPrevResourceId(resourceId);
    setCurrentTimestamp(null);
    setMeta(null);
    setMutedState(false);
  }

  useEffect(() => {
    return () => {
      thumbResolversRef.current.forEach((r) => r.resolve(''));
      thumbResolversRef.current = [];
    };
  }, [resourceId]);

  return {
    currentTimestamp,
    meta,
    duration: meta?.duration ?? null,
    seek,
    play,
    pause,
    muted,
    setMuted,
    toggleMute,
    hideNativeControls,
    requestMeta,
    requestThumbnail,
  };
}

export default useResourceTimestamp;
