from flask import Flask, Blueprint
from flask_cors import CORS
import config


from blueprints.crear_pedidos.crear_pedidos import finalizar_compra_bp 
from blueprints.routes.routes import usuarios_bp
from blueprints.catalogo import productos_bp
from blueprints.auth.auth import auth_bp
from blueprints.ver_pedidos.pedidos import pedidos_bp
from blueprints.carrito.carrito import cart_bp
from blueprints.stock.stock import stock_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY

    CORS(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(productos_bp, url_prefix='/catalogo')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(cart_bp)
    app.register_blueprint(stock_bp, url_prefix='/stock')
    app.register_blueprint(finalizar_compra_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)