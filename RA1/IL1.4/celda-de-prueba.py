import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODELO = "minimax/minimax-m3:free"
DEFAULT_HEADERS = {
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "Diagnóstico",
}

# Simular la llamada de context_precision
eval_prompt = """Evalúa la relevancia de CADA documento para responder la consulta.

Consulta: ¿Qué es la IA?

Documento 1: La inteligencia artificial es una rama de la informática.

Responde SOLO con las etiquetas separadas por comas. Ejemplo: "SI,NO,SI"

Respuesta:"""

try:
    response = client.chat.completions.create(
        model=MODELO,
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0.1,
        max_tokens=50,
        extra_headers=DEFAULT_HEADERS,
    )
    
    print("=== RESPUESTA COMPLETA ===")
    print(response)
    print("\n=== ANÁLISIS ===")
    print(f"Choices: {len(response.choices)}")
    print(f"Finish reason: {response.choices[0].finish_reason}")
    print(f"Content: {repr(response.choices[0].message.content)}")
    print(f"Content es None: {response.choices[0].message.content is None}")
    
except Exception as e:
    print(f"❌ Error: {e}")