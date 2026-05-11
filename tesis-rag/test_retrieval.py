import sys
sys.path.append(r"d:\ESPE\MIC\ACTIVITIES\PROYECTO\tesis-rag")
from services.agent.retrieval import _buscar_evidencia, _prioridad_evidencia
preguntas = [
    "¿Qué diferencia hay entre Peak, VU y RMS?",
    "¿Qué es EQ correctivo y EQ estético?",
    "¿Qué es EQ dinámico?",
    "¿Qué es la ley de panorama?",
    "¿Qué es el mastering?",
    "¿Qué es True Peak?",
    "¿Qué error frecuente hay al filtrar en solo?",
    "¿Qué hago si mi sala me infla los graves?",
    "¿Qué función tiene el mix bus?",
    "¿Qué error frecuente hay con el dither?"
]
for p in preguntas:
    print(f"\n--- PREGUNTA: {p} ---")
    evidencias = _buscar_evidencia(p)
    if evidencias:
        layer_counts = {"canonico": 0, "limpio": 0, "general": 0}
        for i, item in enumerate(evidencias[:3]):
            doc = item["document"]
            meta = doc.metadata or {}
            layer = (meta.get("layer") or meta.get("capa") or "general").lower()
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
            final_prio = _prioridad_evidencia(item, p)
            print(f"  [Top {i+1}] Layer: {layer} | File: {meta.get('filename')} | Prio: {final_prio:.4f} | OrigScore: {item.get('score', 0):.4f}")
            snippet = doc.page_content.replace('\n', ' ')[:100]
            print(f"    Snippet: {snippet}...")
        print(f"  Resumen de capas en Top 3: {layer_counts}")
    else:
        print("  Sin evidencia encontrada.")
