
import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import time
from datetime import datetime
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


# Importa módulos del proyecto
from src.agent.functions import FUNCTION_REGISTRY
from src.agent.dependency_resolver import DependencyResolver
from src.agent.planner_agent import embedding_model, cosine_similarity

# Importa estilos y templates SEPARADOS
from styles import CSS_STYLES, header_html, success_banner_html, footer_html, SIDEBAR_INFO, SIDEBAR_FOOTER
from templates import log_entry_html, plan_step_html, metric_card_html, documentation_html

# ========== CONFIGURACIÓN INICIAL ==========
st.set_page_config(
    page_title="FunctionFlags Planner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(CSS_STYLES, unsafe_allow_html=True)

# ========== COMPONENTES REUTILIZABLES ==========
@st.cache_resource
def get_resolver():
    """Obtiene instancia singleton del resolver (evita reconexiones)"""
    return DependencyResolver()

def visualize_graph(plan_functions: list, target_function: str):
    """Visualiza el grafo de dependencias usando PyVis"""
    G = nx.DiGraph()
    
    resolver = get_resolver()
    with resolver.driver.session() as session:
        result = session.run("""
            MATCH (f:Function)-[:REQUIRES]->(dep:Function)
            RETURN f.name AS from, dep.name AS to
        """)
        for record in result:
            G.add_edge(record["from"], record["to"])
    
    net = Network(
        height='500px',
        width='100%',
        directed=True,
        bgcolor='#ffffff',
        font_color='#000000'
    )
    net.from_nx(G)
    
    for node in net.nodes:
        if node['id'] == target_function:
            node['color'] = '#ff5252'
            node['size'] = 25
        elif node['id'] in plan_functions:
            node['color'] = '#4caf50'
            node['size'] = 20
        else:
            node['color'] = '#2196f3'
            node['size'] = 15
        node['title'] = f"Función: {node['id']}"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
        net.save_graph(f.name)
        with open(f.name, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        st.components.v1.html(html_content, height=500)

def execute_plan(target_function: str):
    """Ejecuta el plan completo y retorna logs + resultados"""
    resolver = get_resolver()
    logs = []
    results = {}
    
    logs.append(("GRAPH", f"Resolviendo dependencias para '{target_function}'"))
    plan = resolver.get_execution_plan(target_function)
    logs.append(("GRAPH", f"Plan generado con {len(plan)} pasos"))
    
    for i, step in enumerate(plan, 1):
        func_name = step['name']
        logs.append(("EXEC", f"Ejecutando [{i}/{len(plan)}]: {func_name}"))
        
        if func_name in FUNCTION_REGISTRY:
            result = FUNCTION_REGISTRY[func_name]()
            results[func_name] = result
            logs.append(("EXEC", f"✅ {func_name} completado"))
        else:
            logs.append(("ERROR", f"❌ Función '{func_name}' no encontrada"))
    
    logs.append(("RESPONSE", "Generando respuesta al usuario"))
    if "crearPedido" in target_function or "comprar" in target_function.lower():
        response = "✅ ¡Pedido creado exitosamente! Tu pedido #ORD-78901 ha sido confirmado y recibirás un email con los detalles."
    elif "stock" in target_function.lower() or "verificarStock" in target_function:
        response = "✅ El producto está disponible en stock (15 unidades)."
    elif "producto" in target_function.lower():
        response = "✅ Información del producto: Laptop Gamer X1 (SKU: LAP-2026), precio: $1,299.99."
    elif "cliente" in target_function.lower():
        response = "✅ Información del cliente: Juan Pérez (ID: 12345)."
    else:
        response = f"✅ Solicitud procesada exitosamente: {target_function}"
    
    logs.append(("RESPONSE", "✅ Respuesta generada"))
    
    return logs, plan, response, results

# ========== INTERFAZ PRINCIPAL ==========
st.markdown(header_html(), unsafe_allow_html=True)
st.markdown("---")

# Sidebar con información (contenido separado en styles.py)
with st.sidebar:
    
    st.image("https://dist.neo4j.com/wp-content/uploads/2024/03/neo4j-logo-2024.svg", width=150)
    st.markdown("<div class='sidebar-title'>ℹ️ Información</div>", unsafe_allow_html=True)
    st.markdown(SIDEBAR_INFO)
    st.markdown(SIDEBAR_FOOTER)

# Tabs principales
tab1, tab2, tab3 = st.tabs(["💬 Ejecutar Agente", "📊 Visualizar Grafo", "📝 Documentación"])

# ========== TAB 1: EJECUTAR AGENTE ==========
with tab1:
    st.subheader("🗣️ Ingresar solicitud del usuario")
    
    user_query = st.text_input(
        "Escribe tu solicitud:",
        placeholder="Ej: Quiero comprar una laptop gamer",
        key="user_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        execute_btn = st.button("🚀 Ejecutar Plan", type="primary", use_container_width=True)
    
    if execute_btn and user_query:
        with st.spinner("🧠 Procesando solicitud..."):
            st.info(f"Generando embedding para: '{user_query}'")
            query_embedding = embedding_model.encode([user_query])[0]
            
            st.info("Realizando búsqueda semántica...")
            function_descriptions = [
                {"name": "obtenerInfoCliente", "desc": "Obtener información del cliente por ID o nombre"},
                {"name": "obtenerInfoProducto", "desc": "Obtener información del producto por SKU o nombre"},
                {"name": "verificarStock", "desc": "Verificar disponibilidad de stock del producto"},
                {"name": "calcularPrecioTotal", "desc": "Calcular el precio total incluyendo impuestos y descuentos"},
                {"name": "crearPedido", "desc": "Crear un nuevo pedido en el sistema"},
                {"name": "enviarConfirmacion", "desc": "Enviar correo de confirmación al cliente"}
            ]
            desc_embeddings = embedding_model.encode([f["desc"] for f in function_descriptions])
            similarities = cosine_similarity(query_embedding.reshape(1, -1), desc_embeddings)[0]
            best_idx = int(similarities.argmax())
            target_function = function_descriptions[best_idx]["name"]
            confidence = float(similarities[best_idx])
            
            st.success(f"🎯 Función objetivo seleccionada: **{target_function}** (confianza: {confidence:.2%})")
            
            time.sleep(1)
            logs, plan, response, results = execute_plan(target_function)
            
            st.markdown("---")
            st.subheader("✅ Resultados de la ejecución")
            
            st.markdown(success_banner_html(response), unsafe_allow_html=True)
            
            st.subheader("📋 Plan de ejecución (orden topológico)")
            plan_col1, plan_col2 = st.columns(2)
            with plan_col1:
                st.markdown("**Pasos ejecutados:**")
                for i, step in enumerate(plan, 1):
                    st.markdown(plan_step_html(i, step['name'], step['description']), unsafe_allow_html=True)
            
            with plan_col2:
                st.markdown("**Resumen:**")
                st.markdown(metric_card_html("Función objetivo", target_function, "🎯"), unsafe_allow_html=True)
                st.markdown(metric_card_html("Total de pasos", str(len(plan)), "📋"), unsafe_allow_html=True)
                st.markdown(metric_card_html("Confianza", f"{confidence:.2%}", "🧠"), unsafe_allow_html=True)
            
            st.subheader("📜 Logs de ejecución")
            for level, message in logs:
                st.markdown(log_entry_html(level, message), unsafe_allow_html=True)
            
            st.subheader("📦 Resultados de funciones")
            for func_name, result in results.items():
                with st.expander(f"Resultado de `{func_name}`"):
                    st.json(result)

# ========== TAB 2: VISUALIZAR GRAFO ==========
with tab2:
    st.subheader("🕸️ Grafo de dependencias de funciones")
    
    resolver = get_resolver()
    target_func = st.selectbox(
        "Selecciona la función objetivo para visualizar su plan:",
        ["crearPedido", "enviarConfirmacion", "verificarStock", "calcularPrecioTotal", "obtenerInfoCliente", "obtenerInfoProducto"],
        index=0
    )
    
    if st.button("📊 Visualizar grafo", type="secondary"):
        with st.spinner("Cargando grafo desde Neo4j..."):
            plan = resolver.get_execution_plan(target_func)
            plan_functions = [step['name'] for step in plan]
            
            st.info(f"Plan para `{target_func}`: {len(plan)} pasos")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Función objetivo", target_func)
            with col2:
                st.metric("Pasos en plan", len(plan))
            with col3:
                st.metric("Dependencias", len(plan) - 1 if len(plan) > 0 else 0)
            
            st.subheader("Visualización interactiva del grafo")
            visualize_graph(plan_functions, target_func)
            
            st.subheader("📋 Dependencias detalladas")
            with resolver.driver.session() as session:
                result = session.run("""
                    MATCH (f:Function)-[r:REQUIRES]->(dep:Function)
                    RETURN f.name AS funcion, dep.name AS dependencia
                    ORDER BY f.name
                """)
                deps = [{"funcion": r["funcion"], "dependencia": r["dependencia"]} for r in result]
            
            if deps:
                st.dataframe(deps, use_container_width=True)
            else:
                st.warning("No se encontraron dependencias en el grafo")

# ========== TAB 3: DOCUMENTACIÓN ==========
with tab3:
    st.subheader("🎓 Documentación del proyecto")
    st.markdown(documentation_html())

# Footer (separado en styles.py)
st.markdown("---")
st.markdown(footer_html(), unsafe_allow_html=True)