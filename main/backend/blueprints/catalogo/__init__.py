from flask import Blueprint

productos_bp = Blueprint('productos', __name__)

from . import routes

