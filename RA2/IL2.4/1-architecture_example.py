"""
IL2.4: Ejemplo de Documentación de Arquitectura
===============================================
Describe brevemente la arquitectura de tu agente o sistema.
"""

# Ejemplo de arquitectura simple:
# - Un agente principal que recibe preguntas y usa una herramienta de cálculo.

class MainAgent:
    def __init__(self, tool):
        self.tool = tool

    def answer(self, question):
        if "suma" in question:
            return self.tool("2+2")
        return "No sé la respuesta."

def calculator(expression):
    return str(eval(expression))

if __name__ == "__main__":
    agent = MainAgent(calculator)
    print(agent.answer("¿Cuánto es la suma de 2+2?"))

# Documentación:
# Componentes:
# - MainAgent: gestiona la interacción.
# - calculator: herramienta de cálculo.
# Flujo: Usuario -> MainAgent -> calculator -> respuesta. 