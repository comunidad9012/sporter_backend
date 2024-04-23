from flask import Blueprint, request, jsonify


admin_bp=Blueprint("admin",__name__,url_prefix=("/admin"))
@admin_bp.route("/protected", methods=["GET"])
def protected_route():
    #obtener la cookie de si está logueado
    logged_in=request.cookies.get("logged_in")
    if logged_in !="true":
        return jsonify({"error":"No autorizado. Primero debe iniciar sesión"}),401
    
    #obtener la cookie para verificar si es admin
    is_admin=request.cookies.get("is_admin")
    if is_admin !="true":
        return jsonify({"error":"Solo tienen acceso los administradores"}),403
    #Si cumple ambos se le permite ingresar a la ruta protegida con permisos solo para admins
    return jsonify({"mensaje":"Bienvenido a la ruta protegida."}),200
    