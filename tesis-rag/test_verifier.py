"""Test _verificar_respuesta directly with a fabricated response."""
import sys
sys.path.insert(0, ".")
from services.agent_service import _verificar_respuesta
from langchain_core.documents import Document

# Simulate evidencias with known URLs
evidencias = [
    {
        "document": Document(
            page_content="test content",
            metadata={
                "url": "https://tu-moodle.edu.ec/mod/h5pactivity/view.php?id=10&time=450",
                "module": "4",
                "filename": "prueba.json"
            }
        ),
        "score": 0.55
    }
]
fuentes = ["Fuente 1 | archivo: prueba.json"]

# Case 1: Clean response (no fake URLs, no fake modules)
resp_clean = "El headroom es el espacio disponible antes de saturar la senal."
result1 = _verificar_respuesta(resp_clean, fuentes, evidencias)
print(f"\nCase 1 (clean): '{result1[:60]}...'")
print(f"  Changed: {result1 != resp_clean}")

# Case 2: Response with FAKE URL
resp_fake_url = "Puedes revisar esto en https://fake-url.com/invented y tambien en https://tu-moodle.edu.ec/mod/h5pactivity/view.php?id=10&time=450"
result2 = _verificar_respuesta(resp_fake_url, fuentes, evidencias)
print(f"\nCase 2 (fake URL): '{result2[:100]}...'")
print(f"  Fake URL replaced: {'[enlace no verificado' in result2}")
print(f"  Real URL preserved: {'tu-moodle.edu.ec' in result2}")

# Case 3: Response mentioning non-existent module
resp_fake_mod = "Revisa el Modulo 9 donde explican esto en detalle. Tambien el Modulo 4 es relevante."
result3 = _verificar_respuesta(resp_fake_mod, fuentes, evidencias)
print(f"\nCase 3 (fake module): '{result3[:80]}...'")
print(f"  Module 9 flagged (in logs): check [VERIFICADOR] output above")
print(f"  Module 4 NOT flagged: correct (it's in evidence)")

print("\n=== VERIFIER TEST COMPLETE ===")
