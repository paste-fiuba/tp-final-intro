from flask import Blueprint, session, request, jsonify

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/add/<int:producto_id>', methods=['POST'])
def add_to_cart(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    cart = session.get('cart', {})
    cart[str(producto_id)] = cart.get(str(producto_id), 0) + cantidad
    session['cart'] = cart
    return jsonify({'ok': True})

@cart_bp.route('/cart/remove/<int:producto_id>', methods=['POST'])
def remove_from_cart(producto_id):
    cart = session.get('cart', {})
    cart.pop(str(producto_id), None)
    session['cart'] = cart
    return jsonify({'ok': True})

@cart_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    return jsonify({'ok': True})

@cart_bp.route('/cart/update/<int:producto_id>', methods=['POST'])
def update_cart(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    cart = session.get('cart', {})
    if cantidad > 0:
        cart[str(producto_id)] = cantidad
    else:
        cart.pop(str(producto_id), None)
    session['cart'] = cart
    return jsonify({'ok': True})

@cart_bp.route('/cart')
def get_cart():
    return jsonify(session.get('cart', {}))