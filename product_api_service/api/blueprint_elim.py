#Aquí se encuentra el endpoint de eliminar producto
from flask import jsonify,request, Blueprint
from sqlalchemy.exc import SQLAlchemyError;
from product_api_service.models import Producto
from product_api_service.database.session import create_local_session
from product_api_service.auth.admin import protected_route

blueprint_eliminar = Blueprint("productos", __name__, url_prefix="/producto")

#endpoint "eliminar producto"
@blueprint_eliminar.route('/eliminar/<id_producto>', methods=["POST"])
@protected_route
def eliminar_producto(id_producto):
    
    if id_producto is not None:
        with create_local_session() as db:
            try:
                producto=db.query(Producto).filter(Producto.id == id_producto).first();
                if producto:
                    db.delete(producto);
                    db.commit();
                    return jsonify({'mensaje':'Producto eliminado correctamente'}),200;
                else:
                    return jsonify({'error':'Producto no encontrado'}),404;
            except SQLAlchemyError as e:
                db.rollback();
                print(f"Error en la base de datos: {e}")
                return jsonify({'error': 'Error en la base de datos'}), 500
    else:
        return jsonify({'error':'Se requiere el id del producto'}),400;