<?php
/**
 * api_webhook_pagos.php - v5.0
 * Flujo: SDK Button -> CheckoutSuccess -> Confirmación PayPhone -> Matrícula Moodle
 */

define('CLI_SCRIPT', false);

require_once('../../config.php');
require_once($CFG->libdir . '/enrollib.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once('tesis_lib.php');

// CORS para desarrollo
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

/**
 * Lee variables desde .env local
 */
function get_backend_env($key) {
    $envPath = __DIR__ . '/.env';
    if (!file_exists($envPath)) {
        return null;
    }

    $lines = file($envPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) {
            continue;
        }
        if (strpos($line, '=') !== false) {
            list($name, $value) = explode('=', $line, 2);
            if (trim($name) === $key) {
                return trim($value);
            }
        }
    }

    return null;
}

/**
 * Logging simple
 */
function webhook_log($message) {
    file_put_contents(
        __DIR__ . '/log_debug_webhook.txt',
        '[' . date('Y-m-d H:i:s') . '] ' . $message . PHP_EOL,
        FILE_APPEND
    );
}

$inputRaw = file_get_contents('php://input');
webhook_log('HIT api_webhook_pagos.php');
webhook_log('INPUT RAW: ' . $inputRaw);

$input = json_decode($inputRaw, true);

if (!$input || !is_array($input)) {
    echo json_encode([
        'success' => false,
        'error' => 'Payload JSON inválido o vacío'
    ]);
    exit;
}

$transactionId = $input['transactionId'] ?? $input['id'] ?? null;
$clientTransactionId = $input['clientTransactionId'] ?? null;

try {
    // 1) Validaciones mínimas
    $payphoneToken = get_backend_env('PAYPHONE_TOKEN');
    if (!$payphoneToken) {
        throw new Exception('Error interno: PAYPHONE_TOKEN no configurado.');
    }

    if (empty($transactionId) || empty($clientTransactionId)) {
        throw new Exception('Faltan parámetros de confirmación: id o clientTransactionId.');
    }

    // 2) Confirmación oficial con PayPhone para flujo Button Redirect
    $urlPayphone = 'https://pay.payphonetodoesposible.com/api/button/V2/Confirm';

    $payloadConfirmArray = [
        'id' => (int)$transactionId,
        'clientTxId' => (string)$clientTransactionId
    ];

    $payloadConfirm = json_encode($payloadConfirmArray);

    webhook_log('CONFIRM URL: ' . $urlPayphone);
    webhook_log('CONFIRM REQUEST: ' . $payloadConfirm);

    $ch = curl_init($urlPayphone);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payloadConfirm);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $payphoneToken,
        'Content-Type: application/json'
    ]);

    $response = curl_exec($ch);

    if ($response === false) {
        $curlError = curl_error($ch);
        $curlErrno = curl_errno($ch);
        curl_close($ch);
        throw new Exception("Error cURL al confirmar con PayPhone: [$curlErrno] $curlError");
    }

    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    webhook_log("CONFIRM RESPONSE HTTP {$httpCode}: " . $response);

    $data = json_decode($response, true);

    if ($httpCode !== 200 || !$data || !is_array($data)) {
        throw new Exception('Error de PayPhone (HTTP ' . $httpCode . '). Respuesta: ' . ($response ?: 'Vacía'));
    }

    $status = $data['transactionStatus'] ?? '';
    $statusCode = isset($data['statusCode']) ? (int)$data['statusCode'] : null;

    webhook_log("PAYPHONE STATUS: transactionStatus={$status}, statusCode=" . var_export($statusCode, true));

    if ($status !== 'Approved') {
        throw new Exception("Pago no aprobado. transactionStatus={$status}");
    }

    // Si PayPhone devuelve statusCode, validamos también
    if ($statusCode !== null && $statusCode !== 3) {
        throw new Exception("Pago no aprobado. statusCode={$statusCode}");
    }

    // 3) Resolver clientTransactionId real para encontrar metadata local
    $resolvedClientTxId =
        $data['clientTransactionId'] ??
        $data['clientTxId'] ??
        $clientTransactionId;

    if (empty($resolvedClientTxId)) {
        throw new Exception('No se pudo resolver clientTransactionId para buscar metadata local.');
    }

    $paymentsDir = __DIR__ . '/payments';
    $localFile = $paymentsDir . '/' . $resolvedClientTxId . '.json';

    webhook_log('LOCAL FILE LOOKUP: ' . $localFile);

    if (!file_exists($localFile)) {
        $foundFiles = glob($paymentsDir . '/*.json');
        $fileList = $foundFiles ? array_map('basename', $foundFiles) : [];
        throw new Exception(
            'No se encontró metadata para ' . $resolvedClientTxId .
            '. Archivos disponibles: ' . implode(', ', $fileList)
        );
    }

    $localData = json_decode(file_get_contents($localFile), true);
    $metadata = $localData['metadata'] ?? null;

    if (($localData['status'] ?? '') === 'approved') {
    webhook_log("TRANSACCIÓN YA PROCESADA: {$resolvedClientTxId}");

    echo json_encode([
        'success' => true,
        'message' => 'Pago ya procesado anteriormente',
        'transactionId' => (int)$transactionId,
        'clientTransactionId' => $resolvedClientTxId,
        'status' => 'Approved',
        'alreadyProcessed' => true
    ]);
    exit;
}

    if (!$metadata) {
        throw new Exception('No se encontró el objeto metadata en el registro local.');
    }

    if (empty($metadata['email']) || empty($metadata['course_id'])) {
        $missing = [];
        if (empty($metadata['email'])) $missing[] = 'email';
        if (empty($metadata['course_id'])) $missing[] = 'course_id';
        throw new Exception('Datos incompletos en registro local. Faltan: ' . implode(', ', $missing));
    }


    $course_id_secure = $metadata['course_id'];
    $email = strtolower(trim($metadata['email']));
    $firstname = trim($metadata['firstname'] ?? 'Estudiante');
    $lastname = trim($metadata['lastname'] ?? 'Kenth');

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        throw new Exception('Correo inválido en metadata local: ' . $email);
    }

    // 4) Resolver curso
    $course_id = kenth_verify_id($course_id_secure);
    if (!$course_id) {
        $course_id = (int)$course_id_secure;
    }

    if (empty($course_id)) {
        throw new Exception('No se pudo resolver el ID del curso.');
    }

    $course = $DB->get_record('course', ['id' => $course_id], '*', MUST_EXIST);

    // SEGURIDAD: el monto confirmado por PayPhone debe coincidir con el precio real del curso.
    $comm = kenth_get_commercial_data($course_id);
    $expectedPrice = (float) $comm['price'];
    if (($comm['offer_price'] ?? 0) > 0) {
        $expectedPrice = (float) $comm['offer_price'];
    }
    $expectedCents = (int) round($expectedPrice * 100);
    $paidCents = isset($data['amount']) ? (int) $data['amount'] : 0;

    if ($expectedCents > 0 && $paidCents !== $expectedCents) {
        webhook_log("MONTO NO COINCIDE: pagado={$paidCents} esperado={$expectedCents} curso={$course_id} tx={$resolvedClientTxId}");
        throw new Exception("El monto pagado no coincide con el precio del curso. Pagado: {$paidCents}, esperado: {$expectedCents} (centavos).");
    }

    // 5) Crear o recuperar usuario
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
        
        // Forma oficial de Moodle para setear password manual de forma segura
        update_internal_user_password($newuser, $plaintext_password);

        $user = $DB->get_record('user', ['id' => $newuser->id], '*', MUST_EXIST);
        set_user_preference('kenth_requires_onboarding', '1', $user->id);

        webhook_log("USUARIO NUEVO CREADO: {$email} con password set via API");

    } else {
        webhook_log("USUARIO EXISTENTE: {$email}");
    }

    // --- ENVÍO DE EMAIL DE CONFIRMACIÓN (Para nuevos y existentes) ---
    $subject = '¡Tu matrícula en KENTH Academy está lista!';
    $login_url = rtrim(get_backend_env('FRONTEND_BASE_URL') ?: 'http://localhost:5173', '/') . '/login';

    $password_section_html = "";
    if ($is_new_user && $plaintext_password) {
        $password_section_html = "
        <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);'>
            <div style='color: rgba(255,255,255,0.4); font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px;'>Contraseña Temporal</div>
            <div style='font-size: 20px; font-weight: 700; color: #C3073F; letter-spacing: 1px;'>{$plaintext_password}</div>
            <div style='color: #ffb800; font-size: 11px; margin-top: 5px;'>* Se te pedirá cambiarla en tu primer acceso.</div>
        </div>";
    }

    $html_message = "
    <div style='background-color: #0d0d0f; padding: 40px 20px; font-family: \"Segoe UI\", Helvetica, Arial, sans-serif;'>
        <div style='max-width: 600px; margin: 0 auto; background-color: #1A1A1D; border-radius: 24px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 40px rgba(0,0,0,0.5);'>
            <div style='background: linear-gradient(135deg, #6F2232 0%, #C3073F 100%); padding: 40px; text-align: center;'>
                <img src='https://i.imgur.com/BXiN2dO.png' alt='KENTH Academy' style='max-width: 200px; height: auto;'>
            </div>

            <!-- Contenido -->
            <div style='padding: 40px; color: #ffffff;'>
                <h2 style='margin-top: 0; font-size: 24px; font-weight: 700;'>¡Bienvenido a la comunidad!</h2>
                <p style='font-size: 16px; line-height: 1.6; color: rgba(255,255,255,0.8);'>
                    Hola <span style='color: #C3073F; font-weight: 700;'>{$firstname}</span>, nos alegra confirmarte que tu pago ha sido procesado con éxito y ya tienes acceso total a tu formación.
                </p>

                <!-- Box de Información -->
                <div style='background-color: rgba(255,255,255,0.05); border-radius: 20px; padding: 30px; margin: 30px 0; border: 1px solid rgba(255,255,255,0.05);'>
                    <div style='margin-bottom: 20px;'>
                        <div style='color: rgba(255,255,255,0.4); font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px;'>Curso Matriculado</div>
                        <div style='font-size: 18px; font-weight: 600; color: #ffffff;'>{$course->fullname}</div>
                    </div>
                    
                    <div style='margin-bottom: 20px;'>
                        <div style='color: rgba(255,255,255,0.4); font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px;'>Usuario de Acceso</div>
                        <div style='font-size: 16px; font-weight: 500; color: #ffffff;'>{$email}</div>
                    </div>

                    {$password_section_html}
                </div>

                <!-- Botón CTA -->
                <div style='text-align: center; margin: 40px 0;'>
                    <a href='{$login_url}' style='background-color: #C3073F; color: #ffffff; padding: 18px 35px; border-radius: 15px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block; box-shadow: 0 10px 20px rgba(195, 7, 63, 0.3);'>
                        EMPEZAR A APRENDER
                    </a>
                </div>

                <p style='font-size: 13px; line-height: 1.5; color: rgba(255,255,255,0.5); text-align: center; margin-top: 40px;'>
                    Si tienes alguna duda, responde a este correo y nuestro equipo te ayudará de inmediato.
                </p>
            </div>

            <!-- Footer -->
            <div style='padding: 30px; background-color: #121214; text-align: center; border-top: 1px solid rgba(255,255,255,0.05);'>
                <p style='margin: 0; font-size: 12px; color: rgba(255,255,255,0.3);'>
                    &copy; 2026 KENTH Academy. Desarrollado con pasión por la tecnología.
                </p>
            </div>
        </div>
    </div>";

    // Correo de confirmación para usuarios NUEVOS y EXISTENTES.
    // La sección de contraseña temporal solo se incluye para nuevos (ver $password_section_html).
    $mail_result = email_to_user(
        $user,
        core_user::get_support_user(),
        $subject,
        strip_tags($html_message),
        $html_message
    );

    if ($mail_result) {
        webhook_log("EMAIL ENVIADO EXITOSAMENTE A: {$email}");
    } else {
        webhook_log("FALLO EL ENVÍO DE EMAIL A: {$email}. Verifica la configuración SMTP de Moodle.");
    }


    // 6) Matricular si no está matriculado aún
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
            throw new Exception('No se encontró instancia de matrícula manual para el curso.');
        }

        $roleid = $DB->get_field('role', 'id', ['shortname' => 'student']);
        if (!$roleid) {
            throw new Exception('No se encontró el rol student.');
        }

        $enrol->enrol_user($manualInstance, $user->id, $roleid);
        webhook_log("USUARIO MATRICULADO: {$email} en curso {$course->id}");
    } else {
        webhook_log("USUARIO YA MATRICULADO: {$email} en curso {$course->id}");
    }

    // 7) Marcar registro local como aprobado
    $localData['status'] = 'approved';
    $localData['confirmed_at'] = date('Y-m-d H:i:s');
    $localData['payphone'] = [
        'transactionId' => (int)$transactionId,
        'clientTransactionId' => $resolvedClientTxId,
        'transactionStatus' => $status,
        'statusCode' => $statusCode
    ];
    file_put_contents($localFile, json_encode($localData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

    echo json_encode([
        'success' => true,
        'message' => $is_new_user ? 'Usuario creado y matriculado' : 'Pago validado y matrícula confirmada',
        'transactionId' => (int)$transactionId,
        'clientTransactionId' => $resolvedClientTxId,
        'status' => 'Approved'
    ]);

} catch (Exception $e) {
    webhook_log('ERROR: ' . $e->getMessage());

    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}