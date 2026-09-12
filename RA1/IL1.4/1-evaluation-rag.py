"""
RAG Evaluation Dashboard - Sistema RAG con Evaluación y Monitoreo
==================================================================

Aplicación Streamlit que implementa un sistema RAG completo con:
- Búsqueda híbrida (semántica + palabras clave con filtro de stopwords)
- Evaluación automática de calidad (faithfulness, relevance, context precision)
- Dashboard con métricas y gráficos interactivos
- Exportación de datos (JSON para LangSmith, CSV)
- Gestión completa de documentos (CRUD + subida de archivos)
- Validación robusta de respuestas del LLM (None-safe)
- Fallback heurístico cuando el LLM falla

Arquitectura híbrida:
- Embeddings: Google AI Studio (API nativa) — OpenRouter NO soporta embeddings
- Chat: OpenRouter (modelo gratuito)

Instalación:
    pip install streamlit openai python-dotenv scikit-learn plotly \\
                langchain-core langchain-google-genai pandas numpy

Ejecución:
    python -m streamlit run 1-evaluation-rag.py

Requisitos (archivo .env):
    GEMINI_API_KEY=AIzaSy...              # https://ai.google.dev (gratis)
    OPENROUTER_API_KEY=sk-or-v1-...       # https://openrouter.ai/keys (gratis)
"""

import streamlit as st
import os
import json
import time
import uuid
from datetime import datetime
import pandas as pd
import numpy as np
import openai
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# LangChain imports (actualizados)
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Cargar variables desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    st.warning("⚠️ python-dotenv no está instalado. Ejecuta: pip install python-dotenv")


# ============================================================
# CONFIGURACIÓN DE PROVEEDORES
# ============================================================

# --- Chat (OpenRouter) ---
CHAT_MODEL = "qwen/qwen3.8-flash"           # Modelo gratuito
BASE_URL_CHAT = "https://openrouter.ai/api/v1"

# --- Embeddings (Google AI Studio, API nativa) ---
EMBEDDING_MODEL = "models/gemini-embedding-001"  # Prefijo 'models/' requerido

# --- Headers por defecto para OpenRouter ---
DEFAULT_HEADERS = {
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "RAG Evaluation",
}

# --- Stopwords en español (para filtro de palabras clave) ---
STOPWORDS_ES = {
    "de", "la", "que", "el", "en", "y", "a", "los", "se", "del",
    "las", "un", "por", "con", "no", "una", "su", "para", "es",
    "al", "lo", "como", "más", "o", "pero", "sus", "le", "ha",
    "me", "si", "sin", "sobre", "este", "ya", "entre", "cuando",
    "todo", "esta", "ser", "son", "dos", "también", "fue", "había",
    "era", "muy", "años", "hasta", "desde", "está", "mi", "porque",
    "qué", "sólo", "han", "yo", "hay", "vez", "puede", "todos",
    "así", "nos", "ni", "parte", "tiene", "él", "uno", "donde",
    "bien", "tiempo", "mismo", "ese", "ahora", "cada", "e", "vida",
    "otro", "después", "te", "otros", "aunque", "esa", "eso", "hace",
    "otra", "tan", "durante", "siempre", "día", "grande", "cosas",
    "ahí", "aquel", "sea", "según", "menos", "mundo", "año", "dijo",
    "sido", "hacer", "mientras", "cual", "cómo", "cuál", "quién",
    "quien", "dónde", "cuándo", "cuanto", "cuánto", "tanto", "tal",
    "solo", "aún", "aun",
}


# ============================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================

st.set_page_config(page_title="RAG Evaluation", page_icon="📊", layout="wide")


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def extraer_palabras_clave(texto):
    """Extrae palabras clave filtrando stopwords y palabras cortas."""
    if not texto:
        return []
    texto = texto.lower()
    for signo in "¿?¡!.,;:()[]{}":
        texto = texto.replace(signo, " ")
    return [p for p in texto.split() if p not in STOPWORDS_ES and len(p) >= 3]


def safe_get_content(response):
    """
    Extrae de forma segura el contenido de una respuesta del LLM.
    Devuelve None si algo falla (choices vacío, message None, content None).
    """
    try:
        if not response or not response.choices:
            return None
        message = response.choices[0].message
        if message is None:
            return None
        return message.content
    except (AttributeError, IndexError):
        return None


def parse_score_from_response(response, default=5.0):
    """
    Extrae un número (score 1-10) de la respuesta del LLM de forma segura.
    Devuelve el valor por defecto si algo falla.
    """
    content = safe_get_content(response)
    if content is None or not content.strip():
        return default
    try:
        score = float(content.strip())
        return max(1.0, min(10.0, score))
    except (ValueError, AttributeError):
        return default


def initialize_client():
    """Inicializa el cliente de OpenRouter para chat."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    try:
        return OpenAI(base_url=BASE_URL_CHAT, api_key=api_key)
    except Exception:
        return None


def initialize_embeddings():
    """Inicializa los embeddings usando la API nativa de Google."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=api_key
        )
    except Exception as e:
        st.error(f"Error inicializando embeddings: {e}")
        return None


def get_embeddings_langchain(embeddings_model, texts):
    """Genera embeddings para una lista de textos usando LangChain."""
    try:
        if isinstance(texts[0], str):
            documents = [Document(page_content=t) for t in texts]
        else:
            documents = texts
        embeddings = embeddings_model.embed_documents([d.page_content for d in documents])
        return np.array(embeddings)
    except Exception as e:
        st.error(f"Error generando embeddings: {e}")
        return None


def get_query_embedding_langchain(embeddings_model, query):
    """Genera el embedding de una consulta."""
    try:
        embedding = embeddings_model.embed_query(query)
        return np.array(embedding)
    except Exception as e:
        st.error(f"Error generando embedding de consulta: {e}")
        return None


# ============================================================
# FUNCIONES DE EVALUACIÓN (con validación robusta de None)
# ============================================================

def evaluate_faithfulness(client, query, context, response):
    """
    Evalúa si la respuesta se basa en el contexto (1-10).
    Robusto ante respuestas None del LLM.
    """
    if not client:
        return 5.0

    eval_prompt = f"""Evalúa si la respuesta es fiel al contexto proporcionado.

Consulta: {query}

Contexto:
{context}

Respuesta:
{response}

¿La respuesta está basada únicamente en la información del contexto?
Responde con un número del 1-10 donde:
- 1-3: Respuesta contradice o no está basada en el contexto
- 4-6: Respuesta parcialmente basada en el contexto
- 7-10: Respuesta completamente fiel al contexto

Responde SOLO con el número:"""

    try:
        result = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.0,
            max_tokens=10,
            extra_headers=DEFAULT_HEADERS,
        )
        return parse_score_from_response(result, default=5.0)
    except openai.AuthenticationError:
        st.warning("⚠️ Error de autenticación en faithfulness")
        return 5.0
    except openai.RateLimitError:
        st.warning("⚠️ Rate limit alcanzado en faithfulness")
        return 5.0
    except Exception as e:
        st.warning(f"⚠️ Error en faithfulness: {e}")
        return 5.0


def evaluate_relevance(client, query, response):
    """
    Evalúa qué tan relevante es la respuesta (1-10).
    Robusto ante respuestas None del LLM.
    """
    if not client:
        return 5.0

    eval_prompt = f"""Evalúa qué tan relevante es la respuesta para la consulta.

Consulta: {query}

Respuesta: {response}

¿Qué tan bien responde la respuesta a la consulta?
Responde con un número del 1-10 donde:
- 1-3: Respuesta no relacionada o irrelevante
- 4-6: Respuesta parcialmente relevante
- 7-10: Respuesta muy relevante y útil

Responde SOLO con el número:"""

    try:
        result = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.0,
            max_tokens=10,
            extra_headers=DEFAULT_HEADERS,
        )
        return parse_score_from_response(result, default=5.0)
    except openai.AuthenticationError:
        st.warning("⚠️ Error de autenticación en relevance")
        return 5.0
    except openai.RateLimitError:
        st.warning("⚠️ Rate limit alcanzado en relevance")
        return 5.0
    except Exception as e:
        st.warning(f"⚠️ Error en relevance: {e}")
        return 5.0


def _fallback_context_precision(query, retrieved_docs):
    """
    Fallback: calcula precision con heurística simple si el LLM falla.
    Compara palabras clave de la query con cada documento.
    """
    query_words = set(extraer_palabras_clave(query))
    if not query_words:
        return 0.0

    relevantes = 0
    for doc in retrieved_docs:
        doc_text = doc['document'] if isinstance(doc, dict) else str(doc)
        doc_words = set(extraer_palabras_clave(doc_text))
        if query_words.intersection(doc_words):
            relevantes += 1

    return relevantes / len(retrieved_docs) if retrieved_docs else 0.0


def evaluate_context_precision(client, query, retrieved_docs):
    """
    Evalúa la precisión del contexto (proporción de docs relevantes).
    Optimizado: UNA sola llamada al LLM para todos los documentos.
    Incluye validación robusta de respuestas None/vacías + fallback.
    """
    if not client or not retrieved_docs:
        return 0.0

    docs_text = "\n\n".join([
        f"Documento {i+1}: {doc['document'][:300]}..."
        for i, doc in enumerate(retrieved_docs)
    ])

    eval_prompt = f"""Evalúa la relevancia de CADA documento para responder la consulta.

Consulta: {query}

{docs_text}

Para cada documento, responde "SI" si es relevante o "NO" si no lo es.
Responde SOLO con las etiquetas separadas por comas, en orden. Ejemplo: "SI,NO,SI"

Respuesta:"""

    try:
        result = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.0,
            max_tokens=100,
            extra_headers=DEFAULT_HEADERS,
        )

        # --- VALIDACIÓN ROBUSTA ---
        content = safe_get_content(result)

        if content is None:
            # Fallback heurístico silencioso (no llena la UI de warnings)
            return _fallback_context_precision(query, retrieved_docs)

        content = content.strip()
        if not content:
            return _fallback_context_precision(query, retrieved_docs)

        # --- PROCESAMIENTO NORMAL ---
        etiquetas = content.upper().split(',')
        etiquetas = [e.strip() for e in etiquetas]
        relevantes = sum(1 for e in etiquetas if 'SI' in e)
        return relevantes / len(retrieved_docs)

    except Exception:
        return _fallback_context_precision(query, retrieved_docs)


# ============================================================
# BÚSQUEDA HÍBRIDA Y GENERACIÓN
# ============================================================

def hybrid_search_with_metrics(query, documents, embeddings, embeddings_model, client, top_k=5):
    """Búsqueda híbrida: 70% semántica + 30% palabras clave (sin stopwords)."""
    start_time = time.time()

    query_embedding = get_query_embedding_langchain(embeddings_model, query)
    if query_embedding is None:
        return [], 0.0

    # Similitud semántica
    semantic_similarities = cosine_similarity([query_embedding], embeddings)[0]

    # Similitud por palabras clave (SIN stopwords)
    query_words = set(extraer_palabras_clave(query))
    keyword_scores = []
    for doc in documents:
        doc_words = set(extraer_palabras_clave(doc))
        if not query_words:
            keyword_scores.append(0.0)
            continue
        overlap = len(query_words.intersection(doc_words))
        keyword_scores.append(overlap / len(query_words))

    # Combinación ponderada
    combined_scores = 0.7 * semantic_similarities + 0.3 * np.array(keyword_scores)
    top_indices = np.argsort(combined_scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            'document': documents[idx],
            'semantic_score': float(semantic_similarities[idx]),
            'keyword_score': float(keyword_scores[idx]),
            'combined_score': float(combined_scores[idx]),
            'index': int(idx)
        })

    retrieval_time = time.time() - start_time
    return results, retrieval_time


def generate_response_with_metrics(client, query, context_docs):
    """Genera la respuesta con el LLM y mide el tiempo. Robusto ante None."""
    if not client:
        return "Error: Cliente no disponible", 0.0

    start_time = time.time()

    # Separador correcto entre documentos
    context = "\n\n".join([
        f"Documento {i+1}: {doc['document']}"
        for i, doc in enumerate(context_docs)
    ])

    prompt = f"""Contexto:
{context}

Pregunta: {query}

Responde basándote únicamente en el contexto proporcionado."""

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
            extra_headers=DEFAULT_HEADERS,
        )
        generation_time = time.time() - start_time

        content = safe_get_content(response)
        if content is None:
            return "⚠️ El modelo no generó respuesta (puede estar saturado).", generation_time

        return content, generation_time

    except openai.AuthenticationError:
        return "Error: Autenticación fallida", time.time() - start_time
    except openai.RateLimitError:
        return "Error: Rate limit alcanzado", time.time() - start_time
    except Exception as e:
        return f"Error generating response: {e}", time.time() - start_time


# ============================================================
# DATASET DE EVALUACIÓN Y LOGGING
# ============================================================

def create_evaluation_dataset():
    """Dataset de prueba para evaluación sistemática."""
    return [
        {
            "query": "¿Qué es la inteligencia artificial?",
            "expected_context": "definición de IA",
            "ground_truth": "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana."
        },
        {
            "query": "¿Cómo funciona RAG?",
            "expected_context": "funcionamiento de RAG",
            "ground_truth": "RAG combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas."
        },
        {
            "query": "¿Qué es LangChain?",
            "expected_context": "descripción de LangChain",
            "ground_truth": "LangChain es un framework que facilita el desarrollo de aplicaciones con modelos de lenguaje."
        }
    ]


def log_interaction(query, response, metrics, context_docs):
    """Guarda una interacción en el historial de la sesión."""
    if 'interaction_logs' not in st.session_state:
        st.session_state.interaction_logs = []

    # Normalizar métricas para evitar NaN por claves inconsistentes
    metricas_completas = {
        'retrieval_time': metrics.get('retrieval_time', 0.0),
        'generation_time': metrics.get('generation_time', 0.0),
        'total_time': metrics.get('total_time', 0.0),
        'docs_retrieved': metrics.get('docs_retrieved', 0),
        'avg_relevance_score': metrics.get('avg_relevance_score', 0.0),
        'faithfulness': metrics.get('faithfulness', np.nan),
        'relevance': metrics.get('relevance', np.nan),
        'context_precision': metrics.get('context_precision', np.nan),
    }

    log_entry = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'response': response,
        'metrics': metricas_completas,
        'context_count': len(context_docs),
        'context_scores': [doc.get('combined_score', 0) for doc in context_docs]
    }

    st.session_state.interaction_logs.append(log_entry)


def export_langsmith_format(logs):
    """Convierte los logs al formato de LangSmith."""
    langsmith_data = []
    for log in logs:
        langsmith_data.append({
            "run_id": log['id'],
            "timestamp": log['timestamp'],
            "inputs": {"query": log['query']},
            "outputs": {"response": log['response']},
            "metrics": log['metrics'],
            "metadata": {
                "context_count": log['context_count'],
                "context_scores": log['context_scores']
            }
        })
    return langsmith_data


# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================

def main():
    st.title("📊 RAG con Evaluación y Monitoreo")
    st.write("Sistema RAG con arquitectura híbrida (Google + OpenRouter) y métricas de calidad")

    # --- Verificación de claves API ---
    if not os.getenv("OPENROUTER_API_KEY"):
        st.error("❌ Falta OPENROUTER_API_KEY en el archivo .env")
        st.info("💡 Tu .env debe contener: OPENROUTER_API_KEY=sk-or-v1-...")
        st.markdown("**Obtén tu clave gratis en:** https://openrouter.ai/keys")
        return
    if not os.getenv("GEMINI_API_KEY"):
        st.error("❌ Falta GEMINI_API_KEY en el archivo .env")
        st.info("💡 Tu .env debe contener: GEMINI_API_KEY=AIzaSy...")
        st.markdown("**Obtén tu clave gratis en:** https://ai.google.dev")
        return

    # --- Inicialización de session_state ---
    if "eval_rag" not in st.session_state:
        st.session_state.eval_rag = {
            'documents': [
                "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana.",
                "Los modelos de lenguaje grande (LLM) son sistemas de IA entrenados en enormes cantidades de texto para generar y comprender lenguaje natural.",
                "RAG (Retrieval-Augmented Generation) combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas.",
                "LangChain es un framework que facilita el desarrollo de aplicaciones con modelos de lenguaje, proporcionando herramientas para cadenas y agentes.",
                "El prompt engineering es la práctica de diseñar instrucciones efectivas para obtener los mejores resultados de los modelos de IA.",
                "Los embeddings son representaciones vectoriales de texto que capturan el significado semántico en un espacio multidimensional.",
                "La búsqueda semántica utiliza embeddings para encontrar contenido relacionado por significado, no solo por palabras clave.",
                "Los sistemas de evaluación de IA miden métricas como relevancia, fidelidad y precisión del contexto."
            ],
            'embeddings': None,
            'embeddings_model': None,
            'enable_logging': True
        }

    if 'interaction_logs' not in st.session_state:
        st.session_state.interaction_logs = []

    if 'editing_doc' not in st.session_state:
        st.session_state.editing_doc = None

    # --- Inicialización de clientes ---
    client = initialize_client()
    if not client:
        return

    if st.session_state.eval_rag['embeddings_model'] is None:
        st.session_state.eval_rag['embeddings_model'] = initialize_embeddings()

    # --- Pestañas ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Consulta", "📄 Documentos", "📊 Métricas", "🧪 Evaluación", "📈 Analytics"
    ])

    # ========================================================
    # TAB 1: CONSULTA
    # ========================================================
    with tab1:
        st.header("💬 Consulta con Monitoreo")

        col1, col2 = st.columns([3, 1])

        with col1:
            query = st.text_input("Haz tu pregunta:")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                top_k = st.slider("Docs a recuperar:", 1, 8, 3)
            with col_b:
                eval_enabled = st.checkbox("Evaluación automática", value=True)
            with col_c:
                st.session_state.eval_rag['enable_logging'] = st.checkbox("Logging", value=True)

        with col2:
            if st.button("🔄 Generar Embeddings"):
                if st.session_state.eval_rag['documents'] and st.session_state.eval_rag['embeddings_model']:
                    with st.spinner("Generando embeddings..."):
                        embeddings = get_embeddings_langchain(
                            st.session_state.eval_rag['embeddings_model'],
                            st.session_state.eval_rag['documents']
                        )
                        if embeddings is not None:
                            st.session_state.eval_rag['embeddings'] = embeddings
                            st.success("✅ Embeddings listos")
                        else:
                            st.error("❌ Error generando embeddings")
                else:
                    st.warning("Modelo de embeddings no disponible")

        if st.button("🚀 Consultar con Métricas") and query:
            if st.session_state.eval_rag['embeddings'] is None:
                st.warning("⚠️ Genera embeddings primero")
            elif st.session_state.eval_rag['embeddings_model'] is None:
                st.warning("⚠️ Modelo de embeddings no inicializado")
            else:
                with st.spinner("Procesando con métricas..."):
                    results, retrieval_time = hybrid_search_with_metrics(
                        query,
                        st.session_state.eval_rag['documents'],
                        st.session_state.eval_rag['embeddings'],
                        st.session_state.eval_rag['embeddings_model'],
                        client,
                        top_k
                    )

                    if not results:
                        st.error("Error en la búsqueda")
                    else:
                        response, generation_time = generate_response_with_metrics(client, query, results)

                        metrics = {
                            'retrieval_time': retrieval_time,
                            'generation_time': generation_time,
                            'total_time': retrieval_time + generation_time,
                            'docs_retrieved': len(results),
                            'avg_relevance_score': float(np.mean([r['combined_score'] for r in results]))
                        }

                        if eval_enabled:
                            context_text = "\n\n".join([r['document'] for r in results])

                            with st.spinner("Evaluando calidad..."):
                                metrics['faithfulness'] = evaluate_faithfulness(client, query, context_text, response)
                                metrics['relevance'] = evaluate_relevance(client, query, response)
                                metrics['context_precision'] = evaluate_context_precision(client, query, results)

                        st.subheader("📋 Documentos Recuperados")
                        for i, result in enumerate(results):
                            with st.expander(f"Doc {i+1} - Score: {result['combined_score']:.3f}"):
                                st.write(result['document'])
                                st.caption(
                                    f"Semántica: {result['semantic_score']:.3f} | "
                                    f"Palabras clave: {result['keyword_score']:.3f}"
                                )

                        st.subheader("🤖 Respuesta")
                        st.write(response)

                        st.subheader("⏱️ Métricas de Rendimiento")
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Tiempo total", f"{metrics['total_time']:.2f}s")
                        c2.metric("Recuperación", f"{metrics['retrieval_time']:.2f}s")
                        c3.metric("Generación", f"{metrics['generation_time']:.2f}s")
                        c4.metric("Docs recuperados", metrics['docs_retrieved'])

                        if eval_enabled:
                            st.subheader("🎯 Métricas de Calidad")
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Fidelidad", f"{metrics['faithfulness']:.1f}/10")
                            c2.metric("Relevancia", f"{metrics['relevance']:.1f}/10")
                            c3.metric("Precisión contexto", f"{metrics['context_precision']:.2f}")

                        if st.session_state.eval_rag['enable_logging']:
                            log_interaction(query, response, metrics, results)

    # ========================================================
    # TAB 2: GESTIÓN DE DOCUMENTOS
    # ========================================================
    with tab2:
        st.header("📄 Gestión de Documentos")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📚 Documentos Actuales")

            for i, doc in enumerate(st.session_state.eval_rag['documents']):
                with st.expander(f"Documento {i+1} ({len(doc)} caracteres)"):
                    st.text_area(
                        f"Contenido del documento {i+1}:",
                        value=doc,
                        height=100,
                        key=f"doc_display_{i}",
                        disabled=True
                    )

                    col_edit, col_delete = st.columns(2)
                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_{i}"):
                            st.session_state.editing_doc = i
                            st.rerun()

                    with col_delete:
                        if st.button("🗑️ Eliminar", key=f"delete_{i}"):
                            st.session_state.eval_rag['documents'].pop(i)
                            st.session_state.eval_rag['embeddings'] = None
                            st.success("Documento eliminado. Recuerda regenerar embeddings.")
                            st.rerun()

            # --- Modo edición ---
            if st.session_state.editing_doc is not None:
                idx = st.session_state.editing_doc
                if 0 <= idx < len(st.session_state.eval_rag['documents']):
                    st.divider()
                    st.subheader(f"✏️ Editando documento {idx+1}")

                    new_content = st.text_area(
                        "Nuevo contenido:",
                        value=st.session_state.eval_rag['documents'][idx],
                        height=150,
                        key="edit_content_area"
                    )

                    c_save, c_cancel = st.columns(2)
                    with c_save:
                        if st.button("💾 Guardar"):
                            st.session_state.eval_rag['documents'][idx] = new_content
                            st.session_state.eval_rag['embeddings'] = None
                            st.session_state.editing_doc = None
                            st.success("Documento actualizado. Recuerda regenerar embeddings.")
                            st.rerun()

                    with c_cancel:
                        if st.button("❌ Cancelar"):
                            st.session_state.editing_doc = None
                            st.rerun()

        with col2:
            st.subheader("➕ Agregar Documento")

            new_doc = st.text_area(
                "Contenido del nuevo documento:",
                height=200,
                placeholder="Escribe aquí el contenido del nuevo documento..."
            )

            if st.button("📝 Agregar Documento"):
                if new_doc.strip():
                    st.session_state.eval_rag['documents'].append(new_doc.strip())
                    st.session_state.eval_rag['embeddings'] = None
                    st.success("Documento agregado exitosamente")
                    st.rerun()
                else:
                    st.warning("El documento no puede estar vacío")

            st.subheader("📊 Estadísticas")
            st.metric("Total documentos", len(st.session_state.eval_rag['documents']))

            if st.session_state.eval_rag['documents']:
                avg_length = np.mean([len(doc) for doc in st.session_state.eval_rag['documents']])
                st.metric("Longitud promedio", f"{avg_length:.0f} caracteres")

                total_words = sum([len(doc.split()) for doc in st.session_state.eval_rag['documents']])
                st.metric("Total palabras", f"{total_words:,}")

            st.subheader("🔄 Acciones")

            if st.button("🗑️ Limpiar Todos"):
                if st.session_state.eval_rag['documents']:
                    st.session_state.eval_rag['documents'] = []
                    st.session_state.eval_rag['embeddings'] = None
                    st.success("Todos los documentos eliminados")
                    st.rerun()

            uploaded_file = st.file_uploader(
                "📁 Cargar archivo de texto",
                type=['txt', 'md'],
                help="Sube un archivo .txt o .md para agregarlo como documento"
            )

            if uploaded_file is not None:
                try:
                    content = uploaded_file.read().decode('utf-8')
                    if st.button("📥 Importar Archivo"):
                        st.session_state.eval_rag['documents'].append(content)
                        st.session_state.eval_rag['embeddings'] = None
                        st.success(f"Archivo '{uploaded_file.name}' importado")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error al leer el archivo: {e}")

            st.subheader("🔧 Estado")
            if st.session_state.eval_rag['embeddings'] is not None:
                st.success("✅ Embeddings generados")
            else:
                st.warning("⚠️ Embeddings no generados")

    # ========================================================
    # TAB 3: MÉTRICAS
    # ========================================================
    with tab3:
        st.header("📊 Dashboard de Métricas")

        if st.session_state.interaction_logs:
            df = pd.DataFrame([
                {
                    'timestamp': log['timestamp'],
                    'query_length': len(log['query']),
                    'response_length': len(log['response']),
                    **log['metrics']
                }
                for log in st.session_state.interaction_logs
            ])

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Response Time")
                fig = px.line(df, x='timestamp', y='total_time', title="Total Time per Query")
                st.plotly_chart(fig, width='stretch')

                if 'faithfulness' in df.columns and df['faithfulness'].notna().any():
                    st.subheader("Faithfulness Distribution")
                    fig = px.histogram(df.dropna(subset=['faithfulness']),
                                       x='faithfulness',
                                       title="Faithfulness Scores Distribution")
                    st.plotly_chart(fig, width='stretch')

            with col2:
                st.subheader("Retrieval Metrics")
                fig = px.scatter(df, x='retrieval_time', y='generation_time',
                                 size='docs_retrieved', title="Retrieval vs Generation Time")
                st.plotly_chart(fig, width='stretch')

                if ('relevance' in df.columns and 'context_precision' in df.columns
                        and df['relevance'].notna().any()):
                    st.subheader("Quality vs Precision")
                    df_clean = df.dropna(subset=['relevance', 'context_precision'])
                    fig = px.scatter(df_clean, x='context_precision', y='relevance',
                                     title="Context Precision vs Relevance")
                    st.plotly_chart(fig, width='stretch')

            st.subheader("📈 Estadísticas Generales")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Queries", len(df))
            c2.metric("Tiempo Promedio", f"{df['total_time'].mean():.2f}s")
            if 'faithfulness' in df.columns and df['faithfulness'].notna().any():
                c3.metric("Fidelidad Promedio", f"{df['faithfulness'].mean():.1f}/10")
            if 'relevance' in df.columns and df['relevance'].notna().any():
                c4.metric("Relevancia Promedio", f"{df['relevance'].mean():.1f}/10")
        else:
            st.info("No hay datos de interacciones aún. Realiza algunas consultas primero.")

    # ========================================================
    # TAB 4: EVALUACIÓN SISTEMÁTICA
    # ========================================================
    with tab4:
        st.header("🧪 Evaluación Sistemática")

        if st.button("🧪 Ejecutar Evaluación Completa"):
            if st.session_state.eval_rag['embeddings'] is None:
                st.warning("⚠️ Genera embeddings primero")
            elif st.session_state.eval_rag['embeddings_model'] is None:
                st.warning("⚠️ Modelo de embeddings no inicializado")
            else:
                eval_dataset = create_evaluation_dataset()
                results = []

                progress = st.progress(0)
                status = st.empty()

                for i, test_case in enumerate(eval_dataset):
                    query = test_case['query']
                    status.text(f"Evaluando: {query}")

                    docs, retrieval_time = hybrid_search_with_metrics(
                        query,
                        st.session_state.eval_rag['documents'],
                        st.session_state.eval_rag['embeddings'],
                        st.session_state.eval_rag['embeddings_model'],
                        client,
                        3
                    )

                    if docs:
                        response, generation_time = generate_response_with_metrics(client, query, docs)

                        context_text = "\n\n".join([d['document'] for d in docs])
                        faithfulness = evaluate_faithfulness(client, query, context_text, response)
                        relevance = evaluate_relevance(client, query, response)
                        context_precision = evaluate_context_precision(client, query, docs)

                        results.append({
                            'query': query,
                            'response': response,
                            'retrieval_time': retrieval_time,
                            'generation_time': generation_time,
                            'faithfulness': faithfulness,
                            'relevance': relevance,
                            'context_precision': context_precision,
                            'ground_truth': test_case['ground_truth']
                        })

                    progress.progress((i + 1) / len(eval_dataset))

                status.text("✅ Evaluación completada")

                if results:
                    st.subheader("📊 Resultados de Evaluación")
                    eval_df = pd.DataFrame(results)
                    st.dataframe(eval_df, width='stretch')

                    st.subheader("📈 Métricas Promedio")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Fidelidad", f"{eval_df['faithfulness'].mean():.1f}/10")
                    c2.metric("Relevancia", f"{eval_df['relevance'].mean():.1f}/10")
                    c3.metric("Precisión", f"{eval_df['context_precision'].mean():.2f}")
                    c4.metric("Tiempo total", f"{(eval_df['retrieval_time'] + eval_df['generation_time']).mean():.2f}s")
                else:
                    st.error("No se pudieron obtener resultados de evaluación")

    # ========================================================
    # TAB 5: ANALYTICS Y EXPORTACIÓN
    # ========================================================
    with tab5:
        st.header("📈 Analytics y Exportación")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📤 Exportar Datos")

            if st.button("📊 Exportar para LangSmith"):
                if st.session_state.interaction_logs:
                    langsmith_data = export_langsmith_format(st.session_state.interaction_logs)
                    st.json(langsmith_data[:2])

                    json_str = json.dumps(langsmith_data, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="💾 Descargar JSON LangSmith",
                        data=json_str,
                        file_name=f"langsmith_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.info("No hay datos para exportar")

            if st.button("📊 Exportar CSV"):
                if st.session_state.interaction_logs:
                    df = pd.DataFrame([
                        {
                            'timestamp': log['timestamp'],
                            'query': log['query'],
                            'response': log['response'][:100] + "...",
                            **log['metrics']
                        }
                        for log in st.session_state.interaction_logs
                    ])

                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="💾 Descargar CSV",
                        data=csv,
                        file_name=f"rag_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No hay datos para exportar")

        with col2:
            st.subheader("📊 Análisis de Documentos")

            if st.session_state.eval_rag['documents']:
                doc_lengths = [len(doc) for doc in st.session_state.eval_rag['documents']]

                fig = px.bar(
                    x=list(range(1, len(doc_lengths) + 1)),
                    y=doc_lengths,
                    title="Distribución de Longitud de Documentos",
                    labels={'x': 'Documento', 'y': 'Caracteres'}
                )
                st.plotly_chart(fig, width='stretch')

                # Top 10 palabras más frecuentes (con filtro de stopwords)
                all_text = " ".join(st.session_state.eval_rag['documents'])
                palabras = extraer_palabras_clave(all_text)
                word_freq = {}
                for word in palabras:
                    word_freq[word] = word_freq.get(word, 0) + 1

                top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

                if top_words:
                    fig = px.bar(
                        x=[w[0] for w in top_words],
                        y=[w[1] for w in top_words],
                        title="Top 10 Palabras Más Frecuentes (sin stopwords)"
                    )
                    st.plotly_chart(fig, width='stretch')
            else:
                st.info("No hay documentos disponibles para analizar")


if __name__ == "__main__":
    main()
