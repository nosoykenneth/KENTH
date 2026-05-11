from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.agent_service import super_agente


QUESTIONS = [
    "quien es napoleon",
    "que relacion tiene la espuma con la interfaz",
    "puedo ecualizar con mis audios ya procesados",
    "como comprimo un ecualizador",
    "que es el headroom",
    "diferencia entre compresion y ecualizacion",
    "en que modulo hablan de frecuencia de corte",
]


def _state(question: str):
    return {
        "pregunta": question,
        "contexto_leccion": "",
        "historial": [],
        "imagen": "",
        "ruta": "",
        "respuesta_final": "",
        "evidencias": [],
        "evidence_level": "",
        "intent": "",
        "answer_type": "",
        "course_module": "",
        "evaluation_category": "",
        "requires_course_evidence": True,
        "warnings": [],
        "retrieved_chunks": [],
        "model_used": "",
        "prompt_id": "",
    }


def _assert_gate(question: str, result: dict):
    answer = result.get("respuesta_final", "")
    answer_type = result.get("answer_type", "")
    intent = result.get("intent", "")
    route = result.get("ruta", "")

    if question == "quien es napoleon":
        assert route == "bloqueo", result
        assert answer_type == "out_of_domain", result
    elif question == "que relacion tiene la espuma con la interfaz":
        assert "espuma" not in answer.lower() or answer_type == "clarification", result
        assert "interfaz" in answer.lower(), result
    elif question == "puedo ecualizar con mis audios ya procesados":
        assert answer_type == "clarification", result
        for term in ["mezcla/master", "stems", "efectos impresos"]:
            assert term in answer.lower(), result
    elif question == "como comprimo un ecualizador":
        assert answer_type == "rag_answer", result
        assert "no se comprime un ecualizador" in answer.lower(), result
        assert "ecualizacion dinamica" in answer.lower() or "compresion multibanda" in answer.lower(), result
    elif question == "que es el headroom":
        assert answer_type == "rag_answer", result
        assert "Fuente " not in answer, result
    elif question == "diferencia entre compresion y ecualizacion":
        assert answer_type == "rag_answer", result
    elif question == "en que modulo hablan de frecuencia de corte":
        assert intent == "busqueda_fuente", result
        assert answer_type == "source_lookup", result


def main():
    for question in QUESTIONS:
        buffer = StringIO()
        with redirect_stdout(buffer):
            result = super_agente.invoke(_state(question))
        _assert_gate(question, result)
        answer = result.get("respuesta_final", "").replace("\n", " ")
        print(
            f"OK | {question} | ruta={result.get('ruta')} "
            f"| intent={result.get('intent')} | answer_type={result.get('answer_type')} "
            f"| fuente_visible={'Fuente ' in answer}"
        )


if __name__ == "__main__":
    main()
