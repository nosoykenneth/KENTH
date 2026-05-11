import { useEffect, useState } from 'react';

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
 *      resolver de bloque del piloto ya sabe devolver el bloque activo
 *      por minuto (ver `/pilot/lessons/{id}/block?t=...`).
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

export default useResourceTimestamp;
