from flask import Blueprint,jsonify,request
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from product_api_service.database.session import create_local_session
from product_api_service.models import User
from product_api_service.auth.admin import protected_route
updateUser_bp=Blueprint("updateUser", __name__, url_prefix="/user")
@updateUser_bp.route("/actualizar", methods=["POST"])
@protected_route
def update_user():
    try:
        usuario=request.form.get("usuario", False)
        nombre=request.form.get("nombre", False)
        correo=request.form.get("correo", False)
        contraseña=request.form.get("contraseña", False)
        is_admin=int(request.form.get("is_admin",0))
        with create_local_session() as db:
            existing_user=db.query(User).filter_by(usuario=usuario).first()
            if existing_user:
                if nombre and nombre != existing_user.nombre:
                    existing_user.nombre=nombre
                    
                if correo and correo != existing_user.correo:
                    existing_user.correo=correo
                    
                if contraseña and not bcrypt.checkpw(contraseña.encode("UTF-8"), existing_user.contraseña.encode("UTF-8")):
                    hashed_password=bcrypt.hashpw(contraseña.encode("UTF-8"),bcrypt.gensalt())
                    existing_user.contraseña=hashed_password
                    
                if is_admin != existing_user.is_admin:
                    existing_user.is_admin=is_admin
                
                db.add(existing_user)
                db.commit()
                return jsonify({"mensaje":"Datos actualizados correctamente"}), 200
            else:
                return jsonify({"error":"Usuario no encontrado"}),404
    except SQLAlchemyError as e:
        return jsonify({"error":"Error en la base de datos"}),500
    except Exception as e:
        return jsonify({"error":"Error interno en el servidor"}),500
                
                
