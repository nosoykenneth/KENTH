<?php
// tesis_login.php - Interceptor de login para manejar el flujo de onboarding

define('AJAX_SCRIPT', true);

require_once(__DIR__ . '/../../config.php');
require_once($CFG->libdir . '/externallib.php');
require_once($CFG->dirroot . '/webservice/lib.php');

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    echo json_encode(['success' => true]);
    exit;
}

ob_start();

$username = required_param('username', PARAM_USERNAME);
$password = required_param('password', PARAM_RAW);
$service  = optional_param('service', 'api_tesis', PARAM_ALPHANUMEXT);

global $DB, $CFG, $USER;

function login_log($message) {
    file_put_contents(
        __DIR__ . '/log_login.txt',
        '[' . date('Y-m-d H:i:s') . '] ' . $message . PHP_EOL,
        FILE_APPEND
    );
}

try {
    // 1) Autenticar usuario
    $user = authenticate_user_login($username, $password);

    login_log("INTENTO LOGIN: user={$username} | resultado=" . ($user ? 'EXITO' : 'FALLO'));

    if (!$user) {
        throw new Exception('Nombre de usuario o contraseña incorrectos');
    }

    // 2) Obtener servicio
    $service_record = $DB->get_record(
        'external_services',
        ['shortname' => $service],
        '*',
        MUST_EXIST
    );

    // 3) Buscar token existente
    $token_record = $DB->get_record(
        'external_tokens',
        [
            'userid' => $user->id,
            'externalserviceid' => $service_record->id
        ]
    );

    if ($token_record && !empty($token_record->token)) {
        $token = $token_record->token;
        login_log("TOKEN EXISTENTE reutilizado para user_id={$user->id}");
    } else {
        // Importante: establecer usuario actual correctamente
        complete_user_login($user);
        $USER = $user;

        // Generar token
        $generated = external_generate_token_for_current_user($service_record);

        // No asumir tipo de retorno
        login_log("TOKEN RAW TYPE: " . gettype($generated) . " para user_id={$user->id}");

        // Volver a leer desde BD, que es la fuente confiable
        $token_record = $DB->get_record(
            'external_tokens',
            [
                'userid' => $user->id,
                'externalserviceid' => $service_record->id
            ],
            '*',
            MUST_EXIST
        );

        if (empty($token_record->token)) {
            throw new Exception('Se generó el token pero quedó vacío en BD.');
        }

        $token = $token_record->token;
        login_log("TOKEN GENERADO DESDE BD para user_id={$user->id}");
    }

    // 4) Onboarding
    $requiresOnboarding = get_user_preferences('kenth_requires_onboarding', '0', $user->id);

    login_log("TOKEN GENERADO: {$token} para user_id={$user->id}");

    // Limpiar cualquier salida previa
    if (ob_get_length()) {
        ob_clean();
    }

    echo json_encode([
        'success' => true,
        'token' => $token,
        'requiresOnboarding' => ($requiresOnboarding === '1'),
        'userid' => $user->id,
        'fullname' => fullname($user)
    ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    login_log("ERROR LOGIN: " . $e->getMessage());

    if (ob_get_length()) {
        ob_clean();
    }

    http_response_code(200);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}