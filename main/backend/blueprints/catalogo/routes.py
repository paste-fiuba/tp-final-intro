from flask import request, jsonify, send_file
import io
import base64
from . import productos_bp
import unicodedata
from . queries import (
    obtener_todos_los_productos,
    obtener_producto_por_id,
    obtener_categorias,
    obtener_producto_por_categoria,
    crear_producto as crear_producto_db,
    actualizar_producto as actualizar_producto_db,
    eliminar_producto as eliminar_producto_db
)

def normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

@productos_bp.route('/api/productos/categorias', methods=['GET'])
def obtener_categorias_productos():
    categorias = obtener_categorias()
    return jsonify(categorias), 200

@productos_bp.route('/api/productos/categoria/<string:producto_tipo>', methods=['GET'])
def obtener_producto_por_categoria(producto_tipo):
    producto = obtener_producto_por_categoria(producto_tipo)
    if producto:
        return jsonify(producto), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/api/productos', methods=['GET'])
def listar_productos():
    productos = obtener_todos_los_productos()
    return jsonify(productos), 200

@productos_bp.route('/api/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if producto:
        return jsonify(producto), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/api/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()
    nuevo_id = crear_producto_db(datos)
    return jsonify({'mensaje': 'Producto creado', 'id': nuevo_id}), 201

@productos_bp.route('/api/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    exito = actualizar_producto_db(producto_id, data)
    if exito:
        return jsonify({'mensaje': 'Producto actualizado'}), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def eliminar(producto_id):
    exito = eliminar_producto_db(producto_id)
    if exito:
        return jsonify({'mensaje': 'Producto eliminado'}), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/buscar', methods=['GET'])
def buscar_productos():
    consulta = normalizar(request.args.get('q', ''))
    if not consulta:
        return jsonify([])
    productos = obtener_todos_los_productos()
    print("PRODUCTOS:", productos)
    resultados = [
        p for p in productos
        if consulta in normalizar(p.get('nombre', '')) or consulta in normalizar(p.get('descripcion', ''))
    ]
    print("RESULTADOS:", resultados)
    return jsonify(resultados)

@productos_bp.route('/api/productos/<int:producto_id>/imagen', methods=['GET'])
def obtener_imagen(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if producto and producto['imagen']:
        try:
            imagen_binaria = base64.b64decode(producto['imagen'])
            return send_file(
                io.BytesIO(imagen_binaria),
                mimetype='image/jpeg',
                as_attachment=False
            )
        except Exception as e:
            return jsonify({'error': 'Error al decodificar la imagen', 'detalle': str(e)}), 500
    return jsonify({'error': 'Imagen no encontrada'}), 404


