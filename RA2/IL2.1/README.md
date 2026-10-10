# IL2.1: Arquitectura y Frameworks de Agentes

## 📋 Descripción General

En este módulo exploramos los fundamentos de la arquitectura de agentes inteligentes basados en LLM, progresando desde implementaciones básicas hasta frameworks avanzados como LangChain y CrewAI. Incluye configuraciones específicas para integración con GitHub Models API y soluciones a problemas comunes de compatibilidad.

## 🎯 Objetivos de Aprendizaje

- Comprender qué es un agente inteligente y sus componentes fundamentales (cerebro, memoria, herramientas, planificación)
- Dominar el ciclo de razonamiento ReAct (Reason + Act) y el Function Calling nativo de OpenAI
- Implementar agentes desde cero y usando frameworks LangChain y CrewAI
- Configurar correctamente frameworks con GitHub Models API
- Diseñar equipos de agentes colaborativos para tareas complejas
- Entender criterios de selección entre diferentes frameworks

## 📚 Contenido del Módulo

### 1. Fundamentos de Agentes Inteligentes
- **[1-agent-fundamentals.ipynb](1-agent-fundamentals.ipynb)** - Implementación de agente básico desde cero
  - Conceptos fundamentales: cerebro, memoria, herramientas
  - Ciclo ReAct (Reason + Act) manual
  - Parsing de texto y gestión de estado
  - Limitaciones y motivación para frameworks

### 2. Function Calling Nativo
- **[2-agent-function-calling.ipynb](2-agent-function-calling.ipynb)** - Mecanismo estructurado de OpenAI
  - Definición de herramientas con JSON Schema
  - Ventajas sobre parsing manual: confiabilidad, seguridad
  - Flujo de llamadas estructuradas
  - Integración con Wikipedia API

### 3. Framework LangChain
- **[3-langchain-agent.ipynb](3-langchain-agent.ipynb)** - Agentes individuales potentes
  - Abstracciones de alto nivel: AgentExecutor, Tool
  - Configuración simplificada con decoradores
  - Gestión automática de historial y errores
  - Tipos de agentes: Zero-shot, Conversational, Structured

### 4. Framework CrewAI
- **[4-crewai-agent.ipynb](4-crewai-agent.ipynb)** - Equipos colaborativos de agentes
  - Conceptos: Agent, Task, Crew, Process
  - Especialización por roles: Investigador, Escritor
  - Coordinación secuencial con dependencias
  - **🔧 CONFIGURACIÓN CRÍTICA**: Mapeo de variables para GitHub Models API

## 🔧 Configuraciones Técnicas Importantes

### Variables de Entorno Requeridas
```bash
export OPENAI_BASE_URL="https://models.inference.ai.azure.com"
export GITHUB_TOKEN="tu_token_de_github"
```

### Configuración para LangChain
```python
# LangChain funciona directamente con las variables estándar
llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

### Configuración para CrewAI (CRÍTICA)
```python
# CrewAI requiere mapeo específico de variables
import os
os.environ["OPENAI_API_BASE"] = os.environ.get("OPENAI_BASE_URL", "")
os.environ["OPENAI_API_KEY"] = os.environ.get("GITHUB_TOKEN", "")
```

## ⚠️ Problemas Comunes y Soluciones

### 1. Error de Autenticación en CrewAI
**Síntoma**: `AuthenticationError: Incorrect API key provided`
**Causa**: CrewAI utiliza LangChain internamente, espera variables específicas
**Solución**: Mapear `GITHUB_TOKEN` → `OPENAI_API_KEY` y `OPENAI_BASE_URL` → `OPENAI_API_BASE`

### 2. Error de Herramientas en CrewAI
**Síntoma**: `'Tool' object is not callable`
**Causa**: Mezclar decorador `@tool` de LangChain con CrewAI
**Solución**: Usar `BaseTool` de `crewai_tools`

### 3. Error de Parámetro Verbose
**Síntoma**: `ValidationError: Input should be a valid boolean`
**Causa**: Usar `verbose=2` en lugar de boolean
**Solución**: Usar `verbose=True` en Crew

## 🏗️ Patrones Arquitectónicos Implementados

| **Patrón** | **Notebook** | **Características** |
|------------|--------------|-------------------|
| **Monolítico** | 1-agent-fundamentals | Toda la lógica en una función, parsing manual |
| **Estructurado** | 2-agent-function-calling | JSON Schema, llamadas nativas |
| **Modular** | 3-langchain-agent | Separación de componentes, abstracciones |
| **Colaborativo** | 4-crewai-agent | Múltiples agentes especializados |

## 🔄 Comparación de Frameworks

| **Criterio** | **LangChain** | **CrewAI** |
|-------------|--------------|------------|
| **Especialización** | Agentes individuales complejos | Equipos colaborativos |
| **Complejidad** | Simple a moderada | Compleja, multi-paso |
| **Flexibilidad** | Muy alta, experimental | Estructurada, workflow-oriented |
| **Configuración** | Directa con variables estándar | Requiere mapeo específico |
| **Curva de aprendizaje** | Moderada | Baja para equipos |
| **Casos de uso** | Experimentación, prototipado | Workflows de producción |

## 📝 Actividades Prácticas

### Ejercicios Implementados
1. **Agente Básico**: Implementación desde cero con ReAct manual
2. **Function Calling**: Agente con Wikipedia usando JSON Schema
3. **LangChain Individual**: Agente con herramientas integradas
4. **Equipo CrewAI**: Investigador + Escritor colaborativo

### Casos de Uso Desarrollados
- **Investigación Automatizada**: Búsqueda y síntesis de información
- **Generación de Contenido**: Biografías basadas en investigación
- **Workflows Multi-agente**: Coordinación secuencial especializada

## 🎓 Preparación para IL2.2

### Conceptos Avanzados Siguientes
- **Memory Systems**: Sistemas de memoria persistente y contextual
- **Model Context Protocol (MCP)**: Estándar para integración de herramientas
- **Advanced Planning**: Algoritmos de planificación y re-planificación
- **Tool Integration**: APIs complejas y bases de datos

### Base Establecida
- ✅ Fundamentos sólidos de agentes inteligentes
- ✅ Experiencia con frameworks principales
- ✅ Configuraciones de producción para GitHub Models API
- ✅ Patrones de colaboración entre agentes
- ✅ Debugging y troubleshooting de sistemas complejos

## 🔗 Recursos Adicionales

### Documentación Oficial
- [LangChain Agents Documentation](https://python.langchain.com/docs/use_cases/autonomous_agents/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

### Herramientas de Desarrollo
- [LangSmith](https://smith.langchain.com/) - Observabilidad para agentes LangChain
- [GitHub Models](https://github.com/marketplace/models) - Acceso a modelos de IA

### Troubleshooting y Soporte
- [GitHub Issues - CrewAI](https://github.com/joaomdmoura/crewAI/issues)
- [LangChain Community](https://github.com/langchain-ai/langchain/discussions)

## 💡 Mejores Prácticas Identificadas

1. **Configuración de Entorno**: Verificar variables antes de ejecutar agentes
2. **Manejo de Errores**: Implementar validación robusta en herramientas
3. **Documentación de Herramientas**: Descripciones claras para mejor selección
4. **Debugging**: Usar modo verbose para observar flujo de decisiones
5. **Versionado**: Mantener compatibilidad entre versiones de frameworks
6. **Testing**: Probar configuraciones en entornos similares a producción