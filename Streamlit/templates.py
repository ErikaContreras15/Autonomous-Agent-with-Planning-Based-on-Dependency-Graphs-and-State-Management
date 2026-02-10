

from datetime import datetime

def log_entry_html(level: str, message: str) -> str:
    """Genera HTML para una entrada de log con estilo por nivel"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_class = f"log-{level.lower()}"
    return f"""
    <div class="log-entry {log_class}">
        <strong>[{timestamp}] [{level}]</strong> {message}
    </div>
    """

def plan_step_html(step_number: int, step_name: str, description: str) -> str:
    """Genera HTML para un paso del plan de ejecución"""
    return f"""
    <div class="function-card">
        <strong>Paso {step_number}:</strong> <code>{step_name}</code>
        <div style="color: #666; margin-top: 0.25rem; font-size: 0.9rem;">
            → {description}
        </div>
    </div>
    """

def metric_card_html(title: str, value: str, icon: str = "📊") -> str:
    """Genera HTML para una tarjeta de métrica"""
    return f"""
    <div style="text-align: center; padding: 1rem; background-color: #f9f9f9; border-radius: 8px; margin: 0.5rem 0;">
        <div style="font-size: 1.8rem; margin-bottom: 0.25rem;">{icon}</div>
        <div style="font-weight: 600; font-size: 0.95rem; color: #555;">{title}</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #1f77b4; margin-top: 0.25rem;">{value}</div>
    </div>
    """

def documentation_html() -> str:
    """Contenido HTML para la pestaña de documentación"""
    return """
    ### Arquitectura del sistema

    ```mermaid
    flowchart TD
        A[Input: Query del usuario<br>ej: "Quiero comprar una laptop gamer"] --> B[Generar embedding<br>Sentence Transformers<br>✅ Herramienta código abierto]
        B --> C[Búsqueda semántica<br>Similitud coseno]
        C --> D[Función objetivo<br>ej: crearPedido]
        D --> E[Explorar grafo Neo4j<br>Relaciones [:REQUIRES]]
        E --> F[Plan topológico ordenado<br>1. obtenerInfoCliente<br>2. obtenerInfoProducto<br>3. verificarStock<br>4. calcularPrecioTotal<br>5. crearPedido]
        F --> G{LangGraph<br>Ejecutar paso?}
        G -->|Sí| H[Ejecutar función<br>simulada con print()]
        H --> I[Registrar resultado<br>+ log timestamp]
        I --> G
        G -->|No| J[Generar respuesta<br>natural al usuario]
        J --> K[Mostrar logs + resumen]
    ```

    ### Requisitos del examen cumplidos

    | Requisito | Implementación |
    |-----------|----------------|
    | **1.a Input usuario** | Interfaz Streamlit + campo de texto |
    | **1.b Logs completos** | Panel de logs con timestamps y colores |
    | **1.c Embeddings código abierto** | Sentence Transformers (all-MiniLM-L6-v2) |
    | **1.d Function Selection** | Búsqueda semántica con similitud coseno |
    | **1.e Exploración grafo** | Neo4j + APOC `subgraphNodes` |
    | **1.f Ejecución LangGraph** | Simulación de orquestación paso a paso |
    | **1.g Respuesta natural** | Template + resumen visual en UI |
    | **Visualización grafo** | PyVis + NetworkX integrado en Streamlit |

    ### Ejecución

    ```bash
    # Levantar Neo4j
    docker compose up -d

    # Ejecutar interfaz gráfica
    streamlit run app.py
    ```

    ### Autores
    - **Nombre:** Erika Contreras
    - **Nombre:** Jorge Pizarro
    - **Asignatura:** Análisis Multivariado
    - **Docente:** Ing. Remigio Hurtado (PhD)
    """