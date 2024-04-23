from os import getenv
from math import ceil
from typing import Any, Dict, Union

from flask import Blueprint, request
from sqlalchemy import Select, func, select, or_

from product_api_service import models
from product_api_service.database.session import create_local_session

read_tag_bp = Blueprint(
    "etiqueta",
    __name__,
    url_prefix="/etiqueta/leer",
)


@read_tag_bp.get("/<identificacion>")
def read_by_product_id(identificacion):
    with create_local_session() as db_session:
        select_by_identifier: Select = select(models.Etiqueta).where(
            or_(
                models.Etiqueta.id == identificacion,
                models.Etiqueta.nombre == identificacion,
            )
        )

        query_result: Union[tuple[models.Etiqueta], None] = db_session.execute(
            select_by_identifier
        ).one_or_none()

        if query_result is None:
            return {
                "msg": f"No se halló Etiqueta identificada por id:'{identificacion}'"
            }, 400

        query_result: models.Etiqueta = query_result[0]

        product_rel_quant_query = (
            select(
                func.count(models.Producto.id),
            )
            .select_from(models.Etiqueta)
            .join(models.Producto, models.Etiqueta.id == models.Producto.id_etiqueta)
            .group_by(models.Etiqueta.id, models.Etiqueta.nombre)
            .where(models.Etiqueta.id == query_result.id)
        )

        tag_product_quant = db_session.execute(product_rel_quant_query).one_or_none()

        if tag_product_quant is None:
            tag_product_quant = 0
        else:
            tag_product_quant = tag_product_quant[0]

    tag_as_dict: Dict = query_result.serialize()
    tag_as_dict["total_productos"] = tag_product_quant

    return tag_as_dict, 200


@read_tag_bp.get("/")
def read_all():
    with create_local_session() as db_session:
        read_all_with_prod_quant: Select = (
            select(
                models.Etiqueta.id,
                models.Etiqueta.nombre,
                func.count(models.Producto.id),
            )
            .select_from(models.Etiqueta)
            .join(
                models.Producto,
                models.Etiqueta.id == models.Producto.id_etiqueta,
                isouter=True,
            )
            .group_by(models.Etiqueta.id, models.Etiqueta.nombre)
        )

        all_tags = db_session.execute(read_all_with_prod_quant).all()

    tags_rows_as_dicts = []

    for tag in all_tags:
        as_dict = dict(zip(["id", "nombre", "total_productos"], tag))
        tags_rows_as_dicts.append(as_dict)

    return tags_rows_as_dicts, 200
