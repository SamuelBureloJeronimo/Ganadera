from collections import namedtuple
import random
from dotenv import load_dotenv
from flask import Blueprint, jsonify, render_template, request, send_from_directory
from database.db import connect_to_database
from config.mail_conf import mail
import os
from mysql.connector import Error

# Cargar variables de entorno
load_dotenv()

BP_ani = Blueprint('BP_ani', __name__)

# Ruta para servir imágenes de animales
@BP_ani.route('/img/<path:filename>')
def public_file(filename):
    return send_from_directory(os.getenv("UPL_FOL_ROUTES"), filename)

# Ruta para mostrar el formulario de registro de animales
@BP_ani.route('/animal', methods=['GET'])
def animal():
    return render_template('animal.html')

# Ruta para registrar un nuevo animal
@BP_ani.route('/animal', methods=['POST'])
def register_animal():
    try:
        data = request.get_json()
        required_fields = ["arete", "raza", "sexo", "aspiracion"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
        
        connection = connect_to_database()
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO ganado (arete, raza, sexo, aspiracion)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (data["arete"], data["raza"], data["sexo"], data["aspiracion"]))
        connection.commit()
        cursor.close()
        return jsonify({"success": True, "message": "Animal registrado exitosamente"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener la lista de animales
@BP_ani.route('/animales', methods=['GET'])
def get_animales():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ganado")
        animales = cursor.fetchall()
        cursor.close()
        return jsonify(animales), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener un animal por ID
@BP_ani.route('/animales/<int:arete>', methods=['GET'])
def get_animal(arete):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ganado WHERE arete = %s", (arete,))
        animal = cursor.fetchone()
        cursor.close()
        
        if not animal:
            return jsonify({"error": "Animal no encontrado"}), 404
        
        return jsonify(animal), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar un animal
@BP_ani.route('/animales/<int:arete>', methods=['PUT'])
def update_animal(arete):
    try:
        data = request.get_json()
        connection = connect_to_database()
        cursor = connection.cursor()
        update_query = """
            UPDATE ganado
            SET raza = %s, sexo = %s, aspiracion = %s
            WHERE arete = %s;
        """
        cursor.execute(update_query, (data["raza"], data["sexo"], data["aspiracion"], arete))
        connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Animal actualizado exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un animal
@BP_ani.route('/animales/<int:arete>', methods=['DELETE'])
def delete_animal(arete):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM ganado WHERE arete = %s", (arete,))
        connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Animal eliminado exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
