<?php
require_once(__DIR__ . '/../../config.php');
require_once('tesis_lib.php');

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

header('Content-Type: application/json; charset=utf-8');

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

try {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);

    if (!$data) {
        throw new Exception('Payload inválido.');
    }

    $clientTransactionId = trim($data['clientTransactionId'] ?? '');
    $courseIdRaw = $data['course_id'] ?? '';
    $email = trim($data['email'] ?? '');
    $firstname = trim($data['firstname'] ?? '');
    $lastname = trim($data['lastname'] ?? '');
    $courseName = trim($data['course_name'] ?? 'Curso KENTH');

    $courseId = kenth_verify_id($courseIdRaw);
    if (!$courseId) {
        $courseId = (int)$courseIdRaw;
    }

    if (!$clientTransactionId || !$courseId || !$email || !$firstname || !$lastname) {
        throw new Exception('Faltan parámetros requeridos.');
    }

    $payphoneToken = get_backend_env('PAYPHONE_TOKEN');
    $storeId = get_backend_env('PAYPHONE_STORE_ID');

    if (!$payphoneToken || !$storeId) {
        throw new Exception('Credenciales PayPhone no configuradas.');
    }

    // SEGURIDAD: el precio SIEMPRE proviene de la BD (kenth_commercial), nunca del cliente.
    $comm = kenth_get_commercial_data($courseId);
    $realPrice = (float) $comm['price'];
    if (($comm['offer_price'] ?? 0) > 0) {
        $realPrice = (float) $comm['offer_price'];
    }

    if ($realPrice <= 0) {
        throw new Exception('El curso no tiene un precio válido configurado.');
    }

    $amountCents = (int) round($realPrice * 100);
    $frontendBase = rtrim(get_backend_env('FRONTEND_BASE_URL') ?: 'http://localhost:5173', '/');

    $payload = [
        'amount' => $amountCents,
        'amountWithoutTax' => $amountCents,
        'currency' => 'USD',
        'clientTransactionId' => $clientTransactionId,
        'storeId' => $storeId,
        'reference' => 'Matrícula: ' . mb_substr($courseName, 0, 100),
        'responseUrl' => $frontendBase . '/checkout-success',
        'cancellationUrl' => $frontendBase . '/checkout/' . $courseIdRaw,
        'email' => $email,
        'lang' => 'es'
    ];

    $ch = curl_init('https://pay.payphonetodoesposible.com/api/button/Prepare');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $payphoneToken,
        'Content-Type: application/json'
    ]);

    $response = curl_exec($ch);

    if ($response === false) {
        throw new Exception('Error cURL: ' . curl_error($ch));
    }

    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $result = json_decode($response, true);

    if ($httpCode < 200 || $httpCode >= 300 || !$result) {
        throw new Exception('Error preparando pago con PayPhone: ' . $response);
    }

    $payUrl =
        $result['payWithCard'] ??
        $result['payWithPayPhone'] ??
        $result['url'] ??
        $result['paymentUrl'] ??
        null;

    if (!$payUrl) {
        throw new Exception('PayPhone no devolvió una URL de pago válida.');
    }

    echo json_encode([
        'success' => true,
        'payUrl' => $payUrl,
        'raw' => $result
    ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}
