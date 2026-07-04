<?php
// tesis_course_settings.php - Gestión de ajustes de curso (Nombre, Resumen, Imagen)
require(__DIR__ . '/../../config.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->libdir . '/gdlib.php');

require_once(__DIR__ . '/tesis_lib.php');

header('Content-Type: application/json');

$token      = required_param('token', PARAM_ALPHANUM);
$identifier = required_param('courseid', PARAM_RAW); // Recibe el Token Base64
$action     = optional_param('action', 'get', PARAM_ALPHA);

// 1. Validar Token y Sesión
$token_record = $DB->get_record('external_tokens', array('token' => $token));
if (!$token_record) {
    echo json_encode(['success' => false, 'error' => 'Token inválido']);
    exit;
}
$user = $DB->get_record('user', array('id' => $token_record->userid, 'deleted' => 0), '*', MUST_EXIST);
complete_user_login($user);

// 2. DECODIZAR Y VERIFICAR EL ID FIRMADO
$courseid = kenth_verify_id($identifier);

if (!$courseid) {
    // Si no es un ID firmado válido, DENERGAR ACCESO.
    // Esto previene que alguien ponga "?courseid=2" manualmente.
    echo json_encode(['success' => false, 'error' => 'Acceso denegado: Identificador de curso no válido o manipulado.']);
    exit;
}

// 3. Buscar el curso
$course = $DB->get_record('course', array('id' => $courseid));
if (!$course) {
    echo json_encode(['success' => false, 'error' => 'Curso no encontrado']);
    exit;
}

$context = context_course::instance($courseid);
error_log("KENTH DEBUG: Acceso seguro validado para user=" . $user->id . " en curso " . $courseid);

// Verificación de seguridad CRÍTICA
if (!is_enrolled($context, $user) && !has_capability('moodle/course:update', $context)) {
    echo json_encode(['success' => false, 'error' => 'No tienes permiso para acceder a este curso']);
    exit;
}

require_capability('moodle/course:update', $context);
error_log("KENTH DEBUG: Permisos validados OK.");

// --- ACCIÓN: OBTENER DATOS DEL CURSO ---
if ($action === 'get') {
    // Obtener la URL de la imagen del curso (overviewfiles)
    // 1. Buscar en overviewfiles (prioridad)
    $fs = get_file_storage();
    $files = $fs->get_area_files($context->id, 'course', 'overviewfiles', false, 'filename', false);
    
    // Si no hay, 2. Buscar en summary (retrocompatibilidad)
    if (empty($files)) {
        $files = $fs->get_area_files($context->id, 'course', 'summary', false, 'filename', false);
    }
    
    $courseimage = null;
    foreach ($files as $file) {
        if ($file->is_valid_image()) {
            $area = $file->get_filearea();
            $courseimage = '/moodle_api/proyecto_curso/api_persistente/tesis_image.php?token=' . $token . '&courseid=' . urlencode($identifier) . '&rev=' . $file->get_timemodified();
            break;
        }
    }

    // Extraer posición Y si existe en el summary ([kenth_pos_y:XX])
    $pos_y = 50;
    $summary_str = $course->summary ?? '';
    if (preg_match('/\[kenth_pos_y:\s*(\d+)\]/', $summary_str, $matches)) {
        $pos_y = (int)$matches[1];
    }

    echo json_encode([
        'success' => true,
        'data' => [
            'fullname'    => $course->fullname,
            'shortname'   => $course->shortname,
            'summary'     => preg_replace('/\[kenth_pos_y:\s*\d+\]/', '', $summary_str), // Limpiar tag para el frontend
            'visible'     => $course->visible,
            'category'    => $course->category,
            'courseimage' => $courseimage,
            'pos_y'       => $pos_y
        ]
    ]);
    exit;
}

// --- ACCIÓN: ACTUALIZAR DATOS ---
if ($action === 'update' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $json = file_get_contents('php://input');
    $data = json_decode($json);

    if (!$data) {
        echo json_encode(['success' => false, 'error' => 'Datos no recibidos']);
        exit;
    }

    // 1. ACTUALIZAMOS LOS DATOS DE TEXTO
    $course_to_update = new stdClass();
    $course_to_update->id        = $course->id;
    
    $summary = isset($data->summary) ? clean_param($data->summary, PARAM_RAW) : ($course->summary ?? '');
    $pos_y   = isset($data->pos_y) ? (int)$data->pos_y : 50;
    
    // Limpiar tags viejos y añadir el nuevo
    $summary = preg_replace('/\[kenth_pos_y:\s*\d+\]/', '', (string)$summary);
    $summary .= " [kenth_pos_y: $pos_y]";
    
    if (isset($data->fullname))  $course_to_update->fullname  = clean_param($data->fullname, PARAM_TEXT);
    else $course_to_update->fullname = $course->fullname;
    
    if (isset($data->shortname)) $course_to_update->shortname = clean_param($data->shortname, PARAM_TEXT);
    else $course_to_update->shortname = $course->shortname;
    $course_to_update->summary   = $summary;
    if (isset($data->visible))   $course_to_update->visible   = (int)$data->visible;
    if (isset($data->category))  $course_to_update->category  = (int)$data->category;

    try {
        // ACTUALIZAMOS EN DB DIRECTAMENTE (Usando la fórmula del perfil para evitar que la API limpie archivos)
        $DB->update_record('course', $course_to_update);
        
        // 2. PROCESAMOS LA IMAGEN (si se envió una nueva)
        if (!empty($data->imageData)) {
            $parts = explode(',', $data->imageData);
            $img_base64 = isset($parts[1]) ? $parts[1] : $parts[0];
            $img_data = base64_decode($img_base64);
            $size = strlen($img_data);
            
            // Log de depuración
            error_log("KENTH DEBUG: Procesando imagen de curso $course->id. Tamaño: $size bytes");
            
            if ($size > 0) {
                $fs = get_file_storage();
                
                // Borrar TODO en el área overviewfiles para este curso
                $fs->delete_area_files($context->id, 'course', 'overviewfiles');
                
                // NOMBRE ÚNICO GARANTIZADO
                $new_filename = 'cover_' . time() . '.jpg';
                
                // Guardar el nuevo archivo
                $file_record = array(
                    'contextid' => $context->id,
                    'component' => 'course',
                    'filearea'  => 'overviewfiles',
                    'itemid'    => 0,
                    'filepath'  => '/',
                    'filename'  => $new_filename, // <-- Usa el nombre único
                    'userid'    => $user->id,
                    'timecreated' => time(),
                    'timemodified' => time()
                );
                
                $fs->create_file_from_string($file_record, $img_data);
                
                // 2. PREPARAMOS LA NUEVA URL PARA MANDARLA A REACT
                $new_image_url = $CFG->wwwroot . '/webservice/pluginfile.php/' . $context->id . '/course/overviewfiles/0//' . $new_filename . '?rev=' . time();
                
                error_log("KENTH DEBUG: Imagen guardada exitosamente como $new_filename.");
            }
        }

        // 3. ACTUALIZAR TIMEMODIFIED Y PURGAR CACHÉS DE MOODLE
        $DB->set_field('course', 'timemodified', time(), array('id' => $course->id));
        
        // Purgar caché específica del curso para que el Dashboard (y getMyCourses) la refresque
        try {
            cache_helper::purge_by_event('changesincourse');
            rebuild_course_cache($course->id, true);
            
            // Purga manual de cachés persistentes de imágenes y contactos
            cache::make('core', 'course_image')->delete($course->id);
            cache::make('core', 'coursecontacts')->purge(); 
            
            // Disparar evento para que Moodle purgue los cachés de Webservices (core_enrol_get_users_courses)
            $event = \core\event\course_updated::create(array(
                'objectid' => $course->id,
                'context' => $context,
                'other' => array('shortname' => $course_to_update->shortname,
                                 'fullname' => $course_to_update->fullname,
                                 'updatedfields' => array('summary' => true, 'overviewfiles' => true))
            ));
            $event->trigger();
        } catch (Throwable $ce) {
            // Ignorar errores de caché
        }

        echo json_encode([
            'success' => true, 
            'message' => 'Curso actualizado correctamente',
            'newImageUrl' => isset($new_image_url) ? $new_image_url : null
        ]);
    } catch (Throwable $e) {
        error_log("KENTH FATAL ERROR: " . $e->getMessage() . " en linea " . $e->getLine());
        echo json_encode(['success' => false, 'error' => $e->getMessage()]);
    }
    exit;
}
