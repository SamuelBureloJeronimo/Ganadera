from flask import Blueprint, jsonify, redirect, render_template, request, send_from_directory, url_for
from database.db import connect_to_database
import os
from mysql.connector import Error

BP_ani = Blueprint('BP_ani', __name__)

# Ruta para servir imágenes de razas de animales
@BP_ani.route('/img/<path:filename>')
def public_file(filename):
    upload_folder = os.getenv("UPL_FOL_ROUTES")
    if not upload_folder:
        return jsonify({"error": "Ruta de imágenes no configurada"}), 500
    return send_from_directory(upload_folder, filename)

# Ruta para mostrar el formulario de registro de animales con opciones de razas y fincas
@BP_ani.route('/animal', methods=['GET'])
def animal():
    connection = None  # Inicializar la conexión
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        # Consulta para razas
        cursor.execute("SELECT id, nom FROM razas")
        razas = cursor.fetchall()

        # Consulta para fincas
        cursor.execute("SELECT id, nombre FROM fincas")
        fincas = cursor.fetchall()

        # Renderizar el formulario con razas y fincas
        return render_template('owner/registros/regis-ganados.html', razas=razas, fincas=fincas)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

# Ruta para registrar un nuevo animal
@BP_ani.route('/animal/registro', methods=['POST'])
@BP_ani.route('/animal/registro', methods=['POST'])
def register_animal():
    connection = None  # Inicializar la conexión
    try:
        data = request.form

        # Validar que todos los campos requeridos estén presentes
        required_fields = ["id", "especie", "raza_id", "sexo", "finca_id", "fech", "estado", "externo"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return redirect(url_for('BP_ani.animal', error=f"Faltan los siguientes campos: {', '.join(missing_fields)}"))

        connection = connect_to_database()
        cursor = connection.cursor()

        # Insertar el nuevo registro en la tabla animales
        insert_query = """
            INSERT INTO animales (id, especie, raza_id, sexo, finca_id, fech, estado, externo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            data["id"], data["especie"], data["raza_id"], data["sexo"],
            data["finca_id"], data["fech"], int(data["estado"]), data["externo"]
        ))
        connection.commit()

        # Redirigir al formulario con un mensaje de éxito
        return redirect(url_for('BP_ani.animal', success="¡Animal registrado exitosamente!"))
    except Error as e:
        # Redirigir al formulario con un mensaje de error en caso de fallo
        return redirect(url_for('BP_ani.animal', error=f"Error al registrar: {str(e)}"))
    finally:
        if connection:
            cursor.close()
            connection.close()
            
# Ruta para obtener razas en formato JSON
@BP_ani.route('/get-razas', methods=['GET'])
def get_razas():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        # Consulta para obtener todas las razas
        cursor.execute("SELECT id, nom FROM razas")
        razas = cursor.fetchall()

        return jsonify(razas), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

# Ruta para obtener fincas en formato JSON
@BP_ani.route('/get-fincas', methods=['GET'])
def get_fincas():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        # Consulta para obtener todas las fincas
        cursor.execute("SELECT id, nombre FROM fincas")
        fincas = cursor.fetchall()

        return jsonify(fincas), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()