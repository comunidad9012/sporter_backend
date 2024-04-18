from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from product_api_service.database.session import create_local_session
from product_api_service import schemas, models
from product_api_service.models import User
from werkzeug.security import generate_password_hash
signup_bp=Blueprint("signup", __name__, url_prefix="/signup")
@signup_bp.route("/register", methods=["POST"])
def register_user():
    try:
        data = request.json
        nombre = data.get('nombre')
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')
        is_admin = data.get('is_admin', False)

        hashed_password=generate_password_hash(contraseña)
        with create_local_session() as db:
            existing_user=db.query(User).filter_by(usuario=usuario).first()
            if existing_user:
                return jsonify({"error": "El usuario ya existe"}), 400
            new_user=User(nombre=nombre, usuario=usuario, contraseña=hashed_password,is_admin=is_admin)
            db.add(new_user)
            db.commit()
        return jsonify({"Mensaje":"Usuario creado exitosamente"}), 200
    except SQLAlchemyError as e:

        return jsonify({"error": "Error en la base de datos"}), 500
    except Exception as e:
        return jsonify({"error":"Ocurrio un error interno en el servidor"}), 500
