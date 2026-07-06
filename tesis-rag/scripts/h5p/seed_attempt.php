<?php
/**
 * Siembra un intento de estudiante en un video H5P (mod_hvp) reproduciendo
 * BYTE-A-BYTE lo que hace un intento real desde el navegador:
 *   1) inserta en {hvp_xapi_results} el mismo árbol (padre IV + hijos por
 *      interacción) que \mod_hvp\xapi_result::store_xapi_data(), y
 *   2) escribe la nota en el gradebook igual que \mod_hvp\user_grades::handle_ajax()
 *      (rawgrade/rawgrademax + hvp_grade_item_update).
 *
 * Sirve para VALIDAR el pipeline resultados->señales->tutor sin depender de un
 * clic manual en el navegador. La fila resultante es indistinguible de un intento
 * real (mismas tablas, mismas columnas, misma nota). Idempotente: borra el intento
 * previo del mismo (content_id,user_id) antes de insertar, igual que mod_hvp.
 *
 * Uso (en el contenedor moodle):
 *   php seed_attempt.php --seed=/tmp/seed_r55.json
 * seed json: {content_id,user_id,score,max_score,children:[{description,interaction_type,raw_score,max_score,response,correct_responses_pattern}]}
 */
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
global $DB, $CFG;
require_once($CFG->dirroot . '/mod/hvp/lib.php');
require_once($CFG->libdir . '/gradelib.php');

$opts = getopt('', ['seed:']);
if (empty($opts['seed']) || !is_file($opts['seed'])) {
    fwrite(STDERR, "ERROR: --seed=<path> requerido\n"); exit(2);
}
$seed = json_decode(file_get_contents($opts['seed']), true);
$contentid = (int)$seed['content_id'];
$userid = (int)$seed['user_id'];
$score = (int)$seed['score'];
$maxscore = (int)$seed['max_score'];

$hvp = $DB->get_record('hvp', ['id' => $contentid], '*', MUST_EXIST);
$cm = get_coursemodule_from_instance('hvp', $contentid, $hvp->course, false, MUST_EXIST);

// 1) Borra intento previo (idéntico a remove_xapi_data) e inserta el árbol.
$DB->delete_records('hvp_xapi_results', ['content_id' => $contentid, 'user_id' => $userid]);
$parentid = $DB->insert_record('hvp_xapi_results', (object) [
    'content_id' => $contentid, 'user_id' => $userid, 'parent_id' => null,
    'interaction_type' => 'compound', 'description' => $hvp->name,
    'correct_responses_pattern' => '', 'response' => '', 'additionals' => '',
    'raw_score' => $score, 'max_score' => $maxscore,
]);
$nchildren = 0;
foreach ($seed['children'] as $ch) {
    $DB->insert_record('hvp_xapi_results', (object) [
        'content_id' => $contentid, 'user_id' => $userid, 'parent_id' => $parentid,
        'interaction_type' => $ch['interaction_type'] ?? 'choice',
        'description' => $ch['description'],
        'correct_responses_pattern' => $ch['correct_responses_pattern'] ?? '',
        'response' => $ch['response'] ?? '', 'additionals' => '',
        'raw_score' => (int)$ch['raw_score'], 'max_score' => (int)$ch['max_score'],
    ]);
    $nchildren++;
}

// 2) Nota al gradebook (idéntico a user_grades::handle_ajax).
$grade = (object) ['userid' => $userid];
$hvp->cmidnumber = $cm->idnumber;
$hvp->name = $cm->name;
$hvp->rawgrade = $score;
$hvp->rawgrademax = $maxscore;
hvp_grade_item_update($hvp, $grade);

$final = grade_get_grades($cm->course, 'mod', 'hvp', $hvp->id, $userid);
$g = isset($final->items[0]->grades[$userid]) ? $final->items[0]->grades[$userid]->grade : null;
echo json_encode([
    'content_id' => $contentid, 'user_id' => $userid,
    'parent_id' => $parentid, 'children' => $nchildren,
    'raw' => $score, 'max' => $maxscore, 'gradebook_grade' => $g,
], JSON_UNESCAPED_UNICODE) . "\n";
echo "SEEDED OK\n";
