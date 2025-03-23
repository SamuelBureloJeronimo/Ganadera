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

# Ruta para mostrar el formulario de registro de animales con opciones de raza y finca
@BP_ani.route('/animal', methods=['GET'])
def animal():
    connection = None  # Inicializar la variable
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id, nom FROM razas")
        razas = cursor.fetchall()

        cursor.execute("SELECT id, nombre FROM fincas")
        fincas = cursor.fetchall()

        return render_template('animal.html', razas=razas, fincas=fincas)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:  # Verificar si la conexión fue establecida
            cursor.close()
            connection.close()

@BP_ani.route('/animal/registro', methods=['POST'])
def register_animal():
    connection = None  # Inicializar la variable
    try:
        data = request.form

        required_fields = ["id","especie", "raza_id", "sexo", "finca_id", "fech", "estado", "externo"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

        connection = connect_to_database()
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO animales (id,especie, raza_id, sexo, finca_id, fech, estado, externo)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            data["id"],data["especie"], data["raza_id"], data["sexo"], 
            data["finca_id"], data["fech"], data["estado"], data["externo"]
        ))
        connection.commit()
         # Redirigir al formulario después del registro exitoso
        return redirect(url_for('BP_ani.animal', success="Animal registrado exitosamente"))
    except Error as e:
        # Enviar un mensaje de error al formulario en caso de excepción.
        
        return redirect(url_for('BP_ani.animal', error=str(e)))    
    finally:
        if connection:  # Verificar si la conexión fue establecida
            cursor.close()
            connection.close()
