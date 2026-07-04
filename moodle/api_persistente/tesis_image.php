<?php
// tesis_image.php - Proxy para servir imágenes de curso de forma segura
require(__DIR__ . '/../../config.php');
require_once(__DIR__ . '/tesis_lib.php');

$token      = isset($_GET['token']) ? clean_param($_GET['token'], PARAM_ALPHANUM) : '';
$identifier = isset($_GET['courseid']) ? clean_param($_GET['courseid'], PARAM_RAW) : '';

if (!$token || !$identifier) {
    header("HTTP/1.0 404 Not Found");
    exit;
}

// 1. Validar Token
$token_record = $DB->get_record('external_tokens', array('token' => $token));
if (!$token_record) {
    header("HTTP/1.0 403 Forbidden");
    exit;
}

// 2. Verificar ID firmado
$courseid = kenth_verify_id($identifier);
if (!$courseid) {
    header("HTTP/1.0 403 Forbidden");
    exit;
}

// 3. Obtener el archivo
$context = context_course::instance($courseid);
$fs = get_file_storage();
$files = $fs->get_area_files($context->id, 'course', 'overviewfiles', false, 'filename', false);
if (empty($files)) {
    $files = $fs->get_area_files($context->id, 'course', 'summary', false, 'filename', false);
}

foreach ($files as $file) {
    if ($file->is_valid_image()) {
        $mimetype = $file->get_mimetype();
        header("Content-Type: $mimetype");
        header("Content-Length: " . $file->get_filesize());
        echo $file->get_content();
        exit;
    }
}

header("HTTP/1.0 404 Not Found");
