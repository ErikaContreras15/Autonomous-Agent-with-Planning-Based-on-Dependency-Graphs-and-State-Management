"""
PASO 2
Funciones simuladas para el EXAMEN VAN LOS PLANEERS
Cada función solo imprime su ejecución (simulación)
"""

def obtenerInfoCliente():
    """Obtiene información del cliente por ID o nombre"""
    print("   → [FUNC] Obteniendo información del cliente...")
    print("   → [FUNC] Cliente: Juan Pérez (ID: 12345)")
    return {"cliente_id": 12345, "nombre": "Juan Pérez", "email": "juan@example.com"}

def obtenerInfoProducto():
    """Obtiene información del producto por SKU o nombre"""
    print("   → [FUNC] Obteniendo información del producto...")
    print("   → [FUNC] Producto: Laptop Gamer X1 (SKU: LAP-2026)")
    return {"sku": "LAP-2026", "nombre": "Laptop Gamer X1", "precio": 1299.99}

def verificarStock():
    """Verifica disponibilidad de stock del producto"""
    print("   → [FUNC] Verificando disponibilidad de stock...")
    print("   → [FUNC] Stock disponible: 15 unidades")
    return {"disponible": True, "cantidad": 15}

def calcularPrecioTotal():
    """Calcula el precio total incluyendo impuestos y descuentos"""
    print("   → [FUNC] Calculando precio total...")
    print("   → [FUNC] Subtotal: $1,299.99 | Impuestos: $156.00 | Total: $1,455.99")
    return {"subtotal": 1299.99, "impuestos": 156.00, "total": 1455.99}

def crearPedido():
    """Crea un nuevo pedido en el sistema"""
    print("   → [FUNC] Creando nuevo pedido en el sistema...")
    print("   → [FUNC] Pedido #ORD-78901 creado exitosamente")
    return {"pedido_id": "ORD-78901", "estado": "confirmado", "total": 1455.99}

def enviarConfirmacion():
    """Envía correo de confirmación al cliente"""
    print("   → [FUNC] Enviando correo de confirmación...")
    print("   → [FUNC] Email enviado a juan@example.com con detalles del pedido")
    return {"enviado": True, "destinatario": "juan@example.com"}

# Mapeo de nombres de funciones (strings) a implementaciones
FUNCTION_REGISTRY = {
    "obtenerInfoCliente": obtenerInfoCliente,
    "obtenerInfoProducto": obtenerInfoProducto,
    "verificarStock": verificarStock,
    "calcularPrecioTotal": calcularPrecioTotal,
    "crearPedido": crearPedido,
    "enviarConfirmacion": enviarConfirmacion
}

if __name__ == "__main__":
    print("🧪 PRUEBA DE FUNCIONES SIMULADAS\n")
    for nombre, func in FUNCTION_REGISTRY.items():
        print(f"Ejecutando: {nombre}")
        resultado = func()
        print(f"   → Resultado: {resultado}\n")