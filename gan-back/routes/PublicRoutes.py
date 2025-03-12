import random
from flask import Blueprint, jsonify, render_template, render_template_string, request, send_from_directory
from flask_mail import Message
from database.db import *
from config.mail_conf import mail
import os

# Cargar variables desde el archivo .env
load_dotenv()

BP_PublicRoutes = Blueprint('BP_PublicRoutes', __name__, url_prefix='/')

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
    email = str(request.form["email"])
    password = str(request.form["password"])

    if email == "admin@gmail.com" and password == "1415":
        return jsonify({"success": True, "message": "Bienvenido"})
    
    return jsonify({"success": False, "message": "Usuario o contraseña incorrecto"})

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