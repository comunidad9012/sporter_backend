
from flask import Flask
from sqlalchemy.orm import sessionmaker
from product_api_service.api.blueprint_elim import blueprint_eliminar
from product_api_service.api import service_api
from product_api_service.database.engine import ENGINE  


app = Flask(__name__)


Session = sessionmaker(bind=ENGINE)

app.register_blueprint(service_api)
app.register_blueprint(blueprint_eliminar)

if __name__ == "__main__":
    app.run(debug=True)