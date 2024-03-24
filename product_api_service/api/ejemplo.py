from typing import Dict
from pydantic import ValidationError
from flask import Blueprint, jsonify, make_response, request, Response

from sqlalchemy import select, Select, or_, update, Update, delete, Delete
from sqlalchemy.exc import IntegrityError

from product_api_service.database.session import create_local_session
from product_api_service import schemas, models

example_crud_bp = Blueprint(
    "example",
    __name__,
    url_prefix="/example",
)


@example_crud_bp.post("/create")
def create_new_example():

    # Este endpoint recive un formulario
    # tomamos el formulario de la request y lo convertimos en diccionario para poder trabajar con el
    example_info_request: Dict = request.form.to_dict()

    # a continuacion validaremos la informacion recibida
    # para eso utilizaremos una schema de pydantic definida en /schemas
    # usamos try except ya que si la validacion falla se eleva una Excepcion
    try:
        validated_example_info = dict(schemas.Ejemplo(**example_info_request))
    except ValidationError as ve:
        # Aqui trabajaremos con las excepciones de Validacion
        # prepararemos una lista con los errores para devolverlos y asi informar al usuario de la api
        # qué falló
        errors_list = []

        # asi conseguimos los errores
        for error in ve.errors():

            # tomamos la informacion de cada error y la metemos en un diccionario por cada error
            error_object = {
                "field": error["loc"][0],
                "invalid_input": error["input"],
                "error_info": error["msg"],
            }

            # agregamos al diccionario a la lista de errores
            errors_list.append(error_object)

        # y devolvemos un mensaje explicando qué salió mal
        return {"msj": "Informacion de ejemplo invalida", "errors": errors_list}, 400

    # Si nada salió mal hasta ahora, registraremos el nuevo ejemplo en la DB
    try:
        # asi iniciamos una sesion de coneccion a la base de datos con SQLAlchemy
        with create_local_session() as db_session:

            # Así creamos un Objeto Ejemplo en base al modelo/clase Ejemplo con la informacion brindada
            example_object = models.Ejemplo(**validated_example_info)

            # asi de facil es insertarlo en la base de datos!
            db_session.add(example_object)
            db_session.commit()

    # esto es para manejar prosibles errores de elementos duplicados
    # prodiamos intentar manejar otras excepciones posibles, no solo esta
    # depende de lo que se intente lograr
    except IntegrityError as ie:
        campo_repetido = ie.orig.args[1].split(".")[-1].strip("'")
        return {
            "msj": f"El ejemplo que intento con {campo_repetido} crear ya existe "
        }, 400

    return {
        "msj": f"Ejemplo {validated_example_info['titulo']} creado exitosamente"
    }, 200


@example_crud_bp.post("/update")
def update_existing_example():

    #
    # ESTO LO COPIE DE CREAR ASI QUE ES CASI IGUAL EXCEPTO POR SQL ALCHEMY
    #

    # Este endpoint recive un formulario
    # tomamos el formulario de la request y lo convertimos en diccionario para poder trabajar con el
    example_info_request: Dict = request.form.to_dict()

    # a continuacion validaremos la informacion recibida
    # para eso utilizaremos una schema de pydantic definida en /schemas
    # usamos try except ya que si la validacion falla se eleva una Excepcion
    try:
        validated_example_info = dict(schemas.Ejemplo(**example_info_request))
    except ValidationError as ve:
        # Aqui trabajaremos con las excepciones de Validacion
        # prepararemos una lista con los errores para devolverlos y asi informar al usuario de la api
        # qué falló
        errors_list = []

        # asi conseguimos los errores
        for error in ve.errors():

            # tomamos la informacion de cada error y la metemos en un diccionario por cada error
            error_object = {
                "field": error["loc"][0],
                "invalid_input": error["input"],
                "error_info": error["msg"],
            }

            # agregamos al diccionario a la lista de errores
            errors_list.append(error_object)

        # y devolvemos un mensaje explicando qué salió mal
        return {"msj": "Informacion de ejemplo invalida", "errors": errors_list}, 400

    # Si nada salió mal hasta ahora, registraremos el nuevo ejemplo en la DB
    try:
        # asi iniciamos una sesion de coneccion a la base de datos con SQLAlchemy
        with create_local_session() as db_session:

            # Así creamos un Objeto Ejemplo en base al modelo/clase Ejemplo con la informacion brindada

            update_example_query: Update = (
                update(models.Ejemplo)
                .where(models.Ejemplo.id == example_info_request["id"])
                .values(
                    titulo=validated_example_info["titulo"],
                    cuerpo=validated_example_info["cuerpo"],
                )
            )

            # asi de facil es insertarlo en la base de datos!
            db_session.execute(update_example_query)
            db_session.commit()

    # esto es para manejar prosibles errores de elementos duplicados
    # prodiamos intentar manejar otras excepciones posibles, no solo esta
    # depende de lo que se intente lograr
    except IntegrityError as ie:
        campo_repetido = ie.orig.args[1].split(".")[-1].strip("'")
        return {
            "msj": f"El ejemplo que intento con {campo_repetido} crear ya existe "
        }, 400

    return {
        "msj": f"Ejemplo {validated_example_info['titulo']} actualizado exitosamente"
    }, 200


@example_crud_bp.get("/read/all")
def read_all_examples():

    with create_local_session() as db_session:
        # con este select podemos hacer, bueno, selects
        read_all_query = select(models.Ejemplo)
        # y asi lo ejecutamos contra la DB
        all_examples_query_result = db_session.execute(read_all_query).all()

    all_examples_dicts_list = []

    # Cuando seleccionamos de la base de datos con SQLAlchemy
    # Este nos devolvera Objetos del tipo seleccionado
    # por ende para devolverlos en una respuesta
    # debemos traducirlos a un objeto python
    # en este caso un diccionario
    # ya que los diccionarios son basicamente lo mismo que un
    # objeto Javascript que son el centro de JSON (JavaScript Object Notation)
    for example in all_examples_query_result:
        user_as_dict = {}
        # esa parte rara nos permite saber cuales son las columnas del modelo
        for column in models.Ejemplo.__table__.columns:
            # tomamos el diccionario instanciado
            # y nombramos a la llave igual que la columna
            # y getatttr nos permite obtener el atributo del Objeto que tenga el mismo nombre que la columna
            user_as_dict.setdefault(column.name, getattr(example[0], column.name))

        # metemos todo en una lista
        all_examples_dicts_list.append(user_as_dict)

    # Y lo devolvemos!
    return jsonify(examples_list=all_examples_dicts_list), 200


@example_crud_bp.get("/read/<examp_id_or_title>")
def read_example_by_id_or_name(examp_id_or_title: str):

    with create_local_session() as db_session:

        # Ahora podemos ver un select mas complejo!
        # esto dice:
        # SELECT * FROM Ejemplo WHERE nombre == examp_id_or_name OR id == examp_id_or_name
        # es decir
        # Seleccionar todo de la tabla Ejemplo
        # donde su nombre sea el mismod de la variable o su id sea el mismo que el de la variable

        read_example_query: Select = select(models.Ejemplo).where(
            or_(
                models.Ejemplo.titulo == examp_id_or_title,
                models.Ejemplo.id == examp_id_or_title,
            )
        )

        # aqui: Ejecutamos la consulta y le pedimos a la session que
        # nos devuelva Un solo objeto, en caso de que haya encontrado uno
        # o que nos devuelva 'None'
        example_result = db_session.execute(read_example_query).one_or_none()

    # Si devolvio None, indiquemos al usuario
    if example_result is None:
        return {"msj": f"No hay ejemplo identificado por '{examp_id_or_title}'"}, 400

    # si todo salio bien, lo convertiremos en un diccionario

    user_as_dict = {}

    for column in models.Ejemplo.__table__.columns:

        user_as_dict.setdefault(column.name, getattr(example_result[0], column.name))

    return user_as_dict, 200


@example_crud_bp.post("/delete/<id>")
def delete_example(id: int):

    with create_local_session() as db_session:

        # Ahora podemos ver un select mas complejo!
        # esto dice:
        # SELECT * FROM Ejemplo WHERE id == id
        # es decir
        # Seleccionar todo de la tabla Ejemplo
        # donde su id sea el mismo que el de la variable

        read_example_query: Delete = delete(models.Ejemplo).where(
            models.Ejemplo.id == id
        )

        db_session.execute(read_example_query)
        db_session.commit()

    return {"msj": f"Ejemplo {id} eliminado"}, 200
