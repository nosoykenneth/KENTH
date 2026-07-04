<?php
define('NO_OUTPUT_BUFFERING', true);
require(__DIR__ . '/../../config.php');
require_once(__DIR__ . '/tesis_lib.php');

// Forzamos el tipo de contenido y el código de respuesta
header('Content-Type: application/json');
http_response_code(200);

try {
    // Usamos $_GET para evitar que required_param de Moodle lance excepciones raras
    $token = isset($_GET['token']) ? clean_param($_GET['token'], PARAM_ALPHANUM) : '';
    
    if (empty($token)) {
        echo json_encode(['error' => 'No token']);
        exit;
    }

    $token_record = $DB->get_record('external_tokens', array('token' => $token));
    if (!$token_record) {
        echo json_encode(['error' => 'Invalid token']);
        exit;
    }

    $userid = $token_record->userid;
$user = $DB->get_record('user', array('id' => $userid), '*', MUST_EXIST);
complete_user_login($user);
    
    // Obtenemos los cursos de forma directa vía SQL para evitar dependencias de API
    $sql = "SELECT c.* 
            FROM {course} c
            JOIN {enrol} e ON e.courseid = c.id
            JOIN {user_enrolments} ue ON ue.enrolid = e.id
            WHERE ue.userid = ? AND c.id <> ?";
    $courses = $DB->get_records_sql($sql, [$userid, SITEID]);

    $categories = $DB->get_records('course_categories');

    $secure_courses = [];
    foreach ($courses as $course) {
        $c = new stdClass();
        $c->id           = kenth_sign_id($course->id);
        $c->fullname     = $course->fullname;
        $c->shortname    = $course->shortname;
        $c->summary      = $course->summary;
        $c->visible      = $course->visible;
        
        // --- LÓGICA PARA LA IMAGEN DEL CURSO ---
        $courseimage = "";
        $course_context = context_course::instance($course->id);
        $fs = get_file_storage();
        $files = $fs->get_area_files($course_context->id, 'course', 'overviewfiles', false, 'filename', false);
        if (empty($files)) {
            $files = $fs->get_area_files($course_context->id, 'course', 'summary', false, 'filename', false);
        }
        
        foreach ($files as $file) {
            if ($file->is_valid_image()) {
                // USAMOS NUESTRO PROPIO PROXY SEGURO QUE SÍ ACEPTA EL ID FIRMADO
                $courseimage = '/moodle_api/proyecto_curso/api_persistente/tesis_image.php?token=' . $token . '&courseid=' . urlencode($c->id) . '&rev=' . $file->get_timemodified();
                break;
            }
        }
        $c->courseimage  = $courseimage;
        
        $catid = $course->category;
        $c->categoryname = isset($categories[$catid]) ? $categories[$catid]->name : 'CURSO';
        
        $secure_courses[] = $c;
    }

    echo json_encode($secure_courses);

} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
