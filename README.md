# FunctionMatcher Planner

> **Agente inteligente que orquesta funciones basadas en dependencias usando Neo4j + LangGraph**  
> *Desarrollado para la asignatura de Análisis Multivariado - Ing. Remigio Hurtado (PhD)*

## 📌 Resumen

El **FunctionMatcher Planner** es un agente AI que resuelve solicitudes del usuario mediante:
1. **Búsqueda semántica** para identificar la función objetivo usando embeddings de código abierto
2. **Exploración del grafo de conocimiento** (Neo4j) para resolver dependencias transitivas `[:REQUIRES]`
3. **Planificación topológica** para ordenar la ejecución de funciones
4. **Orquestación con LangGraph** para ejecutar el plan paso a paso
5. **Respuesta natural** al usuario con resumen de la ejecución

Este sistema implementa el flujo completo requerido en el examen:  
`Input → Embeddings (LMML) → Function Selection → Exploración grafo → Plan → Ejecución → Output`

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Tipo |
|------------|------------|------|
| **Grafo de conocimiento** | Neo4j 5.18 Community (Docker) | Base de datos de grafos |
| **Orquestación** | LangGraph (`StateGraph`) | Framework de flujos de estado |
| **Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`) | ✅ **Herramienta código abierto** (equivalente a LMML) |
| **Búsqueda semántica** | LangChain + Similitud Coseno (scikit-learn) | Matching vectorial |
| **Funciones simuladas** | Python puro (`print()` únicamente) | Sin APIs externas |
| **Visualización** | Neo4j Browser | Interfaz gráfica del grafo |

## 🔄 Flujo del Agente (Diagrama Mermaid)

```mermaid
flowchart TD
    A[Input: Query del usuario<br>ej: \"Quiero comprar una laptop gamer\"] --> B[Generar embedding<br>Sentence Transformers<br>✅ Herramienta código abierto<br>(equivalente a LMML)]
    B --> C[Búsqueda semántica<br>Similitud coseno<br>LangChain]
    C --> D[Función objetivo<br>ej: crearPedido<br>confianza: 39.82%]
    D --> E[Explorar grafo Neo4j<br>Relaciones [:REQUIRES]<br>APOC subgraphNodes]
    E --> F[Plan topológico ordenado<br>1. obtenerInfoCliente<br>2. obtenerInfoProducto<br>3. verificarStock<br>4. calcularPrecioTotal<br>5. crearPedido]
    F --> G{LangGraph<br>Ejecutar paso?}
    G -->|Sí| H[Ejecutar función<br>simulada con print()<br>ej: \"→ [FUNC] Creando pedido...\")
    H --> I[Registrar resultado<br>+ log con timestamp]
    I --> G
    G -->|No| J[Generar respuesta<br>natural al usuario]
    J --> K[Mostrar logs completos<br>+ resumen de ejecución]
    K --> L[✅ Éxito:<br>\"¡Pedido creado exitosamente!<br>Tu pedido #ORD-78901...\"]

🔍 Explicación del diagrama
Input (1.a): El usuario ingresa una solicitud en lenguaje natural (input()).
Embeddings (1.c): Se genera un vector de 384 dimensiones usando Sentence Transformers (herramienta 100% código abierto que cumple el requisito de "LMML" del examen).
Function Selection (1.d): Búsqueda semántica mediante similitud coseno compara el embedding del query con descripciones de funciones predefinidas.
Exploración del grafo (1.e): Neo4j resuelve todas las dependencias transitivas usando APOC y ordena el plan topológicamente (funciones sin dependencias primero).
Ejecución (1.f): LangGraph orquesta la ejecución paso a paso. Cada función simulada solo ejecuta print() (cumple requisito del examen).
Output (1.g): Respuesta en lenguaje natural + logs completos con timestamps y niveles ([INPUT], [EXEC], [RESPONSE]).

🚀 Ejecución Paso a Paso
Requisitos previos
Docker Desktop instalado
Python 3.11+
Neo4j corriendo en Docker
