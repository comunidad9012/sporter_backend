from typing import Dict, Union

from flask import Blueprint
from sqlalchemy import Select, select

from product_api_service import models
from product_api_service.database.session import create_local_session

product_read_bp = Blueprint(
    "producto",
    __name__,
    url_prefix="/producto",
)


@product_read_bp.get("/<id>")
def read_by_product_id(id):
    with create_local_session() as db_session:
        product_query: Select = select(models.Producto).where(
            models.Producto.id == id,
        )

        product_result: Union[models.Producto, None] = db_session.execute(
            product_query
        ).one_or_none()

    if product_result is None:
        return {"msj": f"No se halló Producto identificado por id:'{id}'"}, 400

    product_as_dict: Dict = product_result[0].serialize()

    # TODO: OBTENER IMAGEN DESDE EL FILESYSTEM
    # TODO: AGREGAR IMAGEN AL JSON A DEVOLVER

    product_as_dict.pop("img_rand_name")

    return product_as_dict, 200
