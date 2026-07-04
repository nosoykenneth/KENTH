<?php
define('NO_OUTPUT_BUFFERING', true);
require(__DIR__ . '/../../config.php');
require_once(__DIR__ . '/tesis_lib.php');

header('Content-Type: application/json');

try {
    $token      = isset($_GET['token']) ? clean_param($_GET['token'], PARAM_ALPHANUM) : '';
    $identifier = isset($_GET['courseid']) ? clean_param($_GET['courseid'], PARAM_RAW) : '';

    if (empty($token) || empty($identifier)) {
        die(json_encode(['error' => 'Missing parameters']));
    }

    $token_record = $DB->get_record('external_tokens', array('token' => $token));
    if (!$token_record) {
        die(json_encode(['error' => 'Token invalido']));
    }

    $courseid = kenth_verify_id($identifier);
    if (!$courseid) {
        die(json_encode(['error' => 'Acceso denegado: Firma de curso invalida.']));
    }

    $user = $DB->get_record('user', array('id' => $token_record->userid), '*', MUST_EXIST);
    complete_user_login($user);
    
    $context = context_course::instance($courseid);
    if (!is_enrolled($context, $user) && !is_siteadmin($user)) {
        die(json_encode(['error' => 'No tienes permiso para ver este curso.']));
    }

    // USAMOS LA API EXTERNA QUE ES MÁS SEGURA Y ESTABLE PARA ESTO
    require_once($CFG->dirroot . '/course/externallib.php');
    $contents = core_course_external::get_course_contents($courseid);

    echo json_encode($contents);

} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
