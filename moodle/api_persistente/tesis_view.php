<?php
// tesis_view.php - Tunel para VER y RESPONDER actividades (Estudiantes)
//
// Bridge fase 2 INSTRUMENTADO. Mismo flujo de doble redirect (sale del
// proxy Vite via $CFG->wwwroot, luego sirve el wrapper HTML), pero el
// JS del wrapper ahora:
//
//   - escribe logs con prefijo [KENTH BRIDGE] en cada paso clave,
//   - busca H5P y <video> RECURSIVAMENTE en iframes anidados (hvp
//     embebe el player real en un sub-iframe propio, dos niveles bajo
//     nuestro wrapper),
//   - reporta exactamente que paso encuentra y cual falla.

require(__DIR__ . '/../../config.php');

$token   = required_param('token',   PARAM_ALPHANUM);
$cmid    = required_param('cmid',    PARAM_INT);
$modname = required_param('modname', PARAM_TEXT);
$wrap    = optional_param('_wrap',   0, PARAM_INT);
$hidefs  = optional_param('hidefs',  0, PARAM_INT); // ocultar boton fullscreen (editor)

global $DB, $USER, $CFG;

$token_record = $DB->get_record('external_tokens', array('token' => $token));
if (!$token_record) {
    die('Acceso denegado: Token invalido.');
}

$user = $DB->get_record('user', array('id' => $token_record->userid, 'deleted' => 0));
if (!$user) {
    die('Acceso denegado.');
}

complete_user_login($user);

$is_h5p = ($modname === 'hvp' || $modname === 'h5pactivity');

// ---------------------------------------------------------------------------
// CASO H5P, fase 1: salir del proxy Vite hacia el origen real de Moodle.
// ---------------------------------------------------------------------------
if ($is_h5p && !$wrap) {
    $wrapper_url = new moodle_url('/proyecto_curso/api_persistente/tesis_view.php', array(
        'token'   => $token,
        'cmid'    => $cmid,
        'modname' => $modname,
        '_wrap'   => 1,
        'hidefs'  => $hidefs,
    ));
    redirect($wrapper_url);
}

// ---------------------------------------------------------------------------
// CASO H5P, fase 2: wrapper HTML con bridge instrumentado.
// ---------------------------------------------------------------------------
if ($is_h5p && $wrap) {
    $embed_path  = '/mod/hvp/embed.php?id=' . (int)$cmid;
    $resource_id = (int)$cmid;

    header('Content-Type: text/html; charset=UTF-8');
    header_remove('X-Frame-Options');
    ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>KENTH H5P Wrapper</title>
    <style>
        html, body { margin: 0; padding: 0; height: 100%; width: 100%; background: transparent; overflow: hidden; }
        #kenth-h5p-inner { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; display: block; background: transparent; }
    </style>
</head>
<body>
    <iframe
        id="kenth-h5p-inner"
        name="kenth_h5p_inner"
        src="<?php echo htmlspecialchars($embed_path, ENT_QUOTES, 'UTF-8'); ?>"
        allow="fullscreen *; microphone *; camera *"
        allowfullscreen
        scrolling="no"
        title="H5P Player"
    ></iframe>

    <script>
    (function () {
        var TAG = '[KENTH BRIDGE]';
        var RESOURCE_ID = <?php echo (int)$resource_id; ?>;
        var HIDE_FS = <?php echo $hidefs ? 'true' : 'false'; ?>;
        var inner = document.getElementById('kenth-h5p-inner');

        function log()  { try { var a = ['%c'+TAG, 'color:#0bd; font-weight:bold'].concat([].slice.call(arguments)); console.log.apply(console, a); } catch (e) {} }
        function warn() { try { var a = ['%c'+TAG, 'color:#f80; font-weight:bold'].concat([].slice.call(arguments)); console.warn.apply(console, a); } catch (e) {} }

        log('wrapper loaded, RESOURCE_ID =', RESOURCE_ID);

        // Throttle: solo reemitir cuando cambie el segundo entero o
        // pase un tiempo prudente desde el ultimo envio.
        var lastSecond = -1;
        var lastSentAt = 0;
        var h5pReadyEmitted = false;

        function emit(seconds, reason) {
            if (typeof seconds !== 'number' || !isFinite(seconds) || seconds < 0) return;
            // Alta resolucion para que el resaltado de subtitulos siga el audio:
            // emitir con decimales cuando el tiempo cambie >=0.12s. En pausa no
            // hay cambio, asi que no genera spam.
            if (Math.abs(seconds - lastSecond) < 0.08) return;
            lastSecond = seconds;
            lastSentAt = Date.now();
            try {
                var muteHit = findBestVideo(inner.contentWindow);
                var muteVideo = muteHit && muteHit.v;
                window.parent.postMessage({
                    type: 'kenth:resource_time',
                    seconds: seconds,
                    resourceId: RESOURCE_ID,
                    reason: reason || 'tick',
                    muted: desiredMuted !== null ? desiredMuted : (muteVideo ? !!muteVideo.muted : false)
                }, '*');
            } catch (e) {
                warn('postMessage to parent failed:', e && e.message);
            }
        }

        // ===================================================================
        // Walker: recorre window + todos los iframes anidados accesibles.
        // hvp anida el player real en un iframe interno propio, por eso no
        // basta con mirar inner.contentWindow.document.
        // ===================================================================
        function walkWindows(rootWin, visitor, depth) {
            if (!rootWin || depth > 5) return;
            try {
                visitor(rootWin, depth);
            } catch (e) { /* cross-origin transitorio */ }
            var doc = null;
            try { doc = rootWin.document; } catch (e) { return; }
            if (!doc) return;
            var frames = doc.getElementsByTagName('iframe');
            for (var i = 0; i < frames.length; i++) {
                var sub = null;
                try { sub = frames[i].contentWindow; } catch (e) { sub = null; }
                if (sub) walkWindows(sub, visitor, depth + 1);
            }
        }

        // Busca el primer window que tenga H5P.externalDispatcher.
        function findH5PWindow(rootWin) {
            var found = null;
            walkWindows(rootWin, function (w, depth) {
                if (found) return;
                try {
                    if (w.H5P && w.H5P.externalDispatcher && typeof w.H5P.externalDispatcher.on === 'function') {
                        found = { win: w, depth: depth };
                    }
                } catch (e) {}
            }, 0);
            return found;
        }

        // Busca la instancia H5P con metodo seek() (Interactive Video). Usarla
        // para el seek hace que la BARRA propia de H5P se mueva aunque este en
        // pausa; tocar solo <video>.currentTime no repinta su UI.
        function findH5PInstance(rootWin) {
            var found = null;
            walkWindows(rootWin, function (w) {
                if (found) return;
                try {
                    if (w.H5P && Array.isArray(w.H5P.instances)) {
                        for (var i = 0; i < w.H5P.instances.length; i++) {
                            var inst = w.H5P.instances[i];
                            if (inst && typeof inst.seek === 'function') { found = { instance: inst, win: w }; break; }
                        }
                    }
                } catch (e) {}
            }, 0);
            return found;
        }

        // Avisar al padre cuando el reproductor H5P ya esta renderizado (poster +
        // controles): la instancia de Interactive Video existe, o ya hay un
        // <video>. Sirve para que el visor mantenga su spinner hasta ese momento
        // (el onLoad del iframe wrapper ocurre mucho antes de esto).
        function maybeEmitReady() {
            if (h5pReadyEmitted) return;
            var ready = false;
            try { ready = !!findH5PInstance(inner.contentWindow); } catch (e) {}
            if (!ready) { try { ready = !!findBestVideo(inner.contentWindow); } catch (e) {} }
            if (ready) {
                h5pReadyEmitted = true;
                postToParent({ type: 'kenth:resource_h5p_ready', resourceId: RESOURCE_ID });
                log('h5p ready emitted');
            }
        }

        // Oculta el boton de pantalla completa del H5P (solo cuando el editor
        // pide hidefs=1). Inyecta un <style> en cada documento H5P anidado
        // (mismo origen). Idempotente por documento.
        function hideFullscreenButton(rootWin) {
            if (!HIDE_FS) return;
            walkWindows(rootWin, function (w) {
                try {
                    if (w.__kenthFsHidden) return;
                    var doc = w.document;
                    if (!doc || !doc.head) return;
                    var st = doc.createElement('style');
                    st.setAttribute('data-kenth', 'hide-fs');
                    st.textContent = '.h5p-control.h5p-fullscreen,.h5p-fullscreen,.h5p-actions .h5p-fullscreen,a.h5p-control.h5p-fullscreen{display:none !important;}';
                    doc.head.appendChild(st);
                    w.__kenthFsHidden = true;
                } catch (e) {}
            }, 0);
        }

        // Busca el mejor <video> entre TODOS los iframes anidados.
        // Preferencia: 1) reproduciendose, 2) con currentTime > 0,
        //              3) cualquiera con readyState >= 1.
        function findBestVideo(rootWin) {
            var candidates = [];
            walkWindows(rootWin, function (w, depth) {
                var doc = null;
                try { doc = w.document; } catch (e) { return; }
                if (!doc) return;
                var vids = doc.getElementsByTagName('video');
                for (var i = 0; i < vids.length; i++) {
                    candidates.push({ v: vids[i], depth: depth });
                }
            }, 0);

            if (!candidates.length) return null;

            for (var i = 0; i < candidates.length; i++) {
                if (!candidates[i].v.paused) return candidates[i];
            }
            for (var j = 0; j < candidates.length; j++) {
                if (candidates[j].v.currentTime > 0) return candidates[j];
            }
            for (var k = 0; k < candidates.length; k++) {
                if (candidates[k].v.readyState >= 1) return candidates[k];
            }
            return candidates[0];
        }

        // ===================================================================
        // Bind xAPI
        // ===================================================================
        function timeFromXAPI(statement) {
            if (!statement) return null;
            var ext = statement.result && statement.result.extensions;
            if (ext && typeof ext === 'object') {
                var keys = [
                    'https://w3id.org/xapi/video/extensions/time',
                    'http://id.tincanapi.com/extension/time',
                    'https://h5p.org/x-api/h5p-current-time'
                ];
                for (var i = 0; i < keys.length; i++) {
                    var v = ext[keys[i]];
                    if (typeof v === 'number') return v;
                    if (typeof v === 'string' && !isNaN(parseFloat(v))) return parseFloat(v);
                }
            }
            var objExt = statement.object && statement.object.definition && statement.object.definition.extensions;
            if (objExt && typeof objExt === 'object') {
                var k2 = 'https://w3id.org/xapi/video/extensions/time-from';
                if (typeof objExt[k2] === 'number') return objExt[k2];
                if (typeof objExt[k2] === 'string' && !isNaN(parseFloat(objExt[k2]))) return parseFloat(objExt[k2]);
            }
            return null;
        }

        var xapiBound = false;
        function tryBindXAPI() {
            if (xapiBound) return true;
            var hit = findH5PWindow(inner.contentWindow);
            if (!hit) {
                return false;
            }
            log('externalDispatcher detected at iframe depth =', hit.depth);
            try {
                hit.win.H5P.externalDispatcher.on('xAPI', function (event) {
                    try {
                        var stmt = event && event.data && event.data.statement;
                        var verb = stmt && stmt.verb && stmt.verb.id;
                        log('xAPI event received, verb =', verb || '(none)');
                        var t = timeFromXAPI(stmt);
                        if (t != null) emit(t, 'xapi');
                    } catch (e) {
                        warn('xAPI handler error:', e && e.message);
                    }
                });
                xapiBound = true;
                log('xAPI listener bound');
                return true;
            } catch (e) {
                warn('xAPI bind failed:', e && e.message);
                return false;
            }
        }

        // ===================================================================
        // Polling de <video>
        // ===================================================================
        var pollHandle = null;
        var lastVideoLogState = '';
        var lastMetaDuration = -1;
        var muteApplyHandle = null;
        var desiredMuted = null;
        var lastNonZeroVolume = 0.8;

        // Sincronizacion frame-accurate: requestVideoFrameCallback dispara en
        // cada frame presentado, asi el playhead y el subtitulo activo siguen
        // el audio sin el retardo del sondeo. Se auto-reengancha; en pausa no
        // dispara (sin spam) y al reanudar/seek vuelve solo.
        function attachFrameCallback(v) {
            if (!v || v.__kenthRVFC) return;
            if (typeof v.requestVideoFrameCallback !== 'function') return;
            v.__kenthRVFC = true;
            var cb = function (now, metadata) {
                try {
                    var t = (metadata && typeof metadata.mediaTime === 'number') ? metadata.mediaTime : v.currentTime;
                    emit(t, 'rvfc');
                } catch (e) {}
                try { v.requestVideoFrameCallback(cb); } catch (e) {}
            };
            try { v.requestVideoFrameCallback(cb); } catch (e) { v.__kenthRVFC = false; }
        }
        function startVideoPolling() {
            if (pollHandle) return;
            log('polling started');
            pollHandle = setInterval(function () {
                try {
                    var hit = findBestVideo(inner.contentWindow);
                    if (!hit) {
                        if (lastVideoLogState !== 'none') {
                            warn('video element not found (yet) in any nested iframe');
                            lastVideoLogState = 'none';
                        }
                        return;
                    }
                    if (lastVideoLogState !== 'found') {
                        log('video element found at iframe depth =', hit.depth,
                            'paused =', hit.v.paused,
                            'currentTime =', hit.v.currentTime);
                        lastVideoLogState = 'found';
                        // Avisar metadatos al padre en cuanto exista el <video>
                        // (duracion/URL para el timeline del editor).
                        sendMeta();
                    }
                    // Enganchar sync por frame (idempotente por <video>).
                    attachFrameCallback(hit.v);
                    // Reemitir metadatos en cuanto la duracion este disponible
                    // (loadedmetadata puede tardar; al inicio llega como null).
                    var dur = hit.v.duration;
                    if (isFinite(dur) && dur > 0 && dur !== lastMetaDuration) {
                        lastMetaDuration = dur;
                        sendMeta();
                    }
                    if (isFinite(hit.v.currentTime)) {
                        emit(hit.v.currentTime, hit.v.paused ? 'pause-poll' : 'play-poll');
                    }
                    maybeEmitReady();
                    hideFullscreenButton(inner.contentWindow);
                } catch (e) {
                    warn('polling tick error:', e && e.message);
                }
            }, 250);
        }
        function stopVideoPolling() {
            if (pollHandle) { clearInterval(pollHandle); pollHandle = null; }
        }

        // ===================================================================
        // Canal de comandos: padre (React) -> wrapper.
        // Permite al editor de leccion controlar el video (seek/play/pause),
        // pedir metadatos (duracion/URL) y generar miniaturas por canvas.
        // Mismo origen (pluginfile de Moodle), asi que el canvas no queda
        // "tainted" y toDataURL funciona.
        // ===================================================================
        function postToParent(payload) {
            try { window.parent.postMessage(payload, '*'); }
            catch (e) { warn('postMessage to parent failed:', e && e.message); }
        }

        function sendMeta() {
            var hit = findBestVideo(inner.contentWindow);
            var v = hit && hit.v;
            postToParent({
                type: 'kenth:resource_meta',
                resourceId: RESOURCE_ID,
                duration: (v && isFinite(v.duration)) ? v.duration : null,
                videoWidth: v ? (v.videoWidth || 0) : 0,
                videoHeight: v ? (v.videoHeight || 0) : 0,
                src: v ? (v.currentSrc || '') : '',
                ready: !!v,
                muted: desiredMuted !== null ? desiredMuted : (v ? !!v.muted : false),
                volume: v ? v.volume : null
            });
        }

        // <video> offscreen reutilizable para capturar miniaturas sin tocar
        // la reproduccion del player real. Se clona el currentSrc del video
        // activo. Se sirve un thumbnail por peticion (cola simple).
        var thumbVideo = null;
        var thumbCanvas = null;
        var thumbBusy = false;
        var thumbQueue = [];

        function ensureThumbTools(src) {
            if (!thumbCanvas) {
                thumbCanvas = document.createElement('canvas');
            }
            if (!thumbVideo || thumbVideo.__src !== src) {
                if (thumbVideo) { try { thumbVideo.remove(); } catch (e) {} }
                thumbVideo = document.createElement('video');
                thumbVideo.__src = src;
                thumbVideo.muted = true;
                thumbVideo.crossOrigin = 'anonymous';
                thumbVideo.preload = 'auto';
                thumbVideo.src = src;
                thumbVideo.style.position = 'absolute';
                thumbVideo.style.width = '1px';
                thumbVideo.style.height = '1px';
                thumbVideo.style.opacity = '0';
                thumbVideo.style.pointerEvents = 'none';
                document.body.appendChild(thumbVideo);
            }
            return thumbVideo;
        }

        function processThumbQueue() {
            if (thumbBusy || !thumbQueue.length) return;
            var job = thumbQueue.shift();
            thumbBusy = true;

            var hit = findBestVideo(inner.contentWindow);
            var liveSrc = hit && hit.v ? hit.v.currentSrc : '';
            if (!liveSrc) {
                postToParent({ type: 'kenth:resource_thumbnail', resourceId: RESOURCE_ID, time: job.time, dataUrl: '', error: 'no-src' });
                thumbBusy = false;
                return processThumbQueue();
            }

            var vid = ensureThumbTools(liveSrc);

            function cleanup() {
                vid.removeEventListener('seeked', onSeeked);
                vid.removeEventListener('error', onError);
            }
            function onError() {
                cleanup();
                postToParent({ type: 'kenth:resource_thumbnail', resourceId: RESOURCE_ID, time: job.time, dataUrl: '', error: 'video-error' });
                thumbBusy = false;
                processThumbQueue();
            }
            function grab() {
                try {
                    var w = vid.videoWidth || 320;
                    var h = vid.videoHeight || 180;
                    var targetW = 240;
                    var targetH = Math.max(1, Math.round(targetW * (h / w)));
                    thumbCanvas.width = targetW;
                    thumbCanvas.height = targetH;
                    var ctx = thumbCanvas.getContext('2d');
                    ctx.drawImage(vid, 0, 0, targetW, targetH);
                    var url = thumbCanvas.toDataURL('image/jpeg', 0.6);
                    postToParent({ type: 'kenth:resource_thumbnail', resourceId: RESOURCE_ID, time: job.time, dataUrl: url });
                } catch (e) {
                    warn('thumbnail capture failed:', e && e.message);
                    postToParent({ type: 'kenth:resource_thumbnail', resourceId: RESOURCE_ID, time: job.time, dataUrl: '', error: 'taint-or-draw' });
                }
                thumbBusy = false;
                processThumbQueue();
            }
            function onSeeked() {
                cleanup();
                grab();
            }

            vid.addEventListener('seeked', onSeeked);
            vid.addEventListener('error', onError);

            var doSeek = function () {
                try {
                    var dur = isFinite(vid.duration) ? vid.duration : null;
                    var t = job.time;
                    if (dur != null) t = Math.min(Math.max(0, t), Math.max(0, dur - 0.05));
                    vid.currentTime = t;
                } catch (e) { onError(); }
            };

            if (vid.readyState >= 1) {
                doSeek();
            } else {
                vid.addEventListener('loadedmetadata', doSeek, { once: true });
            }
        }

        function requestThumbnail(time) {
            if (typeof time !== 'number' || !isFinite(time) || time < 0) return;
            // Coalesce: una sola miniatura pendiente por hover.
            thumbQueue = [{ time: time }];
            processThumbQueue();
        }
        function setPlayerMuted(muted) {
            var next = !!muted;
            desiredMuted = next;
            var changed = false;
            var hit = findBestVideo(inner.contentWindow);
            var v = hit && hit.v;
            if (v) {
                try {
                    if (v.volume && v.volume > 0) lastNonZeroVolume = v.volume;
                    v.muted = next;
                    v.defaultMuted = next;
                    if (next) {
                        v.volume = 0;
                        v.setAttribute('muted', '');
                    } else {
                        v.removeAttribute('muted');
                        if (!v.volume || v.volume === 0) v.volume = lastNonZeroVolume || 0.8;
                    }
                    changed = true;
                    log('muted via video element ->', next);
                } catch (e) {
                    warn('video mute failed:', e && e.message);
                }
            }

            // Algunos H5P recrean el <video> despues del comando; reintentar
            // un momento mantiene el estado aplicado al elemento real. Solo
            // puede existir un reintento activo para evitar pelea entre estados.
            if (muteApplyHandle) {
                clearInterval(muteApplyHandle);
                muteApplyHandle = null;
            }
            var tries = 0;
            muteApplyHandle = setInterval(function () {
                tries++;
                var h = findBestVideo(inner.contentWindow);
                var media = h && h.v;
                if (media) {
                    try {
                        if (media.volume && media.volume > 0) lastNonZeroVolume = media.volume;
                        media.muted = next;
                        media.defaultMuted = next;
                        if (next) {
                            media.volume = 0;
                            media.setAttribute('muted', '');
                        } else {
                            media.removeAttribute('muted');
                            if (!media.volume || media.volume === 0) media.volume = lastNonZeroVolume || 0.8;
                        }
                        changed = true;
                    } catch (e) {}
                }
                if (tries >= 40) {
                    clearInterval(muteApplyHandle);
                    muteApplyHandle = null;
                }
            }, 50);

            postToParent({
                type: 'kenth:resource_meta',
                resourceId: RESOURCE_ID,
                duration: (v && isFinite(v.duration)) ? v.duration : null,
                videoWidth: v ? (v.videoWidth || 0) : 0,
                videoHeight: v ? (v.videoHeight || 0) : 0,
                src: v ? (v.currentSrc || '') : '',
                ready: !!v,
                muted: next,
                volume: next ? 0 : (v ? (v.volume || lastNonZeroVolume || 0.8) : lastNonZeroVolume)
            });
            return changed;
        }
        function handleCommand(data) {
            if (!data || data.type !== 'kenth:cmd') return;
            if (data.resourceId != null && Number(data.resourceId) !== RESOURCE_ID) return;
            var hit, v;
            switch (data.action) {
                case 'seek':
                    if (typeof data.seconds !== 'number' || !isFinite(data.seconds)) break;
                    var secs = Math.max(0, data.seconds);
                    var seeked = false;
                    // 1) Preferir la API de H5P (mueve su barra aunque este pausado).
                    var ivHit = findH5PInstance(inner.contentWindow);
                    if (ivHit && ivHit.instance && typeof ivHit.instance.seek === 'function') {
                        try { ivHit.instance.seek(secs); seeked = true; log('seek via H5P IV API ->', secs); }
                        catch (e) { warn('IV seek failed:', e && e.message); }
                    }
                    // 2) Fallback: <video>.currentTime (mueve el dato, no la UI de H5P).
                    if (!seeked) {
                        hit = findBestVideo(inner.contentWindow); v = hit && hit.v;
                        if (v) { try { v.currentTime = secs; seeked = true; log('seek via video.currentTime ->', secs); } catch (e) {} }
                    }
                    // Emitir la posicion al instante para que el playhead del editor
                    // salte ya, sin esperar al sondeo de 1s.
                    if (seeked) { lastSecond = -1; emit(secs, 'seek-cmd'); }
                    break;
                case 'play':
                    hit = findBestVideo(inner.contentWindow); v = hit && hit.v;
                    if (v) { try { v.play(); } catch (e) {} }
                    break;
                case 'pause':
                    hit = findBestVideo(inner.contentWindow); v = hit && hit.v;
                    if (v) { try { v.pause(); } catch (e) {} }
                    break;
                case 'mute':
                    setPlayerMuted(true);
                    break;
                case 'unmute':
                    setPlayerMuted(false);
                    break;
                case 'setMuted':
                case 'muted':
                    setPlayerMuted(!!data.muted);
                    break;
                case 'setProperty':
                    if (data.property === 'muted') setPlayerMuted(!!data.value);
                    break;
                case 'volume':
                case 'setVolume':
                    setPlayerMuted(!!data.muted || Number(data.volume) === 0);
                    break;
                case 'meta':
                    sendMeta();
                    break;
                case 'thumbnail':
                    requestThumbnail(data.time);
                    break;
                default:
                    break;
            }
        }

        window.addEventListener('message', function (ev) {
            try { handleCommand(ev && ev.data); } catch (e) { warn('command handler error:', e && e.message); }
        });

        // ===================================================================
        // Orquestador
        // ===================================================================
        function tick(attempt) {
            var win = null;
            try { win = inner.contentWindow; } catch (e) {}
            if (!win) {
                warn('inner.contentWindow not accessible (attempt ' + attempt + ')');
                return;
            }
            // Diagnostico al primer intento.
            if (attempt === 1) {
                try {
                    var hasH5P = false;
                    walkWindows(win, function (w) { try { if (w.H5P) hasH5P = true; } catch (e) {} }, 0);
                    log(hasH5P ? 'H5P detected somewhere in nested iframes' : 'H5P NOT detected yet');
                } catch (e) {}
            }
            tryBindXAPI();
            startVideoPolling();
            maybeEmitReady();
            hideFullscreenButton(inner.contentWindow);
        }

        inner.addEventListener('load', function () {
            log('inner iframe load fired');
            var attempts = 0;
            var iv = setInterval(function () {
                attempts++;
                tick(attempts);
                // Reintentamos el bind de xAPI durante ~10s (H5P puede
                // tardar en inicializar). El polling ya quedo armado en
                // el primer tick y sigue solo.
                if (xapiBound || attempts > 40) {
                    if (!xapiBound) warn('xAPI never bound after ' + attempts + ' attempts (polling fallback continues)');
                    clearInterval(iv);
                }
            }, 250);
        });

        // Si por alguna razon el load nunca llega (recursos cacheados),
        // arrancamos un tick despues de 1s.
        setTimeout(function () {
            if (!pollHandle) {
                warn('inner load did not fire within 1s, forcing tick');
                tick(1);
            }
        }, 1000);

        window.addEventListener('beforeunload', stopVideoPolling);
    })();
    </script>
</body>
</html>
    <?php
    exit;
}

// ---------------------------------------------------------------------------
// CASO no-H5P: comportamiento original (quiz, etc.)
// ---------------------------------------------------------------------------
$redirect_url = new moodle_url('/mod/' . $modname . '/view.php', array(
    'id' => $cmid,
    'isheadless' => 1
));
redirect($redirect_url);






