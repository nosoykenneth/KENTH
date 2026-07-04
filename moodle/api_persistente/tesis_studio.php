<?php
// tesis_studio.php - Túnel de autenticación Headless para React

// 1. Iniciar el motor de Moodle
require(__DIR__ . '/../../config.php');

global $DB, $USER;

// 2. Recibir el token desde el Iframe de React
$token = required_param('token', PARAM_ALPHANUM);

// 3. Buscar a quién le pertenece este token de la API
$token_record = $DB->get_record('external_tokens', array('token' => $token));

if (!$token_record) {
    die('Acceso denegado: Token inválido o expirado.');
}

// 4. Obtener los datos del usuario
$user = $DB->get_record('user', array('id' => $token_record->userid, 'deleted' => 0));

if (!$user) {
    die('Acceso denegado: Usuario no encontrado.');
}

// 5. ¡LA MAGIA! Forzar el inicio de sesión web en el navegador.
// Esto genera la cookie de sesión y el anhelado sesskey para este usuario.
complete_user_login($user);

// 6. Determinar el modo: Crear, Editar o Ver
$modname = required_param('modname', PARAM_RAW);

// El courseid que recibimos de React es el IDENTIFICADOR FIRMADO (Base64)
$identifier = required_param('courseid', PARAM_RAW);
require_once(__DIR__ . '/tesis_lib.php');

$courseid = kenth_verify_id($identifier);

if (!$courseid) {
    die('Acceso denegado: Firma de curso inválida o expirada.');
}

if ($modname === '__edit__') {
    // MODO EDICIÓN: Abrir formulario de edición de un módulo existente
    $cmid = required_param('cmid', PARAM_INT);
    
    $redirect_url = new moodle_url('/course/modedit.php', array(
        'update' => $cmid,
        'return' => 0,
        'sr' => 0,
        'sesskey' => sesskey(),
        'isheadless' => 1
    ));
} else {
    // MODO CREACIÓN: Crear un módulo nuevo
    // LEER LA SECCIÓN DESDE LA URL (Si no viene, por defecto es 0)
    $sectionnum = optional_param('section', 0, PARAM_INT);
    
    $redirect_url = new moodle_url('/course/modedit.php', array(
        'add' => $modname,
        'type' => '',
        'course' => $courseid,
        'section' => $sectionnum,
        'return' => 0,
        'sr' => 0,
        'sesskey' => sesskey(),
        'isheadless' => 1
    ));
}

// 7. Lanzar el Iframe al destino
redirect($redirect_url);
