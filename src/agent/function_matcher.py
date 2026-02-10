"""
FunctionMatcher Planner - Paso 1: Input del usuario + Logs básicos
EXAMEN VAN LOS PLANEERS - Ing. Remigio Hurtado (PhD)
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

class FunctionMatcherPlanner:
    """Agente planificador que orquesta funciones basadas en dependencias"""
    
    def __init__(self):
        self.logs = []
        self.start_time = None
        print("="*70)
        print("🚀 FUNCTION MATCHER PLANNER - PLANEERS")
        print("="*70)
        print(f"📍 Conexión Neo4j: {os.getenv('NEO4J_URI', 'bolt://localhost:7687')}")
        print()
    
    def log(self, message: str, level: str = "INFO"):
        """Registra logs con timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def get_user_query(self) -> str:
        """1.a. Input: Recibe query del usuario"""
        self.log("🔄 Esperando input del usuario...", "INPUT")
        print()
        query = input("💬 Usuario: ")
        print()
        self.log(f"✅ Query recibido: '{query}'", "INPUT")
        return query
   
    def show_logs(self):
        """Muestra todos los logs al finalizar"""
        print()
        print("="*70)
        print("📋 LOGS COMPLETOS DEL PROCESO")
        print("="*70)
        for log in self.logs:
            print(log)
        print("="*70)
        print(f"⏱️  Tiempo total: {datetime.now() - self.start_time}")
        print("="*70)

def main():
    # Inicializa el planificador
    planner = FunctionMatcherPlanner()
    planner.start_time = datetime.now()
    
    try:
        # 1.a. Input del usuario
        user_query = planner.get_user_query()
        
        # 1.b. Logs del proceso (ejemplo inicial)
        planner.log("🔍 Iniciando análisis semántico...", "PROCESS")
        planner.log("⚠️  Paso 1 completado: Input recibido", "SUCCESS")
        
        # Mensaje temporal (completaremos en pasos siguientes)
        planner.log("⏳ Próximos pasos: embeddings → selección → plan → ejecución", "INFO")
        
        # Muestra logs finales
        planner.show_logs()
        
        print()
        print("✅ PASO 1 COMPLETADO: Input + Logs básicos funcionando")
        print("➡️  Siguiente paso: Funciones simuladas (functions.py)")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Ejecución cancelada por el usuario")
    except Exception as e:
        planner.log(f"❌ Error: {str(e)}", "ERROR")
        planner.show_logs()

if __name__ == "__main__":
    main()

