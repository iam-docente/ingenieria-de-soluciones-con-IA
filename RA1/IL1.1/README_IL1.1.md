# IL1.1 - Introducción a LLMs y Conexiones API

## Introducción

Esta unidad introduce los conceptos fundamentales de los Modelos de Lenguaje Grandes (LLMs) y las técnicas para establecer conexiones API efectivas. Aprenderás a interactuar con diferentes proveedores de LLMs y comprender las bases técnicas para el desarrollo de aplicaciones con IA generativa.

## Videos de cada archivo del curso:

- **1-github_model_api.ipynb**: Conexión directa a la API de GitHub Models.
  [![Ver Video](https://img.youtube.com/vi/oYvwSROBTl0/hqdefault.jpg)](https://www.youtube.com/watch?v=oYvwSROBTl0)
- **2-langchain_model_api.ipynb**: Abstracción de la API con LangChain.
  [![Ver Video](https://img.youtube.com/vi/v6Dgw0CMAfs/hqdefault.jpg)](https://www.youtube.com/watch?v=v6Dgw0CMAfs)
- **3-langchain_streaming.ipynb**: Implementación de respuestas en tiempo real (Streaming).
  [![Ver Video](https://img.youtube.com/vi/xENs45V5C3k/hqdefault.jpg)](https://www.youtube.com/watch?v=xENs45V5C3k)
- **4-langchain_memory.ipynb**: Gestión de memoria en conversaciones.
  [![Ver Video](https://img.youtube.com/vi/cM_CJPaD0kQ/hqdefault.jpg)](https://www.youtube.com/watch?v=cM_CJPaD0kQ)


## Objetivos de Aprendizaje

Al completar esta unidad, serás capaz de:

1.  **Comprender los fundamentos de los LLMs**: Arquitectura, funcionamiento y capacidades.
2.  **Establecer conexiones API**: Configurar y usar APIs de diferentes proveedores.
3.  **Implementar patrones básicos**: Llamadas síncronas, streaming y gestión de memoria.
4.  **Aplicar mejores prácticas**: Configuración segura, manejo de errores y optimización.

## Contenido del Módulo

Este módulo está compuesto por cuatro cuadernos de Jupyter que te guiarán progresivamente desde una conexión básica hasta la creación de un chatbot con memoria.

### Notebook 1: Conexión Directa con GitHub Models API (`1-apirouter_model_api.ipynb`)
Este cuaderno es el punto de partida. Aprenderás a realizar llamadas directas a un modelo de lenguaje utilizando la API de GitHub Models y el cliente de OpenAI.
- **Qué aprenderás**:
    - Configurar las variables de entorno y el cliente de `openai`.
    - Realizar una llamada básica `chat.completions.create`.
    - Usar parámetros clave como `model`, `messages`, `temperature` y `max_tokens`.
    - Aplicar el rol `system` para guiar el comportamiento del modelo.
- **Cómo usarlo**:
    1. Asegúrate de tener las variables de entorno `GITHUB_BASE_URL` y `GITHUB_TOKEN` configuradas.
    2. Instala la dependencia `openai`.
    3. Ejecuta las celdas secuencialmente para ver cómo se establece la conexión y se interactúa con el modelo.

### Notebook 2: Abstracción con LangChain (`2-langchain_model_api.ipynb`)
Una vez que entiendes la conexión directa, introducimos LangChain, un framework que simplifica la interacción con LLMs.
- **Qué aprenderás**:
    - Las ventajas de usar un framework como LangChain.
    - Configurar el objeto `ChatOpenAI` para conectarse a diferentes proveedores de modelos.
    - Utilizar el método `invoke` para interactuar con el modelo.
    - Entender la estructura de mensajes de LangChain (`HumanMessage`, `AIMessage`, `SystemMessage`).
- **Cómo usarlo**:
    1. Instala las dependencias `langchain` y `langchain-openai`.
    2. Las mismas variables de entorno son utilizadas por `ChatOpenAI`.
    3. Ejecuta las celdas para comparar la simplicidad del código de LangChain frente a la llamada directa.

### Notebook 3: Streaming en Tiempo Real con LangChain (`3-langchain_streaming.ipynb`)
Este cuaderno se enfoca en mejorar la experiencia de usuario mostrando las respuestas del modelo en tiempo real.
- **Qué aprenderás**:
    - Qué es el streaming y por qué es crucial para aplicaciones interactivas.
    - Implementar streaming usando el método `.stream()` de LangChain.
    - Procesar los "chunks" de datos que llegan en tiempo real.
    - Construir un chatbot simple que responde de forma fluida.
- **Cómo usarlo**:
    1. Ejecuta las celdas para ver la diferencia visual y de percepción entre una respuesta normal (`invoke`) y una con streaming.
    2. Prueba el chatbot interactivo al final del cuaderno para experimentar el streaming en acción.

### Notebook 4: Gestión de Memoria con LangChain (`4-langchain_memory.ipynb`)
Un LLM no tiene estado. Este cuaderno enseña cómo darle "memoria" para que pueda recordar interacciones pasadas.
- **Qué aprenderás**:
    - La importancia de la memoria para conversaciones coherentes.
    - Implementar diferentes estrategias de memoria:
        - `ConversationBufferMemory`: Guarda todo el historial.
        - `ConversationBufferWindowMemory`: Guarda las últimas `k` interacciones.
        - `ConversationSummaryMemory`: Usa un LLM para resumir la conversación y ahorrar tokens.
    - Integrar la memoria en cadenas de conversación (`ConversationChain`).
- **Cómo usarlo**:
    1. Ejecuta los ejemplos de cada tipo de memoria para entender sus ventajas y desventajas.
    2. Analiza la comparación final para ver cómo cada tipo de memoria responde a la misma secuencia de preguntas.
    3. Experimenta con el chatbot de memoria configurable para cambiar de estrategia en tiempo real.

## Configuración del Entorno

### Variables de Entorno Requeridas

```bash
export GITHUB_BASE_URL="https://models.github.ai/inference"
export GITHUB_TOKEN="tu_token_de_github"
export OPENAI_BASE_URL="https://models.github.ai/inference"
```

> **Nota:** el endpoint anterior (`https://models.inference.ai.azure.com`) fue deprecado el 17 de julio de 2025. Usa siempre `https://models.github.ai/inference`.

### Dependencias

```bash
pip install "openai>=1.50" "langchain>=0.3,<0.4" "langchain-openai>=0.2"
```

> Se fijan rangos de versión para evitar romper el código con cambios futuros de LangChain (por ejemplo, `langchain.memory` y `langchain.schema` fueron removidos/movidos en versiones posteriores).

## Arquitectura Técnica

### Patrón de Conexión API

```python
# Configuración estándar
from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("GITHUB_BASE_URL"),
    api_key=os.environ.get("GITHUB_TOKEN")
)
```

### Abstracción con LangChain

```python
# Framework approach
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("GITHUB_TOKEN"),
    model="openai/gpt-4o"
)
```

## Consideraciones Técnicas

### Seguridad
- Nunca hardcodear API keys en el código
- Usar variables de entorno para credenciales
- Implementar rate limiting y error handling

### Performance
- Configurar timeouts apropiados
- Usar streaming para respuestas largas
- Optimizar el uso de tokens

### Escalabilidad
- Considerar patrones de retry y circuit breaker
- Implementar logging para debugging
- Planificar para múltiples proveedores

## Evaluación

Esta unidad incluye:
- **Quiz teórico** (8 preguntas) sobre fundamentos de LLMs
- **Práctica dirigida** con los notebooks proporcionados
- **Ejercicios de implementación** para reforzar conceptos

## Recursos Adicionales

- [Documentación OpenAI API](https://platform.openai.com/docs)
- [GitHub Models Documentation](https://docs.github.com/en/github-models)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Transformer Architecture Paper](https://arxiv.org/abs/1706.03762)

## Próximos Pasos

Al completar IL1.1, estarás preparado para:
- **IL1.2**: Técnicas avanzadas de prompt engineering
- **IL1.3**: Implementación de sistemas RAG
- **IL1.4**: Evaluación y optimización de LLMs
