from collections import namedtuple
from datetime import date, datetime
from flask import Blueprint, jsonify, make_response, request, send_from_directory, session
from flask_jwt_extended import create_access_token
from flask_mail import Message
from config.mail_conf import mail
from database.db import *
import os
from mysql.connector import Error

from guards.RoutesGuards import with_session, with_transaction

# Cargar variables desde el archivo .env
load_dotenv()

GeneralRoutes = Blueprint('GeneralRoutes', __name__)

@GeneralRoutes.route('/confirm_mail', methods=["GET", "POST"])
def confirm_mail():
    email = str(request.form["email"])
    confirmEmail = str(request.form["confirmEmail"])

    if email == confirmEmail:
        return jsonify({"success": True, "message": "Bienvenido"})
    
    return jsonify({"success": False, "message": "Usuario o contraseña incorrecto"})



@GeneralRoutes.route('/login_user', methods=["GET", "POST"])
@with_transaction
def login_user(cursor):
    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    email = str(request.form.get("email"))
    password = str(request.form.get("password"))

    try:
        # Consulta para obtener la información del usuario y su puesto
        query = '''
            SELECT personas.rfc, personas.correo, usuarios.rol, usuarios.rfc_comp
            FROM personas 
            JOIN usuarios ON usuarios.rfc = personas.rfc
            WHERE personas.correo=%s AND usuarios.pass=%s;
        '''
        cursor.execute(query, (email, password))
        res1 = cursor.fetchone()

        if res1 is None:
            return jsonify({"message": "Credenciales inválidas"}), 400

        rol_usuario = res1[2]  
        url = "/dashboard/" 

        if rol_usuario == "-1":
            url += "superuser/metrics"
        elif rol_usuario == "0":
            url += "owner/salud-general"
        elif rol_usuario in ["1", "3", "4"]:  # Solo empleados
            url += "empleoyes/panelEmpleados"
        elif rol_usuario in "2":
            url += "capataz/panel"
               

        # Generar token JWT
        access_token = create_access_token(identity=str(email), additional_claims={"rol": rol_usuario, "rfc_comp": res1[3]})
        response = make_response(jsonify({"success": True, "message": "Inicio de sesión exitoso", "token": access_token, "url": url}), 200)
        
        # Guardar el token en una cookie
        response.set_cookie("token", access_token)


        query1 = "UPDATE usuarios SET last_session=%s WHERE RFC=%s;"
        cursor.execute(query1, (datetime.now(), res1[0]));

        return response

    except Error as e:
        return jsonify({"success": False, "message": str(e)}), 400


# Registrar asistencia
@GeneralRoutes.route('/registrar_asistencia', methods=["POST"])
@with_session
def registrar_asistencia(cursor):
    if 'rfc' not in session:
        return jsonify({"message": "Usuario no autenticado"}), 403

    data = request.get_json()
    tipo = data.get("tipo")  # Puede ser 'entrada' o 'salida'
    rfc = session['rfc']
    hoy = date.today()

    try:
        if tipo == "entrada":
            # Verificar si ya hay una entrada registrada hoy
            cursor.execute("SELECT COUNT(*) FROM asistencias WHERE rfc_emp = %s AND fechentra = %s", (rfc, hoy))
            if cursor.fetchone()[0] > 0:
                return jsonify({"message": "Ya registraste tu entrada hoy"}), 400

            # Insertar la nueva entrada
            cursor.execute("INSERT INTO asistencias (rfc_emp, fechentra, hora_entrada, estado) VALUES (%s, %s, NOW(), 1)", (rfc, hoy))
            cursor._connection.commit()  # Corregimos el commit

            if cursor.rowcount > 0:
                return jsonify({"message": "Entrada registrada correctamente"}), 200
            else:
                return jsonify({"message": "Error al registrar entrada"}), 500

        elif tipo == "salida":
            # Verificar que exista una entrada antes de permitir registrar la salida
            cursor.execute("SELECT COUNT(*) FROM asistencias WHERE rfc_emp = %s AND fechentra = %s", (rfc, hoy))
            if cursor.fetchone()[0] == 0:
                return jsonify({"message": "No puedes registrar salida sin haber registrado entrada"}), 400

            # Actualizar la salida
            cursor.execute("UPDATE asistencias SET fecsalida = %s, hora_salida = NOW() WHERE rfc_emp = %s AND fechentra = %s", (hoy, rfc, hoy))
            cursor._connection.commit()  # Corregimos el commit

            if cursor.rowcount > 0:
                return jsonify({"message": "Salida registrada correctamente"}), 200
            else:
                return jsonify({"message": "Error al registrar salida"}), 500

        else:
            return jsonify({"message": "Tipo de asistencia inválido"}), 400

    except Exception as e:
        return jsonify({"message": f"Error en la base de datos: {str(e)}"}), 500


@GeneralRoutes.route("/send_account", methods=['POST'])
def enviar_codigo():
    correo = request.form.get("correo");
    password = request.form.get("password");
    
    # Cargar la plantilla y reemplazar valores
    with open("email_template.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    html_content = html_content.format(
        correo=correo,
        password=password
    )

    msg = Message("Tu cuenta ha sido creada", recipients=[correo])
    msg.html = html_content

    mail.send(msg)

    return jsonify("Correo enviado con éxito."), 200

def convertToObject(cursor):
    columnas = [column[0] for column in cursor.description]  # Obtiene los nombres de las columnas
    # Usar namedtuple para tratar las filas como objetos
    TABLE = namedtuple('TABLE', columnas)  # Crear una clase con los nombres de las columnas como atributos
    response = cursor.fetchall()

    # Crear una lista de objetos Pais
    object_data = [TABLE(*row) for row in response]
    # Retornar la respuesta como JSON con los nombres de las columnas y los datos
    return [object._asdict() for object in object_data]  # Convertir namedtuple a diccionario para JSON

@GeneralRoutes.route('/<path:filename>')
def public_files(filename):
    return send_from_directory(os.getenv("URL_FOR_ROUTES"), filename)



@GeneralRoutes.route('/get-paises', methods=['GET'])
@with_session
def get_paises(cursor):
    
    insert_query = "SELECT id, nom FROM paises;"
    cursor.execute(insert_query)

    data = convertToObject(cursor)

    return jsonify(data), 200
    

@GeneralRoutes.route('/get-estados/<id_pais>', methods=['GET'])
@with_session
def get_estados(cursor, id_pais):
    insert_query = "SELECT id, nom FROM estados WHERE pais_id=%s;"
    cursor.execute(insert_query, (id_pais,))

    data = convertToObject(cursor)

    return jsonify(data), 200

@GeneralRoutes.route('/get-municipios/<id_estado>', methods=['GET'])
@with_session
def get_municipios(cursor, id_estado):
    
    insert_query = "SELECT id, nom FROM municipios WHERE est_id=%s;"
    cursor.execute(insert_query, (id_estado,))

    data = convertToObject(cursor)

    return jsonify(data), 200

@GeneralRoutes.route('/get-colonias/<id_municipio>', methods=['GET'])
@with_session
def get_colonias(cursor, id_municipio):
    
    insert_query = "SELECT id, nom FROM colonias WHERE mun_id=%s;"
    cursor.execute(insert_query, (id_municipio,))

    data = convertToObject(cursor)

    return jsonify(data), 200

@GeneralRoutes.route('/get-col-by-cp/<cp>', methods=['GET'])
@with_session
def get_colonias_by_cp(cursor, cp):
    
    insert_query = "SELECT id, nom, mun_id FROM colonias WHERE cp=%s;"
    cursor.execute(insert_query, (cp,))
    colonias = convertToObject(cursor)
    
    insert_query = "SELECT nom, est_id FROM municipios WHERE id=%s;"
    cursor.execute(insert_query, (colonias[0]['mun_id'],))
    mun = convertToObject(cursor)

    insert_query = "SELECT nom FROM estados WHERE id=%s;"
    cursor.execute(insert_query, (mun[0]['est_id'],))
    esta = convertToObject(cursor)

    return jsonify({"colonias": colonias, "mun": mun[0]['nom'], "est": esta[0]['nom']}), 200