<?php
// api_request_password_reset.php
// Solicitud de restablecimiento de contraseña.
// Usa la infraestructura nativa de Moodle (tabla user_password_resets) y envía
// un correo con un enlace al frontend. SIEMPRE responde de forma genérica para
// no permitir enumeración de usuarios.

require_once(__DIR__ . '/../../config.php');
require_once($CFG->dirroot . '/login/lib.php');

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    echo json_encode(['success' => true]);
    exit;
}

function get_backend_env($key) {
    $envPath = __DIR__ . '/.env';
    if (!file_exists($envPath)) return null;

    $lines = file($envPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        if (strpos($line, '=') !== false) {
            [$name, $value] = explode('=', $line, 2);
            if (trim($name) === $key) return trim($value);
        }
    }
    return null;
}

function reset_log($message) {
    file_put_contents(
        __DIR__ . '/log_password_reset.txt',
        '[' . date('Y-m-d H:i:s') . '] ' . $message . PHP_EOL,
        FILE_APPEND
    );
}

global $DB, $CFG;

// Respuesta genérica: se devuelve siempre, exista o no la cuenta (anti-enumeración).
$generic_response = [
    'success' => true,
    'message' => 'Si la cuenta existe, te enviamos un correo con instrucciones para restablecer tu contraseña. Revisa tu bandeja de entrada y la carpeta de spam.'
];

try {
    // Aceptar form-urlencoded (caso normal del frontend) y, como respaldo, JSON.
    $identifier = trim(optional_param('identifier', '', PARAM_RAW));
    if ($identifier === '') {
        $identifier = trim(optional_param('email', '', PARAM_RAW));
    }
    if ($identifier === '') {
        $identifier = trim(optional_param('username', '', PARAM_RAW));
    }
    if ($identifier === '') {
        $raw = file_get_contents('php://input');
        if (!empty($raw)) {
            $json = json_decode($raw, true);
            if (is_array($json)) {
                $identifier = trim($json['identifier'] ?? ($json['email'] ?? ($json['username'] ?? '')));
            }
        }
    }

    if ($identifier === '') {
        echo json_encode(['success' => false, 'error' => 'Debes ingresar tu correo o tu usuario.'], JSON_UNESCAPED_UNICODE);
        exit;
    }

    // Buscar la cuenta por email o por username, en el host local y no borrada.
    $user = null;
    if (strpos($identifier, '@') !== false) {
        $user = $DB->get_record_select(
            'user',
            'deleted = 0 AND mnethostid = :mnethostid AND LOWER(email) = LOWER(:email)',
            ['mnethostid' => $CFG->mnet_localhost_id, 'email' => $identifier]
        );
    }
    if (!$user) {
        $user = $DB->get_record('user', [
            'mnethostid' => $CFG->mnet_localhost_id,
            'deleted' => 0,
            'username' => core_text::strtolower($identifier)
        ]);
    }

    if (!$user) {
        reset_log("SOLICITUD para identificador inexistente: {$identifier}");
        echo json_encode($generic_response, JSON_UNESCAPED_UNICODE);
        exit;
    }

    // No procesar cuentas suspendidas, sin confirmar, o con auth no interna.
    if (!empty($user->suspended) || empty($user->confirmed) || !in_array($user->auth, ['manual', 'email'], true)) {
        reset_log("SOLICITUD bloqueada (suspendido/no confirmado/auth={$user->auth}) user_id={$user->id}");
        echo json_encode($generic_response, JSON_UNESCAPED_UNICODE);
        exit;
    }

    // Anti-spam: si pidió un reset hace menos de 60s, no reenviar (responde genérico igual).
    $existing = $DB->get_records('user_password_resets', ['userid' => $user->id], 'timerequested DESC', '*', 0, 1);
    $last = $existing ? reset($existing) : null;
    if ($last && (time() - (int)$last->timerequested) < 60) {
        reset_log("SOLICITUD ignorada por anti-spam (<60s) user_id={$user->id}");
        echo json_encode($generic_response, JSON_UNESCAPED_UNICODE);
        exit;
    }

    // Un único token activo por usuario: limpiar previos y generar uno nuevo.
    $DB->delete_records('user_password_resets', ['userid' => $user->id]);
    $resetrecord = core_login_generate_password_reset($user);
    $token = $resetrecord->token;

    $frontendBase = rtrim(get_backend_env('FRONTEND_BASE_URL') ?: 'http://localhost:5173', '/');
    $reset_url = $frontendBase . '/reset-password?token=' . rawurlencode($token);
    $minutes = (int) round((!empty($CFG->pwresettime) ? $CFG->pwresettime : 1800) / 60);

    $subject = 'Restablece tu contraseña — KENTH Academy';

    $html_message = "
    <div style='background-color: #0d0d0f; padding: 40px 20px; font-family: \"Segoe UI\", Helvetica, Arial, sans-serif;'>
        <div style='max-width: 600px; margin: 0 auto; background-color: #1A1A1D; border-radius: 24px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 40px rgba(0,0,0,0.5);'>
            <div style='background: linear-gradient(135deg, #6F2232 0%, #C3073F 100%); padding: 40px; text-align: center;'>
                <img src='https://i.imgur.com/BXiN2dO.png' alt='KENTH Academy' style='max-width: 200px; height: auto;'>
            </div>

            <div style='padding: 40px; color: #ffffff;'>
                <h2 style='margin-top: 0; font-size: 24px; font-weight: 700;'>Restablece tu contraseña</h2>
                <p style='font-size: 16px; line-height: 1.6; color: rgba(255,255,255,0.8);'>
                    Hola <span style='color: #C3073F; font-weight: 700;'>{$user->firstname}</span>, recibimos una solicitud para restablecer la contraseña de tu cuenta en KENTH Academy.
                </p>
                <p style='font-size: 15px; line-height: 1.6; color: rgba(255,255,255,0.7);'>
                    Haz clic en el siguiente botón para crear una contraseña nueva. Este enlace caduca en <strong style='color:#ffffff;'>{$minutes} minutos</strong>.
                </p>

                <div style='text-align: center; margin: 40px 0;'>
                    <a href='{$reset_url}' style='background-color: #C3073F; color: #ffffff; padding: 18px 35px; border-radius: 15px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block; box-shadow: 0 10px 20px rgba(195, 7, 63, 0.3);'>
                        CREAR NUEVA CONTRASEÑA
                    </a>
                </div>

                <p style='font-size: 12px; line-height: 1.5; color: rgba(255,255,255,0.5);'>
                    Si el botón no funciona, copia y pega esta dirección en tu navegador:<br>
                    <a href='{$reset_url}' style='color: #C3073F; word-break: break-all;'>{$reset_url}</a>
                </p>

                <p style='font-size: 13px; line-height: 1.5; color: rgba(255,255,255,0.5); margin-top: 30px;'>
                    Si tú no solicitaste este cambio, puedes ignorar este correo: tu contraseña actual seguirá funcionando.
                </p>
            </div>

            <div style='padding: 30px; background-color: #121214; text-align: center; border-top: 1px solid rgba(255,255,255,0.05);'>
                <p style='margin: 0; font-size: 12px; color: rgba(255,255,255,0.3);'>
                    &copy; 2026 KENTH Academy. Desarrollado con pasión por la tecnología.
                </p>
            </div>
        </div>
    </div>";

    $text_message =
        "Hola {$user->firstname},\n\n" .
        "Recibimos una solicitud para restablecer la contraseña de tu cuenta en KENTH Academy.\n\n" .
        "Abre este enlace para crear una contraseña nueva (caduca en {$minutes} minutos):\n" .
        "{$reset_url}\n\n" .
        "Si tú no solicitaste este cambio, ignora este correo: tu contraseña actual seguirá funcionando.\n\n" .
        "— KENTH Academy";

    $mail_result = email_to_user(
        $user,
        core_user::get_support_user(),
        $subject,
        $text_message,
        $html_message
    );

    reset_log("RESET generado user_id={$user->id} email={$user->email} mail=" . ($mail_result ? 'OK' : 'FALLO'));

    echo json_encode($generic_response, JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    reset_log('ERROR: ' . $e->getMessage());
    // Incluso ante un error interno respondemos genérico para no filtrar información.
    echo json_encode($generic_response, JSON_UNESCAPED_UNICODE);
}
