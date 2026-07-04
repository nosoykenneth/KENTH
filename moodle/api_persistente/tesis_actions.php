<?php
// tesis_actions.php - Micro-servicio para acciones de gestión de módulos y secciones
// Acciones: hide, show, duplicate, delete, move, rename_section, add_section, move_section

require(__DIR__ . '/../../config.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once(__DIR__ . '/tesis_lib.php');

header('Content-Type: application/json');

$token = required_param('token', PARAM_ALPHANUM);
$action = required_param('action', PARAM_ALPHANUMEXT); 

global $DB, $CFG;

try {
    // 1. Validar token y usuario
    $token_record = $DB->get_record('external_tokens', array('token' => $token));
    if (!$token_record) {
        throw new Exception("Token inválido");
    }
    $user = $DB->get_record('user', array('id' => $token_record->userid, 'deleted' => 0));
    complete_user_login($user);

    // 2. Ejecutar la acción según su tipo
    switch ($action) {
        // --- ACCIONES DE SECCIÓN ---
        
        case 'rename_section':
            $sectionid = required_param('sectionid', PARAM_INT);
            $newname   = required_param('name', PARAM_TEXT);

            $section = $DB->get_record('course_sections', array('id' => $sectionid), '*', MUST_EXIST);
            $context = context_course::instance($section->course);
            if (!has_capability('moodle/course:update', $context)) throw new Exception("Sin permisos");

            $course = $DB->get_record('course', array('id' => $section->course), '*', MUST_EXIST);
            $sectionname = trim($newname) === '' ? null : trim($newname);
            course_update_section($course, $section, array('name' => $sectionname));
            
            echo json_encode(array('success' => true));
            break;

        case 'add_section':
            $identifier = required_param('courseid', PARAM_RAW);
            $location   = optional_param('location', 0, PARAM_INT);

            $courseid = kenth_verify_id($identifier);
            if (!$courseid) throw new Exception("Firma de curso inválida");

            $context = context_course::instance($courseid);
            if (!has_capability('moodle/course:update', $context)) throw new Exception("Sin permisos");

            $course = $DB->get_record('course', array('id' => $courseid), '*', MUST_EXIST);
            $newsection = course_create_section($course, $location);
            echo json_encode(array('success' => true, 'sectionid' => $newsection->id, 'sectionnum' => $newsection->section));
            break;

        case 'move_section':
            $sectionid = required_param('sectionid', PARAM_INT);
            $newpos    = required_param('newpos', PARAM_INT);

            $section = $DB->get_record('course_sections', array('id' => $sectionid), '*', MUST_EXIST);
            $context = context_course::instance($section->course);
            if (!has_capability('moodle/course:update', $context)) throw new Exception("Sin permisos");

            $course = $DB->get_record('course', array('id' => $section->course), '*', MUST_EXIST);
            
            // SEGURIDAD: Moodle prohíbe mover cualquier cosa a la posición 0 (General)
            // o mover la propia sección 0.
            if ($newpos <= 0 || $section->section <= 0) {
                throw new Exception("No es posible mover temas hacia o desde la posición de cabecera (General).");
            }

            move_section_to($course, $section->section, $newpos);
            echo json_encode(array('success' => true));
            break;

        case 'update_section_summary':
            $sectionid = required_param('sectionid', PARAM_INT);
            $summary   = required_param('summary', PARAM_RAW); // RAW porque puede traer HTML

            $section = $DB->get_record('course_sections', array('id' => $sectionid), '*', MUST_EXIST);
            $context = context_course::instance($section->course);
            if (!has_capability('moodle/course:update', $context)) throw new Exception("Sin permisos");

            $course = $DB->get_record('course', array('id' => $section->course), '*', MUST_EXIST);
            
            // Actualizar el campo summary
            course_update_section($course, $section, array('summary' => $summary));
            
            echo json_encode(array('success' => true));
            break;

        case 'delete_section':
            $sectionid = required_param('sectionid', PARAM_INT);
            
            $section = $DB->get_record('course_sections', array('id' => $sectionid), '*', MUST_EXIST);
            $context = context_course::instance($section->course);
            if (!has_capability('moodle/course:update', $context)) throw new Exception("Sin permisos");

            if ($section->section <= 0) throw new Exception("No se puede eliminar la sección general");

            $course = $DB->get_record('course', array('id' => $section->course), '*', MUST_EXIST);
            
            // Moodle API para borrar sección y sus contenidos
            // El tercer parámetro true indica que se deben borrar los módulos que contiene
            course_delete_section($course, $section, true);
            
            echo json_encode(array('success' => true));
            break;

        // --- ACCIONES DE MÓDULO (ACTIVIDAD) ---

        case 'hide':
        case 'show':
        case 'delete':
        case 'duplicate':
        case 'move':
            $cmid = required_param('cmid', PARAM_INT);
            $cm = get_coursemodule_from_id('', $cmid);
            if (!$cm) throw new Exception("Módulo no encontrado");

            $context = context_course::instance($cm->course);
            if (!has_capability('moodle/course:manageactivities', $context)) throw new Exception("Sin permisos");

            if ($action === 'hide') {
                set_coursemodule_visible($cmid, 0);
                \core\event\course_module_updated::create_from_cm($cm)->trigger();
                echo json_encode(array('success' => true));
            } else if ($action === 'show') {
                set_coursemodule_visible($cmid, 1);
                \core\event\course_module_updated::create_from_cm($cm)->trigger();
                echo json_encode(array('success' => true));
            } else if ($action === 'delete') {
                course_delete_module($cmid);
                echo json_encode(array('success' => true));
            } else if ($action === 'duplicate') {
                $course = $DB->get_record('course', array('id' => $cm->course), '*', MUST_EXIST);
                $newcm = duplicate_module($course, $cm);
                echo json_encode(array('success' => true));
            } else if ($action === 'move') {
                $targetsectionid = required_param('targetsection', PARAM_INT);
                $beforecmid = optional_param('beforecmid', 0, PARAM_INT);
                $section = $DB->get_record('course_sections', array('id' => $targetsectionid), '*', MUST_EXIST);
                $beforecm = $beforecmid ? get_coursemodule_from_id('', $beforecmid) : null;
                moveto_module($cm, $section, $beforecm);
                echo json_encode(array('success' => true));
            }
            break;

        default:
            echo json_encode(array('success' => false, 'error' => 'Acción no válida'));
    }

} catch (Exception $e) {
    echo json_encode(array('success' => false, 'error' => $e->getMessage()));
}