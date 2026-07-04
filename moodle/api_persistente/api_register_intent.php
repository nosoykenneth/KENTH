<?php
/**
 * api_register_intent.php - v5.0
 * Registra la intención de pago SOLO si vienen los datos mínimos requeridos.
 */

// Alinear la zona horaria con el webhook (que hereda la hora local del servidor vía
// Moodle config.php). Este script es ligero y NO carga config.php, así que sin esto
// created_at quedaba en otra zona que confirmed_at (parecía "creado después de confirmado").
date_default_timezone_set('America/Guayaquil');

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

function intent_log($message) {
    file_put_contents(
        __DIR__ . '/log_intent.txt',
        '[' . date('Y-m-d H:i:s') . '] ' . $message . PHP_EOL,
        FILE_APPEND
    );
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode([
        "success" => false,
        "error" => "Método no permitido"
    ]);
    exit;
}

$input = file_get_contents('php://input');
$data = json_decode($input, true);

intent_log('INPUT RAW: ' . $input);

if (!$data || !is_array($data)) {
    echo json_encode([
        "success" => false,
        "error" => "JSON inválido o vacío"
    ]);
    exit;
}

$txId = trim($data['clientTransactionId'] ?? '');
$courseId = trim($data['course_id'] ?? '');
$email = trim($data['email'] ?? '');
$firstname = trim($data['firstname'] ?? '');
$lastname = trim($data['lastname'] ?? '');

if ($txId === '') {
    echo json_encode([
        "success" => false,
        "error" => "Falta clientTransactionId"
    ]);
    exit;
}

if ($courseId === '') {
    echo json_encode([
        "success" => false,
        "error" => "Falta course_id"
    ]);
    exit;
}

if ($email === '') {
    echo json_encode([
        "success" => false,
        "error" => "Falta email"
    ]);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode([
        "success" => false,
        "error" => "Email inválido"
    ]);
    exit;
}

// Nombres por defecto solo si realmente no llegaron
if ($firstname === '') {
    $firstname = 'Estudiante';
}
if ($lastname === '') {
    $lastname = 'Kenth';
}

$paymentsDir = __DIR__ . '/payments';
if (!file_exists($paymentsDir)) {
    mkdir($paymentsDir, 0777, true);
}

$registry = [
    "metadata" => [
        "course_id" => $courseId,
        "email" => $email,
        "firstname" => $firstname,
        "lastname" => $lastname
    ],
    "status" => "pending",
    "created_at" => date('Y-m-d H:i:s'),
    "source" => "SDK_Button_Frontend"
];

$filePath = $paymentsDir . '/' . $txId . '.json';
file_put_contents($filePath, json_encode($registry, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

intent_log("REGISTERED: {$txId} | course_id={$courseId} | email={$email}");

echo json_encode([
    "success" => true,
    "message" => "Intención registrada correctamente",
    "clientTransactionId" => $txId
]);