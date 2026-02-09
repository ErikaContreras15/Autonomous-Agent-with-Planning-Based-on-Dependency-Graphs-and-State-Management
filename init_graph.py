
"""
Inicializa el grafo de FUNCIONES con sus dependencias [:REQUIRES]
Modelo requerido por el examen: FunctionMatcher Planner
"""

from neo4j import GraphDatabase
from typing import List, Dict

# Configuración local (segura)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

# Definición de funciones con sus dependencias
FUNCTIONS: List[Dict] = [
    {
        "name": "obtenerInfoCliente",
        "description": "Obtiene información del cliente por ID o nombre",
        "requires": []  # Sin dependencias
    },
    {
        "name": "obtenerInfoProducto",
        "description": "Obtiene información del producto por SKU o nombre",
        "requires": []  # Sin dependencias
    },
    {
        "name": "verificarStock",
        "description": "Verifica disponibilidad de stock del producto",
        "requires": ["obtenerInfoProducto"]  # Depende de obtenerInfoProducto
    },
    {
        "name": "calcularPrecioTotal",
        "description": "Calcula el precio total incluyendo impuestos y descuentos",
        "requires": ["obtenerInfoProducto", "obtenerInfoCliente"]  # Depende de ambas
    },
    {
        "name": "crearPedido",
        "description": "Crea un nuevo pedido en el sistema",
        "requires": ["obtenerInfoCliente", "obtenerInfoProducto", "verificarStock", "calcularPrecioTotal"]
    },
    {
        "name": "enviarConfirmacion",
        "description": "Envía correo de confirmación al cliente",
        "requires": ["crearPedido", "obtenerInfoCliente"]
    }
]

class FunctionGraphInitializer:
    """Inicializa el grafo de funciones en Neo4j"""
    
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def clean_database(self):
        """Limpia la base de datos (solo para desarrollo)"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✅ Base de datos limpiada")
    def create_constraints(self):
        """Crea constraints únicos para evitar duplicados"""
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT function_name_unique IF NOT EXISTS FOR (f:Function) REQUIRE f.name IS UNIQUE")
            session.run("CREATE INDEX function_name_index IF NOT EXISTS FOR (f:Function) ON (f.name)")
            print("✅ Constraints e índices creados")        
    
    def create_functions(self):
        """Crea nodos de tipo Function"""
        with self.driver.session() as session:
            for func in FUNCTIONS:
                session.run(
                    """
                    CREATE (f:Function {
                        name: $name,
                        description: $description,
                        embedding: []  // Placeholder para embeddings (se llenará después)
                    })
                    """,
                    name=func["name"],
                    description=func["description"]
                )
            print(f"✅ {len(FUNCTIONS)} funciones creadas")
    
    def create_dependencies(self):
        """Crea relaciones [:REQUIRES] entre funciones"""
        with self.driver.session() as session:
            for func in FUNCTIONS:
                for dep_name in func["requires"]:
                    session.run(
                        """
                        MATCH (f:Function {name: $func_name})
                        MATCH (d:Function {name: $dep_name})
                        CREATE (f)-[:REQUIRES]->(d)
                        """,
                        func_name=func["name"],
                        dep_name=dep_name
                    )
            print("✅ Relaciones de dependencias creadas")
    
    def verify_graph(self):
        """Verifica la estructura del grafo"""
        with self.driver.session() as session:
            # Contar funciones
            result = session.run("MATCH (f:Function) RETURN count(f) as total")
            total_funcs = result.single()["total"]
            
            # Contar relaciones
            result = session.run("MATCH ()-[:REQUIRES]->() RETURN count(*) as total")
            total_rels = result.single()["total"]
            
            # Mostrar grafo
            print(f"\n📊 Estado del grafo:")
            print(f"   • Funciones: {total_funcs}")
            print(f"   • Dependencias [:REQUIRES]: {total_rels}")
            
            # Mostrar dependencias
            print(f"\n🔗 Dependencias detectadas:")
            result = session.run("""
                MATCH (f:Function)-[:REQUIRES]->(d:Function)
                RETURN f.name as funcion, collect(d.name) as dependencias
                ORDER BY f.name
            """)
            for record in result:
                deps = ", ".join(record["dependencias"])
                print(f"   • {record['funcion']} → requiere: [{deps}]")
    def update_embedding(self, function_name: str, embedding_vector: List[float]):
        """
        Actualiza el embedding de una función específica
        Útil para integrar con LMML después de generar embeddings
        """
        with self.driver.session() as session:
            session.run(
              """
               MATCH (f:Function {name: $name})
               SET f.embedding = $embedding
               RETURN f.name
               """,
            name=function_name,
            embedding=embedding_vector
        )
        print(f"✅ Embedding actualizado para: {function_name}")
   
   
def main():
    print("="*70)
    print("🚀 INICIALIZANDO GRAFO DE FUNCIONES PARA FUNCTION MATCHER")
    print("="*70)
    
    initializer = FunctionGraphInitializer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Paso 1: Limpiar base
        initializer.clean_database()
        
        # Paso 2: Crear funciones
        initializer.create_functions()
        
        # Paso 3: Crear dependencias
        initializer.create_dependencies()
        
        # Paso 4: Verificar
        initializer.verify_graph()
        
        print("\n" + "="*70)
        print("✅ GRAFO DE FUNCIONES INICIALIZADO CORRECTAMENTE")
        print("="*70)
        print("\n💡 Accede al Neo4j Browser: http://localhost:7474")
        print("   Usuario: neo4j | Contraseña: password123")
        print("\n🔍 Ejecuta esta consulta para visualizar el grafo:")
        print("   MATCH path=(f:Function)-[:REQUIRES*]->(dep) RETURN path")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Verifica que Neo4j esté corriendo:")
        print("   docker-compose up -d")
    finally:
        initializer.close()

if __name__ == "__main__":
    main()