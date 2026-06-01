"""Cliente para Moodle Web Services REST.

Razon arquitectonica:
- El plugin `local_tesisai` y sus tablas `mdl_local_tesisai_*` son contrato del proyecto.
- Cualquier informacion proveniente de Moodle "core" (usuarios, contenidos del curso,
  calificaciones, progresos) debe llegar via Web Services para no acoplar FastAPI al
  esquema interno del LMS.

Funciones cubiertas:
- core_user_get_users_by_field
- core_course_get_contents
- gradereport_user_get_grade_items
- core_completion_get_activities_completion_status
- Cualquier funcion expuesta por `local_tesisai` puede invocarse via `call()`.

El token y la URL base se configuran via variables de entorno (config.py).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import httpx

from config import MOODLE_WS_BASE, MOODLE_WS_TOKEN

logger = logging.getLogger(__name__)


class MoodleWSError(Exception):
    """Error en una llamada al Web Service de Moodle."""


class MoodleWSClient:
    """Wrapper minimo y reusable sobre la REST API de Moodle.

    Uso:
        client = MoodleWSClient()
        user = await client.get_user_by_id(42)
        contents = await client.get_course_contents(2)
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = (base_url or MOODLE_WS_BASE or "").strip()
        self.token = (token or MOODLE_WS_TOKEN or "").strip()
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.token)

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def aclose(self) -> None:
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()

    async def call(self, function: str, **params: Any) -> Any:
        """Invoca cualquier funcion REST de Moodle.

        Args:
            function: nombre de la wsfunction (ej. 'core_user_get_users_by_field').
            **params: parametros del request (Moodle requiere notacion plana,
                      este metodo se encarga de transformar listas/dicts).

        Returns:
            Respuesta deserializada (dict o list).

        Raises:
            MoodleWSError: si el WS responde con `exception` o el cliente no esta configurado.
        """
        if not self.configured:
            raise MoodleWSError(
                "MoodleWSClient no esta configurado: MOODLE_WS_BASE o MOODLE_WS_TOKEN vacios."
            )

        data: Dict[str, Any] = {
            "wstoken": self.token,
            "wsfunction": function,
            "moodlewsrestformat": "json",
        }
        data.update(_flatten_params(params))

        client = await self._get_client()
        response = await client.post(self.base_url, data=data)
        response.raise_for_status()
        payload = response.json()

        if isinstance(payload, dict) and payload.get("exception"):
            logger.error(
                "moodle_ws_error",
                extra={
                    "function": function,
                    "errorcode": payload.get("errorcode"),
                    "message": payload.get("message"),
                },
            )
            raise MoodleWSError(
                f"{function}: {payload.get('errorcode')} - {payload.get('message')}"
            )
        return payload

    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        result = await self.call(
            "core_user_get_users_by_field",
            field="id",
            values=[str(user_id)],
        )
        if isinstance(result, list) and result:
            return result[0]
        return None

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        result = await self.call(
            "core_user_get_users_by_field",
            field="username",
            values=[username],
        )
        if isinstance(result, list) and result:
            return result[0]
        return None

    async def get_course_contents(self, course_id: int) -> List[Dict[str, Any]]:
        result = await self.call("core_course_get_contents", courseid=course_id)
        return result if isinstance(result, list) else []

    async def get_user_grades(self, user_id: int, course_id: int) -> Dict[str, Any]:
        return await self.call(
            "gradereport_user_get_grade_items",
            courseid=course_id,
            userid=user_id,
        )

    async def get_activity_completion(
        self, user_id: int, course_id: int
    ) -> Dict[str, Any]:
        return await self.call(
            "core_completion_get_activities_completion_status",
            courseid=course_id,
            userid=user_id,
        )


_singleton: Optional[MoodleWSClient] = None


def get_moodle_ws_client() -> MoodleWSClient:
    """Devuelve un cliente compartido para inyectar via FastAPI Depends.

    El cliente reusa la misma conexion httpx para todas las requests.
    """
    global _singleton
    if _singleton is None:
        _singleton = MoodleWSClient()
    return _singleton


def _flatten_params(params: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """Aplana listas/dicts al formato que Moodle espera (PHP-style).

    Ejemplo:
        {"values": ["a", "b"]} -> {"values[0]": "a", "values[1]": "b"}
        {"options": {"hidden": 1}} -> {"options[hidden]": 1}
    """
    flat: Dict[str, Any] = {}
    for key, value in params.items():
        full_key = f"{prefix}[{key}]" if prefix else key
        if isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    flat.update(_flatten_params(item, f"{full_key}[{index}]"))
                else:
                    flat[f"{full_key}[{index}]"] = item
        elif isinstance(value, dict):
            flat.update(_flatten_params(value, full_key))
        elif value is not None:
            flat[full_key] = value
    return flat
