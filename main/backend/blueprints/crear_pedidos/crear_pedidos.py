from flask import Blueprint, request, jsonify, session
from db import get_connection

finalizar_compra_bp = Blueprint('finalizar_compra', __name__)

@finalizar_compra_bp.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    carrito = data.get('carrito')  

    if not usuario_id or not carrito:
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_connection()
    cursor = conn.cursor()

  
    cursor.execute("INSERT INTO Pedido (usuario_id) VALUES (%s)", (usuario_id,))
    pedido_id = cursor.lastrowid

   
    for item in carrito:
        producto_id = item['producto_id']
        cantidad = item['cantidad']
        precio = item['precio']

        cursor.execute(
            "INSERT INTO PedidoDetalle (pedido_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)",
            (pedido_id, producto_id, cantidad, precio)
        )
        
        cursor.execute(
            "UPDATE Productos SET stock = stock - %s WHERE id = %s AND stock >= %s",
            (cantidad, producto_id, cantidad)
        )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Compra finalizada', 'pedido_id': pedido_id}), 201