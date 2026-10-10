"""
IL2.3: Planificación con LangChain
=================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos usando herramientas.
"""

# Requiere: pip install langchain openai
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
import os

# Configura tu API key de OpenAI
os.environ["OPENAI_API_KEY"] = "sk-..."

# Herramienta personalizada: suma
def sumar(x):
    try:
        return str(eval(x))
    except Exception:
        return "Error en la operación"

herramienta_suma = Tool(
    name="Calculadora",
    func=sumar,
    description="Realiza sumas y operaciones matemáticas simples."
)

# Inicializa el LLM y el agente
llm = OpenAI(temperature=0)
agente = initialize_agent(
    tools=[herramienta_suma],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    print("Planificación y ejecución con LangChain:")
 