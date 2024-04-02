from flask import Blueprint

service_api = Blueprint("api", __name__, url_prefix="/api")

from product_api_service.api.altaProduct import altaProductBP as _altaProductBP

service_api.register_blueprint(_altaProductBP)

from product_api_service.api.producto_leer import product_read_bp as _product_read_bp

service_api.register_blueprint(_product_read_bp)

from product_api_service.api.api_update import updateProduct_bp as _updateProduct_bp

service_api.register_blueprint(_updateProduct_bp)
