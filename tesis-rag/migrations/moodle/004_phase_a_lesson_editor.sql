-- Fase A del Editor de Lección (jun 2026).
-- Equivalente manual de upgrade.php 2026061100 y de _ensure_phase_a_schema()
-- en services/db_service.py (que aplica esto solo en runtime de forma idempotente).
--
-- 1) Lecciones: campos nuevos del profesor (listas JSON) y drop de deprecados.
ALTER TABLE mdl_local_tesisai_lessons
  ADD COLUMN delegated_to_tutor_json LONGTEXT NULL,
  ADD COLUMN attribution_constraints_json LONGTEXT NULL;

ALTER TABLE mdl_local_tesisai_lessons
  DROP COLUMN source_script_file,
  DROP COLUMN expected_actions_json;

-- 2) course_id denormalizado en tablas hijas (desde la lección padre)
--    + índice compuesto (course_id, lesson_id).
ALTER TABLE mdl_local_tesisai_lesson_blocks ADD COLUMN course_id VARCHAR(64) NOT NULL DEFAULT '';
UPDATE mdl_local_tesisai_lesson_blocks b
  JOIN mdl_local_tesisai_lessons l ON l.lesson_id = b.lesson_id
  SET b.course_id = l.course_id;
CREATE INDEX idx_block_course_lesson ON mdl_local_tesisai_lesson_blocks (course_id, lesson_id);

ALTER TABLE mdl_local_tesisai_lesson_prompts ADD COLUMN course_id VARCHAR(64) NOT NULL DEFAULT '';
UPDATE mdl_local_tesisai_lesson_prompts p
  JOIN mdl_local_tesisai_lessons l ON l.lesson_id = p.lesson_id
  SET p.course_id = l.course_id;
CREATE INDEX idx_prompt_course_lesson ON mdl_local_tesisai_lesson_prompts (course_id, lesson_id);

ALTER TABLE mdl_local_tesisai_transcript_segments ADD COLUMN course_id VARCHAR(64) NOT NULL DEFAULT '';
UPDATE mdl_local_tesisai_transcript_segments t
  JOIN mdl_local_tesisai_lessons l ON l.lesson_id = t.lesson_id
  SET t.course_id = l.course_id;
CREATE INDEX idx_transcript_course_lesson ON mdl_local_tesisai_transcript_segments (course_id, lesson_id);
