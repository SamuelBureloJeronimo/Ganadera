from collections import namedtuple
import random
from flask import Blueprint, jsonify, make_response, render_template, render_template_string, request, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required
from flask_mail import Message
from sqlalchemy import func
from database.db import *
from config.mail_conf import mail
import os
from mysql.connector import Error

from guards.SuperuserGuard import super_protected, with_session

# Cargar variables desde el archivo .env
load_dotenv()

BP_PublicRoutes = Blueprint('BP_PublicRoutes', __name__)

@BP_PublicRoutes.route('/img/<path:filename>')
def public_files(filename):
    return send_from_directory(os.getenv("URL_FOR_ROUTES"), filename)

@BP_PublicRoutes.route('/')
def index():
    images = ["/img/slide/img1.png", "/img/slide/img2.webp", "/img/slide/img3.png", "/img/slide/img4.png"]  # Agrega más imágenes si es necesario
    return render_template("home.html", images=images)

@BP_PublicRoutes.route('/login')
def login():
    return render_template('login.html')

@BP_PublicRoutes.route('/sales')
def sales():
    return render_template('sale.html')

@BP_PublicRoutes.route('/login_user', methods=["GET", "POST"])
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
                        SELECT personas.rfc, personas.correo, usuarios.rol
                        FROM personas JOIN usuarios ON usuarios.rfc = personas.rfc
                        WHERE personas.correo=%s AND usuarios.pass=%s;
                        '''
        cursor.execute(insert_query, (email, password))
        res1 = cursor.fetchone()

        if res1 == None:
            return jsonify({"message": "Credenciales invalidas"}), 400
        
        access_token = create_access_token(identity=str(email), additional_claims={"rol": res1[2]})
        response = make_response(jsonify({"success": True, "message": "Inicio de sesión éxitoso", "token": access_token}), 200)
        
        response.set_cookie(
            "token", access_token, httponly=True, secure=True, samesite="Lax"
        )

        # Mostrar los datos en la página
        return response

    except Error as e:
        return jsonify({"success": False, "message": str(e)}), 400

@BP_PublicRoutes.route('/confirm_mail', methods=["GET", "POST"])
def confirm_mail():
    email = str(request.form["email"])
    confirmEmail = str(request.form["confirmEmail"])

    if email == confirmEmail:
        return jsonify({"success": True, "message": "Bienvenido"})
    
    return jsonify({"success": False, "message": "Usuario o contraseña incorrecto"})

@BP_PublicRoutes.route('/contact')
def contact():
    return render_template('contact.html')

@BP_PublicRoutes.route('/dashboard/superuser/home', methods=["GET"])
@super_protected
def dashboard(cursor):
    return render_template('dashboard.html')

@BP_PublicRoutes.route("/send_code/<email>")
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
