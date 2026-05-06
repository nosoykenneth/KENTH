"""Fachada temporal para mantener imports historicos del agente.

La implementacion principal vive en services.agent.graph durante la Fase 1A.
"""

from services.agent.graph import _verificar_respuesta, super_agente

__all__ = ["super_agente", "_verificar_respuesta"]
