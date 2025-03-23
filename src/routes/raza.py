from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from database.db import connect_to_database
import os
from mysql.connector import Error

BP_raza = Blueprint('BP_raza', __name__)

# Configuración de la carpeta de subida de imágenes
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Asegúrate de que exista la carpeta de uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Validar extensión de archivos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para mostrar el formulario de registro de razas
@BP_raza.route('/raza', methods=['GET'])
def raza_form():
    return render_template('owner/registros/regis-raza.html')

# Ruta para registrar una nueva raza
@BP_raza.route('/register_raza', methods=['POST'])
def register_raza():
    connection = None  # Inicializar la conexión
    try:
        data = request.form
        file = request.files.get('img')

        # Validar que el campo 'nom' esté presente
        if not data.get("nom"):
            return redirect(url_for('BP_ani.raza_form', error="El nombre de la raza es obligatorio."))

        # Manejar la subida de la imagen
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)  # Guardar la imagen en la carpeta de uploads
            ruta_imagen = image_path  # Ruta que se guardará en la base de datos
        else:
            ruta_imagen = None  # No se subió ninguna imagen

        connection = connect_to_database()
        cursor = connection.cursor()

        # Insertar el nuevo registro en la tabla de razas
        insert_query = """
            INSERT INTO razas (nom, img, descrip)
            VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (data["nom"], ruta_imagen, data.get("desc", "")))
        connection.commit()

        # Redirigir al formulario con un mensaje de éxito
        return redirect(url_for('BP_ani.raza_form', success="¡Raza registrada exitosamente!"))
    except Error as e:
        # Redirigir al formulario con un mensaje de error
        return redirect(url_for('BP_ani.raza_form', error=f"Error al registrar: {str(e)}"))
    finally:
        if connection:
            cursor.close()
            connection.close()