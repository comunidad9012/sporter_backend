from typing import Dict
from flask import Blueprint, jsonify, request
from sqlalchemy import select, update, delete, or_
from sqlalchemy.exc import IntegrityError
from product_api_service.database.session import create_local_session
from product_api_service import schemas, models
from pydantic import ValidationError

updateProduct_bp = Blueprint(
    "updateProduct",
    __name__,
    url_prefix="/update",
)

@updateProduct_bp.post("/updateProduct")
def update_existingProduct():
    UpdateRequest: Dict = request.form.to_dict()

    try:
        RequestValidada = dict(schemas.Producto(**UpdateRequest))
    except ValidationError as ve:
        errors_list = []
        for error in ve.errors():
            error_object = {
                "field": error["loc"][0],
                "invalid_input": error["input"],
                "error_info": error["msg"],
            }
            errors_list.append(error_object)

        return {"msj": "Informacion de ejemplo invalida", "errors": errors_list}, 400

    try:
        with create_local_session() as db_session:

            # Con este se actualiza

            update_example_query: update = (
                update(models.Ejemplo)
                .where(models.Ejemplo.id == RequestValidada["id"])
                .values(
                    nombre=RequestValidada["nombre"],
                    descripcion=RequestValidada["descripcion"],
                    imagen=RequestValidada["imagen"],
                    precio=RequestValidada["precio"],
                    cantidad=RequestValidada["cantidad"],
                )
            )
            db_session.execute(update_example_query)
            db_session.commit()

            
            # Eliminar el registro
            delete_example_query = (
                delete(models.Ejemplo)
                .where(models.Ejemplo.id == RequestValidada["id"])
            )
            db_session.execute(delete_example_query)

    except IntegrityError as ie:
        campo_repetido = ie.orig.args[1].split(".")[-1].strip("'")
        return {"msj": f"El ejemplo que intento con {campo_repetido} crear ya existe "}, 400
    except Exception as e:
        db_session.rollback()
        return {"msj": "Error interno del servidor"}, 500

    return {"msj": f"Ejemplo {RequestValidada['nombre']} actualizado exitosamente"}, 200



