"""
IL2.3: Orquestación Multi-Agente Básica
======================================
Ejemplo de cómo dos agentes pueden coordinarse para resolver una tarea.
"""

class AgentA:
    def act(self, info):
        return f"Agente A busca información sobre '{info}'"

class AgentB:
    def act(self, data):
        return f"Agente B analiza los datos: '{data}'"

if __name__ == "__main__":
    a = AgentA()
    b = AgentB()
    info = "recetas de café"
    datos = a.act(info)
    print(datos)
    resultado = b.act(datos)
    print(resultado) 