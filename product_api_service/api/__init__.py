from flask import Blueprint, jsonify


service_api = Blueprint("api", __name__, url_prefix="/api")

from product_api_service.api.altaProduct import altaProductBP as _altaProductBP

service_api.register_blueprint(_altaProductBP)

from product_api_service.api.producto_leer import product_read_bp as _product_read_bp

service_api.register_blueprint(_product_read_bp)

from product_api_service.api.api_update import updateProduct_bp as _updateProduct_bp

service_api.register_blueprint(_updateProduct_bp)

from product_api_service.api.blueprint_elim import blueprint_eliminar

service_api.register_blueprint(blueprint_eliminar)

from product_api_service.api.leer_etiqueta import read_tag_bp

service_api.register_blueprint(read_tag_bp)
#Sign up
from product_api_service.api.signup import signup_bp as _signup_bp
service_api.register_blueprint(_signup_bp)
#Login
from product_api_service.api.login import login_bp as _login_bp
service_api.register_blueprint(_login_bp)