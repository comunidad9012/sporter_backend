from flask import jsonify, request, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from product_api_service.models import User  
from product_api_service.database.session import create_local_session
from product_api_service.auth.admin import protected_route

blueprint_eliminar_usuario = Blueprint("usuarios", __name__, url_prefix="/user")

# Endpoint para eliminar usuario
@blueprint_eliminar_usuario.route('/eliminar/<id_usuario>', methods=["POST"])
@protected_route
def eliminar_usuario(id_usuario):
    if id_usuario is not None:
        with create_local_session() as db:
            try:
                usuario = db.query(User).filter(User.id == id_usuario).first()
                if usuario:
                    db.delete(usuario)
                    db.commit()
                    return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200
                else:
                    return jsonify({'error': 'Usuario no encontrado'}), 404
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error en la base de datos: {e}")
                return jsonify({'error': 'Error en la base de datos'}), 500
    else:
        return jsonify({'error': 'Se requiere el id del usuario'}), 400
