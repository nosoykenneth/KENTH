<?php
require_once($CFG->libdir . '/externallib.php');

class local_tesisai_external extends external_api {
    
    // 1. Definimos quÃ© recibimos (AÃ±adimos el 4to parÃ¡metro: usar_internet)
    public static function ask_ollama_parameters() {
        return new external_function_parameters(
            array(
                'prompt'         => new external_value(PARAM_RAW, 'Pregunta del estudiante'),
                'course_context' => new external_value(PARAM_RAW, 'Contexto de la lecciÃ³n', VALUE_DEFAULT, ''),
                'image_base64'   => new external_value(PARAM_RAW, 'Imagen en Base64', VALUE_DEFAULT, ''),
                'usar_internet'  => new external_value(PARAM_BOOL, 'Bandera para forzar busqueda web', VALUE_DEFAULT, false),
                'session_id'     => new external_value(PARAM_RAW, 'ID opcional de sesion conversacional', VALUE_DEFAULT, '')
            )
        );
    }

    // 2. La lÃ³gica principal orquestada por Python
    // (AÃ±adimos $usar_internet = false en los argumentos)
    public static function ask_ollama($prompt, $course_context = '', $image_base64 = '', $usar_internet = false, $session_id = '') {
        global $USER;

        $url = "http://127.0.0.1:8000/chat";

        // Limpiamos la imagen de cabeceras innecesarias si existe
        if (!empty($image_base64)) {
            $image_base64 = preg_replace('#^data:image/\w+;base64,#i', '', $image_base64);
        }

        // Si Moodle no envia una sesion explicita, generamos una estable por usuario y contexto.
        // Esto permite memoria conversacional sin cambiar la UI ni romper llamadas existentes.
        $userid = isset($USER->id) ? $USER->id : 0;
        if (empty($session_id)) {
            $context_hash = !empty($course_context) ? md5($course_context) : 'general';
            $session_id = "moodle_user_{$userid}_{$context_hash}";
        }

        // Armamos el paquete JSON asegurÃ¡ndonos de enviar el booleano
        $payload = array(
            'pregunta' => $prompt,
            'contexto_leccion' => $course_context,
            'imagen' => $image_base64,
            'usar_internet' => (bool)$usar_internet,
            'session_id' => $session_id,
            'source_client' => 'moodle',
            'user_id' => (string)$userid
        );

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 300); 
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        $result = curl_exec($ch);
        curl_close($ch);

        $json = json_decode($result);
        return isset($json->respuesta) ? $json->respuesta : "Error en el microservicio Python.";
    }

    // 3. Definimos quÃ© devolvemos (El texto generado)
    public static function ask_ollama_returns() {
        return new external_value(PARAM_RAW, 'Respuesta de la IA');
    }

    ////////////////////////////////////////////////////////////////
    // FUNCION PARA CREAR ETIQUETA EN CURSO
    ////////////////////////////////////////////////////////////////

    public static function create_label_parameters() {
        return new external_function_parameters(
            array(
                'courseid' => new external_value(PARAM_INT, 'ID del curso'),
                'section'  => new external_value(PARAM_INT, 'Numero de seccion/tema donde inyectar', VALUE_DEFAULT, 0),
                'content'  => new external_value(PARAM_RAW, 'Contenido HTML de la etiqueta')
            )
        );
    }

    public static function create_label($courseid, $section, $content) {
        global $DB, $CFG, $USER;
        require_once($CFG->dirroot.'/course/modlib.php');
        require_once($CFG->dirroot.'/course/lib.php');

        $params = self::validate_parameters(self::create_label_parameters(), array(
            'courseid' => $courseid,
            'section' => $section,
            'content' => $content
        ));

        $course = $DB->get_record('course', array('id' => $params['courseid']), '*', MUST_EXIST);
        $context = context_course::instance($course->id);
        self::validate_context($context); 

        $module = $DB->get_record('modules', array('name' => 'label'), '*', MUST_EXIST);
        
        // 1. Encontrar o crear la secciÃ³n correspondiente
        $sectionnum = (int)$params['section'];
        $section = $DB->get_record('course_sections', array('course' => $course->id, 'section' => $sectionnum));
        if (!$section) {
            $section = new stdClass();
            $section->course = $course->id;
            $section->section = $sectionnum;
            $section->summary = '';
            $section->summaryformat = FORMAT_HTML;
            $section->sequence = '';
            $section->visible = 1;
            $section->id = $DB->insert_record('course_sections', $section);
        }

        // 2. Insertar en la tabla original del mÃ³dulo `label`
        $label = new stdClass();
        $label->course = $course->id;
        $label->name = 'Etiqueta autogenerada';
        $label->intro = $params['content'];
        $label->introformat = FORMAT_HTML;
        $label->timemodified = time();
        $label->id = $DB->insert_record('label', $label);

        // 3. Vincular con `course_modules`
        $cm = new stdClass();
        $cm->course = $course->id;
        $cm->module = $module->id;
        $cm->instance = $label->id;
        $cm->section = $section->id;
        $cm->added = time();
        $cm->score = 0;
        $cm->indent = 0;
        $cm->visible = 1;
        $cm->visibleoncoursepage = 1;
        $cm->visibleold = 1;
        $cm->groupmode = 0;
        $cm->groupingid = 0;
        $cm->completion = 0;
        $cm->showdescription = 1;
        $cm->id = $DB->insert_record('course_modules', $cm);

        // 4. Actualizar la secuencia en `course_sections`
        $sequence = $section->sequence;
        if (empty($sequence)) {
            $sequence = $cm->id;
        } else {
            $sequence .= ",".$cm->id;
        }
        $DB->set_field('course_sections', 'sequence', $sequence, array('id' => $section->id));

        // 5. Refrescar cache de Moodle
        rebuild_course_cache($course->id);

        return "Â¡Contenido creado exitosamente mediante DB Direct (CMID: {$cm->id})!";
    }

    public static function create_label_returns() {
        return new external_value(PARAM_TEXT, 'Mensaje de estado');
    }

    ////////////////////////////////////////////////////////////////
    // FUNCION PARA CREAR TAREA (ASSIGN) EN CURSO HIBRIDA
    ////////////////////////////////////////////////////////////////

    public static function create_assign_parameters() {
        return new external_function_parameters(
            array(
                'courseid' => new external_value(PARAM_INT, 'ID del curso'),
                'section'  => new external_value(PARAM_INT, 'Numero de seccion/tema donde inyectar', VALUE_DEFAULT, 0),
                'name'     => new external_value(PARAM_TEXT, 'Titulo de la tarea'),
                'description'  => new external_value(PARAM_RAW, 'Instrucciones HTML'),
                'duedate'  => new external_value(PARAM_INT, 'Fecha limite formato UNIX timestamp')
            )
        );
    }

    public static function create_assign($courseid, $sectionnum, $name, $description, $duedate) {
        global $DB, $CFG, $USER;
        require_once($CFG->dirroot.'/course/lib.php');

        $params = self::validate_parameters(self::create_assign_parameters(), array(
            'courseid' => $courseid,
            'section' => $sectionnum,
            'name' => $name,
            'description' => $description,
            'duedate' => $duedate
        ));

        $course = $DB->get_record('course', array('id' => $params['courseid']), '*', MUST_EXIST);
        $context = context_course::instance($course->id);
        self::validate_context($context); 

        $module = $DB->get_record('modules', array('name' => 'assign'), '*', MUST_EXIST);
        
        // 1. Encontrar o crear la secciÃ³n
        $section = $DB->get_record('course_sections', array('course' => $course->id, 'section' => $params['section']));
        if (!$section) {
            $section = new stdClass();
            $section->course = $course->id;
            $section->section = $params['section'];
            $section->summary = '';
            $section->summaryformat = FORMAT_HTML;
            $section->sequence = '';
            $section->visible = 1;
            $section->id = $DB->insert_record('course_sections', $section);
        }

        // 2. Insertar en tabla base ASSIGN (Minimos indispensables hibridos)
        $assign = new stdClass();
        $assign->course = $course->id;
        $assign->name = $params['name'];
        $assign->intro = $params['description'];
        $assign->introformat = FORMAT_HTML;
        $assign->alwaysshowdescription = 1;
        $assign->submissiondrafts = 0;
        $assign->sendnotifications = 0;
        $assign->sendlatenotifications = 0;
        $assign->duedate = $params['duedate'];
        $assign->allowsubmissionsfromdate = time();
        $assign->cutoffdate = 0;
        $assign->gradingduedate = 0;
        $assign->grade = 100;
        $assign->timemodified = time();
        $assign->completionsubmit = 0;
        $assign->requiresubmissionstatement = 0;
        $assign->teamsubmission = 0;
        $assign->requireallteammemberssubmit = 0;
        $assign->blindmarking = 0;
        $assign->hidegrader = 0;
        $assign->revealidentities = 0;
        $assign->attemptreopenmethod = 'none';
        $assign->maxattempts = -1;
        $assign->markingworkflow = 0;
        $assign->markingallocation = 0;
        $assign->sendstudentnotifications = 1;
        $assign->preventsubmissionnotingroup = 0;
        
        $assign->id = $DB->insert_record('assign', $assign);

        // Activamos entrega por archivo y texto online por defecto en los plugins de Assign
        $plugin_file = new stdClass();
        $plugin_file->assignment = $assign->id;
        $plugin_file->plugin = 'file';
        $plugin_file->subtype = 'assignsubmission';
        $plugin_file->name = 'enabled';
        $plugin_file->value = '1';
        $DB->insert_record('assign_plugin_config', $plugin_file);

        $plugin_text = new stdClass();
        $plugin_text->assignment = $assign->id;
        $plugin_text->plugin = 'onlinetext';
        $plugin_text->subtype = 'assignsubmission';
        $plugin_text->name = 'enabled';
        $plugin_text->value = '1';
        $DB->insert_record('assign_plugin_config', $plugin_text);

        // 3. Vincular con `course_modules`
        $cm = new stdClass();
        $cm->course = $course->id;
        $cm->module = $module->id;
        $cm->instance = $assign->id;
        $cm->section = $section->id;
        $cm->added = time();
        $cm->score = 0;
        $cm->indent = 0;
        $cm->visible = 1;
        $cm->visibleoncoursepage = 1;
        $cm->visibleold = 1;
        $cm->groupmode = 0;
        $cm->groupingid = 0;
        $cm->completion = 0;
        $cm->showdescription = 1;
        $cm->id = $DB->insert_record('course_modules', $cm);

        // 4. Actualizar la secuencia en `course_sections`
        $sequence = $section->sequence;
        if (empty($sequence)) {
            $sequence = $cm->id;
        } else {
            $sequence .= ",".$cm->id;
        }
        $DB->set_field('course_sections', 'sequence', $sequence, array('id' => $section->id));

        // 5. Crear el context de este mÃ³dulo para roles (Requisito de Tareas)
        context_module::instance($cm->id);

        // 6. Refrescar cache de Moodle
        rebuild_course_cache($course->id);

        return "Tarea HÃ­brida Creada Exitosamente (CMID: {$cm->id})";
    }

    public static function create_assign_returns() {
        return new external_value(PARAM_TEXT, 'Mensaje de confirmaciÃ³n');
    }

    // ============================================================
    // get_permissions: fuente de verdad de autorizacion por CAPABILITIES.
    // La consumen el frontend (token del usuario) y FastAPI (token de
    // servicio + userid). Devuelve flags derivados de has_capability en el
    // contexto del curso. Contrato identico a tesis_role.php.
    // ============================================================
    public static function get_permissions_parameters() {
        return new external_function_parameters(
            array(
                'courseid' => new external_value(PARAM_INT, 'ID del curso (<=1 = contexto de sitio)'),
                'userid'   => new external_value(PARAM_INT, 'Usuario a consultar (0 = dueno del token)', VALUE_DEFAULT, 0),
            )
        );
    }

    public static function get_permissions($courseid, $userid = 0) {
        global $USER;

        $params = self::validate_parameters(self::get_permissions_parameters(),
            array('courseid' => $courseid, 'userid' => $userid));
        $courseid = (int)$params['courseid'];
        $targetuserid = (int)$params['userid'];

        // Resolver el usuario objetivo. Por defecto, el dueno del token.
        // Solo se permite consultar OTRO usuario si el caller es de confianza
        // (siteadmin o moodle/role:review en el sistema) -> uso server-to-server.
        if ($targetuserid > 0 && $targetuserid != $USER->id) {
            $systemctx = context_system::instance();
            if (!is_siteadmin() && !has_capability('moodle/role:review', $systemctx)) {
                throw new moodle_exception('nopermissions', 'error', '', 'consultar permisos de otro usuario');
            }
        } else {
            $targetuserid = $USER->id;
        }

        $es_tecnico = is_siteadmin($targetuserid);

        // Contexto de sitio (courseid <= 1 = SITEID): solo flags globales.
        if ($courseid <= 1) {
            return array(
                'puede_ver_curso'         => true,
                'es_profesor'             => false,
                'puede_administrar_curso' => false,
                'puede_revisar'           => false,
                'es_tecnico_rag'          => $es_tecnico,
                'es_invitado'             => false,
                'rol_efectivo'            => $es_tecnico ? 'siteadmin' : 'usuario',
            );
        }

        $context = context_course::instance($courseid, IGNORE_MISSING);
        if (!$context) {
            return array(
                'puede_ver_curso'         => $es_tecnico,
                'es_profesor'             => false,
                'puede_administrar_curso' => false,
                'puede_revisar'           => false,
                'es_tecnico_rag'          => $es_tecnico,
                'es_invitado'             => false,
                'rol_efectivo'            => $es_tecnico ? 'siteadmin' : 'desconocido',
            );
        }

        // Seguridad WS: el usuario del token debe poder acceder al contexto.
        self::validate_context($context);

        $enrolled  = is_enrolled($context, $targetuserid);
        $puede_ver = $es_tecnico || $enrolled || has_capability('moodle/course:view', $context, $targetuserid);

        // ESTRUCTURA/ADMIN DEL CURSO: se decide por ROL manager/coursecreator (o
        // siteadmin), NO por moodle/course:update. Motivo: por defecto el
        // editingteacher TIENE course:update, asi que usar esa capability
        // mezclaria "profesor editor" con "gestor" y le abriria el editor
        // avanzado. El rol separa correctamente ambos tiers.
        $has_manager_role = false;
        foreach (get_user_roles($context, $targetuserid, true) as $r) {
            if ($r->shortname === 'manager' || $r->shortname === 'coursecreator') {
                $has_manager_role = true;
                break;
            }
        }

        $es_profesor   = has_capability('moodle/course:manageactivities', $context, $targetuserid);
        $puede_admin   = $es_tecnico || $has_manager_role;
        $puede_revisar = $es_profesor || $puede_admin
            || has_capability('moodle/grade:viewall', $context, $targetuserid);
        // Invitado: ve el curso pero NO esta matriculado ni es docente/admin/tecnico.
        $es_invitado   = $puede_ver && !$enrolled && !$es_profesor && !$puede_admin && !$es_tecnico;

        if ($es_tecnico) {
            $rol = 'siteadmin';
        } else if ($puede_admin) {
            $rol = 'gestor';
        } else if ($es_profesor) {
            $rol = 'profesor';
        } else if ($puede_revisar) {
            $rol = 'profesor_sin_edicion';
        } else if ($es_invitado) {
            $rol = 'invitado';
        } else if ($puede_ver) {
            $rol = 'estudiante';
        } else {
            $rol = 'desconocido';
        }

        return array(
            'puede_ver_curso'         => $puede_ver,
            'es_profesor'             => $es_profesor,
            'puede_administrar_curso' => $puede_admin,
            'puede_revisar'           => $puede_revisar,
            'es_tecnico_rag'          => $es_tecnico,
            'es_invitado'             => $es_invitado,
            'rol_efectivo'            => $rol,
        );
    }

    public static function get_permissions_returns() {
        return new external_single_structure(
            array(
                'puede_ver_curso'         => new external_value(PARAM_BOOL, 'moodle/course:view o matriculado'),
                'es_profesor'             => new external_value(PARAM_BOOL, 'moodle/course:manageactivities'),
                'puede_administrar_curso' => new external_value(PARAM_BOOL, 'moodle/course:update'),
                'puede_revisar'           => new external_value(PARAM_BOOL, 'moodle/grade:viewall'),
                'es_tecnico_rag'          => new external_value(PARAM_BOOL, 'is_siteadmin'),
                'es_invitado'             => new external_value(PARAM_BOOL, 'acceso guest / sin matricula'),
                'rol_efectivo'            => new external_value(PARAM_ALPHANUMEXT, 'etiqueta derivada (solo UI)'),
            )
        );
    }
}


