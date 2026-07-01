"""Asistente "Preparar tutor con IA" (autoría asistida del profesor).

Genera un BORRADOR pedagógico a partir de la transcripción de una lección usando
modelos locales de Ollama, de forma estratégica y configurable por tarea. El
borrador vive AISLADO en `metadata.ai_prepare` y NO alimenta al tutor hasta que el
profesor lo revisa y lo ACEPTA (promoción a los campos vivos). Nada se indexa ni
se publica automáticamente desde aquí.

Submódulos:
- models.py   selección de modelo por tarea + cliente Ollama robusto (timeout/retry/num_ctx).
- schema.py   contrato JSON estricto + sanitización + límites.
- prompts.py  prompts pedagógicos específicos (ES), anti-recetas y anti-inyección.
- service.py  orquestación: transcripción -> análisis -> JSON -> validación -> draft.
"""
