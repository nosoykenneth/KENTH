import sys
sys.path.append(r"d:\ESPE\MIC\ACTIVITIES\PROYECTO\tesis-rag")
from services.agent.graph import nodo_rag
from models.schemas import EstadoAgente

preguntas = [
    "¿Qué es EQ correctivo y EQ estético?",
    "¿Qué es EQ dinámico?",
    "¿Qué es el mastering?",
    "¿Qué es la ley de panorama?"
]

for p in preguntas:
    print(f"\n{'='*60}\nPREGUNTA: {p}\n{'='*60}")
    state = EstadoAgente(pregunta=p, ruta="teoria", intent="aclaracion_concepto", historial=[])
    
    # We will temporarily patch `_verificar_respuesta` inside verification.py to capture the raw response
    # Actually, we can just look at `nodo_rag` return which gives the final response. 
    # But to get raw response, let's just intercept the LLM or we can just print it.
    
    # Alternatively, just running the agent graph will give the final response.
    # To get raw, I'll patch the verifier to just print it.
    
    import services.agent.verification as verif
    original_verificar = verif._verificar_respuesta
    def mock_verificar(respuesta, fuentes, evidencias):
        print(f"\n>>> RESPUESTA CRUDA:\n{respuesta}\n")
        return original_verificar(respuesta, fuentes, evidencias)
    
    verif._verificar_respuesta = mock_verificar
    
    try:
        resultado = nodo_rag(state)
        print(f"\n>>> RESPUESTA FINAL:\n{resultado['respuesta_final']}\n")
        print(f">>> EVIDENCIAS SELECCIONADAS (TOP 3):")
        for i, ev in enumerate(resultado['evidencias'][:3]):
            print(f"  [{i+1}] {ev.get('filename')} (score: {ev.get('score')})")
    finally:
        verif._verificar_respuesta = original_verificar
