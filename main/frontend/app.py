from flask import Flask, render_template, request, redirect, url_for, flash,  session, jsonify, Response, abort
import requests
import base64
import datetime

from urllib.parse import quote

app = Flask(__name__)
app.secret_key = 'clave'

BACKEND_URL = 'http://localhost:5000'

@app.context_processor
def inject_user():
    return {'perfil_usuario': session.get('user')}

def invocar_categorias():
    try:
        resp = requests.get('http://localhost:5000/catalogo/api/productos/categorias')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de categorías: {e}")
        return []

def invocar_productos():
    try:
        resp = requests.get('http://localhost:5000/catalogo/api/productos')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de productos: {e}")
        return []

def invocar_productos_por_id(product_id):
    try:
        resp = requests.get(f'http://localhost:5000/catalogo/api/productos/{product_id}')
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                return data[0] if data else None
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de productos: {e}")
        return None



def invocar_perfil_usuario():
    user = session.get('user')
    if not user:
        return {}
    try:
        user_id = user['id']
        resp = requests.get(f'http://localhost:5000/usuarios/user/{user_id}',)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de perfil de usuario: {e}")
        return {}


def invocar_pedidos():
    try:
        resp = requests.get('http://localhost:5000/pedidos')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar pedidos {e}")
        return []


def invocar_detalles_pedidos():
    try:
        resp = requests.get('http://localhost:5000/pedidos/detalles')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar pedidos {e}")
        return []
    
def invocar_pedidos_por_id(id):
    try:
        resp = requests.get(f'http://localhost:5000/pedidos/idpedido/{id}')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar pedidos {e}")
        return []

def invocar_pedidos_por_idusuario(idu):
    try:
        resp = requests.get(f'http://localhost:5000/pedidos/idusuario/{idu}')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar pedidos {e}")
        return []

def invocar_carrito():
    try:
        resp = requests.get('http://localhost:5000/cart')
        if resp.status_code == 200:
            return resp.json()
        else:
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el carrito: {e}")
        return {}

def invocar_busqueda_productos(consulta):
    try:
        resp = requests.get(f'http://localhost:5000/catalogo/buscar?q={consulta}')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar productos: {e}")
        return []

def ver_stock():
    try:
        resp = requests.get(f'http://localhost:5000/stock')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al ver stock: {e}")
        return []


def modificar_stock(nstock, producto):
    try:
        resp = requests.get(f'http://localhost:5000/stock/agregar/{nstock}/{producto}')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al modificar stock: {e}")
        return []


def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart

@app.context_processor
def inject_cart_count():
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return dict(cart_count=cart_count)

@app.context_processor
def poner_nombre():
    return dict(BRAND_NAME="Ludoteca central")

@app.context_processor
def poner_mail():
    return dict(MAIL= "ludotecacentral@gmail.com")

@app.context_processor
def poner_mail():
    return dict(NUMERO= "+54 11 60217938")

@app.context_processor
def inject_auth_status():
    return {'logged_in': session.get('logged_in', False),
             'user': session.get('user')
            }

@app.context_processor
def inject_auth_status():
    return dict(
        logged_in=session.get('logged_in', False),
        username=session.get('username')
    )

@app.route('/')
def index():
    productos = invocar_productos()
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    return render_template("index.html", categorias=categorias, productos=productos, perfil_usuario=perfil_usuario)

@app.route('/shop_mixed')
def shop_mixed():
    categoria = request.args.get('categoria', '')
    stock_disponible = request.args.get('stock_disponible')
    productos = invocar_productos()
    if categoria:
        productos = [p for p in productos if p.get('categoria') == categoria]
    if stock_disponible:
        productos = [p for p in productos if int(p.get('stock', 0)) > 0]
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    return render_template(
        "shop_mixed.html",
        productos=productos,
        categorias=categorias,
        categoria=categoria,
        stock_disponible=stock_disponible,
        perfil_usuario=perfil_usuario
    )

@app.route('/shopping-cart')
def shopping_cart():
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    categorias = invocar_categorias()
    cart = session.get('cart', {})
    carrito_detallado = []
    total = 0
    for pid, cantidad in cart.items():
        producto = next((p for p in productos if str(p['id']) == str(pid)), None)
        if producto:
            precio = float(producto['precio'])
            cantidad_int = int(cantidad)
            producto_detalle = producto.copy()
            producto_detalle['cantidad'] = cantidad_int
            producto_detalle['subtotal'] = precio * cantidad_int
            total += producto_detalle['subtotal']
            carrito_detallado.append(producto_detalle)
    return render_template(
        "shopping-cart.html",
        categorias=categorias,
        perfil_usuario=perfil_usuario,
        carrito_detallado=carrito_detallado,
        total=total,productos=productos
    )

@app.route('/cart/add/<int:producto_id>', methods=['POST'])
def add_to_cart(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    cart = get_cart()
    cart[str(producto_id)] = cart.get(str(producto_id), 0) + cantidad
    save_cart(cart)
    flash('Producto agregado al carrito', 'success')
    return redirect(request.referrer or url_for('shop_mixed'))

@app.route('/cart/update/<int:producto_id>', methods=['POST'])
def update_cart(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    cart = get_cart()
    if cantidad > 0:
        cart[str(producto_id)] = cantidad
    else:
        cart.pop(str(producto_id), None)
    save_cart(cart)
    flash('Carrito actualizado', 'success')
    return redirect(url_for('shopping_cart'))

@app.route('/cart/remove/<int:producto_id>', methods=['POST'])
def remove_from_cart(producto_id):
    cart = get_cart()
    cart.pop(str(producto_id), None)
    save_cart(cart)
    flash('Producto eliminado del carrito', 'success')
    return redirect(url_for('shopping_cart'))

@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    save_cart({})
    flash('Carrito vaciado', 'success')
    return redirect(url_for('shopping_cart'))

@app.route('/product-details/<int:product_id>')
def product_details(product_id):
    perfil_usuario = invocar_perfil_usuario()
    categorias = invocar_categorias()
    productos = invocar_productos()
    producto = invocar_productos_por_id(product_id)
    return render_template(
        "product-details.html",
        categorias=categorias,
        perfil_usuario=perfil_usuario,
        product=producto,
        productos=productos
    )

@app.route('/my_account')
def my_account():
    perfil_usuario = invocar_perfil_usuario()
    pedido_usuario = invocar_pedidos_por_idusuario(perfil_usuario.get('id'))
    detalles_pedidos = [invocar_pedidos_por_id(p['id']) for p in pedido_usuario]
    categorias = invocar_categorias()
    productos = invocar_productos()
    return render_template("my_account.html", detalles=detalles_pedidos, pedido=pedido_usuario, categorias=categorias, perfil_usuario=perfil_usuario, productos=productos)


@app.route('/purchase-completed')
def purchase_completed():
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    pedido_id = session.get('ultimo_pedido_id')
    pedido = None
    if pedido_id:
        pedido_data = requests.get(f'http://localhost:5000/pedidos/idpedido/{pedido_id}').json()
        pedido_info = requests.get(f'http://localhost:5000/pedidos/idusuario/{perfil_usuario["id"]}').json()
        pedido = {
            'id': pedido_id,
            'cliente': perfil_usuario.get('username', ''),
            'productos': [],
            'fecha': None,
            'total': 0
        }
        total = 0
        for item in pedido_data:
            prod = next((p for p in productos if p['id'] == item['producto_id']), None)
            if prod:
                cantidad = int(item['cantidad'])
                precio = float(item['precio'])
                pedido['productos'].append({
                    'nombre': prod['nombre'],
                    'cantidad': cantidad,
                    'precio': precio
                })
                total += cantidad * precio
        pedido['total'] = total

        
        for p in pedido_info:
            if str(p['id']) == str(pedido_id):
                fecha_str = p['fecha']
                try:
                    pedido['fecha'] = datetime.datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pedido['fecha'] = None  
                break

    session.pop('ultimo_pedido_id', None)
    return render_template(
        "purchase-completed.html",
        categorias=categorias,
        perfil_usuario=perfil_usuario,
        productos=productos,
        pedido=pedido
    )

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    perfil_usuario = invocar_perfil_usuario()
    cart = session.get('cart', {})
    if not perfil_usuario or not cart:
        flash('Debes iniciar sesión y tener productos en el carrito.', 'error')
        return redirect(url_for('shopping_cart'))

    productos = []
    productos_backend = invocar_productos()
    for pid, cantidad in cart.items():
        producto = next((p for p in productos_backend if str(p['id']) == str(pid)), None)
        if producto:
            productos.append({
                'producto_id': int(pid),
                'cantidad': int(cantidad),
                'precio': float(producto['precio'])
            })

    data = {
        'usuario_id': perfil_usuario['id'],
        'carrito': productos
    }

    resp = requests.post('http://localhost:5000/finalizar-compra', json=data)
    if resp.status_code == 201:
        session['cart'] = {}
        pedido_id = resp.json().get('pedido_id')
        session['ultimo_pedido_id'] = pedido_id  
        return redirect(url_for('purchase_completed'))
    else:
        flash('Error al finalizar la compra.', 'error')
        return redirect(url_for('shopping_cart'))



@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    perfil_usuario = invocar_perfil_usuario()
    categorias = invocar_categorias()
    productos = invocar_productos()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        # Aquí puedes guardar el mensaje, enviarlo por email, etc.
        flash('¡Mensaje enviado correctamente!', 'success')
        return redirect(url_for('contact_us'))
    return render_template("contact-us.html", categorias=categorias, perfil_usuario=perfil_usuario, productos=productos)

@app.route('/administrar-pagina', methods=['GET', 'POST'])
def administrar_pagina():
    verpedidos = invocar_pedidos()
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    stock = ver_stock()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        stock_nuevo = request.form.get('stock_nuevo')
        modificar_stock(stock_nuevo, nombre)
        return redirect(url_for('administrar_pagina'))

    return render_template("administrar-pagina.html", stock=stock, verpedidos=verpedidos, perfil_usuario=perfil_usuario, categorias=categorias, productos=productos)



@app.route('/administrar-pagina/pedidos', methods=['GET','POST'])
def administrar_pedidos():
    verpedidos = invocar_pedidos()
    perfil_usuario = invocar_perfil_usuario()
    if request.method == 'POST':
        id = request.form['pedido_id']
        verpedidosid = invocar_pedidos_por_id(id)
        return render_template('pedidos.html',datos=verpedidos, datosid=verpedidosid, perfil_usuario=perfil_usuario,  id=id, modal=True)
    else:
        return render_template('pedidos.html', datos=verpedidos, perfil_usuario=perfil_usuario, modal=False)

@app.route('/buscar')
def buscar_productos():
    consulta = request.args.get('q', '')
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    productos = []
    if consulta:
        productos = invocar_busqueda_productos(consulta)
    return render_template(
        "resultados_busqueda.html",
        categorias=categorias,
        productos=productos,
        perfil_usuario=perfil_usuario,
        consulta=consulta
    )

@app.route('/eliminar-producto/<int:product_id>', methods=['POST'])
def eliminar_producto(product_id):
    try:
        resp = requests.delete(f'http://localhost:5000/catalogo/api/productos/{product_id}')
        if resp.status_code == 200:
            flash('Producto eliminado exitosamente', 'success')
        else:
            flash('No se pudo eliminar el producto', 'danger')
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar el producto: {e}")
        flash('Error al eliminar el producto', 'danger')
    return redirect(url_for('administrar_pagina'))

@app.route('/agregar-producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        stock = request.form.get('stock')
        imagen = request.files.get('imagen')

        if not nombre or not descripcion or not precio or not categoria:
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('administrar_pagina'))

        imagen_base64 = None
        if imagen and imagen.filename != '':
            imagen_binaria = imagen.read()
            imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
        
        data = {
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'stock': stock,
                'categoria': categoria,
                'imagen': imagen_base64
            }
        
        try:    
            resp = requests.post('http://localhost:5000/catalogo/api/productos', json=data)

            if resp.status_code == 201:
                flash('Producto agregado exitosamente', 'success')
            else:
                flash('No se pudo agregar el producto', 'danger')
        except requests.exceptions.RequestException as e:
            print(f"Error al agregar el producto: {e}")
            flash('Error al agregar el producto', 'danger')
        print(resp.status_code, resp.text)
    return redirect(url_for('shop_mixed'))

@app.route('/productos/<int:producto_id>/imagen')
def obtener_imagen_producto(producto_id):
    try:
        resp = requests.get(f'{BACKEND_URL}/catalogo/api/productos/{producto_id}/imagen')
        if resp.status_code == 200:
            return Response(resp.content, content_type=resp.headers.get('Content-Type', 'image/jpeg'))
        else:
            abort(404)
    except requests.exceptions.RequestException as e:
        print("Error de conexion", e)
        abort(500)
    
@app.route('/ingresar', methods=['POST', 'GET'])
def ingresar():
    desde_registro = request.args.get('desde_registro', False)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            data = {
                'username': username,
                'email': email,
                'password': password
            }

            resp = requests.post('http://localhost:5000/usuarios/auth/login', json=data)

            if resp.status_code == 200:
                user_data = resp.json()
                session['token'] = user_data.get('token')
                session['logged_in'] = True
                session['username'] = user_data.get('username')
                session['user_id'] = user_data.get('user_id')
                session['user'] = {
                    'id': user_data.get('user_id'),
                    'role': user_data.get('role'),
                    'username' : user_data.get('username')
                }
                flash('Inicio de sesión exitoso', 'success')
                return(redirect(url_for('my_account')))
            else:
                error_msg = 'Usuario, email, o contraseña incorrecta. Intente de nuevo.'
                return render_template('index.html', login_error=error_msg, open_login_modal=True)
        except requests.exceptions.RequestException as e:
            error_msg = 'No se pudo conectar al servicio de autenticación'
            return render_template('index.html', login_error=error_msg, open_login_modal=True)
    return render_template('index.html', open_login_modal=bool(desde_registro))

@app.route('/registro', methods=['POST'])
def registro():    
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    data = {
            "username": username,
            "password": password,
            "email": email
        }
    
    resp = requests.post('http://localhost:5000/usuarios/auth/register', json=data)

    if resp.status_code == 201:
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('ingresar', desde_registro=True))
    else:
        error_msg = resp.json().get('message', 'Error al registrar usuario')
        return render_template('index.html', signup_error=error_msg, open_register_modal=True)

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('index'))

@app.route('/usuarios/auth/status')
def auth_status():
    if 'user_id' in session:
        return jsonify({"logged_in" : True, "username" : session.get("username")})
    else:
        return jsonify({"logged_in" : False})
    
@app.route('/agregar-admin', methods=['POST'])
def agregar_admin():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    payload = {
        'username': username,
        'email': email,
        'password': password
    }
    
    token = session.get('token')
    
    if not token:
        flash('Token no encontrado en la sesión', 'error')
        return redirect(url_for('administrar_pagina'))
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.post('http://localhost:5000/usuarios/admin/create_admin', json=payload, headers=headers)
        data = response.json()
        if response.status_code == 201:
            flash(data.get('message', 'Admin creado exitosamente'), 'success')
        else:
            flash(data.get('message', 'Error al crear admin'), 'error')
        return redirect(url_for('administrar_pagina'))
    except requests.exceptions.RequestException:
        flash('Error al conectar con el backend', 'error')
        return redirect(url_for('administrar_pagina'))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    
if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)