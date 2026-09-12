# 🧠 Ingeniería de Soluciones con Inteligencia Artificial

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0-green.svg)](https://python.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Repositorio oficial del curso **Ingeniería de Soluciones con Inteligencia Artificial**, con materiales, ejemplos, notebooks y prácticas organizados en tres módulos de aprendizaje (RA) y sus respectivos submódulos (IL).

> **🎥 Videotutoriales:** [Lista de reproducción completa en YouTube](https://www.youtube.com/playlist?list=PL2gz3vdpKdfVHQqH39oPu4mxLrmAUd2eX)

---

## ⚠️ Nota importante sobre versiones

**LangChain 1.0 fue liberado oficialmente.** Algunos bloques de código de versiones anteriores pueden estar deprecados. Este repositorio se encuentra en **mantenimiento activo**, pero se recomienda revisar la [documentación oficial de LangChain](https://python.langchain.com/) para asegurar el uso de las APIs más recientes (`langchain_core`, `langchain_openai`, `langchain_google_genai`, etc.).

**Además**, GitHub Models fue retirado el **30 de julio de 2026**. Todos los ejemplos han sido migrados a **OpenRouter** (chat) y **Google AI Studio** (embeddings), manteniendo una arquitectura híbrida y gratuita.

---

## 📑 Tabla de Contenidos

- [Descripción general](#-descripción-general)
- [Requisitos previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración de variables de entorno](#-configuración-de-variables-de-entorno)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Cómo usar este repositorio](#-cómo-usar-este-repositorio)
- [Proveedores de IA soportados](#-proveedores-de-ia-soportados)
- [Buenas prácticas de seguridad](#-buenas-prácticas-de-seguridad)
- [Evaluaciones y entregables](#-evaluaciones-y-entregables)
- [Recursos adicionales](#-recursos-adicionales)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## 📚 Descripción general

Este curso cubre desde los fundamentos de la IA generativa y el prompt engineering hasta el desarrollo de agentes inteligentes y las mejores prácticas para llevar soluciones a producción (observabilidad, seguridad, ética y escalabilidad).

| Aspecto | Detalle |
| :--- | :--- |
| **Nivel** | Intermedio |
| **Modalidad** | Práctica y conceptual |
| **Duración** | 3 módulos (RA) con 4 submódulos (IL) cada uno |
| **Requisitos** | Python básico, interés en IA |
| **Lenguaje** | Python 3.10+ |
| **Framework principal** | LangChain 1.0 |

### Objetivos de aprendizaje

Al finalizar el curso, el estudiante será capaz de:

1. **Comprender** los fundamentos de la IA generativa y las APIs de LLMs.
2. **Aplicar** técnicas de prompting (zero-shot, few-shot, CoT, avanzadas).
3. **Construir** sistemas RAG (Retrieval-Augmented Generation) completos.
4. **Evaluar** la calidad de sistemas RAG con métricas objetivas.
5. **Desarrollar** agentes inteligentes con memoria y herramientas.
6. **Documentar** arquitecturas técnicas y soluciones de IA.
7. **Llevar a producción** soluciones observables, seguras y escalables.

---

## 🔧 Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10 o superior** ([descarga](https://www.python.org/downloads/))
- **Git** ([descarga](https://git-scm.com/downloads))
- **Jupyter Notebook** o **JupyterLab** (opcional, para notebooks `.ipynb`)
- **Una cuenta en OpenRouter** ([registro gratuito](https://openrouter.ai/keys))
- **Una cuenta en Google AI Studio** ([registro gratuito](https://ai.google.dev))

### Conocimientos recomendados

- Programación básica en Python
- Uso de terminal / línea de comandos
- Conceptos básicos de APIs REST
- Manejo de entornos virtuales (`venv`, `conda` o `pyenv`)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/iam-docente/ingenieria-de-soluciones-con-IA.git
cd ingenieria-de-soluciones-con-IA
```

### 2. Crear un entorno virtual (recomendado)

```bash
# Con venv (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# Con venv (Windows PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# Con conda
conda create -n ai-course python=3.11
conda activate ai-course
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`, puedes instalar las dependencias principales manualmente:

```bash
pip install langchain langchain-openai langchain-google-genai \
            langchain-community langchain-text-splitters \
            openai streamlit plotly scikit-learn \
            pandas numpy python-dotenv jupyter
```

### 4. Verificar la instalación

```bash
python -c "import langchain; print('LangChain:', langchain.__version__)"
python -c "import openai; print('OpenAI:', openai.__version__)"
```

---

## 🔐 Configuración de variables de entorno

Crea un archivo llamado **`.env`** en la raíz del repositorio (nunca lo subas a Git, ya está incluido en `.gitignore`):

```env
# ============================================
# Claves de proveedores de IA (gratuitas)
# ============================================

# OpenRouter - para chat (https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-tu-clave-aqui

# Google AI Studio - para embeddings (https://ai.google.dev)
GEMINI_API_KEY=AIzaSy-tu-clave-aqui

# ============================================
# Claves opcionales
# ============================================

# LangSmith - para trazabilidad (https://smith.langchain.com)
LANGCHAIN_API_KEY=lsv2_tu-clave-aqui
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=AI-Course

# ============================================
# Configuración regional (opcional)
# ============================================
TZ=America/Santiago
```

### Cómo obtener cada clave

| Variable | Proveedor | Enlace | Capa gratuita |
| :--- | :--- | :--- | :--- |
| `OPENROUTER_API_KEY` | OpenRouter | [openrouter.ai/keys](https://openrouter.ai/keys) | ✅ 50 req/día |
| `GEMINI_API_KEY` | Google AI Studio | [ai.google.dev](https://ai.google.dev) | ✅ 1.500 req/día |
| `LANGCHAIN_API_KEY` | LangSmith | [smith.langchain.com](https://smith.langchain.com) | ✅ 5.000 trazas/mes |

---

## 🏗️ Estructura del proyecto

```
.
├── RA1/                          # Fundamentos de IA Generativa y Prompt Engineering
│   ├── IL1.1/                    # Introducción a LLMs y APIs
│   │   ├── 1-github_model_api.ipynb       # (migrado a OpenRouter)
│   │   ├── 2-langchain_model_api.ipynb
│   │   ├── 3-langchain_streaming.ipynb
│   │   └── 4-langchain_memory.ipynb
│   ├── IL1.2/                    # Técnicas de prompting
│   │   ├── 1-zero-shot-prompting.ipynb
│   │   ├── 2-few-shot-prompting.ipynb
│   │   ├── 3-chain-of-thought.ipynb
│   │   └── 4-advanced-techniques.ipynb
│   ├── IL1.3/                    # Infraestructura RAG
│   │   ├── 1-basic-rag.ipynb
│   │   ├── 2-text-chunking.py             # App Streamlit
│   │   ├── 3-embeddings-simple-rag.ipynb
│   │   └── 4-vector-rag.ipynb
│   └── IL1.4/                    # Evaluación y optimización
│       ├── 1-evaluation-rag.py            # App Streamlit
│       └── 2-langsmith-evaluation.ipynb
│
├── RA2/                          # Desarrollo de Agentes Inteligentes
│   ├── IL2.1/                    # Arquitectura y frameworks
│   ├── IL2.2/                    # Memoria y herramientas externas
│   ├── IL2.3/                    # Planificación y orquestación
│   └── IL2.4/                    # Documentación técnica
│
├── RA3/                          # Observabilidad, Seguridad y Ética
│   ├── IL3.1/                    # Observabilidad y métricas
│   ├── IL3.2/                    # Trazabilidad y logs
│   ├── IL3.3/                    # Seguridad y ética
│   └── IL3.4/                    # Escalabilidad y sostenibilidad
│
├── .env                          # Variables de entorno (NO subir a Git)
├── .env.example                  # Plantilla de variables (sí subir)
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias del proyecto
├── README.md                     # Este archivo
└── LICENSE                       # Licencia del proyecto
```

---

## 🚦 Cómo usar este repositorio

1. **Lee los `README.md`** de cada carpeta RA/IL para entender el objetivo de cada módulo.
2. **Configura el archivo `.env`** con tus claves (ver sección anterior).
3. **Ejecuta los notebooks** con Jupyter:
   ```bash
   jupyter notebook
   ```
4. **Ejecuta las apps Streamlit** con:
   ```bash
   python -m streamlit run RA1/IL1.4/1-evaluation-rag.py
   ```
5. **Sigue la secuencia pedagógica**: los notebooks están numerados y diseñados para ejecutarse en orden.
6. **Consulta los archivos `.md`** para teoría, mejores prácticas y requisitos de cada entrega.

---

## 🤖 Proveedores de IA soportados

Este curso utiliza una **arquitectura híbrida** para maximizar el uso de capas gratuitas:

| Componente | Proveedor | Modelo por defecto | Capa gratuita |
| :--- | :--- | :--- | :--- |
| **Chat / Generación** | OpenRouter | `minimax/minimax-m3:free` | 50 req/día |
| **Embeddings** | Google AI Studio | `models/gemini-embedding-001` | 1.500 req/día |
| **Trazabilidad** | LangSmith | — | 5.000 trazas/mes |

### ⚠️ Consideraciones importantes

- **OpenRouter NO soporta embeddings.** Para vectorizar texto, usa Google AI Studio, Hugging Face o `sentence-transformers` local.
- **Los modelos gratuitos cambian frecuentemente.** Si un modelo deja de funcionar, verifica en [openrouter.ai/chat](https://openrouter.ai/chat) cuáles están activos.
- **Usa `langchain_core`** en lugar de `langchain` para las importaciones de utilidades (prompts, runnables, messages).
- **Evita `RetrievalQA` y `load_evaluator("qa")`**, deprecados desde LangChain 0.3. Usa `RunnableSequence` y evaluadores personalizados.

---

## 🔐 Buenas prácticas de seguridad

Este repositorio sigue las siguientes reglas de seguridad:

1. **Nunca subas archivos `.env`** a Git. Ya están en `.gitignore`.
2. **Rota tus claves API** si sospechas que han sido expuestas.
3. **Usa `getpass`** para ingreso interactivo de claves en notebooks compartidos.
4. **No imprimas claves completas** en la salida de celdas (solo los primeros 10 caracteres).
5. **Valida las claves al inicio del notebook** para fallar rápido con mensajes claros.
6. **Usa entornos virtuales** para aislar las dependencias del proyecto.

### Si accidentalmente subes una clave:

1. **Revoca la clave inmediatamente** en el panel del proveedor (OpenRouter, Google, etc.).
2. **Genera una nueva clave** y actualiza tu `.env`.
3. **Limpia el historial de Git** si es necesario (`git filter-repo` o BFG Repo-Cleaner).
4. **Considera la clave comprometida** aunque la hayas borrado después.

---

## 📑 Evaluaciones y entregables

| Tipo | Peso | Descripción |
| :--- | :--- | :--- |
| **Quizzes teóricos** | 20% | Uno por cada módulo (RA1, RA2, RA3) |
| **Proyectos prácticos** | 40% | Uno por submódulo (IL) |
| **Proyecto final transversal** | 40% | Aplicación de IA funcional y documentada |

---

## 📖 Recursos adicionales

### Documentación oficial
- [LangChain Docs](https://python.langchain.com/)
- [LangChain 1.0 Migration Guide](https://python.langchain.com/docs/versions/migrating)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [Google AI Studio Docs](https://ai.google.dev/gemini-api/docs)
- [CrewAI Docs](https://docs.crewai.com/)
- [Streamlit Docs](https://docs.streamlit.io/)

### Arquitectura y buenas prácticas
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [The Twelve-Factor App](https://12factor.net/)
- [RAG Best Practices](https://python.langchain.com/docs/use_cases/question_answering/)

### Papers y artículos
- [Retrieval-Augmented Generation (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)
- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903)
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un error, tienes una mejora o quieres añadir un ejemplo:

1. **Abre un Issue** describiendo el problema o la sugerencia.
2. **Haz un Fork** del repositorio.
3. **Crea una rama** con un nombre descriptivo:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
4. **Realiza tus cambios** siguiendo el estilo del proyecto.
5. **Haz commit** con mensajes claros:
   ```bash
   git commit -m "feat: agregar ejemplo de RAG con streaming"
   ```
6. **Push a tu fork** y abre un **Pull Request**.

### Convenciones de commits

Este proyecto sigue la especificación [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `refactor:` refactorización sin cambio funcional
- `chore:` tareas de mantenimiento
- `test:` añadir o modificar tests

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2026 [Tu Nombre / Institución]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📬 Contacto

- **Autor:** Cristián R. Araya
- **Email:** caraya.salazar@gmail.com | cr.arayas@profesor.duoc.cl
- **Institución:** DUOC UC
- **Issues:** [github.com/tu-usuario/tu-repo/issues](https://github.com/tu-usuario/tu-repo/issues)

---

## 🙏 Agradecimientos

- A la comunidad de **LangChain** por el framework y la documentación.
- A **OpenRouter** y **Google AI Studio** por las capas gratuitas.
- A todos los estudiantes del curso por sus preguntas y retroalimentación.

---

## 📊 Estado del proyecto

![Status](https://img.shields.io/badge/status-activo-brightgreen)
![Maintenance](https://img.shields.io/badge/maintenance-sí-blue)

**Última actualización:** Septiembre 2026

---

<p align="center">
  <strong>¡Explora, experimenta y aprende a construir soluciones de IA listas para producción! 🚀</strong>
</p>
