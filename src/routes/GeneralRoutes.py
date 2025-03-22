from collections import namedtuple
import random
from flask import Blueprint, jsonify, make_response, render_template_string, request, send_from_directory
from flask_jwt_extended import create_access_token
from flask_mail import Message
from database.db import *
from config.mail_conf import mail
import os
from mysql.connector import Error

from guards.RoutesGuards import with_session

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
@with_session
def login_user(cursor):

    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    

    email = str(request.form.get("email"))
    password = str(request.form.get("password"))

    try:
        insert_query = '''
                        SELECT personas.rfc, personas.correo, usuarios.rol, usuarios.rfc_comp
                        FROM personas JOIN usuarios ON usuarios.rfc = personas.rfc
                        WHERE personas.correo=%s AND usuarios.pass=%s;
                        '''
        cursor.execute(insert_query, (email, password))
        res1 = cursor.fetchone()

        if res1 == None:
            return jsonify({"message": "Credenciales invalidas"}), 400
        
        url = "/dashboard/"
        
        if res1[2] == "-1":
            url += "superuser/metrics"
        if res1[2] == "0":
            url += "owner/panel"

        formData = {
            "logo": "Logoruta"
        }

        
        access_token = create_access_token(identity=str(email), additional_claims={"rol": res1[2], "rfc_comp": res1[3]})
        response = make_response(jsonify({"success": True, "message": "Inicio de sesión éxitoso", "token": access_token, "url": url}), 200)
        
        response.set_cookie("token", access_token)

        # Mostrar los datos en la página
        return response

    except Error as e:
        return jsonify({"success": False, "message": str(e)}), 400

@GeneralRoutes.route("/send_code/<email>")
def enviar_codigo(email):
    nombre_usuario = "Juan Pérez"
    codigo_verificacion = str(random.randint(100000, 999999))
    
    # Cargar la plantilla HTML para el correo
    html_content = render_template_string(open('send_code.html').read(), nombre_usuario=nombre_usuario, codigo_verificacion=codigo_verificacion)

    # Crear el mensaje
    msg = Message("Verificación de Cuenta - El Herrado", recipients=[email])
    msg.html = html_content
    msg.charset = 'utf-8'  # Establecer la codificación para asegurar que los acentos se manejen correctamente
    msg.content_type = 'text/html; charset=utf-8'

    # Enviar el mensaje
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