"""
IL2.3: Orquestación Multi-Agente con CrewAI
==========================================
Ejemplo de cómo dos agentes CrewAI colaboran para resolver una tarea.
"""

# Requiere: pip install crewai
from crewai import Agent, Task, Crew

# Agente 1: Investigador
investigador = Agent(
    role="Investigador",
    goal="Buscar información sobre la capital de Francia",
    backstory="Eres experto en encontrar datos rápidos."
)

# Agente 2: Redactor
redactor = Agent(
    role="Redactor",
    goal="Redactar una respuesta clara y breve",
    backstory="Eres especialista en explicar conceptos de forma sencilla."
)

# Tareas
tarea_investigar = Task(
    description="Busca cuál es la capital de Francia",
    agent=investigador
)
tarea_redactar = Task(
    description="Redacta una respuesta usando la información encontrada",
    agent=redactor,
    context=[tarea_investigar]
)

# Crew (equipo)
crew = Crew(
    agents=[investigador, redactor],
    tasks=[tarea_investigar, tarea_redactar],
    verbose=True
)

if __name__ == "__main__":
    print("Orquestación multi-agente con CrewAI:")
    print(crew.kickoff()) 