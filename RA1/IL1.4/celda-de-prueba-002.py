import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODELO = "minimax/minimax-m3:free"

# Reproducir la llamada exacta de context_precision
eval_prompt = """Evalúa la relevancia de CADA documento para responder la consulta.

Consulta: ¿Qué es la IA?

Documento 1: La inteligencia artificial es una rama de la informática.

Responde SOLO con las etiquetas separadas por comas. Ejemplo: "SI,NO,SI"

Respuesta:"""

print("Haciendo 3 llamadas al modelo para ver su comportamiento...\n")

for i in range(3):
    try:
        response = client.chat.completions.create(
            model=MODELO,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.1,
            max_tokens=100,
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Diagnóstico"
            }
        )
        
        msg = response.choices[0].message
        print(f"Llamada {i+1}:")
        print(f"  finish_reason: {response.choices[0].finish_reason}")
        print(f"  content: {repr(msg.content)}")
        print(f"  content es None: {msg.content is None}")
        
        # Verificar si hay reasoning (algunos modelos lo usan)
        if hasattr(msg, 'reasoning_content'):
            print(f"  reasoning_content: {repr(msg.reasoning_content)[:100]}...")
        
        print()
    except Exception as e:
        print(f"Llamada {i+1} falló: {e}\n")