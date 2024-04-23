from flask import Blueprint,jsonify,request
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from product_api_service.database.session import create_local_session
from product_api_service.models import User
updateUser_bp=Blueprint("updateUser", __name__, url_prefix="/user")
@updateUser_bp.route("/actualizar", methods=["POST"])
def update_user():
    try:
        usuario=request.form.get("usuario")
        nombre=request.form.get("nombre")
        correo=request.form.get("correo")
        contraseña=request.form.get("contraseña")
        is_admin=request.form.get("is_admin")
        with create_local_session() as db:
            existing_user=db.query(User).filter_by(usuario=usuario).first()
            if existing_user:
                if nombre:
                    existing_user.nombre=nombre
                elif correo:
                    existing_user.correo=correo
                elif contraseña:
                    hashed_password=bcrypt.hashpw(contraseña.encode("UTF-8"),bcrypt.gensalt())
                    existing_user.contraseña=hashed_password
                elif is_admin:
                    existing_user.is_admin=is_admin
                db.commit()
                return jsonify({"mensaje":"Datos actualizados correctamente"}), 200
            else:
                return jsonify({"error":"Usuario no encontrado"}),404
    except SQLAlchemyError as e:
        return jsonify({"error":"Error en la base de datos"}),500
    except Exception as e:
        return jsonify({"error":"Error interno en el servidor"}),500
                
                
