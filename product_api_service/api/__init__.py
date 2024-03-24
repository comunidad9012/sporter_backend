from flask import Blueprint

service_api = Blueprint("api", __name__, url_prefix="/api")

from product_api_service.api.ejemplo import example_crud_bp as _example_crud_bp

service_api.register_blueprint(_example_crud_bp)
