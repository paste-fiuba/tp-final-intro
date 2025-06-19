from flask import Blueprint, request, jsonify
from db import get_connection

stock_bp = Blueprint('stock',__name__)

@stock_bp.route('/')
def get_stock():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre,stock FROM Productos")
    stock = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(stock)

@stock_bp.route('/agregar/<int:nstock>/<string:producto>', methods=['GET','PUT'])
def modificar_stock(nstock,producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Productos SET stock=%s WHERE nombre=%s", (nstock, producto))
    conn.commit()
    modificado = cursor.rowcount > 0
    cursor.close()
    conn.close()
    if modificado:
        return jsonify({'message': 'Stock actualizado correctamente'}), 200
    else:
        return jsonify({'message': 'Producto no encontrado o stock no modificado'}), 404

