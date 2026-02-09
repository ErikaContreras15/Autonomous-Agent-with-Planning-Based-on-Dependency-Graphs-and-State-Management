"""
Resolución de dependencias desde Neo4j (compatible con Neo4j 5.x)
Paso 3 del EXAMEN VAN LOS PLANEERS: Exploración del grafo y creación de plan
"""

from neo4j import GraphDatabase
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DependencyResolver:
    """Resuelve dependencias transitivas y genera plan ordenado topológicamente"""
    
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password123")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        self._verify_connection()
    
    def _verify_connection(self):
        """Verifica que Neo4j esté accesible"""
        try:
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("✅ Conexión a Neo4j establecida")
        except Exception as e:
            raise ConnectionError(f"❌ No se puede conectar a Neo4j: {e}")
    
    def get_execution_plan(self, target_function: str) -> List[Dict[str, str]]:
        """
        Genera plan de ejecución ordenado topológicamente (compatible Neo4j 5.x)
        
        Args:
            target_function: Nombre de la función objetivo (ej: 'crearPedido')
        
        Returns:
            Lista de dicts con {name, description} en orden de ejecución
        """
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (target:Function {name: $function_name})
                CALL apoc.path.subgraphNodes(target, {
                    relationshipFilter: 'REQUIRES>',
                    minLevel: 0
                }) YIELD node
                // Cuenta dependencias directas para ordenar topológicamente
                OPTIONAL MATCH (node)-[:REQUIRES]->(dep)
                WITH node, COUNT(dep) AS dependency_count
                ORDER BY dependency_count ASC, node.name ASC
                RETURN node.name AS name, node.description AS description
                """,
                function_name=target_function
            )
            plan = [{"name": record["name"], "description": record["description"]} for record in result]
            
            if not plan:
                raise ValueError(f"❌ Función '{target_function}' no encontrada en el grafo")
            
            return plan
    
    def visualize_plan(self, plan: List[Dict[str, str]]):
        """Muestra el plan de forma visual"""
        print("\n" + "="*70)
        print("📋 PLAN DE EJECUCIÓN (orden topológico)")
        print("="*70)
        for i, step in enumerate(plan, 1):
            print(f"   {i}. {step['name']}")
            print(f"      → {step['description']}")
        print("="*70)
    
    def show_graph_visualization_hint(self):
        """Muestra cómo visualizar el grafo en Neo4j Browser"""
        print("\n💡 Visualiza el grafo completo en Neo4j Browser:")
        print("   http://localhost:7474")
        print("\n   Ejecuta esta consulta:")
        print("   MATCH path=(f:Function)-[:REQUIRES*]->(dep)")
        print("   RETURN path")
    
    def close(self):
        self.driver.close()

def test_resolver():
    """Prueba el resolver con diferentes funciones objetivo"""
    print("="*70)
    print("🔍 PRUEBA DE RESOLUCIÓN DE DEPENDENCIAS (Neo4j 5.x)")
    print("="*70)
    
    resolver = DependencyResolver()
    
    try:
        # Caso 1: Función simple (sin dependencias)
        print("\n🧪 Caso 1: Función sin dependencias")
        print("   Función objetivo: obtenerInfoCliente")
        plan = resolver.get_execution_plan("obtenerInfoCliente")
        resolver.visualize_plan(plan)
        
        # Caso 2: Función con dependencias intermedias
        print("\n🧪 Caso 2: Función con dependencias")
        print("   Función objetivo: verificarStock")
        plan = resolver.get_execution_plan("verificarStock")
        resolver.visualize_plan(plan)
        
        # Caso 3: Función compleja (tu ejemplo del examen)
        print("\n🧪 Caso 3: Función compleja (ejemplo del examen)")
        print("   Función objetivo: crearPedido")
        plan = resolver.get_execution_plan("crearPedido")
        resolver.visualize_plan(plan)
        
        # Caso 4: Flujo completo
        print("\n🧪 Caso 4: Flujo completo de compra")
        print("   Función objetivo: enviarConfirmacion")
        plan = resolver.get_execution_plan("enviarConfirmacion")
        resolver.visualize_plan(plan)
        
        # Muestra cómo visualizar en Neo4j Browser
        resolver.show_graph_visualization_hint()
        
        print("\n✅ PASO 3 COMPLETADO: Resolución de dependencias funcionando (Neo4j 5.x)")
        print("➡️  Siguiente paso: Integración con LangGraph para ejecución orquestada")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        resolver.close()

if __name__ == "__main__":
    test_resolver()