<?php
require_once(__DIR__ . '/../../config.php');
require_once($CFG->libdir . '/enrollib.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once('tesis_lib.php');

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

global $DB, $CFG;

try {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);

    if (!$data || !is_array($data)) {
        throw new Exception('Payload inválido.');
    }

    $paypalOrderId = trim($data['paypalOrderId'] ?? '');
    $courseIdRaw = $data['course_id'] ?? '';
    $email = strtolower(trim($data['email'] ?? ''));
    $firstname = trim($data['firstname'] ?? 'Estudiante');
    $lastname = trim($data['lastname'] ?? 'KENTH');

    if (!$paypalOrderId || !$courseIdRaw || !$email) {
        throw new Exception('Faltan parámetros requeridos.');
    }

    $course_id = kenth_verify_id($courseIdRaw);
    if (!$course_id) {
        $course_id = (int)$courseIdRaw;
    }

    if (!$course_id) {
        throw new Exception('No se pudo resolver el ID del curso.');
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        throw new Exception('Correo inválido.');
    }

    $course = $DB->get_record('course', ['id' => $course_id], '*', MUST_EXIST);

    $user = $DB->get_record('user', [
        'email' => $email,
        'deleted' => 0
    ]);

    $is_new_user = false;
    $plaintext_password = null;

    if (!$user) {
        $is_new_user = true;
        $plaintext_password = bin2hex(random_bytes(4)) . 'Kt!';

        $newuser = new stdClass();
        $newuser->username = $email;
        $newuser->email = $email;
        $newuser->firstname = $firstname;
        $newuser->lastname = $lastname;
        $newuser->auth = 'manual';
        $newuser->mnethostid = $CFG->mnet_localhost_id;
        $newuser->confirmed = 1;
        $newuser->lang = 'es';

        $newuser->id = user_create_user($newuser);
        update_internal_user_password($newuser, $plaintext_password);

        $user = $DB->get_record('user', ['id' => $newuser->id], '*', MUST_EXIST);
        set_user_preference('kenth_requires_onboarding', '1', $user->id);
    }

    $context = context_course::instance($course->id);
    $alreadyEnrolled = is_enrolled($context, $user->id);

    if (!$alreadyEnrolled) {
        $enrol = enrol_get_plugin('manual');
        $instances = enrol_get_instances($course->id, true);

        $manualInstance = null;
        foreach ($instances as $instance) {
            if ($instance->enrol === 'manual') {
                $manualInstance = $instance;
                break;
            }
        }

        if (!$manualInstance) {
            throw new Exception('No se encontró instancia de matrícula manual.');
        }

        $roleid = $DB->get_field('role', 'id', ['shortname' => 'student']);
        if (!$roleid) {
            throw new Exception('No se encontró el rol student.');
        }

        $enrol->enrol_user($manualInstance, $user->id, $roleid);
    }

    if ($is_new_user) {
        $subject = '¡Tu matrícula en KENTH Academy está lista!';
        $login_url = 'http://localhost:5173/login';

        $html_message = "
        <div style='font-family: Arial, sans-serif; padding: 24px; background:#111; color:#fff;'>
          <h2>¡Bienvenido a KENTH Academy!</h2>
          <p>Hola {$firstname}, tu pago ha sido confirmado.</p>
          <p><strong>Curso:</strong> {$course->fullname}</p>
          <p><strong>Usuario:</strong> {$email}</p>
          <p><strong>Contraseña temporal:</strong> {$plaintext_password}</p>
          <p><a href='{$login_url}' style='color:#ff7a00;'>Ir al login</a></p>
        </div>";

        email_to_user(
            $user,
            core_user::get_support_user(),
            $subject,
            strip_tags($html_message),
            $html_message
        );
    }

    echo json_encode([
        'success' => true,
        'message' => $alreadyEnrolled
            ? 'Pago registrado; el usuario ya estaba matriculado'
            : 'Pago registrado y matrícula completada'
    ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}