-- Fase 2: Moodle Sections como fuente de verdad.
-- Migracion segura: NO borra datos legacy a ciegas.
-- Primero deja reporte auditable de filas que aun dependen de axis_id sin
-- moodle_section_id. Cuando este reporte quede vacio, se puede ejecutar una
-- migracion destructiva posterior para eliminar columnas axis_id y la tabla axes.

SET @prefix := 'mdl_';
SET @db := DATABASE();

SET @lessons := CONCAT(@prefix, 'local_tesisai_lessons');
SET @links := CONCAT(@prefix, 'local_tesisai_resource_lesson_links');
SET @resources := CONCAT(@prefix, 'local_tesisai_course_resources');
SET @documents := CONCAT(@prefix, 'local_tesisai_documents');
SET @axes := CONCAT(@prefix, 'local_tesisai_axes');
SET @report := CONCAT(@prefix, 'local_tesisai_axes_legacy_report');

CREATE TABLE IF NOT EXISTS mdl_local_tesisai_axes_legacy_report (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  table_name VARCHAR(128) NOT NULL,
  entity_id VARCHAR(255) NOT NULL DEFAULT '',
  course_id VARCHAR(64) NOT NULL DEFAULT '',
  axis_id VARCHAR(64) NOT NULL DEFAULT '',
  reason VARCHAR(255) NOT NULL DEFAULT '',
  detected_at BIGINT NOT NULL DEFAULT 0,
  KEY idx_table_course (table_name, course_id),
  KEY idx_axis (axis_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

TRUNCATE TABLE mdl_local_tesisai_axes_legacy_report;

SET @now := UNIX_TIMESTAMP();

SET @sql := IF(
  EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema=@db AND table_name=@lessons),
  CONCAT('INSERT INTO ', @report, ' (table_name, entity_id, course_id, axis_id, reason, detected_at) ',
         'SELECT ''lessons'', lesson_id, course_id, axis_id, ''lesson_has_axis_without_moodle_section_id'', ', @now, ' FROM ', @lessons,
         ' WHERE COALESCE(axis_id, '''') <> '''' AND COALESCE(moodle_section_id, '''') = '''''),
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := IF(
  EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema=@db AND table_name=@links),
  CONCAT('INSERT INTO ', @report, ' (table_name, entity_id, course_id, axis_id, reason, detected_at) ',
         'SELECT ''resource_lesson_links'', resource_id, course_id, axis_id, ''link_has_axis_without_moodle_section_id'', ', @now, ' FROM ', @links,
         ' WHERE COALESCE(axis_id, '''') <> '''' AND COALESCE(moodle_section_id, '''') = '''''),
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := IF(
  EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema=@db AND table_name=@resources),
  CONCAT('INSERT INTO ', @report, ' (table_name, entity_id, course_id, axis_id, reason, detected_at) ',
         'SELECT ''course_resources'', resource_id, course_id, axis_id, ''resource_has_axis_without_moodle_section_id'', ', @now, ' FROM ', @resources,
         ' WHERE COALESCE(axis_id, '''') <> '''' AND COALESCE(moodle_section_id, '''') = '''''),
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := IF(
  EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema=@db AND table_name=@documents),
  CONCAT('INSERT INTO ', @report, ' (table_name, entity_id, course_id, axis_id, reason, detected_at) ',
         'SELECT ''documents'', doc_id, course_id, axis_id, ''document_has_axis_without_moodle_section_id'', ', @now, ' FROM ', @documents,
         ' WHERE COALESCE(axis_id, '''') <> '''' AND COALESCE(moodle_section_id, '''') = '''''),
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Indices legacy de axis: se eliminan solo si no hay reporte pendiente.
SET @pending := (SELECT COUNT(*) FROM mdl_local_tesisai_axes_legacy_report);

SET @sql := IF(
  @pending = 0 AND EXISTS (
    SELECT 1 FROM information_schema.statistics
    WHERE table_schema=@db AND table_name=@lessons AND index_name='idx_axis'
  ),
  CONCAT('ALTER TABLE ', @lessons, ' DROP INDEX idx_axis'),
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Tabla legacy axes: se conserva si existe cualquier fila o reporte pendiente.
-- Borrarla sin migracion semantica destruiria titulos antiguos no mapeados a Moodle.
-- La aplicacion Fase 2 ya no la consulta como fuente de verdad.
