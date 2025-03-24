

from collections import namedtuple
import secrets
import string
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from guards.RoutesGuards import with_session, with_transaction


BP_Owner = Blueprint('BP_Owner', __name__)

@BP_Owner.route("/create_employee", methods=["POST"])
@jwt_required()
@with_transaction
def create_employee(cursor):

    jwt_data = get_jwt()

    rfc_comp = jwt_data.get("rfc_comp")
    
    required_fields = ["rol", "rfc", "nombre", "correo", "app", "apm", "fech_nac", "sex", "tel", "id_colonia"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    rfc = request.form.get("rfc")
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    app = request.form.get("app")
    apm = request.form.get("apm")
    fech_nac = request.form.get("fech_nac")
    sex = request.form.get("sex")
    tel = request.form.get("tel")
    rol = request.form.get("rol")
    id_colonia = request.form.get("id_colonia")

    query = "INSERT INTO personas (rfc, nombre, correo, app, apm, fech_nac, sex, tel, id_colonia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (rfc, nombre, correo, app, apm, fech_nac, sex, tel, id_colonia))

    query = "INSERT INTO usuarios (rfc, pass, rol, rfc_comp) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (rfc, gn_pass(7), rol, rfc_comp))
    
    return jsonify({"success": True, "msg": "Usuario creado correctamente"}), 200

def gn_pass(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

@BP_Owner.route("/create_finca", methods=["POST"])
@jwt_required()
@with_transaction

def create_finca(cursor):

    jwt_data = get_jwt()
    rfc_comp = jwt_data.get("rfc_comp")
    
    required_fields = ["nombre", "capacidad", "id_colonia"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    nombre = request.form.get("nombre")
    capacidad = request.form.get("capacidad")
    descrip = request.form.get("descrip")
    id_colonia = request.form.get("id_colonia")

    query = "INSERT INTO fincas (nombre, capacidad, descrip, id_colonia, rfc_comp) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(query, (nombre, capacidad, descrip, id_colonia, rfc_comp))

    return jsonify({"success": True, "msg": "Finca registrada correctamente"}), 200


@BP_Owner.route("/get-all-fincas", methods=["GET"])
@jwt_required()
@with_session
def get_fincas(cursor):

    jwt_data = get_jwt()

    rfc_comp = jwt_data.get("rfc_comp")

    query = "SELECT * FROM fincas WHERE rfc_comp=%s;"
    cursor.execute(query, (rfc_comp,))

    data = convertToObject(cursor)

    return jsonify(data), 200


def convertToObject(cursor):
    columnas = [column[0] for column in cursor.description]  # Obtiene los nombres de las columnas
    # Usar namedtuple para tratar las filas como objetos
    TABLE = namedtuple('TABLE', columnas)  # Crear una clase con los nombres de las columnas como atributos
    response = cursor.fetchall()

    # Crear una lista de objetos Pais
    object_data = [TABLE(*row) for row in response]
    # Retornar la respuesta como JSON con los nombres de las columnas y los datos
    return [object._asdict() for object in object_data]  # Convertir namedtuple a diccionario para JSON

