<?php
define('NO_OUTPUT_BUFFERING', true);
require(__DIR__ . '/../../config.php');
require_once(__DIR__ . '/tesis_lib.php');

header('Content-Type: application/json');
http_response_code(200);

try {
    $token      = isset($_GET['token']) ? clean_param($_GET['token'], PARAM_ALPHANUM) : '';
    $identifier = isset($_GET['courseid']) ? clean_param($_GET['courseid'], PARAM_RAW) : '';

    if (empty($token) || empty($identifier)) {
        echo json_encode(['error' => 'Missing parameters']);
        exit;
    }

    // 1. Validar Token
    $token_record = $DB->get_record('external_tokens', array('token' => $token));
    if (!$token_record) {
        echo json_encode(['error' => 'Token invalido']);
        exit;
    }

    // 2. VERIFICAR EL ID FIRMADO
    $courseid = kenth_verify_id($identifier);
    if (!$courseid) {
        echo json_encode(['error' => 'Acceso denegado: Firma de curso invalida.']);
        exit;
    }

    // 3. Validar permisos (Site Admin o Enrolled)
    $isadmin = is_siteadmin($token_record->userid);
    $context = context_course::instance($courseid);
    if (!$isadmin && !is_enrolled($context, $token_record->userid)) {
        echo json_encode(['error' => 'No tienes permiso para ver este curso.']);
        exit;
    }

    // 4. Obtener contenidos
    require_once($CFG->dirroot . '/course/lib.php');
    $course = $DB->get_record('course', array('id' => $courseid), '*', MUST_EXIST);
    $contents = get_course_contents($course->id);

    echo json_encode($contents);

} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
