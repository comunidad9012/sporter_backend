from os import getenv
from math import ceil
from typing import Any, Dict, Union

from flask import Blueprint, request
from sqlalchemy import Select, func, select

from product_api_service import models
from product_api_service.database.session import create_local_session
from product_api_service.auth.admin import protected_route

user_read_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user",
)


@user_read_bp.get("/<id>")
@protected_route
def read_by_product_id(id):
    with create_local_session() as db_session:
        user_query: Select = select(models.User).where(
            models.User.id == id,
        )

        user_result: Union[tuple[models.User], None] = db_session.execute(
            user_query
        ).one_or_none()

        if user_result is None:
            return {"msj": f"No se halló Usuario identificado por id:'{id}'"}, 400

        user_result: models.User = user_result[0]

        sesiones : list[int] = user_result.sesiones

    user_as_dict: Dict = user_result.serialize()
    user_as_dict.pop("contraseña")

    user_as_dict["sesiones"] = [s.login_time_unix * 1000 for s in sesiones]

    return user_as_dict, 200


@user_read_bp.get("/")
def read_by_query():
    
    http_query = request.args

    elements_per_page = 30
    page = int(request.args.get("page", 1))

    with create_local_session() as db_session:

        total_match = _get_match_total_pages(db_session)
        total_pages = ceil(total_match / elements_per_page)

        if total_pages <= 0:
            return {"msg": "No se hallaron resultados para esta búsqueda"}, 400

        if total_pages < page:
            page = total_pages

        select_query: Select = select(models.User)

        select_query: Select = _add_filters(select_query)

        select_query: Select = select_query.limit(elements_per_page).offset(
            (page - 1) * elements_per_page
        )

        fetched_results: Union[list[tuple[models.User]], None] = db_session.execute(
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

    count_match: Select = select(func.count(models.User.id))

    count_match: Select = _add_filters(count_match)

    total_match = session.execute(count_match).one()[0]

    return total_match


def _serialize_query_result(list_of_rows):

    serialized_list: list[Dict[str, Any]] = []

    for row in list_of_rows:
        serialized_user = row[0].serialize()
        serialized_user.pop("contraseña")
        serialized_list.append(serialized_user)

    return serialized_list


def _add_filters(query: Select):

    if "nombre" in request.args:
        query = query.where(
            models.User.nombre.like("%" + request.args.get("nombre") + "%")
        )
        
    if "usuario" in request.args:
        query = query.where(
            models.User.usuario.like("%" + request.args.get("usuario") + "%")
        )
        
    if "correo" in request.args:
        query = query.where(
            models.User.correo.like("%" + request.args.get("correo") + "%")
        )

    if "is_admin" in request.args:
        query = query.where(
            models.User.is_admin == True
            )

    return query

