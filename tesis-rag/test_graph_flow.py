import sys
sys.path.append(r"d:\ESPE\MIC\ACTIVITIES\PROYECTO\tesis-rag")
from services.agent.retrieval import _buscar_evidencia, _ordenar_para_respuesta_directa, _construir_contexto_evidencia
from services.agent.verification import _verificar_respuesta
from services.agent.graph import llm_logico
from models.schemas import EstadoAgente

preguntas = [
    "¿Qué es EQ correctivo y EQ estético?",
    "¿Qué es EQ dinámico?",
    "¿Qué es el mastering?",
    "¿Qué es la ley de panorama?"
]

for p in preguntas:
    print(f"\n{'='*40}\nPREGUNTA: {p}\n{'='*40}")
    
    # 1. Evidencias de buscar (ya probadas que funcionan bien)
    evidencias_crudas = _buscar_evidencia(p)
    print("--- 1. Top 3 crudo (despues de _buscar_evidencia) ---")
    for i, item in enumerate(evidencias_crudas[:3]):
        print(f"  [Top {i+1}] {item['document'].metadata.get('filename')}")
        
    # 2. Re-orden
    evidencias_ordenadas = _ordenar_para_respuesta_directa(evidencias_crudas, p)
    print("--- 2. Top 3 ordenado (despues de _ordenar_para_respuesta_directa) ---")
    for i, item in enumerate(evidencias_ordenadas[:3]):
        print(f"  [Top {i+1}] {item['document'].metadata.get('filename')}")

    # 3. Contexto al LLM
    teoria, fuentes = _construir_contexto_evidencia(evidencias_ordenadas)
    print("--- 3. Contexto construido ---")
    print(teoria[:500] + "...\n(truncado)")

    # Nos saltamos llamar al LLM por ahora para ser rápidos, o podríamos hacer un mock
