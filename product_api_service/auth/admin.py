from flask import request, jsonify
import functools

def protected_route(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
            #obtener la cookie de si está logueado
        logged_in=int(request.cookies.get("logged_in",0))
        is_admin=int(request.cookies.get("is_admin",0))
        
        if not logged_in:
            return jsonify({"error":"No autorizado. Primero debe iniciar sesión"}),401
        
        #obtener la cookie para verificar si es admin
        if not is_admin:
            return jsonify({"error":"Solo tienen acceso los administradores"}),403

        return func(*args, **kwargs)

    return wrapper
