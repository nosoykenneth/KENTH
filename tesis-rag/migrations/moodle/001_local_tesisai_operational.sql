-- Moodle/MariaDB extension tables for local_tesisai.
-- Apply inside Moodle DB (`moodle`), with Moodle prefix `mdl_`.
-- These are operational/relational tables only; editorial corpus stays in files/RAG.
--
-- v2: añade course_id/lesson_id a sessions, user_id a messages,
--     índices compuestos para escalabilidad multiusuario.

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_lessons (
  lesson_id VARCHAR(64) PRIMARY KEY,
  course_id VARCHAR(64) NOT NULL DEFAULT '',
  axis_id VARCHAR(32) NOT NULL DEFAULT '',
  title VARCHAR(255) NOT NULL DEFAULT '',
  lesson_order INT NOT NULL DEFAULT 0,
  learning_goal TEXT NULL,
  expected_action TEXT NULL,
  source_script_file VARCHAR(512) NOT NULL DEFAULT '',
  is_pilot TINYINT(1) NOT NULL DEFAULT 0,
  learning_goals_json LONGTEXT NULL,
  expected_actions_json LONGTEXT NULL,
  resources_json LONGTEXT NULL,
  prerequisites_json LONGTEXT NULL,
  notes LONGTEXT NULL,
  metadata_json LONGTEXT NULL,
  timecreated BIGINT NOT NULL,
  timemodified BIGINT NOT NULL,
  KEY idx_axis (axis_id),
  KEY idx_course (course_id),
  KEY idx_pilot (is_pilot)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_lesson_blocks (
  block_id VARCHAR(96) PRIMARY KEY,
  lesson_id VARCHAR(64) NOT NULL,
  block_order INT NOT NULL DEFAULT 0,
  start_time DOUBLE NULL,
  end_time DOUBLE NULL,
  block_title VARCHAR(255) NOT NULL DEFAULT '',
  summary LONGTEXT NULL,
  interaction_mode VARCHAR(64) NOT NULL DEFAULT '',
  tutor_focus LONGTEXT NULL,
  concepts_json LONGTEXT NULL,
  preguntas_probables_json LONGTEXT NULL,
  metadata_json LONGTEXT NULL,
  timecreated BIGINT NOT NULL,
  timemodified BIGINT NOT NULL,
  UNIQUE KEY uq_lesson_order (lesson_id, block_order),
  KEY idx_lesson_time (lesson_id, start_time, end_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_course_resources (
  resource_id VARCHAR(96) PRIMARY KEY,
  course_id VARCHAR(64) NOT NULL DEFAULT '',
  axis_id VARCHAR(32) NOT NULL DEFAULT '',
  lesson_id VARCHAR(64) NOT NULL DEFAULT '',
  resource_type VARCHAR(64) NOT NULL DEFAULT 'lesson_note',
  resource_subtype VARCHAR(64) NOT NULL DEFAULT '',
  title VARCHAR(255) NOT NULL DEFAULT '',
  source_uri VARCHAR(512) NOT NULL DEFAULT '',
  duration_seconds INT NULL,
  page_count INT NULL,
  language VARCHAR(16) NOT NULL DEFAULT 'es',
  tags_json LONGTEXT NULL,
  metadata_json LONGTEXT NULL,
  timecreated BIGINT NOT NULL,
  timemodified BIGINT NOT NULL,
  KEY idx_resource_lesson (lesson_id),
  KEY idx_resource_course (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_resource_lesson_links (
  resource_id VARCHAR(96) PRIMARY KEY,
  course_id VARCHAR(64) NOT NULL DEFAULT '',
  lesson_id VARCHAR(64) NOT NULL,
  axis_id VARCHAR(32) NOT NULL DEFAULT '',
  resource_type VARCHAR(64) NOT NULL DEFAULT '',
  resource_subtype VARCHAR(64) NOT NULL DEFAULT '',
  timecreated BIGINT NOT NULL,
  timemodified BIGINT NOT NULL,
  KEY idx_link_course (course_id),
  KEY idx_link_lesson (lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_lesson_prompts (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  lesson_id VARCHAR(64) NOT NULL,
  prompt_type VARCHAR(32) NOT NULL,
  prompt_order INT NOT NULL DEFAULT 0,
  prompt_text LONGTEXT NOT NULL,
  timecreated BIGINT NOT NULL,
  timemodified BIGINT NOT NULL,
  UNIQUE KEY uq_prompt (lesson_id, prompt_type, prompt_order),
  KEY idx_prompt_lesson (lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLAS DE CONVERSACIONES DEL TUTOR (PRIVACIDAD)
-- Cada sesión y cada mensaje llevan user_id explícito.
-- Índices compuestos para consultas multiusuario rápidas.
-- =====================================================

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_tutor_sessions (
  session_id VARCHAR(128) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL DEFAULT '',
  course_id VARCHAR(64) NOT NULL DEFAULT '',
  lesson_id VARCHAR(64) NOT NULL DEFAULT '',
  title VARCHAR(255) NOT NULL DEFAULT 'Nuevo chat',
  timecreated BIGINT NOT NULL,
  timemodified BIGINT NOT NULL,
  KEY idx_session_user (user_id),
  KEY idx_session_user_time (user_id, timemodified)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_tutor_messages (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  session_id VARCHAR(128) NOT NULL,
  user_id VARCHAR(64) NOT NULL DEFAULT '',
  role VARCHAR(32) NOT NULL,
  content LONGTEXT NOT NULL,
  timecreated BIGINT NOT NULL,
  KEY idx_msg_session (session_id, id),
  KEY idx_msg_user (user_id, timecreated)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_message_traces (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  session_id VARCHAR(128) NOT NULL,
  message_id BIGINT NULL,
  trace_json LONGTEXT NOT NULL,
  timecreated BIGINT NOT NULL,
  KEY idx_trace_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_interaction_traces (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  session_id VARCHAR(128) NOT NULL,
  question LONGTEXT NOT NULL,
  answer LONGTEXT NOT NULL,
  context_json LONGTEXT NULL,
  sources_json LONGTEXT NULL,
  timecreated BIGINT NOT NULL,
  KEY idx_interaction_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_session_context (
  session_id VARCHAR(128) PRIMARY KEY,
  student_id VARCHAR(64) NOT NULL DEFAULT '',
  active_context_json LONGTEXT NULL,
  state_json LONGTEXT NULL,
  timemodified BIGINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- MIGRACIÓN INCREMENTAL: aplicar si las tablas ya existen
-- =====================================================

-- ALTER TABLE mdl_local_tesisai_tutor_sessions ADD COLUMN course_id VARCHAR(64) NOT NULL DEFAULT '' AFTER user_id;
-- ALTER TABLE mdl_local_tesisai_tutor_sessions ADD COLUMN lesson_id VARCHAR(64) NOT NULL DEFAULT '' AFTER course_id;
-- ALTER TABLE mdl_local_tesisai_tutor_sessions ADD KEY idx_session_user_time (user_id, timemodified);
-- ALTER TABLE mdl_local_tesisai_tutor_messages ADD COLUMN user_id VARCHAR(64) NOT NULL DEFAULT '' AFTER session_id;
-- ALTER TABLE mdl_local_tesisai_tutor_messages ADD KEY idx_msg_user (user_id, timecreated);
-- UPDATE mdl_local_tesisai_tutor_messages m JOIN mdl_local_tesisai_tutor_sessions s ON m.session_id = s.session_id SET m.user_id = s.user_id WHERE m.user_id = '';
