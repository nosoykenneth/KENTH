<?php
/**
 * Inyecta interacciones formativas en videos InteractiveVideo de mod_hvp,
 * SIN reimportar .h5p (preserva cmid / video / gradebook). Estrategia B:
 * edita mdl_hvp.json_content y re-filtra con el core de mod_hvp
 * (H5PCore::filterParameters) que recalcula `filtered` + dependencias de
 * librería (mdl_hvp_contents_libraries) para que el player cargue el JS de
 * MultiChoice / TrueFalse / Summary.
 *
 * SOLO reemplaza interactiveVideo.assets.interactions. No toca el video ni el
 * resto de params. Idempotente (subContentId deterministas desde el builder).
 *
 * Uso (dentro del contenedor moodle):
 *   php apply_h5p_interactions.php --build=/tmp/h5p_build_course2.json --dry-run
 *   php apply_h5p_interactions.php --build=/tmp/h5p_build_course2.json --apply
 *   php apply_h5p_interactions.php --build=/tmp/h5p_build_course2.json --apply --only=21
 */

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
global $DB, $CFG;

// --- args ---
$opts = getopt('', ['build:', 'apply', 'dry-run', 'only:', 'backup-dir:']);
$buildpath = $opts['build'] ?? '';
$apply = array_key_exists('apply', $opts);
$only = isset($opts['only']) ? (int)$opts['only'] : 0;
$backupdir = $opts['backup-dir'] ?? '/tmp/hvp_params_pre_apply';
if ($buildpath === '' || !is_file($buildpath)) {
    fwrite(STDERR, "ERROR: --build=<path> requerido y existente\n");
    exit(2);
}
if (!$apply) { echo "== MODO DRY-RUN (no escribe) ==\n"; }
@mkdir($backupdir, 0775, true);

$build = json_decode(file_get_contents($buildpath), true);
if (!is_array($build) || empty($build['activities'])) {
    fwrite(STDERR, "ERROR: build JSON inválido\n");
    exit(2);
}

require_once($CFG->dirroot . '/mod/hvp/locallib.php');
$core = \mod_hvp\framework::instance();

$summary = [];
foreach ($build['activities'] as $act) {
    $hid = (int)$act['hvp_content_id'];
    if ($only && $hid !== $only) { continue; }
    $lesson = $act['lesson_id'];
    $newinteractions = $act['interactions'];

    $rec = $DB->get_record('hvp', ['id' => $hid]);
    if (!$rec) { echo "  [$lesson] hvp=$hid NO EXISTE, salto\n"; continue; }

    $params = json_decode($rec->json_content, true);
    if (!isset($params['interactiveVideo']['assets'])) {
        echo "  [$lesson] hvp=$hid sin interactiveVideo.assets, salto\n"; continue;
    }
    $before = count($params['interactiveVideo']['assets']['interactions'] ?? []);

    // Backup byte-accurate del params actual (además del dump global).
    file_put_contents($backupdir . "/hvp_{$hid}_params.json", $rec->json_content);

    // ÚNICO cambio: reemplazar el array de interacciones.
    $params['interactiveVideo']['assets']['interactions'] = $newinteractions;
    $newjson = json_encode($params, JSON_UNESCAPED_SLASHES);

    echo "  [$lesson] hvp=$hid interacciones: $before -> " . count($newinteractions)
        . " | json " . strlen($rec->json_content) . " -> " . strlen($newjson) . " bytes\n";

    if (!$apply) {
        // Validación en seco: decodifica el nuevo json para confirmar que es válido.
        if (json_decode($newjson, true) === null) { echo "    ! nuevo json inválido\n"; }
        continue;
    }

    // Escribe params + fuerza re-filtrado.
    $DB->set_field('hvp', 'json_content', $newjson, ['id' => $hid]);
    $DB->set_field('hvp', 'filtered', '', ['id' => $hid]);
    $DB->set_field('hvp', 'timemodified', time(), ['id' => $hid]);

    // Re-filtra vía core: recomputa `filtered` + dependencias de librería.
    $content = $core->loadContent($hid);
    $filtered = $core->filterParameters($content);
    $flen = is_string($filtered) ? strlen($filtered) : 0;

    // Verificación: ¿cuántas interacciones sobrevivieron al validador?
    $after = $DB->get_field('hvp', 'json_content', ['id' => $hid]);
    $afterparams = json_decode($after, true);
    $kept = count($afterparams['interactiveVideo']['assets']['interactions'] ?? []);
    $deps = $DB->get_records('hvp_contents_libraries', ['hvp_id' => $hid]);
    $depnames = [];
    foreach ($deps as $d) {
        $lib = $DB->get_record('hvp_libraries', ['id' => $d->library_id]);
        if ($lib) { $depnames[] = $lib->machine_name; }
    }
    $depnames = array_values(array_unique($depnames));
    sort($depnames);
    echo "    aplicado: interactions_kept=$kept filtered_len=$flen deps=[" . implode(',', $depnames) . "]\n";
    $summary[] = compact('lesson', 'hid', 'kept', 'flen') + ['deps' => $depnames];
}

if ($apply) {
    // Purga sólo caches de H5P para que el player reconstruya assets del content.
    if (function_exists('purge_all_caches')) {
        // Evitamos purge_all_caches (pesado en prod); H5P regenera al ver.
    }
    echo "== RESUMEN APLICADO ==\n" . json_encode($summary, JSON_UNESCAPED_UNICODE) . "\n";
}
echo "DONE\n";
