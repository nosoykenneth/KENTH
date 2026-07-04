<?php
defined('MOODLE_INTERNAL') || die();

function xmldb_local_tesisai_upgrade($oldversion) {
    global $CFG, $DB;

    $dbman = $DB->get_manager();

    if ($oldversion < 2026051101) {
        require_once($CFG->libdir . '/xmldb/xmldb_file.php');

        $xmldbfile = new xmldb_file($CFG->dirroot . '/local/tesisai/db/install.xml');
        if ($xmldbfile->fileExists()) {
            $xmldbfile->loadXMLStructure();
            $structure = $xmldbfile->getStructure();
            foreach ($structure->getTables() as $table) {
                if (!$dbman->table_exists($table)) {
                    $dbman->create_table($table);
                }
            }
        }

        upgrade_plugin_savepoint(true, 2026051101, 'local', 'tesisai');
    }

    if ($oldversion < 2026052700) {
        // Crea las tablas nuevas declaradas en install.xml que aun no existan
        // (local_tesisai_axes, local_tesisai_documents). Patron idempotente.
        require_once($CFG->libdir . '/xmldb/xmldb_file.php');

        $xmldbfile = new xmldb_file($CFG->dirroot . '/local/tesisai/db/install.xml');
        if ($xmldbfile->fileExists()) {
            $xmldbfile->loadXMLStructure();
            $structure = $xmldbfile->getStructure();
            foreach ($structure->getTables() as $table) {
                if (!$dbman->table_exists($table)) {
                    $dbman->create_table($table);
                }
            }
        }

        upgrade_plugin_savepoint(true, 2026052700, 'local', 'tesisai');
    }

    if ($oldversion < 2026060300) {
        // Crea las tablas nuevas declaradas en install.xml que aun no existan
        // (local_tesisai_transcript_segments). Patron idempotente.
        require_once($CFG->libdir . '/xmldb/xmldb_file.php');

        $xmldbfile = new xmldb_file($CFG->dirroot . '/local/tesisai/db/install.xml');
        if ($xmldbfile->fileExists()) {
            $xmldbfile->loadXMLStructure();
            $structure = $xmldbfile->getStructure();
            foreach ($structure->getTables() as $table) {
                if (!$dbman->table_exists($table)) {
                    $dbman->create_table($table);
                }
            }
        }

        upgrade_plugin_savepoint(true, 2026060300, 'local', 'tesisai');
    }

    if ($oldversion < 2026060600) {
        // Fase 1 saneamiento: alinea el esquema XMLDB con las columnas que el
        // backend Python ya creaba por ALTER TABLE en runtime. Patron idempotente:
        // solo agrega campos/tablas que aun no existan. No elimina nada.
        require_once($CFG->libdir . '/ddllib.php');

        // 1) Columnas nuevas en local_tesisai_documents.
        $documents = new xmldb_table('local_tesisai_documents');
        $docfields = [
            new xmldb_field('lesson_id', XMLDB_TYPE_CHAR, '64', null, XMLDB_NOTNULL, null, '', 'axis_id'),
            new xmldb_field('visible_to_student', XMLDB_TYPE_INTEGER, '1', null, XMLDB_NOTNULL, null, '0', 'allowed_for_indexing'),
            new xmldb_field('media_type', XMLDB_TYPE_CHAR, '32', null, XMLDB_NOTNULL, null, '', 'visible_to_student'),
            new xmldb_field('scope', XMLDB_TYPE_CHAR, '16', null, XMLDB_NOTNULL, null, 'course', 'media_type'),
            new xmldb_field('is_global', XMLDB_TYPE_INTEGER, '1', null, XMLDB_NOTNULL, null, '0', 'scope'),
            new xmldb_field('index_status', XMLDB_TYPE_CHAR, '16', null, XMLDB_NOTNULL, null, 'pending', 'is_global'),
            new xmldb_field('chunk_count', XMLDB_TYPE_INTEGER, '10', null, XMLDB_NOTNULL, null, '0', 'index_status'),
        ];
        if ($dbman->table_exists($documents)) {
            foreach ($docfields as $field) {
                if (!$dbman->field_exists($documents, $field)) {
                    $dbman->add_field($documents, $field);
                }
            }
            $scopeix = new xmldb_index('doc_scope_ix', XMLDB_INDEX_NOTUNIQUE, ['scope']);
            if (!$dbman->index_exists($documents, $scopeix)) {
                $dbman->add_index($documents, $scopeix);
            }
            $lessonix = new xmldb_index('doc_lesson_ix', XMLDB_INDEX_NOTUNIQUE, ['lesson_id']);
            if (!$dbman->index_exists($documents, $lessonix)) {
                $dbman->add_index($documents, $lessonix);
            }
        }

        // 2) Columnas nuevas en local_tesisai_tutor_sessions.
        $sessions = new xmldb_table('local_tesisai_tutor_sessions');
        if ($dbman->table_exists($sessions)) {
            $sessfields = [
                new xmldb_field('course_id', XMLDB_TYPE_CHAR, '64', null, XMLDB_NOTNULL, null, '', 'user_id'),
                new xmldb_field('lesson_id', XMLDB_TYPE_CHAR, '64', null, XMLDB_NOTNULL, null, '', 'course_id'),
            ];
            foreach ($sessfields as $field) {
                if (!$dbman->field_exists($sessions, $field)) {
                    $dbman->add_field($sessions, $field);
                }
            }
        }

        // 3) Columna user_id en local_tesisai_tutor_messages.
        $messages = new xmldb_table('local_tesisai_tutor_messages');
        if ($dbman->table_exists($messages)) {
            $msguser = new xmldb_field('user_id', XMLDB_TYPE_CHAR, '64', null, XMLDB_NOTNULL, null, '', 'session_id');
            if (!$dbman->field_exists($messages, $msguser)) {
                $dbman->add_field($messages, $msguser);
            }
        }

        upgrade_plugin_savepoint(true, 2026060600, 'local', 'tesisai');
    }

    if ($oldversion < 2026060700) {
        // Fase 2: resource_type semantico (uso pedagogico) en documents.
        require_once($CFG->libdir . '/ddllib.php');
        $documents = new xmldb_table('local_tesisai_documents');
        if ($dbman->table_exists($documents)) {
            $rt = new xmldb_field('resource_type', XMLDB_TYPE_CHAR, '32', null, XMLDB_NOTNULL, null, 'other', 'media_type');
            if (!$dbman->field_exists($documents, $rt)) {
                $dbman->add_field($documents, $rt);
            }
        }
        upgrade_plugin_savepoint(true, 2026060700, 'local', 'tesisai');
    }

    if ($oldversion < 2026061100) {
        // Fase A del editor de leccion:
        // - lessons: + moodle_section_id (alinea con el runtime Python),
        //   + delegated_to_tutor_json, + attribution_constraints_json,
        //   - source_script_file, - expected_actions_json (deprecados, sin datos).
        // - lesson_blocks / lesson_prompts / transcript_segments: + course_id
        //   (denormalizado desde la leccion padre) + indice (course_id, lesson_id).
        require_once($CFG->libdir . '/ddllib.php');

        $lessons = new xmldb_table('local_tesisai_lessons');
        if ($dbman->table_exists($lessons)) {
            $adds = [
                new xmldb_field('moodle_section_id', XMLDB_TYPE_CHAR, '64', null, XMLDB_NOTNULL, null, '', 'axis_id'),
                new xmldb_field('delegated_to_tutor_json', XMLDB_TYPE_TEXT, null, null, null, null, null, 'prerequisites_json'),
                new xmldb_field('attribution_constraints_json', XMLDB_TYPE_TEXT, null, null, null, null, null, 'delegated_to_tutor_json'),
            ];
            foreach ($adds as $field) {
                if (!$dbman->field_exists($lessons, $field)) {
                    $dbman->add_field($lessons, $field);
                }
            }
            $drops = [
                new xmldb_field('source_script_file'),
                new xmldb_field('expected_actions_json'),
            ];
            foreach ($drops as $field) {
                if ($dbman->field_exists($lessons, $field)) {
                    $dbman->drop_field($lessons, $field);
                }
            }
            $sectionix = new xmldb_index('course_section_ix', XMLDB_INDEX_NOTUNIQUE, ['course_id', 'moodle_section_id']);
            if (!$dbman->index_exists($lessons, $sectionix)) {
                $dbman->add_index($lessons, $sectionix);
            }
        }

        $children = [
            ['local_tesisai_lesson_blocks', 'block_course_lesson_ix', 'block_id'],
            ['local_tesisai_lesson_prompts', 'prompt_course_lesson_ix', 'id'],
            ['local_tesisai_transcript_segments', 'transcript_course_lesson_ix', 'id'],
        ];
        foreach ($children as [$tablename, $indexname, $after]) {
            $table = new xmldb_table($tablename);
            if (!$dbman->table_exists($table)) {
                continue;
            }
            $courseid = new xmldb_field('course_id', XMLDB_TYPE_CHAR, '64', null, XMLDB_NOTNULL, null, '', $after);
            if (!$dbman->field_exists($table, $courseid)) {
                $dbman->add_field($table, $courseid);
            }
            $index = new xmldb_index($indexname, XMLDB_INDEX_NOTUNIQUE, ['course_id', 'lesson_id']);
            if (!$dbman->index_exists($table, $index)) {
                $dbman->add_index($table, $index);
            }
        }

        // Backfill del course_id en tablas hijas desde la leccion padre.
        $lessonstable = '{local_tesisai_lessons}';
        foreach (['local_tesisai_lesson_blocks', 'local_tesisai_lesson_prompts', 'local_tesisai_transcript_segments'] as $tablename) {
            $DB->execute("
                UPDATE {{$tablename}} child
                JOIN {$lessonstable} l ON l.lesson_id = child.lesson_id
                SET child.course_id = l.course_id
                WHERE child.course_id = ''
            ");
        }

        upgrade_plugin_savepoint(true, 2026061100, 'local', 'tesisai');
    }

    return true;
}
