# Módulo IL2.2: Sistemas de Memoria e Integración de Herramientas

Este módulo se centra en dotar a los agentes de IA de **memoria**, una capacidad crucial para pasar de interacciones simples a conversaciones coherentes y contextuales. Exploramos cómo los agentes pueden recordar información pasada para responder preguntas de seguimiento y mantener un diálogo fluido.

## Contenidos del Módulo

### 1. Agentes con Memoria Conversacional
- **`1-memory-agent.ipynb`**: Introduce el concepto de memoria en los agentes de LangChain. Se implementa un agente que utiliza un historial de chat gestionado manualmente para responder preguntas de seguimiento, demostrando la importancia del contexto en una conversación.

### 2. Sistemas de Memoria Avanzados
- **`2-memory-agent-advanced.ipynb`**: Profundiza en las soluciones de memoria automatizadas que ofrece LangChain para superar las limitaciones de la gestión manual. Se implementan y comparan tres estrategias clave:
  - **`ConversationBufferMemory`**: Para un historial de conversación completo.
  - **`ConversationBufferWindowMemory`**: Para mantener un historial de tamaño fijo, conservando solo las interacciones más recientes.
  - **`ConversationSummaryMemory`**: Para gestionar conversaciones largas resumiendo el historial y ahorrando tokens.

## Conceptos Clave

- **Memoria Conversacional**: La capacidad de un agente para retener y utilizar información de interacciones pasadas.
- **Gestión de Estado (Stateful vs. Stateless)**: La diferencia entre un agente que recuerda el contexto (stateful) y uno que no lo hace (stateless).
- **Estrategias de Memoria**: Diferentes enfoques para gestionar el historial de una conversación, cada uno con sus propias ventajas y casos de uso (Buffer, Window, Summary).
- **Integración de Herramientas (Tool Integration)**: La capacidad de los agentes para utilizar herramientas externas (APIs, bases de datos, etc.) para realizar acciones y obtener información del mundo real.

## Próximos Pasos

Una vez que un agente puede recordar conversaciones y usar herramientas, el siguiente paso es enseñarle a planificar. El **Módulo IL2.3** se centrará en la **planificación y orquestación**, permitiendo a los agentes descomponer objetivos complejos en una serie de pasos ejecutables.