from flask import Blueprint, jsonify, request, make_response
import bcrypt
#import jwt
from product_api_service.models import User, Sesion
from product_api_service.database.session import create_local_session

login_bp=Blueprint("login",__name__,url_prefix="/user")
@login_bp.route("/login", methods=["POST"])
def login():
    try:
        usuario=request.form.get("usuario")
        contraseña=request.form.get("contraseña")
        with create_local_session() as db:
            user=db.query(User).filter_by(usuario=usuario).first()
            if user and bcrypt.checkpw(contraseña.encode("UTF-8"), user.contraseña.encode("UTF-8")):
                respuesta=make_response(jsonify({"mensaje":"Inicio de sesión exitosa"}))
                respuesta.set_cookie("logged_in","1",max_age=3600)
                respuesta.set_cookie("is_admin", str(int(user.is_admin)), max_age=3600)

                tiempo_inicio_sesion = int(request.headers.environ["HTTP_STARTED"][:-3])
                registro_sesion = Sesion(id_usuario = user.id, login_time_unix=tiempo_inicio_sesion)
                db.add(registro_sesion)
                db.commit()

                return respuesta, 200  
            else:
                respuesta=make_response(jsonify({"error":"Credenciales inválidas"}),401)
                respuesta.set_cookie("login_error","Credenciales inválidas", max_age=3600)
                return respuesta
    except Exception as e:
        respuesta=make_response(jsonify({"error":"Ocurrió un error interno en el servidor"}),500)
        respuesta.set_cookie("login_error","Error interno", max_age=3600)
        return respuesta
            