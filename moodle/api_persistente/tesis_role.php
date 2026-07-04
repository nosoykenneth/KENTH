<?php
// tesis_role.php - Micro-servicio para verificar permisos en Headless

require(__DIR__ . '/../../config.php');
require_once(__DIR__ . '/tesis_lib.php');
header('Content-Type: application/json');

// 1. Recibir parámetros
$token = required_param('token', PARAM_ALPHANUM);
$identifier = optional_param('courseid', '', PARAM_RAW);
$sitemode = optional_param('site', 0, PARAM_BOOL);

global $DB;

// 2. Buscar al usuario dueño del token
$token_record = $DB->get_record('external_tokens', array('token' => $token));
if (!$token_record) {
    echo json_encode(array('esProfesor' => false, 'error' => 'Token inválido'));
    exit;
}

// 2b. MODO SITIO: sin curso (para la barra lateral / entradas de admin de sitio).
//     Solo resuelve el flag global esTecnicoRAG (is_siteadmin) desde el token;
//     no requiere id firmado. Espeja la rama de sitio de la WS get_permissions.
if ($sitemode || $identifier === '' || $identifier === 'site') {
    $es_tecnico = is_siteadmin($token_record->userid);
    echo json_encode(array(
        'esProfesor'            => false,
        'puedeAdministrarCurso' => false,
        'esTecnicoRAG'          => $es_tecnico,
        'puedeVerCurso'         => true,
        'puedeRevisar'          => false,
        'esInvitado'            => false,
        'rolEfectivo'           => $es_tecnico ? 'siteadmin' : 'usuario',
    ));
    exit;
}

// 3. DECODIZAR Y VERIFICAR EL ID FIRMADO
$courseid = kenth_verify_id($identifier);

if (!$courseid) {
    echo json_encode(array('esProfesor' => false, 'error' => 'Acceso denegado'));
    exit;
}

// 4. Buscar el curso
$course = $DB->get_record('course', array('id' => $courseid));
if (!$course) {
    echo json_encode(array('esProfesor' => false, 'error' => 'Curso no encontrado'));
    exit;
}

$context = context_course::instance($courseid);
$userid  = $token_record->userid;

// 4. Capacidades reales en el contexto del curso (fuente de verdad de roles).
//    Contrato IDENTICO a la WS local_tesisai_get_permissions (has_capability):
//      - puedeVerCurso            -> moodle/course:view OR matriculado (incluye guest)
//      - esProfesor  (pedagogia)  -> moodle/course:manageactivities (editingteacher+)
//      - puedeAdministrarCurso    -> ROL manager/coursecreator (o siteadmin). Se usa el
//        ROL, NO course:update, porque el editingteacher TIENE course:update por defecto
//        (usar la capability mezclaria profesor con gestor y le abriria el editor avanzado).
//      - puedeRevisar (analitica) -> moodle/grade:viewall (incluye profesor sin edicion)
//      - esTecnicoRAG             -> is_siteadmin
//      - esInvitado               -> ve el curso pero no matriculado ni docente/admin
$es_tecnico = is_siteadmin($userid);
$enrolled   = is_enrolled($context, $userid);
$puede_ver  = $es_tecnico || $enrolled || has_capability('moodle/course:view', $context, $userid);

// Verificación de seguridad: sin acceso alguno al curso -> denegar.
if (!$puede_ver) {
    echo json_encode(array(
        'esProfesor' => false, 'puedeAdministrarCurso' => false, 'esTecnicoRAG' => false,
        'puedeVerCurso' => false, 'puedeRevisar' => false, 'esInvitado' => false,
        'rolEfectivo' => 'desconocido', 'error' => 'No tienes acceso a este curso',
    ));
    exit;
}

$has_manager_role = false;
foreach (get_user_roles($context, $userid, true) as $r) {
    if ($r->shortname === 'manager' || $r->shortname === 'coursecreator') { $has_manager_role = true; break; }
}

$es_profesor   = has_capability('moodle/course:manageactivities', $context, $userid);
$puede_admin   = $es_tecnico || $has_manager_role;
$puede_revisar = $es_profesor || $puede_admin || has_capability('moodle/grade:viewall', $context, $userid);
$es_invitado   = $puede_ver && !$enrolled && !$es_profesor && !$puede_admin && !$es_tecnico;

if ($es_tecnico)          { $rol = 'siteadmin'; }
else if ($puede_admin)    { $rol = 'gestor'; }
else if ($es_profesor)    { $rol = 'profesor'; }
else if ($puede_revisar)  { $rol = 'profesor_sin_edicion'; }
else if ($es_invitado)    { $rol = 'invitado'; }
else                      { $rol = 'estudiante'; }

// 5. Devolver la respuesta a React (camelCase; esProfesor se conserva por compat).
echo json_encode(array(
    'esProfesor'            => $es_profesor,
    'puedeAdministrarCurso' => $puede_admin,
    'esTecnicoRAG'          => $es_tecnico,
    'puedeVerCurso'         => $puede_ver,
    'puedeRevisar'          => $puede_revisar,
    'esInvitado'            => $es_invitado,
    'rolEfectivo'           => $rol,
));