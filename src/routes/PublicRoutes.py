from collections import namedtuple
import random
from flask import Blueprint, jsonify, render_template, render_template_string, request, send_from_directory
from flask_mail import Message
from sqlalchemy import func
from database.db import *
from config.mail_conf import mail
import os
from mysql.connector import Error

# Cargar variables desde el archivo .env
load_dotenv()

BP_PublicRoutes = Blueprint('BP_PublicRoutes', __name__)

@BP_PublicRoutes.route('/img/<path:filename>')
def public_files(filename):
    return send_from_directory(os.getenv("UPL_FOL_ROUTES"), filename)

@BP_PublicRoutes.route('/')
def index():
    return render_template('home.html')

@BP_PublicRoutes.route('/login')
def login():
    return render_template('login.html')

@BP_PublicRoutes.route('/sales')
def sales():
    return render_template('sale.html')

@BP_PublicRoutes.route('/login_user', methods=["GET", "POST"])
def login_user():

    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    

    email = str(request.form.get("email"))
    password = str(request.form.get("password"))

    try:
        # Conectar a la base de datos
        connection = connect_to_database()
        if connection is None:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
        cursor = connection.cursor()
        insert_query =  '''
                        SELECT personas.rfc, personas.correo
                        FROM personas JOIN usuarios ON usuarios.rfc = personas.rfc
                        WHERE personas.correo=%s AND usuarios.pass=%s;
                        '''
        cursor.execute(insert_query, (email, password))
        res1 = cursor.fetchone()

        if res1 == None:
            return jsonify({"message": "Credenciales invalidas"}), 400
        
        cursor.close()

        # Mostrar los datos en la página
        return jsonify({"success": True, "message": "Inicio de sesión éxitoso"}), 200

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

@BP_PublicRoutes.route('/dashboard')
def dashboard():
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
