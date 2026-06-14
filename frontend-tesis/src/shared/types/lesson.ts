/**
 * Schema canónico del Editor de Lección (Fase A, aprobado jun 2026).
 *
 * Es el contrato de wire con el backend de autoría (/authoring/lessons*):
 * los nombres coinciden 1:1 con los payloads Pydantic (authoring.py) y con
 * el shape de lesson_service.load_lesson. Las etiquetas visibles en la UI
 * pueden diferir (p.ej. learning_goals se muestra como "Criterios de logro").
 */

/**
 * Modo pedagógico del bloque. Vocabulario único compartido con
 * InteractionMode (tesis-rag/models/context.py): ambos listados deben
 * ser idénticos.
 */
export type ModoPedagogico =
  | 'teoria'
  | 'practica'
  | 'troubleshooting'
  | 'revision'
  | 'navegacion_de_recurso'
  | 'criterio_operativo';

export const MODOS_PEDAGOGICOS: ModoPedagogico[] = [
  'navegacion_de_recurso',
  'criterio_operativo',
  'practica',
  'teoria',
  'troubleshooting',
  'revision',
];

/** Bloque temporal del video. Los conceptos son POR BLOQUE (lista). */
export interface Bloque {
  block_id: string;
  block_order: number;
  start_time: number; // t_inicio (segundos)
  end_time: number;   // t_fin (segundos)
  block_title: string;
  summary: string;                  // resumen: qué pasa en pantalla
  interaction_mode: ModoPedagogico; // modo pedagógico
  tutor_focus: string;              // foco del tutor en este bloque
  concepts: string[];               // conceptos del bloque
  preguntas_probables: string[];
}

/** Prompts del tutor por lección (tabla lesson_prompts). */
export interface PromptsTutor {
  proactive_message: string;   // mensaje proactivo
  suggested_prompts: string[]; // preguntas sugeridas
}

export interface Leccion extends PromptsTutor {
  lesson_id: string; // anclado al cmid del recurso (decisión jun 2026)
  course_id: string;
  moodle_section_id: string;
  lesson_title: string; // wire: "title" en BD
  order: number;
  prerequisites: string[];
  learning_goal: string;    // objetivo de aprendizaje
  learning_goals: string[]; // criterios de logro (UI: "Criterios de logro")
  expected_action: string;  // acción esperada

  /** Qué le delega el profesor al tutor en esta lección. Se inyecta al prompt. */
  delegated_to_tutor: string[];
  /**
   * Reglas de comportamiento obligatorias (citas, atribuciones, límites).
   * Se inyectan SIEMPRE con framing imperativo en el prompt del tutor.
   */
  attribution_constraints: string[];

  blocks: Bloque[];
  /** Notas internas del profesor: NUNCA se inyectan al tutor. */
  notes: string;
}

/** Segmento de transcripción (una línea de subtítulo). */
export interface SegmentoTranscripcion {
  seq: number;
  start_time: number;
  end_time: number;
  text: string;
  speaker: string;
}
