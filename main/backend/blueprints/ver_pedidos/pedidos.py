from flask import Blueprint, request, jsonify, render_template
from db import get_connection
import pymysql

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/')
def get_pedidos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedido")
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No hay pedidos"
    return jsonify(pedidos)


@pedidos_bp.route('/detalles')
def get_detalles_pedidos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PedidoDetalle")
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No hay pedidos"
    return jsonify(pedidos)

@pedidos_bp.route('idpedido/<int:idp>')
def get_idp_pedido(idp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PedidoDetalle WHERE pedido_id = %s", (idp,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No existe ningun pedido con ID de Pedido {idp}"
    return jsonify(pedidos)


@pedidos_bp.route('producto/<int:idproducto>')
def get_producto_pedido(idproducto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PedidoDetalle WHERE  producto_id = %s", (idproducto,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No hay ningun pedido del producto {idproducto}"
    return jsonify(pedidos)

@pedidos_bp.route('idusuario/<int:idusuario>')
def get_idusuario_pedido(idusuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedido WHERE usuario_id = %s", (idusuario,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No hay ningun pedido del usuario {idusuario}"
    return jsonify(pedidos)