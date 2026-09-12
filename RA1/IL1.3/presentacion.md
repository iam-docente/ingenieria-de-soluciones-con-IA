# Presentación IL1.3 - Infraestructura RAG

## Slide 1: Título y Objetivos
**Título:** IL1.3 - Infraestructura RAG (Retrieval-Augmented Generation)
**Subtítulo:** Conectando LLMs con Conocimiento Externo y Verificable

**Objetivos:**
- Comprender la arquitectura RAG y sus componentes.
- Implementar el flujo completo: Carga, División, Embeddings y Generación.
- Utilizar bases de datos vectoriales para una recuperación de información eficiente.
- Aplicar RAG para mejorar la precisión y fiabilidad de los LLMs.

---

## Slide 2: ¿Qué es RAG y Por Qué es Crucial?
**Título:** El Framework de Recuperación Aumentada

**Contenido:**
- **Definición:** Una arquitectura que combina un recuperador de información con un generador (LLM) para producir respuestas basadas en un corpus de conocimiento externo.
- **Proceso:**
    1.  **Recuperar:** Busca fragmentos de información relevante para la consulta del usuario.
    2.  **Aumentar:** Inserta esos fragmentos como contexto en el prompt del LLM.
    3.  **Generar:** El LLM sintetiza una respuesta a partir del contexto proporcionado.
- **Beneficios:** Reduce alucinaciones, permite el uso de datos actualizados y privados, y aumenta la transparencia al poder citar fuentes.

---

## Slide 3: Notebooks 1 & 2 - Fundamentos y Preparación de Datos
**Título:** Del Documento a los Fragmentos (`Chunks`)

**Notebook `1-basic-rag.ipynb`:**
- Se introduce el concepto de RAG con un ejemplo mínimo y funcional.
- Se muestra el flujo completo de manera simplificada para entender la interacción entre el recuperador y el generador.

**Notebook `2-text-chunking.py`:**
- Se explora la importancia de la **división de texto** (`Text Splitting`).
- Se analizan diferentes estrategias (ej. `RecursiveCharacterTextSplitter`) y el impacto del tamaño y solapamiento (`chunk_size`, `chunk_overlap`) en la calidad de la recuperación.

---

## Slide 4: Notebooks 3 & 4 - Embeddings y Búsqueda Vectorial
**Título:** De Fragmentos a Respuestas Inteligentes

**Notebook `3-embeddings-simple-rag.ipynb`:**
- Se explica cómo los **modelos de embeddings** convierten los `chunks` de texto en vectores numéricos que capturan su significado semántico.
- Se implementa una búsqueda de similitud simple para encontrar los `chunks` más relevantes.

**Notebook `4-vector-rag.ipynb`:**
- Se introduce el concepto de **Base de Datos Vectorial** (`Vector Store`).
- Se utiliza una base de datos como FAISS o Chroma para almacenar los embeddings de forma eficiente y realizar búsquedas a gran escala, creando un sistema RAG más robusto.

---

## Slide 5: Evaluación del Módulo
**Título:** Componentes de Evaluación

**Quiz teórico:**
- Preguntas sobre la arquitectura RAG, sus componentes (Retriever, Vector Store) y sus beneficios (reducción de alucinaciones).

**Práctica dirigida:**
- Ejecución de los 4 notebooks, desde el RAG básico hasta la implementación con base de datos vectorial.
- Experimentación con diferentes estrategias de `chunking` y su impacto en las respuestas.

**Ejercicios adicionales:**
- Aplicar el sistema RAG a un nuevo documento PDF o de texto.
- Intercambiar el modelo de embeddings y observar los cambios en la calidad de la recuperación.

---

## Slide 6: Recursos y Próximos Pasos
**Título:** Continuando el Aprendizaje

**Recursos adicionales:**
- [LangChain RAG Documentation](https://python.langchain.com/docs/use_cases/question_answering/)
- [Blog de Pinecone: ¿Qué es RAG?](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [FAISS: A library for efficient similarity search](https://engineering.fb.com/2017/03/29/faiss-a-library-for-efficient-similarity-search/)

**Próximos módulos:**
- **IL1.4: Evaluación y Optimización de LLMs:** Aprenderemos a medir cuantitativamente el rendimiento de nuestro sistema RAG para poder mejorarlo.