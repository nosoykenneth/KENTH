"""Capa de dominio: carga el conocimiento de curso (Domain Pack) desde datos,
para que el agente sea agnostico al dominio. Ver domain_pack.py."""

from services.domain.domain_pack import DomainPack, get_domain_pack

__all__ = ["DomainPack", "get_domain_pack"]
