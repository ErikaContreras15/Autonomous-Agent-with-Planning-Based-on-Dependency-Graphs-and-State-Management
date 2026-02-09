

Agente inteligente que orquesta funciones basadas en dependencias usando Neo4j + LangGraph. Implementa búsqueda semántica con embeddings de código abierto para seleccionar funciones objetivo y resolver planes de ejecución.

## Stack tecnológico
- **Grafo de conocimiento**: Neo4j 5.18 (Docker)
- **Orquestación**: LangGraph (StateGraph)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2) - código abierto
- **Búsqueda semántica**: Similitud coseno con scikit-learn
- **Visualización**: Neo4j Browser

## Flujo del agente

flowchart TD
    A[Función objetivo<br>e.g. crearPedido] --> B[Query Cypher<br>subgraphNodes + REQUIRES]
    B --> C[Orden topológico<br>por profundidad de dependencias]
    C --> D[Plan ordenado:<br>1. obtenerInfoCliente<br>2. obtenerInfoProducto<br>3. verificarStock<br>4. calcularPrecioTotal<br>5. crearPedido]
    D --> E[LangGraph:<br>Ejecución paso a paso]

flowchart TD
    A[Input: Query usuario] --> B[Generar embedding<br>Sentence Transformers]
    B --> C[Búsqueda semántica<br>Similitud coseno]
    C --> D[Función objetivo<br>e.g. crearPedido]
    D --> E[Explorar grafo Neo4j<br>[:REQUIRES]]
    E --> F[Plan ordenado<br>topológicamente]
    F --> G{LangGraph<br>Ejecutar paso?}
    G -->|Sí| H[Ejecutar función<br>simulada]
    H --> I[Registrar resultado]
    I --> G
    G -->|No| J[Generar respuesta<br>natural]
    J --> K[Mostrar logs + resumen]

## Ejecución   
# 1. Levantar Neo4j
docker compose up -d

# 2. Inicializar grafo
python init_graph.py

# 3. Ejecutar agente
python planner_agent.py

## Autores
Erika Contreras
Jorge Pizarro

## Contacto

econtrerasz@est.ups.edu.ec
jpizarro  @est.ups.edu.ec

## Demostracion

1. **Muestra el grafo en Neo4j Browser**:
   - Abre http://localhost:7474
   - Ejecuta: `MATCH path=(f:Function)-[:REQUIRES*]->(dep) RETURN path`
   - Click en pestaña **"Graph"** para visualización visual

2. **Ejecuta el agente en vivo**:
   ```powershell
   python planner_agent.py

Ingresa: Quiero comprar una laptop gamer
Observa los  logs en tiempo real + respuesta final
