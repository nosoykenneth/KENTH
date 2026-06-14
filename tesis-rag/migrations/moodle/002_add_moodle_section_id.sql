-- Fase 1: Moodle Sections como fuente de verdad en paralelo con axis_id.
-- No elimina columnas ni tablas legacy; solo agrega moodle_section_id.

SET @db := DATABASE();
SET @prefix := 'mdl_';

SET @lessons := CONCAT(@prefix, 'local_tesisai_lessons');
SET @links := CONCAT(@prefix, 'local_tesisai_resource_lesson_links');
SET @resources := CONCAT(@prefix, 'local_tesisai_course_resources');
SET @documents := CONCAT(@prefix, 'local_tesisai_documents');

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('ALTER TABLE ', @lessons, ' ADD COLUMN moodle_section_id VARCHAR(64) NOT NULL DEFAULT '''' AFTER axis_id'),
    'SELECT 1'
  )
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @lessons AND COLUMN_NAME = 'moodle_section_id'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('ALTER TABLE ', @links, ' ADD COLUMN moodle_section_id VARCHAR(64) NOT NULL DEFAULT '''' AFTER axis_id'),
    'SELECT 1'
  )
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @links AND COLUMN_NAME = 'moodle_section_id'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('ALTER TABLE ', @resources, ' ADD COLUMN moodle_section_id VARCHAR(64) NOT NULL DEFAULT '''' AFTER axis_id'),
    'SELECT 1'
  )
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @resources AND COLUMN_NAME = 'moodle_section_id'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('ALTER TABLE ', @documents, ' ADD COLUMN moodle_section_id VARCHAR(64) NOT NULL DEFAULT '''' AFTER axis_id'),
    'SELECT 1'
  )
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @documents AND COLUMN_NAME = 'moodle_section_id'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('CREATE INDEX idx_lesson_course_section ON ', @lessons, ' (course_id, moodle_section_id)'),
    'SELECT 1'
  )
  FROM information_schema.STATISTICS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @lessons AND INDEX_NAME = 'idx_lesson_course_section'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('CREATE INDEX idx_link_course_section ON ', @links, ' (course_id, moodle_section_id)'),
    'SELECT 1'
  )
  FROM information_schema.STATISTICS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @links AND INDEX_NAME = 'idx_link_course_section'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('CREATE INDEX idx_link_resource_course ON ', @links, ' (resource_id, course_id)'),
    'SELECT 1'
  )
  FROM information_schema.STATISTICS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @links AND INDEX_NAME = 'idx_link_resource_course'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('CREATE INDEX idx_resource_course_section ON ', @resources, ' (course_id, moodle_section_id)'),
    'SELECT 1'
  )
  FROM information_schema.STATISTICS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @resources AND INDEX_NAME = 'idx_resource_course_section'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    COUNT(*) = 0,
    CONCAT('CREATE INDEX idx_doc_course_section ON ', @documents, ' (course_id, moodle_section_id)'),
    'SELECT 1'
  )
  FROM information_schema.STATISTICS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @documents AND INDEX_NAME = 'idx_doc_course_section'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
