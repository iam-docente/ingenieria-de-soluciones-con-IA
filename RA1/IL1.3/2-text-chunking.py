"""
📝 Demostrador de División de Texto en Chunks (Chunking)
=========================================================

Aplicación interactiva con Streamlit para visualizar y comparar
diferentes métodos de chunking de texto, paso fundamental en RAG.

Ejecución:
    streamlit run 2-text-chunking.py

Autor: Curso de RAG
"""

import streamlit as st
import re

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Text Chunking Demo",
    page_icon="📝",
    layout="wide"
)


# ============================================================
# FUNCIONES DE CHUNKING
# ============================================================

def chunking_text(text, chunk_size=200, overlap=50):
    """
    Divide el texto en chunks de N palabras con solapamiento.
    
    Args:
        text (str): Texto a dividir.
        chunk_size (int): Número de palabras por chunk.
        overlap (int): Número de palabras de solapamiento entre chunks.
    
    Returns:
        list: Lista de chunks (strings).
    """
    if not text or not text.strip():
        return []
    
    words = text.split()
    chunks = []
    
    # Validar que el solapamiento sea menor que el tamaño del chunk
    if overlap >= chunk_size:
        overlap = chunk_size - 1
    
    step = max(1, chunk_size - overlap)  # Asegurar que el paso sea al menos 1
    
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        # Si ya cubrimos el final, salir
        if i + chunk_size >= len(words):
            break
        
        i += step
    
    return chunks


def chunking_by_sentences(text, max_sentences=5, overlap_sentences=1):
    """
    Divide el texto por oraciones, preservando los signos de puntuación
    originales (¿?, ¡!, ., etc.).
    
    Args:
        text (str): Texto a dividir.
        max_sentences (int): Máximo de oraciones por chunk.
        overlap_sentences (int): Solapamiento en oraciones.
    
    Returns:
        list: Lista de chunks.
    """
    if not text or not text.strip():
        return []
    
    # Regex que captura cada oración CON su signo de puntuación final
    # Explicación: [^.!?]+ captura todo lo que no sea . ! ?,
    # y [.!?]+ captura el signo final (uno o más).
    sentences = re.findall(r'[^.!?]+[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Si no se detectaron oraciones (texto sin puntuación), usar el texto completo
    if not sentences:
        sentences = [text.strip()]
    
    chunks = []
    
    # Validar solapamiento
    if overlap_sentences >= max_sentences:
        overlap_sentences = max_sentences - 1
    
    step = max(1, max_sentences - overlap_sentences)
    
    i = 0
    while i < len(sentences):
        chunk_sentences = sentences[i:i + max_sentences]
        # Unir con espacio (las oraciones ya incluyen su puntuación)
        chunk = ' '.join(chunk_sentences)
        chunks.append(chunk)
        
        if i + max_sentences >= len(sentences):
            break
        
        i += step
    
    return chunks


def chunking_by_paragraphs(text):
    """
    Divide el texto por párrafos (separados por doble salto de línea).
    
    Args:
        text (str): Texto a dividir.
    
    Returns:
        list: Lista de párrafos.
    """
    if not text or not text.strip():
        return []
    
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]


def chunking_by_characters(text, chunk_size=500, overlap=100):
    """
    Divide el texto por número de caracteres con solapamiento.
    
    Args:
        text (str): Texto a dividir.
        chunk_size (int): Número de caracteres por chunk.
        overlap (int): Solapamiento en caracteres.
    
    Returns:
        list: Lista de chunks.
    """
    if not text or not text.strip():
        return []
    
    chunks = []
    
    # Validar solapamiento
    if overlap >= chunk_size:
        overlap = chunk_size - 1
    
    step = max(1, chunk_size - overlap)
    
    i = 0
    while i < len(text):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        
        if i + chunk_size >= len(text):
            break
        
        i += step
    
    return chunks


# ============================================================
# TEXTOS DE EJEMPLO
# ============================================================

EXAMPLE_TEXTS = {
    "Artículo científico": """La inteligencia artificial (IA) es una rama de la informática que se ocupa de la creación de sistemas capaces de realizar tareas que normalmente requieren inteligencia humana. Estos sistemas pueden aprender, razonar, percibir y tomar decisiones.

El aprendizaje automático es un subconjunto de la IA que permite a las máquinas aprender y mejorar automáticamente a partir de la experiencia sin ser programadas explícitamente. Los algoritmos de aprendizaje automático construyen un modelo matemático basado en datos de entrenamiento para hacer predicciones o decisiones.

Las redes neuronales artificiales son un modelo computacional inspirado en las redes neuronales biológicas. Están compuestas por nodos interconectados que procesan información de manera similar a como lo hacen las neuronas en el cerebro humano.

El procesamiento de lenguaje natural (PLN) es otra área importante de la IA que se centra en la interacción entre computadoras y lenguaje humano. El PLN permite a las máquinas leer, entender y generar texto de manera similar a como lo hacen los humanos.""" ,

    "Historia": """La Revolución Industrial fue un período de grandes cambios tecnológicos, socioeconómicos y culturales que comenzó en Gran Bretaña a finales del siglo XVIII y se extendió por Europa y América del Norte durante el siglo XIX.

Este período se caracterizó por el paso de una economía rural basada principalmente en la agricultura y el comercio a una economía de carácter urbano, industrializada y mecanizada. La introducción de maquinaria en los procesos de producción supuso un cambio radical en las formas de trabajo.

La máquina de vapor, inventada por James Watt, fue una de las innovaciones más importantes de este período. Permitió el desarrollo de fábricas que no dependían de fuentes de energía naturales como el agua o el viento.

El ferrocarril revolucionó el transporte de mercancías y personas, conectando ciudades y regiones de manera más eficiente que nunca antes. Esto facilitó el comercio y la migración de trabajadores hacia los centros industriales.""" ,

    "Receta": """Para preparar una deliciosa pasta carbonara necesitarás los siguientes ingredientes: 400g de espaguetis, 200g de panceta o guanciale, 4 huevos enteros, 100g de queso parmesano rallado, pimienta negra recién molida y sal.

Primero, pon a hervir abundante agua con sal en una olla grande. Mientras tanto, corta la panceta en cubitos pequeños y cocínala en una sartén grande a fuego medio hasta que esté dorada y crujiente.

En un bol, bate los huevos con el queso parmesano rallado y una generosa cantidad de pimienta negra. Esta mezcla será la base cremosa de tu carbonara.

Cuando el agua hierva, añade los espaguetis y cocínalos según las instrucciones del paquete hasta que estén al dente. Reserva una taza del agua de cocción antes de escurrir la pasta.

Inmediatamente después de escurrir, añade los espaguetis calientes a la sartén con la panceta. Retira del fuego y añade la mezcla de huevos y queso, removiendo rápidamente para crear una salsa cremosa. Si es necesario, añade un poco del agua de cocción reservada."""
}


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    st.title("📝 Demostrador de División de Texto en Chunks")
    st.write(
        "Herramienta interactiva para visualizar y comparar "
        "diferentes métodos de chunking, paso clave en sistemas RAG."
    )
    
    # --------------------------------------------------------
    # SIDEBAR: Configuración
    # --------------------------------------------------------
    st.sidebar.header("⚙️ Configuración")
    
    chunking_method = st.sidebar.selectbox(
        "Método de división:",
        ["Por palabras", "Por oraciones", "Por párrafos", "Por caracteres"]
    )
    
    # Variables con valores por defecto (para evitar NameError)
    chunk_size = 200
    overlap = 50
    max_sentences = 5
    overlap_sentences = 1
    
    # Configuraciones específicas según el método
    if chunking_method == "Por palabras":
        chunk_size = st.sidebar.slider(
            "Tamaño del chunk (palabras):", 50, 500, 200, 25
        )
        overlap = st.sidebar.slider(
            "Solapamiento (palabras):", 0, chunk_size - 1,
            min(50, chunk_size - 1), 10
        )
        
    elif chunking_method == "Por oraciones":
        max_sentences = st.sidebar.slider(
            "Máximo oraciones por chunk:", 1, 10, 5
        )
        overlap_sentences = st.sidebar.slider(
            "Solapamiento (oraciones):", 0, max_sentences - 1,
            min(1, max_sentences - 1)
        )
        
    elif chunking_method == "Por caracteres":
        chunk_size = st.sidebar.slider(
            "Tamaño del chunk (caracteres):", 100, 2000, 500, 100
        )
        overlap = st.sidebar.slider(
            "Solapamiento (caracteres):", 0, chunk_size - 1,
            min(100, chunk_size - 1), 50
        )
    
    # --------------------------------------------------------
    # LAYOUT: Dos columnas
    # --------------------------------------------------------
    col1, col2 = st.columns([1, 1])
    
    # ========================================================
    # COLUMNA 1: Texto Original
    # ========================================================
    with col1:
        st.header("📄 Texto Original")
        
        # ✅ Inicialización por defecto para evitar NameError
        text_input = ""
        
        input_method = st.radio(
            "Método de entrada:",
            ["Texto manual", "Texto de ejemplo"]
        )
        
        if input_method == "Texto manual":
            text_input = st.text_area(
                "Ingresa tu texto:",
                height=300,
                placeholder="Escribe o pega aquí el texto que quieres dividir en chunks..."
            )
        else:
            selected_example = st.selectbox(
                "Selecciona un texto de ejemplo:",
                list(EXAMPLE_TEXTS.keys())
            )
            text_input = EXAMPLE_TEXTS[selected_example]
            st.text_area(
                "Texto seleccionado:",
                value=text_input,
                height=300,
                disabled=True
            )
    
    # ========================================================
    # COLUMNA 2: Chunks Generados
    # ========================================================
    with col2:
        st.header("🔪 Chunks Generados")
        
        # ✅ Cálculo automático (reactivo, sin botón)
        if text_input.strip():
            # Generar chunks según el método seleccionado
            if chunking_method == "Por palabras":
                chunks = chunking_text(text_input, chunk_size, overlap)
            elif chunking_method == "Por oraciones":
                chunks = chunking_by_sentences(
                    text_input, max_sentences, overlap_sentences
                )
            elif chunking_method == "Por párrafos":
                chunks = chunking_by_paragraphs(text_input)
            else:  # Por caracteres
                chunks = chunking_by_characters(text_input, chunk_size, overlap)
            
            # ------------------------------------------------
            # Estadísticas
            # ------------------------------------------------
            st.subheader("📊 Estadísticas")
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                st.metric("Total chunks", len(chunks))
            with col_s2:
                st.metric("Palabras originales", len(text_input.split()))
            with col_s3:
                avg = (
                    sum(len(c.split()) for c in chunks) / len(chunks)
                    if chunks else 0
                )
                st.metric("Promedio palabras/chunk", f"{avg:.1f}")
            
            # ------------------------------------------------
            # Visualización de chunks
            # ------------------------------------------------
            st.subheader("📋 Chunks Generados")
            
            # ✅ Limitar visualización para no colapsar la UI
            MAX_CHUNKS_MOSTRAR = 20
            chunks_mostrados = chunks[:MAX_CHUNKS_MOSTRAR]
            
            for i, chunk in enumerate(chunks_mostrados):
                num_palabras = len(chunk.split())
                num_caracteres = len(chunk)
                
                with st.expander(
                    f"Chunk {i+1} ({num_palabras} palabras, {num_caracteres} caracteres)"
                ):
                    st.write(chunk)
                    st.caption(
                        f"Palabras: {num_palabras} | "
                        f"Caracteres: {num_caracteres}"
                    )
            
            # Aviso si hay más chunks de los mostrados
            if len(chunks) > MAX_CHUNKS_MOSTRAR:
                st.info(
                    f"ℹ️ Mostrando {MAX_CHUNKS_MOSTRAR} de {len(chunks)} chunks totales. "
                    f"Ajusta los parámetros para reducir el número de chunks."
                )
        
        elif not text_input.strip():
            st.info(
                "👈 Ingresa o selecciona un texto en la columna izquierda "
                "para ver los chunks generados."
            )
    
    # --------------------------------------------------------
    # INFORMACIÓN ADICIONAL
    # --------------------------------------------------------
    st.header("ℹ️ Información sobre Métodos de Chunking")
    
    with st.expander("📖 Detalles de cada método"):
        st.markdown("""
        **🔤 Por palabras:**
        - Divide el texto en chunks de un número específico de palabras.
        - Permite solapamiento para mantener contexto entre chunks.
        - Útil para textos largos y uniformes.
        
        **📝 Por oraciones:**
        - Agrupa oraciones completas en cada chunk.
        - **Preserva los signos de puntuación originales** (¿?, ¡!, ., etc.).
        - Mantiene la coherencia semántica.
        - Ideal para textos narrativos o explicativos.
        
        **📄 Por párrafos:**
        - Cada párrafo se convierte en un chunk.
        - Preserva la estructura original del texto.
        - Perfecto para textos bien estructurados.
        - ⚠️ No permite solapamiento.
        
        **🔡 Por caracteres:**
        - División basada en número de caracteres.
        - Control preciso del tamaño.
        - Útil cuando hay limitaciones estrictas de longitud (APIs).
        """)
    
    with st.expander("🎯 ¿Cuándo usar cada método?"):
        st.markdown("""
        | Caso de uso | Método recomendado | Por qué |
        | :--- | :--- | :--- |
        | **Documentos largos y uniformes** | Por palabras con solapamiento | Control balanceado del tamaño |
        | **Artículos y ensayos** | Por oraciones o párrafos | Mantiene coherencia semántica |
        | **Textos técnicos** | Por párrafos | Conserva conceptos completos |
        | **APIs con límites de caracteres** | Por caracteres | Control exacto del tamaño |
        | **Análisis de sentimientos** | Por oraciones | Preserva contexto emocional |
        | **Documentos legales** | Por párrafos | Respeta la estructura legal |
        """)
    
    with st.expander("💡 Consejos para elegir el mejor chunking"):
        st.markdown("""
        **Regla general:** El tamaño ideal de un chunk depende del caso de uso.
        
        - **Chunks muy grandes (500+ palabras):**
          - ✅ Retienen más contexto.
          - ❌ Pueden incluir información irrelevante.
          - ❌ Consumen más tokens en retrieval.
        
        - **Chunks muy pequeños (50-100 palabras):**
          - ✅ Recuperación más precisa.
          - ❌ Pueden perder contexto importante.
          - ❌ Generan más chunks y mayor costo.
        
        - **Solapamiento (overlap):**
          - Recomendado: 10-20% del tamaño del chunk.
          - Ayuda a no perder información en los límites.
          - Aumenta el número total de chunks (cuidado con el costo).
        
        **En producción**, se recomienda experimentar con varios tamaños
        y evaluar la calidad del retrieval con preguntas reales.
        """)


# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    main()