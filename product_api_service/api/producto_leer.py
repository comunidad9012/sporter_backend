from base64 import encodebytes
from os import getenv
from math import ceil
from typing import Any, Dict, Union

from flask import Blueprint, request
from sqlalchemy import Select, func, select

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

        product_result: Union[tuple[models.Producto], None] = db_session.execute(
            product_query
        ).one_or_none()

        if product_result is None:
            return {"msj": f"No se halló Producto identificado por id:'{id}'"}, 400

        product_result: models.Producto = product_result[0]

        product_tag = product_result.etiqueta

    product_as_dict: Dict = product_result.serialize()
    product_as_dict["etiqueta"] = {
        "id": product_tag.id,
        "nombre": product_tag.nombre,
    }

    product_as_dict.pop("id_etiqueta")

    product_as_dict["imagen"] = _get_image_binary_utf8(
        product_as_dict.pop("img_rand_name")
    )

    return product_as_dict, 200


@product_read_bp.get("/")
def read_by_query():

    http_query = request.args

    elements_per_page = 10
    page = int(request.args.get("page", 1))

    with create_local_session() as db_session:

        total_match = _get_match_total_pages(db_session)
        total_pages = ceil(total_match / elements_per_page)

        if total_pages <= 0:
            return {"msg": "No se hallaron resultados para esta búsqueda"}, 400

        if total_pages < page:
            page = total_pages

        select_query: Select = select(models.Producto)

        select_query: Select = _add_filters(select_query)

        select_query: Select = select_query.limit(elements_per_page).offset(
            (page - 1) * elements_per_page
        )

        fetched_results: Union[list[tuple[models.Producto]], None] = db_session.execute(
            select_query
        ).all()

        serialized_products_list = _serialize_query_result(fetched_results)

    if fetched_results is None:
        return {
            "msj": "No se encontraron resultados",
            "search_query": http_query,
        }, 400

    return {
        "search_result": serialized_products_list,
        "search_query": http_query,
        "total_hits": total_match,
        "total_pages": total_pages,
        "current_page": page,
    }, 200


def _get_match_total_pages(session) -> int:

    count_match: Select = select(func.count(models.Producto.id))

    count_match: Select = _add_filters(count_match)

    total_match = session.execute(count_match).one()[0]

    return total_match


def _serialize_query_result(list_of_rows):

    serialized_list: list[Dict[str, Any]] = []

    for row in list_of_rows:
        serialized_product = row[0].serialize()

        serialized_product["etiqueta"] = {
            "id": row[0].etiqueta.id,
            "nombre": row[0].etiqueta.nombre,
        }

        serialized_product.pop("id_etiqueta")

        serialized_product["imagen"] = _get_image_binary_utf8(
            serialized_product.pop("img_rand_name")
        )

        serialized_list.append(serialized_product)

    return serialized_list


def _add_filters(query: Select):

    if "precio_min" in request.args and "precio_max" in request.args:
        query = query.where(
            models.Producto.precio > request.args.get("precio_min"),
            models.Producto.precio < request.args.get("precio_max"),
        )
    elif "precio_min" in request.args:
        query = query.where(models.Producto.precio > request.args.get("precio_min"))
    elif "precio_max" in request.args:
        query = query.where(models.Producto.precio < request.args.get("precio_max"))

    if "exis_min" in request.args and "exis_max" in request.args:
        query = query.where(
            models.Producto.existencias > request.args.get("exis_min"),
            models.Producto.existencias < request.args.get("exis_max"),
        )
    elif "exis_min" in request.args:
        query = query.where(models.Producto.existencias > request.args.get("exis_min"))
    elif "exis_max" in request.args:
        query = query.where(models.Producto.existencias < request.args.get("exis_max"))

    if "nombre" in request.args:
        query = query.where(
            models.Producto.nombre.like("%" + request.args.get("nombre") + "%")
        )

    if "etiqueta" in request.args:
        query = query.join(
            models.Etiqueta, models.Producto.id_etiqueta == models.Etiqueta.id
        ).where(models.Etiqueta.nombre == request.args.get("etiqueta"))

    return query


def _get_image_binary_utf8(image_rand_id):
    with open(getenv("FILES_DIR") + "/" + image_rand_id, "rb") as image_file:
        image_hex = image_file.read()

    image_bin = encodebytes(image_hex).decode("utf-8")

    return image_bin
