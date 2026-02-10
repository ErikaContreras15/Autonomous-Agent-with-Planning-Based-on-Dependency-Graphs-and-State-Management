
CSS_STYLES = """
<style>
    /* Header principal */
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    /* Logs con colores por nivel */
    .log-entry {
        font-family: monospace;
        font-size: 0.9rem;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        margin: 0.35rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .log-input { background-color: #e3f2fd; border-left: 4px solid #1976d2; }
    .log-embedding { background-color: #f3e5f5; border-left: 4px solid #7b1fa2; }
    .log-selection { background-color: #e8f5e8; border-left: 4px solid #388e3c; }
    .log-graph { background-color: #fff3e0; border-left: 4px solid #f57c00; }
    .log-exec { background-color: #e0f7fa; border-left: 4px solid #0097a7; }
    .log-response { background-color: #f8bbd0; border-left: 4px solid #c2185b; }
    .log-error { 
        background-color: #ffcdd2; 
        color: #b71c1c; 
        border-left: 4px solid #d32f2f;
        font-weight: 500;
    }
    
    /* Tarjetas de función */
    .function-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.75rem 0;
        background-color: #fafafa;
        transition: all 0.2s ease;
    }
    .function-card:hover {
        border-color: #1f77b4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    
    /* Banner de éxito */
    .success-banner {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        padding: 1.5rem 0;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
    
    /* Sidebar */
    .sidebar-title {
        color: #1f77b4;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
    }
</style>
"""

# ========== HTML TEMPLATES ==========
def header_html() -> str:
    """Header principal de la aplicación"""
    return """
    <div class="main-header">
        <h1>🚀 FunctionMatcher Planner</h1>
        
    </div>
    """

def success_banner_html(message: str) -> str:
    """Banner de éxito con mensaje personalizado"""
    return f'<div class="success-banner">{message}</div>'

def footer_html() -> str:
    """Footer de la aplicación"""
    return """
    <div class="app-footer">
        🚀 FunctionMatcher Planner | Neo4j 5.18 + LangGraph + Sentence Transformers | © 2026
    </div>
    """

# ========== SIDEBAR CONTENT ==========
SIDEBAR_INFO = """
**Stack Tecnológico:**
- 🧠 Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
- 🕸️ Grafo: Neo4j 5.18 + APOC
- ⚙️ Orquestación: LangGraph
- 📊 Visualización: PyVis + Streamlit

**Funciones disponibles:**
- `obtenerInfoCliente`
- `obtenerInfoProducto`
- `verificarStock`
- `calcularPrecioTotal`
- `crearPedido`
- `enviarConfirmacion`
"""

SIDEBAR_FOOTER = """
---
### 🔗 Acceso rápido
[🔗 Abrir Neo4j Browser](http://localhost:7474)
"""