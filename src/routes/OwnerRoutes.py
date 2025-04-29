

from collections import namedtuple
from datetime import datetime, timedelta
import secrets
import string
from flask import Blueprint, jsonify, render_template_string, request
from flask_jwt_extended import get_jwt, jwt_required
from flask_mail import Message
from config.mail_conf import mail
from guards.RoutesGuards import with_session, with_transaction


BP_Owner = Blueprint('BP_Owner', __name__)

@BP_Owner.route("/create_employee", methods=["POST"])
@jwt_required()
@with_transaction
def create_employee(cursor):

    jwt_data = get_jwt()

    rfc_comp = jwt_data.get("rfc_comp")
    
    required_fields = ["rol", "rfc", "nombre", "correo", "app", "apm", "fech_nac", "sex", "tel", "id_colonia", "finca_id"]
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
    turno = request.form.get("turno")
    id_colonia = request.form.get("id_colonia")

    password = gn_pass(7)

    query = "INSERT INTO personas (rfc, nombre, correo, app, apm, fech_nac, sex, tel, id_colonia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (rfc, nombre, correo, app, apm, fech_nac, sex, tel, id_colonia))

    query = "INSERT INTO usuarios (rfc, pass, rol, rfc_comp) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (rfc, password, rol, rfc_comp))

    finca_id = request.form.get("finca_id")

    query = "INSERT INTO empleados (rfc, puesto_id, finca_id, turno) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (rfc, rol, finca_id, turno))
    
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

@BP_Owner.route("/update_finca/<id_finca>", methods=["PUT"])
@jwt_required()
@with_transaction
def update_finca(cursor, id_finca):
    jwt_data = get_jwt()
    rfc_comp = jwt_data.get("rfc_comp")
    
    required_fields = ["id", "nombre", "capacidad", "descrip", "id_colonia"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    _id = request.form.get("id")
    nombre = request.form.get("nombre")
    capacidad = request.form.get("capacidad")
    descrip = request.form.get("descrip")
    id_colonia = request.form.get("id_colonia")

    query = "UPDATE fincas SET nombre=%s, capacidad=%s, descrip=%s, id_colonia=%s WHERE id=%s;"
    cursor.execute(query, (nombre, capacidad, descrip, id_colonia, _id))

    return jsonify({"success": True, "msg": "Finca actualizada correctamente"}), 200

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

@BP_Owner.route("/get-all-puestos", methods=["GET"])
@jwt_required()
@with_session
def get_puestos(cursor):

    jwt_data = get_jwt()

    rfc_comp = jwt_data.get("rfc_comp")

    print("ENTRO", rfc_comp)

    query = '''
            SELECT 
            puestos.id AS puesto_id,
            puestos.nombre,
            puestos.descripcion,
            config_puestos.id AS config_id,
            config_puestos.salario_base,
            config_puestos.dias_lab,
            config_puestos.h_ent,
            config_puestos.h_sal,
            config_puestos.rfc_comp
        FROM puestos
        JOIN config_puestos ON config_puestos.id_puesto = puestos.id;
            '''
    cursor.execute(query)

    puestos = cursor.fetchall()
    print(puestos)
    

    puestos = convertToObject(cursor);


    print(puestos)

    return jsonify(puestos), 200

@BP_Owner.route("/update-puesto", methods=["PUT"])
@jwt_required()
@with_transaction
def update_puesto(cursor):

    required_fields = ["id", "salario_base", "h_ent", "h_sal", "dias_lab"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    _id = request.form.get("id")
    salario_base = request.form.get("salario_base")
    h_ent = request.form.get("h_ent")
    h_sal = request.form.get("h_sal")
    dias_lab = request.form.get("dias_lab")

    query = "UPDATE config_puestos SET salario_base=%s, dias_lab=%s, h_ent=%s, h_sal=%s WHERE id=%s;"
    cursor.execute(query, (salario_base, dias_lab, h_ent, h_sal, _id))

    return jsonify("El puesto fue actualizado correctamente."), 200




def convertToObject(cursor):
    columnas = [column[0] for column in cursor.description]  # Obtener nombres de columnas
    TABLE = namedtuple('TABLE', columnas)  # Crear namedtuple
    response = cursor.fetchall()

    object_data = [TABLE(*row) for row in response]  # Convertir filas en objetos

    def serialize_value(value):
        """Convierte valores no serializables a formatos compatibles con JSON"""
        if isinstance(value, timedelta):  # Si es un TIME de MySQL (timedelta)
            # Convertir timedelta a horas y minutos en formato 24H (HH:MM)
            total_seconds = value.total_seconds()
            hours = int(total_seconds // 3600)  # Horas
            minutes = int((total_seconds % 3600) // 60)  # Minutos
            return f"{hours:02d}:{minutes:02d}"  # Formato HH:MM (24H)

        return value  # Devolver el valor normal si no es timedelta

    return [{key: serialize_value(value) for key, value in obj._asdict().items()} for obj in object_data]

