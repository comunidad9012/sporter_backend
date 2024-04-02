from flask import Blueprint

service_api = Blueprint("api", __name__, url_prefix="/api")

from product_api_service.api.altaProduct import altaProductBP as _altaProductBP

service_api.register_blueprint(_altaProductBP)
