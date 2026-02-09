import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph

load_dotenv()

print('🔍 Conectando a Neo4j...')
graph = Neo4jGraph(
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USER'),
    password=os.getenv('NEO4J_PASSWORD'),
    database='neo4j'
)

print('\n✅ Prueba 1: Query básica')
result = graph.query("RETURN 'Conexión exitosa' AS message")
print(f'   → {result[0]["message"]}')

print('\n✅ Prueba 2: Plugin APOC')
result = graph.query("RETURN apoc.version() AS version")
print(f'   → APOC v{result[0]["version"]}')

print('\n✅ Prueba 3: Crear nodo Function')
result = graph.query("""
CREATE (f:Function {
    name: 'hello_world',
    description: 'Función de prueba para EXAMEN VAN LOS PLANEERS',
    status: 'active',
    created_at: datetime()
})
RETURN f.name AS function_name
""")
print(f'   → Nodo creado: "{result[0]["function_name"]}"')

print('\n✅ Prueba 4: Leer nodos')
result = graph.query("MATCH (f:Function) RETURN f.name AS name, f.status AS status")
for r in result:
    print(f'   → {r["name"]} [{r["status"]}]')

print('\n🎉 ¡ÉXITO! Neo4j + Python funcionando correctamente.')