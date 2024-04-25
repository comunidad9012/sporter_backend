from flask import Flask, request
from flask_cors import CORS


def create_app():
    new_app = Flask(__name__)
    cors_app = CORS(new_app)
    new_app.config['CORS_HEADERS'] = 'Content-Type' 
    new_app.config['Access-Control-Allow-Credentials'] = "true" 

    @new_app.route("/")
    def home_page():
        request_query = request.args
        if request_query:

            response = ["Counter Server Working (Not that counter...)", "<ul>"]

            for arg, value in request_query.items():
                response.append(f"<li>{arg}: {value}</li>")

            response.append("</ul>")

            response = "".join(response)

            return response

        return "Product API Server Working (Not that counter...)"

    @new_app.after_request
    def allow_cors(resp):
        resp.headers['Access-Control-Allow-Credentials'] = "true" 
        return resp

    from product_api_service.database import cli_setup

    new_app.cli.add_command(cli_setup.db_setup)

    from product_api_service.api import service_api

    new_app.register_blueprint(service_api)

    return new_app
