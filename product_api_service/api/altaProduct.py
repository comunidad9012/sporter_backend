from typing import Dict
from pydantic import ValidationError
from flask import Blueprint, jsonify, make_response, request, Response, current_app

import uuid
import os

from sqlalchemy import select, Select, or_, update, Update, delete, Delete
from sqlalchemy.exc import IntegrityError

from product_api_service.database.session import create_local_session
from product_api_service import schemas, models

from product_api_service.auth.admin import protected_route

altaProductBP = Blueprint(
    "altaProductBP",
    __name__,
    url_prefix="/producto",
)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@altaProductBP.post("/crear")
@protected_route
def altaProduct():

    formRespuesta: Dict = request.form.to_dict()


    if 'filename' not in request.files:
        return {"msg": "Debes cargar una imagen"}, 400
    
    file = request.files['filename']

    formRespuesta["img_orig_name"]=file.filename

    if file.filename == '':
        return {"msg": "Debes cargar una imagen"}, 400
    
    if file and allowed_file(file.filename):
        filename = uuid.uuid4()
        formRespuesta["img_rand_name"]=str(filename)
        file.save(os.path.join(os.getenv("FILES_DIR"), str(filename)))


    try:
        validaRespuesta = dict(schemas.Producto(**formRespuesta))
    except ValidationError as e:
        listaErrores=[]

        for errores in e.errors():

            erroresProduct = {
                "field": errores["loc"][0],
                "invalid input": errores["input"],
                "error_info": errores["msg"]
            }

        return { "msg": "Se produjo el siguiente error :", "errores": listaErrores }, 400
    try:
        with create_local_session() as db_session:
            objetoProduct = models.Producto(**validaRespuesta)
            db_session.add(objetoProduct)
            db_session.commit()

    except IntegrityError as e:
        objeto_repetido = e.orig.args[1].split(".")[-1].strip("'")
        return {
            "msj": f"El ejemplo que intento con {objeto_repetido} crear ya existe "
        }, 400

    return {
        "msj": f"{validaRespuesta['nombre']} creado exitosamente"
    }, 200

