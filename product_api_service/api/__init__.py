from flask import Blueprint, jsonify


service_api = Blueprint("api", __name__, url_prefix="/api")

from product_api_service.api.blueprint_elim import blueprint_eliminar
service_api.register_blueprint(blueprint_eliminar)