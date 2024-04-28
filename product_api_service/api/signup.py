from flask import Blueprint, jsonify, request, make_response
from sqlalchemy.exc import SQLAlchemyError
from product_api_service.database.session import create_local_session
from product_api_service import schemas, models
from product_api_service.models import User
import bcrypt
from product_api_service.auth.admin import protected_route
signup_bp=Blueprint("signup", __name__, url_prefix="/user")
@signup_bp.route("/register", methods=["POST"])
def register_user():
    try:
        nombre=request.form.get("nombre")
        usuario=request.form.get("usuario")
        correo=request.form.get("correo")
        contraseña=request.form.get("contraseña")
        is_admin=int(request.form.get("is_admin", 0))

        hashed_password=bcrypt.hashpw(contraseña.encode("UTF-8"), bcrypt.gensalt())
        with create_local_session() as db:
            existing_user=db.query(User).filter_by(usuario=usuario).first()
            if existing_user:
                respuesta=make_response(jsonify({"error":"El usuario ya existe"}))
                respuesta.set_cookie("error_registro","Usuario ya existe", max_age=3600)
                return respuesta
            new_user=User(nombre=nombre, usuario=usuario, contraseña=hashed_password,is_admin=is_admin, correo=correo)
            db.add(new_user)
            db.commit()
            respuesta=make_response(jsonify({"mensaje":"Usuario creado correctamente"}),200)
            respuesta.set_cookie("ultimo_registro",usuario,max_age=3600)
            return respuesta
    except SQLAlchemyError as e:
        respuesta=make_response(jsonify({"error":"Error en la base de datos"}),500)
        respuesta.set_cookie("error_registro","Error en la base de datos", max_age=3600)
        return respuesta
    except Exception as e:
        return jsonify({"error":"Ocurrio un error interno en el servidor"}), 500
