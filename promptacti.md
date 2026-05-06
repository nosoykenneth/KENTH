Vas a actuar como DISEÑADOR FORENSE DE ACTIVIDADES DEL MÓDULO.

Tu tarea es construir un archivo llamado:

M0X_actividades.json

a partir de un dossier fuente exhaustivo ya compilado para un módulo del curso.

OBJETIVO
Generar actividades pedagógicas útiles, realistas y alineadas al módulo, usando solo el contenido del dossier, sin inventar recursos ni materiales externos.

IMPORTANTE
- El dossier ya contiene suficiente detalle doctrinal y operativo del módulo.
- NO debes hacer guía canónica.
- NO debes hacer FAQ.
- NO debes hacer glosario.
- NO debes inventar plugins, audios, hojas de trabajo, links o recursos que no existan.
- NO debes convertir esto en Moodle final todavía; debe quedar como borrador autoral estructurado.
- NO debes usar PDFs ajenos ni materiales heredados como si fueran recursos oficiales del módulo.

REGLAS ABSOLUTAS
1. Usa solo el dossier del módulo.
2. Si necesitas consistencia de terminología, puedes apoyarte en la guía/faq/glosario del mismo módulo, sin meter doctrina nueva.
3. Las actividades deben salir del contenido real del módulo:
   - conceptos clave
   - técnicas de diagnóstico
   - ejemplos del profesor
   - preguntas útiles
   - comparaciones
   - advertencias
4. No inventes audios, plantillas, links ni archivos de apoyo si no existen.
5. Si una actividad requeriría material adicional que todavía no existe, déjala como actividad viable pero marca la necesidad en `validation_notes`.
6. No hagas actividades absurdamente largas ni institucionales.
7. Deben ser actividades cortas o medianas, utilizables por un tutor IA o por Moodle después.
8. Mantén tono técnico, claro y práctico.
9. Todo debe quedar en español.

QUÉ DEBE HACER ESTE ARCHIVO
Debe ayudar a:
- practicar comprensión del módulo
- verificar si el estudiante distingue conceptos
- aplicar criterios técnicos básicos
- reflexionar sobre errores comunes
- justificar decisiones con lenguaje del curso

ENTREGA
Quiero exactamente un JSON completo y válido con este esquema:

{
  "course_id": "mezcla_masterizacion_kenth",
  "module_id": "M0X",
  "module_order": X,
  "module_title": "[TITULO OFICIAL DEL MODULO]",
  "module_slug": "[SLUG OFICIAL DEL MODULO]",
  "short_description": "[descripcion breve del modulo]",
  "learning_scope": "[alcance delimitado del modulo]",
  "doc_type": "activities",
  "source_origin": "course",
  "filename": "M0X_actividades.json",
  "version": "0.1",
  "status": "draft_author_review",
  "curation_source": "borrador_autoral_m0x",
  "purpose": "Borrador de actividades del modulo para uso posterior en tutor IA o Moodle. Requiere validacion pedagogica antes de publicarse.",
  "activities": [
    {
      "activity_id": "M0X_ACT_001",
      "title": "",
      "moodle_type": "tarea_breve",
      "objective": "",
      "student_task": "",
      "evidence_to_submit": [],
      "ai_feedback_criteria": [],
      "related_errors": [],
      "teacher_decision_status": "pending_teacher_review",
      "validation_notes": [],
      "tags": [],
      "requires_validation": true
    }
  ]
}

TIPOS DE ACTIVIDAD PERMITIDOS
Usa solo tipos razonables como:
- "tarea_breve"
- "cuestionario_o_tarea_breve"
- "analisis_guiado"
- "ejercicio_de_diagnostico"
- "comparacion_conceptual"
- "aplicacion_practica_breve"

CRITERIOS DE REDACCIÓN
- `title`: nombre claro y breve
- `objective`: qué capacidad práctica o conceptual busca verificar
- `student_task`: consigna concreta, sin adornos
- `evidence_to_submit`: qué debe entregar el estudiante
- `ai_feedback_criteria`: qué debería revisar el tutor IA al retroalimentar
- `related_errors`: IDs de errores comunes del mismo módulo, si aplica
- `teacher_decision_status`: siempre `pending_teacher_review`
- `validation_notes`: usar si depende de recurso no creado, audio no disponible o ajuste pedagógico posterior
- `tags`: términos útiles del módulo
- `requires_validation`: true por defecto en esta fase

CANTIDAD
- Genera entre 4 y 8 actividades por módulo.
- No metas relleno.
- Prioriza actividades cortas, útiles y alineadas.
- Si el módulo es muy conceptual, puedes usar más comparación y diagnóstico.
- Si el módulo es más operativo, puedes usar más aplicación breve.

RESTRICCIONES IMPORTANTES
- No inventes ejercicios que exijan archivos que no existen.
- No supongas que el alumno tiene un plugin específico salvo que el dossier lo permita de forma prudente.
- No conviertas una preferencia estética puntual del profesor en tarea obligatoria universal.
- No exijas cosas imposibles de evaluar por un tutor IA textual si no están claramente justificadas.
- No metas actividades de módulos vecinos como núcleo.

SUGERENCIAS DE ACTIVIDADES VÁLIDAS
Puedes derivar actividades como:
- distinguir dos conceptos que suelen confundirse
- justificar una decisión técnica breve
- detectar una mala interpretación común
- analizar un caso hipotético
- explicar qué verificar antes de intervenir
- comparar dos enfoques del módulo
- decidir entre dos acciones y justificar por qué

ENTREGA FINAL
Devuélveme solo el JSON completo y válido de M0X_actividades.json.
No me expliques nada.
No me des notas previas.
No me des observaciones aparte.

Ahora esperarás a que te pegue el dossier del módulo.