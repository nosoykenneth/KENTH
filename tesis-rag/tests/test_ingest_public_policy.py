import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingest import es_documento_aprobado_para_indexar


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(*parts):
    return os.path.join(BASE_DIR, *parts)


def test_canonico_operativo_aprobado():
    path = _path(
        "documentos",
        "oficial",
        "ejes",
        "eje_2_integridad_senal",
        "01_contenido_canonico.md",
    )

    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)

    assert aprobado, razones


def test_paquete_limpio_operativo_bloqueado():
    path = _path(
        "documentos",
        "oficial",
        "ejes",
        "eje_2_integridad_senal",
        "02_paquete_limpio.md",
    )

    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)

    assert not aprobado
    assert any("patron prohibido" in razon for razon in razones)


def test_paquete_limpio_legacy_bloqueado():
    path = _path(
        "documentos",
        "oficial",
        "ejes",
        "paquetes_limpios",
        "KENTH_Eje1_Paquete_Limpio.md",
    )

    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)

    assert not aprobado
    assert any("carpetas publicas" in razon or "patron prohibido" in razon for razon in razones)


def test_course_runtime_publico_aprobado_si_no_refiere_paquete_limpio():
    path = _path("course_runtime", "resources", "res_E0_canonico.json")

    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)

    assert aprobado, razones


def test_course_runtime_que_refiere_paquete_limpio_bloqueado():
    path = _path("course_runtime", "resources", "res_E0_paquete_limpio.json")

    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)

    assert not aprobado
    assert any("material interno" in razon or "patron prohibido" in razon for razon in razones)


if __name__ == "__main__":
    test_canonico_operativo_aprobado()
    test_paquete_limpio_operativo_bloqueado()
    test_paquete_limpio_legacy_bloqueado()
    test_course_runtime_publico_aprobado_si_no_refiere_paquete_limpio()
    test_course_runtime_que_refiere_paquete_limpio_bloqueado()
    print("OK - ingest public policy")
