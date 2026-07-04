<?php
require_once(__DIR__ . '/../../config.php');
require_once($CFG->libdir . '/enrollib.php');
require_once('tesis_lib.php');

header('Content-Type: application/json; charset=utf-8');

$email = required_param('email', PARAM_EMAIL);
$course_id_raw = required_param('course_id', PARAM_RAW);

global $DB;

try {
    $email = strtolower(trim($email));

    $course_id = kenth_verify_id($course_id_raw);
    if (!$course_id) {
        $course_id = (int)$course_id_raw;
    }

    if (empty($email) || empty($course_id)) {
        throw new Exception('Faltan parámetros requeridos.');
    }

    $user = $DB->get_record('user', [
        'email' => $email,
        'deleted' => 0
    ]);

    if (!$user) {
        echo json_encode([
            'success' => true,
            'exists' => false,
            'isEnrolled' => false
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    $context = context_course::instance($course_id);
    $isEnrolled = is_enrolled($context, $user->id);

    echo json_encode([
        'success' => true,
        'exists' => true,
        'isEnrolled' => $isEnrolled,
        'fullname' => fullname($user)
    ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}