<?php
// api_confirm_password_reset.php
// Verifica un token de restablecimiento (tabla user_password_resets) y, si es
// válido, establece la nueva contraseña aplicando la política de Moodle.
//
// Acciones:
//   action=validate -> solo comprueba el token (para precargar el formulario).
//   action=reset    -> requiere 'password' y actualiza la contraseña.

require_once(__DIR__ . '/../../config.php');

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

/** Enmascara un correo: jo***@dominio.com */
function kenth_mask_email($email) {
    $parts = explode('@', (string)$email);
    if (count($parts) !== 2) return '';
    $name = $parts[0];
    $domain = $parts[1];
    $visible = core_text::substr($name, 0, min(2, core_text::strlen($name)));
    return $visible . str_repeat('*', max(1, core_text::strlen($name) - core_text::strlen($visible))) . '@' . $domain;
}

global $DB, $CFG;

try {
    $token    = optional_param('token', '', PARAM_ALPHANUM);
    $action   = optional_param('action', 'reset', PARAM_ALPHA);
    $password = optional_param('password', '', PARAM_RAW);

    // Respaldo JSON.
    if ($token === '') {
        $raw = file_get_contents('php://input');
        if (!empty($raw)) {
            $json = json_decode($raw, true);
            if (is_array($json)) {
                $token = clean_param($json['token'] ?? '', PARAM_ALPHANUM);
                if (!empty($json['action'])) $action = clean_param($json['action'], PARAM_ALPHA);
                if (isset($json['password'])) $password = (string)$json['password'];
            }
        }
    }

    if ($token === '') {
        throw new Exception('Falta el token de restablecimiento.');
    }

    $record = $DB->get_record('user_password_resets', ['token' => $token]);
    if (!$record) {
        throw new Exception('El enlace de restablecimiento no es válido o ya fue utilizado.');
    }

    // Expiración (Moodle: $CFG->pwresettime, por defecto 1800s).
    $pwresettime = !empty($CFG->pwresettime) ? (int)$CFG->pwresettime : 1800;
    if ((time() - (int)$record->timerequested) > $pwresettime) {
        $DB->delete_records('user_password_resets', ['id' => $record->id]);
        throw new Exception('El enlace de restablecimiento expiró. Solicita uno nuevo.');
    }

    $user = $DB->get_record('user', ['id' => $record->userid, 'deleted' => 0]);
    if (!$user) {
        $DB->delete_records('user_password_resets', ['id' => $record->id]);
        throw new Exception('La cuenta asociada ya no está disponible.');
    }

    // Solo comprobar el token (sin cambiar nada).
    if ($action === 'validate') {
        echo json_encode([
            'success' => true,
            'valid' => true,
            'email_masked' => kenth_mask_email($user->email)
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    // --- action = reset ---
    if (!empty($user->suspended) || !in_array($user->auth, ['manual', 'email'], true)) {
        throw new Exception('Esta cuenta no permite restablecer la contraseña por este medio.');
    }

    if ($password === '') {
        throw new Exception('Debes ingresar una nueva contraseña.');
    }

    // Aplicar la política de contraseñas del sitio.
    $errmsg = '';
    if (!check_password_policy($password, $errmsg, $user)) {
        throw new Exception($errmsg !== '' ? strip_tags($errmsg) : 'La contraseña no cumple la política de seguridad del sitio.');
    }

    // Forma oficial de Moodle para actualizar el hash de contraseña.
    update_internal_user_password($user, $password);

    // Invalidar todos los tokens de reset del usuario.
    $DB->delete_records('user_password_resets', ['userid' => $user->id]);

    // El usuario acaba de definir una contraseña: no forzar cambio en el siguiente login
    // y quitar cualquier bloqueo de cuenta por intentos fallidos.
    set_user_preference('auth_forcepasswordchange', 0, $user->id);
    if (function_exists('login_unlock_account')) {
        login_unlock_account($user);
    }

    echo json_encode([
        'success' => true,
        'message' => 'Tu contraseña se actualizó correctamente. Ya puedes iniciar sesión.'
    ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}
