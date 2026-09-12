# Módulo 4: Evaluación y Optimización de LLMs y RAG

Este módulo se centra en un aspecto crítico del desarrollo de sistemas de IA: la **evaluación y optimización**. A través de herramientas prácticas y conceptos teóricos, aprenderás a medir y mejorar el rendimiento de los sistemas de Generación Aumentada por Recuperación (RAG).

## Objetivos de Aprendizaje

- **Comprender la importancia de la evaluación sistemática** en los sistemas RAG para identificar fallos en la recuperación y generación.
- **Identificar y aplicar métricas clave** como la Precisión del Contexto, Fidelidad de la Respuesta y Relevancia.
- **Utilizar LangSmith** como plataforma para la trazabilidad, monitoreo y evaluación automatizada de pipelines de RAG.
- **Implementar un ciclo de mejora continua**: evaluar, analizar resultados y optimizar el sistema de forma iterativa.

## Contenido del Módulo

### Conceptos Fundamentales

- **¿Por qué evaluar?**: Se explora la necesidad de ir más allá de la intuición y adoptar un enfoque basado en datos para la optimización de sistemas RAG.
- **Métricas Clave**:
    - **Recuperación (Retrieval)**: `Context Precision` y `Context Recall`.
    - **Generación (Generation)**: `Faithfulness` (Fidelidad) y `Answer Relevancy` (Relevancia de la Respuesta).

### Archivos y Actividades Prácticas

1.  **`1-evaluation-rag.py`**
    - **Descripción**: Una aplicación interactiva construida con **Streamlit** que permite visualizar un sistema RAG en acción. Podrás modificar documentos, realizar consultas y ver métricas de rendimiento y calidad en tiempo real.
    - **Uso**: Ejecuta este script para obtener una comprensión práctica de cómo las métricas de RAG se comportan en un entorno dinámico.

2.  **`2-langsmith-evaluation.ipynb`**
    - **Descripción**: Un Jupyter Notebook que te guía paso a paso en el uso de **LangSmith** para una evaluación más formal y sistemática.
    - **Actividades**:
        - Configurar la trazabilidad con LangSmith.
        - Crear un dataset de evaluación con preguntas y respuestas de referencia (`ground truth`).
        - Ejecutar evaluadores automáticos para medir la calidad del sistema.
        - Analizar los resultados para identificar puntos débiles.

3.  **`langsmith-evaluation.md` y `presentacion.md`**
    - **Descripción**: Documentos de apoyo que resumen los conceptos teóricos y los pasos prácticos cubiertos en las actividades. Úsalos como guía de referencia rápida y para consolidar tu aprendizaje.

## ¿Cómo Empezar?

1.  **Configura tu Entorno**: Asegúrate de tener las variables de entorno necesarias en un archivo `.env`, como se describe en `1-evaluation-rag.py` y `2-langsmith-evaluation.ipynb`. Necesitarás tus claves de API para los modelos de IA y para LangSmith.
2.  **Explora la Aplicación Interactiva**:
    ```bash
    streamlit run RA1/IL1.4/1-evaluation-rag.py
    ```
3.  **Realiza la Evaluación Sistemática**:
    - Abre y ejecuta las celdas del notebook `2-langsmith-evaluation.ipynb`.
    - Crea tu propia cuenta de LangSmith para visualizar las trazas y los resultados de los experimentos.
4.  **Itera y Mejora**: Basándote en los resultados de la evaluación, intenta modificar el sistema (por ejemplo, cambiando los prompts o la lógica de recuperación) y vuelve a evaluar para medir el impacto de tus cambios.
