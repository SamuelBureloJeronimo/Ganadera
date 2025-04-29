from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.utils import secure_filename
from database.db import connect_to_database
import os
from mysql.connector import Error

# Crear el Blueprint para razas
BP_raza = Blueprint('BP_raza', __name__)

# Configuración de la carpeta de subida de imágenes
UPLOAD_FOLDER = os.getenv("URL_FOR_ROUTES")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

'''
# Asegúrate de que exista la carpeta de uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
'''

# Validar extensión de archivos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para mostrar el formulario de registro de razas
@BP_raza.route('/dashboard/owner/register_raza', methods=['GET'])
def raza_form():
    return render_template('owner/registros/regis-raza.html')

# Ruta para registrar una nueva raza
@BP_raza.route('/register_raza', methods=['POST'])
@jwt_required()
def register_raza():
    jwt_data = get_jwt()
    rfc_comp = jwt_data.get("rfc_comp")
    
    required_fields = ["nom", "desc"]
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