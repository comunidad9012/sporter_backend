from typing import Dict
from flask import Blueprint, jsonify, request
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from product_api_service.database.session import create_local_session
from product_api_service import schemas, models
from pydantic import ValidationError
from product_api_service.auth.admin import protected_route
import os


updateProduct_bp = Blueprint(
    "updateProduct",
    __name__,
    url_prefix="/producto",
)


@updateProduct_bp.post("/actualizar")
@protected_route
def update_existingProduct():

    new_image: bool = False
    # obtener de request: Datos e Imagen
    UpdateRequest: Dict = request.form.to_dict()
    UpdateFiles: Dict = request.files
    # Si no hay imagen, tomar nota y no validar nombre de imagen, ya que no se modificara
    if "filename" in UpdateFiles:
        imagen = UpdateFiles["filename"]
        new_image: bool = True

    if new_image and imagen.filename :  # Verificar si el nombre del archivo está vacío
        UpdateRequest["img_orig_name"] = imagen.filename

    # validar info

    try:
        # Validar utilizando el esquema de Producto
        # Evitamos validar el nombre aleatorio, puesto que reutilizaremos
        # el que esta en la DB para sobre escribir el archivo anterior
        RequestValidada = dict(
            schemas.Producto(**UpdateRequest).model_dump(exclude_defaults=True)
        )

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
            # chequear que producto exista
            find_product_query = select(models.Producto).where(
                models.Producto.id == UpdateRequest["id"]
            )

            product_to_update = db_session.execute(find_product_query).one_or_none()

            # si no, error
            if product_to_update is None:
                return {
                    "msg": f"No se halló un producto con esta id {UpdateRequest['id']}"
                }, 404
            # si si:
            product_to_update = product_to_update[0]
            # Si no hay imagen, no cambiar cosas relacionadas a imagen
            # Si hay imagen, obtener el nombre aleatorio original y sobre escribir
            if new_image:
                # sobre escribir
                imagen.save(
                    os.path.join(
                        os.getenv("FILES_DIR"), product_to_update.img_rand_name
                    )
                )

            # Guardar nueva info de producto (id, nombre, descr, imag_orig, precio, exis)
            update_product_query = (
                update(models.Producto)
                .where(models.Producto.id == product_to_update.id)
                .values(**RequestValidada)
            )

            db_session.execute(update_product_query)
            db_session.commit()

    except IntegrityError as ie:
        campo_repetido = ie.orig.args[1].split(".")[-1].strip("'")
        return {
            "msj": f"El ejemplo que intento con {campo_repetido} crear ya existe "
        }, 400
    except Exception as e:
        db_session.rollback()
        return {"msj": "Error interno del servidor"}, 500

    return {
        "msg": f"Producto {UpdateRequest['id']} - {RequestValidada['nombre']} actualizado exitosamente"
    }, 200
