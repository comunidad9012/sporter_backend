from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from product_api_service.models import User
from product_api_service.database.session import create_local_session
login_bp=Blueprint("login",__name__,url_prefix="/login")
@login_bp.route("/authenticate", methods=["POST"])
def login():
    try:
        data=request.json
        usuario=data.get('usuario')
        contraseña=data.get('contraseña')
        with create_local_session() as db:
            user=db.query(User).filter_by(User.usuario==usuario).first()
            if user and check_password_hash(user.contraseña,contraseña):
                return jsonify({"mensaje":"Inicio de sesión exitosa"}),200
            else:
                return jsonify({"error":"Credenciales inválidas"}), 401
    except Exception as e:
        return jsonify({"error":"Ocurrió un error interno en el servidor"}),500
            