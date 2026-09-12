# Módulo 4: Evaluación y Optimización de LLMs y RAG

## Objetivos de la Sesión
- Comprender la importancia de evaluar sistemáticamente los sistemas RAG.
- Identificar las métricas clave para medir la calidad de la recuperación y la generación.
- Aprender a utilizar LangSmith como herramienta para la evaluación y trazabilidad de pipelines RAG.
- Aplicar los conceptos para crear un ciclo de evaluación y mejora continua.

## 1. ¿Por qué es Crucial Evaluar los Sistemas RAG?

Un sistema RAG tiene dos componentes principales que pueden fallar: el **recuperador (Retriever)** y el **generador (Generator)**. Sin una evaluación rigurosa, es imposible saber qué componente está fallando o cómo mejorar el rendimiento general.

- **Fallas de Recuperación**: El sistema puede traer documentos irrelevantes (baja precisión) u omitir documentos importantes (bajo recall).
- **Fallas de Generación**: La respuesta puede no ser fiel al contexto recuperado (alucinaciones) o no responder adecuadamente a la pregunta del usuario.

La evaluación nos permite pasar de un desarrollo basado en la intuición a uno **guiado por datos**, identificando cuellos de botella y optimizando el sistema de forma iterativa.

## 2. Métricas Fundamentales para la Evaluación RAG

Evaluamos los dos componentes del RAG de forma separada.

### Métricas de Recuperación (Retrieval)

Miden la calidad de los documentos que el sistema recupera.

- **Context Precision (Precisión del Contexto)**:
  - **Pregunta**: De los documentos recuperados, ¿cuántos son realmente relevantes para la pregunta?
  - **Fórmula**: `(Número de documentos relevantes recuperados) / (Total de documentos recuperados)`
  - **Objetivo**: Maximizar. Una baja precisión significa que el generador recibe "ruido".

- **Context Recall (Exhaustividad del Contexto)**:
  - **Pregunta**: De todos los documentos relevantes que existen en la base de conocimiento, ¿cuántos logramos recuperar?
  - **Fórmula**: `(Número de documentos relevantes recuperados) / (Total de documentos relevantes existentes)`
  - **Objetivo**: Maximizar. Un bajo recall significa que el generador no tiene toda la información que necesita.

### Métricas de Generación (Generation)

Miden la calidad de la respuesta final generada por el LLM.

- **Faithfulness (Fidelidad)**:
  - **Pregunta**: ¿La respuesta generada se basa estrictamente en el contexto proporcionado?
  - **Medición**: Se evalúa si la respuesta contiene información que no se puede verificar en los documentos recuperados.
  - **Objetivo**: Maximizar. Una baja fidelidad indica que el modelo está "alucinando" o inventando información.

- **Answer Relevancy (Relevancia de la Respuesta)**:
  - **Pregunta**: ¿La respuesta aborda de forma directa y útil la pregunta original del usuario?
  - **Medición**: Se evalúa la utilidad y pertinencia de la respuesta en relación con la consulta inicial.
  - **Objetivo**: Maximizar. Una respuesta puede ser fiel al contexto pero no ser útil para el usuario.

## 3. LangSmith: Una Plataforma para la Evaluación

**LangSmith** es una herramienta de LangChain diseñada para la **observabilidad, monitoreo y evaluación** de aplicaciones LLM.

Para los sistemas RAG, nos ofrece:
- **Trazabilidad Completa**: Permite ver cada paso del pipeline (recuperación, construcción del prompt, llamada al LLM) para un debugging sencillo.
- **Gestión de Datasets**: Facilita la creación de conjuntos de datos con preguntas y respuestas de referencia (ground truth).
- **Evaluadores Automáticos**: Proporciona métricas predefinidas (como `cot_qa` para corrección) y la capacidad de crear evaluadores personalizados.
- **Análisis Visual**: Ofrece dashboards para comparar experimentos, analizar resultados y encontrar áreas de mejora.

## 4. Pasos para Evaluar un RAG con LangSmith

El notebook `2-langsmith-evaluation.ipynb` nos guía a través de un proceso práctico:

### Paso 1: Configuración e Instrumentación
- Se instalan las librerías necesarias (`langsmith`, `langchain`, `openai`).
- Se configuran las variables de entorno para conectar con la API de LangSmith.
- Se "instrumenta" el código del RAG usando el decorador `@traceable` para que LangSmith pueda capturar cada paso.

### Paso 2: Creación de un Dataset de Evaluación
- Se define un `dataset` en LangSmith, que actúa como nuestro "ground truth".
- Se añaden ejemplos al dataset, cada uno con:
  - `inputs`: La pregunta del usuario (e.g., `{"query": "¿Qué es RAG?"}`).
  - `outputs`: La respuesta correcta de referencia (e.g., `{"answer": "RAG combina búsqueda y generación..."}`).

### Paso 3: Ejecución de la Evaluación
- Se utiliza la función `evaluate()` de LangSmith.
- Se le indica qué función debe ejecutar (`target_function`), qué dataset usar y qué evaluadores aplicar.
- LangSmith ejecuta el pipeline RAG para cada pregunta del dataset y compara la respuesta generada con la respuesta de referencia usando un LLM como juez.

### Paso 4: Análisis de Resultados
- LangSmith genera un informe detallado del experimento.
- Se puede analizar una tabla con las puntuaciones de cada métrica para cada pregunta.
- Es posible "profundizar" en cada ejecución para ver la traza completa y entender por qué el sistema falló o tuvo éxito.

## Actividad Práctica

El entregable de este módulo consiste en:
1.  **Ejecutar el notebook `1-evaluation-rag.py`** para comprender conceptualmente las métricas.
2.  **Configurar y ejecutar el notebook `2-langsmith-evaluation.ipynb`**, conectándolo con tu propia cuenta de LangSmith.
3.  **Crear tu propio dataset de evaluación** con al menos 5 ejemplos relevantes para los documentos proporcionados.
4.  **Ejecutar la evaluación** y analizar los resultados en el dashboard de LangSmith.
5.  **Proponer una mejora** al sistema RAG (ej. modificar el prompt, cambiar el método de retrieval) y **ejecutar una nueva evaluación** para comparar los resultados.

## Conclusiones y Próximos Pasos

- La evaluación no es un paso final, sino un **ciclo continuo** de medición, análisis y optimización.
- Herramientas como LangSmith son fundamentales para escalar el desarrollo de aplicaciones de IA robustas y confiables.
- En el siguiente módulo, exploraremos arquitecturas de agentes más complejas y cómo aplicar estos mismos principios de evaluación.
