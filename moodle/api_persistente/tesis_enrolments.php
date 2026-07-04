<?php
// tesis_enrolments.php - Gestión de matriculaciones y participantes del curso
// Acciones: list, enrol, unenrol

require(__DIR__ . '/../../config.php');
require_once(__DIR__ . '/tesis_lib.php');
require_once($CFG->dirroot . '/enrol/locallib.php');

header('Content-Type: application/json');

$token = required_param('token', PARAM_ALPHANUM);
$action = required_param('action', PARAM_ALPHANUMEXT);
$identifier = required_param('courseid', PARAM_RAW);

global $DB, $CFG;

$log = [];

try {
    $log[] = "Iniciando verificación de ID de curso...";
    $courseid = kenth_verify_id($identifier);
    if (!$courseid) throw new Exception("ID de curso inválido: $identifier");
    $log[] = "ID de curso verificado: $courseid";

    $log[] = "Validando token...";
    $token_record = $DB->get_record('external_tokens', array('token' => $token));
    if (!$token_record) throw new Exception("Token inválido o expirado");
    $log[] = "Token validado para el usuario Moodle ID: " . $token_record->userid;
    
    $log[] = "Cargando objeto usuario ejecutor...";
    $user_ejecutor = $DB->get_record('user', array('id' => $token_record->userid, 'deleted' => 0), '*', MUST_EXIST);
    $USER = $user_ejecutor; 
    $log[] = "Usuario cargado: " . fullname($USER);

    $log[] = "Obteniendo contexto del curso...";
    $context = context_course::instance($courseid);
    $log[] = "Contexto obtenido.";
    
    $log[] = "Verificando capacidades (Admin/Profesor)...";
    $esAdminSitio = is_siteadmin($USER->id);
    $esProfesor = has_capability('enrol/manual:enrol', $context, $USER->id) || has_capability('moodle/course:enrolreview', $context, $USER->id);

    if (!$esAdminSitio && !$esProfesor) {
        throw new Exception("No tienes permisos suficientes (Admin o Profesor) para ver participantes.");
    }
    $log[] = "Permisos verificados.";

    switch ($action) {
        case 'list':
            $log[] = "Consultando usuarios matriculados vía Moodle Core...";
            // Usamos la función estándar pero SOLO con campos reales de la tabla user
            $enrolled_users = get_enrolled_users($context, '', 0, 'u.id, u.firstname, u.lastname, u.email');
            $data = [];
            $log[] = "Usuarios encontrados: " . count($enrolled_users);

            foreach ($enrolled_users as $u) {
                $role_names = [];
                $is_target_admin = is_siteadmin($u->id);
                
                $log[] = "Procesando roles del usuario: " . $u->id;
                
                // Función correcta de Moodle para obtener los roles en un contexto
                $roles = get_user_roles($context, $u->id, true);
                if ($roles) {
                    foreach ($roles as $r) {
                        // role_get_name es la forma segura de obtener el nombre traducido del rol
                        $role_names[] = role_get_name($r, $context);
                    }
                }

                if (empty($role_names)) {
                    $role_names[] = "Estudiante"; 
                }

                $data[] = [
                    'id' => $u->id,
                    'fullname' => fullname($u),
                    'email' => $u->email,
                    'roles' => $role_names,
                    'isAdmin' => $is_target_admin,
                    'canBeUnenrolled' => ($esAdminSitio || (!$is_target_admin && $u->id != $USER->id))
                ];
            }

            echo json_encode([
                'success' => true, 
                'users' => $data,
                'count' => count($enrolled_users),
                'debug_log' => $log
            ]);
            break;

        case 'unenrol':
            $userid_to_remove = required_param('userid', PARAM_INT);
            
            // Seguridad: Un profe no puede desmatricular a un admin de sitio
            if (!$esAdminSitio && is_siteadmin($userid_to_remove)) {
                throw new Exception("No tienes permisos para desmatricular a un administrador");
            }

            // No puedes desmatricularte a ti mismo si no eres admin de sitio
            if (!$esAdminSitio && $userid_to_remove == $user_ejecutor->id) {
                throw new Exception("No puedes desmatricularte a ti mismo");
            }

            $instances = enrol_get_instances($courseid, true);
            $manual_instance = null;
            foreach ($instances as $instance) {
                if ($instance->enrol === 'manual') {
                    $manual_instance = $instance;
                    break;
                }
            }

            if (!$manual_instance) throw new Exception("No se encontró el método de matriculación manual");

            $plugin = enrol_get_plugin('manual');
            $plugin->unenrol_user($manual_instance, $userid_to_remove);

            echo json_encode(['success' => true]);
            break;

        case 'enrol':
            $email = required_param('email', PARAM_RAW);
            $target_user = $DB->get_record('user', array('email' => $email, 'deleted' => 0));
            
            if (!$target_user) {
                // Intentar por username si no es email
                $target_user = $DB->get_record('user', array('username' => $email, 'deleted' => 0));
            }

            if (!$target_user) throw new Exception("Usuario no encontrado");

            $instances = enrol_get_instances($courseid, true);
            $manual_instance = null;
            foreach ($instances as $instance) {
                if ($instance->enrol === 'manual') {
                    $manual_instance = $instance;
                    break;
                }
            }

            if (!$manual_instance) throw new Exception("El curso no tiene habilitada la matriculación manual");

            $roleid = $DB->get_field('role', 'id', array('shortname' => 'student'));
            $plugin = enrol_get_plugin('manual');
            $plugin->enrol_user($manual_instance, $target_user->id, $roleid);

            echo json_encode(['success' => true]);
            break;

        default:
            throw new Exception("Acción no válida");
    }

} catch (Throwable $e) {
    $error_msg = $e->getMessage();
    if (method_exists($e, 'get_debuginfo')) {
        $error_msg .= " [Debug: " . $e->get_debuginfo() . "]";
    } else if (isset($e->debuginfo)) {
        $error_msg .= " [Debug: " . $e->debuginfo . "]";
    }
    
    // Si es un error de Moodle, a veces el mensaje está en $e->a
    if (empty($error_msg) && isset($e->errorcode)) {
        $error_msg = "Moodle Error: " . $e->errorcode;
    }

    echo json_encode([
        'success' => false, 
        'error' => $error_msg ?: 'Error desconocido', 
        'debug_log' => $log,
        'trace' => $e->getTraceAsString()
    ]);
}
