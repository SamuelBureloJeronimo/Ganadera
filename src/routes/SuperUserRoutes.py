import secrets
import string
from flask import Blueprint, request, jsonify
from database.db import *

import os

from guards.SuperuserGuard import super_protected, super_protected_Route, with_transaction

# Cargar variables desde el archivo .env
load_dotenv()

BP_SuperUserRoutes = Blueprint('BP_SuperUserRoutes', __name__)

@BP_SuperUserRoutes.route('/create_owner', methods=["POST"])
@super_protected_Route
@with_transaction
def create_owner(cursor):

    required_fields = ["rfc_comp", "nom_comp", "rfc", "nombre", "correo", "app", "apm", "fech_nac", "sex", "tel", "id_colonia"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    rfc_comp = request.form.get("rfc_comp")
    nom_comp = request.form.get("nom_comp")
    
    query = "INSERT INTO companies (rfc_comp, nom) VALUES (%s, %s);"
    cursor.execute(query, (rfc_comp, nom_comp))

    rfc = request.form.get("rfc")
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    app = request.form.get("app")
    apm = request.form.get("apm")
    fech_nac = request.form.get("fech_nac")
    sex = request.form.get("sex")
    tel = request.form.get("tel")
    id_colonia = request.form.get("id_colonia")

    query = "INSERT INTO personas (rfc, nombre, correo, app, apm, fech_nac, sex, tel, id_colonia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (rfc, nombre, correo, app, apm, fech_nac, sex, tel, id_colonia))

    query = "INSERT INTO usuarios (rfc, pass, rol, rfc_comp) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (rfc, gn_pass(7), 0, rfc_comp))
    
    return jsonify({"success": True, "msg": "Usuario creado correctamente"}), 200

def gn_pass(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))