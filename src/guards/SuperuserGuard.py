from functools import wraps
import os
from dotenv import load_dotenv
import jwt
from mysql.connector import Error
from flask import jsonify, redirect, request

from database.db import connect_to_database

# Cargar variables desde el archivo .env
load_dotenv()

def with_transaction(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Conectar a la base de datos
            conn = connect_to_database()
            if conn is None:
                return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
            
            print("Sesión ABIERTA");
            
            # Desactivar autocommit y crear el cursor
            conn.autocommit = False
            cursor = conn.cursor()

            # Iniciar la transacción
            conn.start_transaction()

            response = f(cursor, *args, **kwargs)  # Pasamos el cursor
            print("Se confirmarón los CAMBIOS");
            conn.commit()
            return response
        except Error as e:
            print(str(e))
            # Revertir cambios si ocurre un error
            print("ROLLBACK aplicado");
            conn.rollback()
            return jsonify({"error": "Error de integridad en la base de datos.", "detalle": str(e)}), 400
        
        finally:
            # Cerrar cursor y conexión
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            print("Sesión Cerrada");
    return decorated_function

def with_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Conectar a la base de datos
            conn = connect_to_database()
            if conn is None:
                return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
            
            print("Sesión ABIERTA");
            
            # Crear el cursor
            cursor = conn.cursor()

            response = f(cursor, *args, **kwargs)  # Pasamos el cursor
            return response
        except Error as e:
            print(str(e))
            return jsonify({"error": "Error de integridad en la base de datos.", "detalle": str(e)}), 400
        
        finally:
            # Cerrar cursor y conexión
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            print("Sesión Cerrada");
    return decorated_function


def super_protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.cookies.get("token")  # Leer token desde la cookie
            decoded = jwt.decode(token, os.getenv("SECRET_KEY_JWT"), algorithms=["HS256"])
            print(decoded)
            if(decoded['rol'] != str(-1)):
                return redirect('/')
            
            response = f(*args, **kwargs)
            return response
        
        except jwt.ExpiredSignatureError:
            return redirect('/')

        except jwt.InvalidTokenError:
            return redirect('/')

    return decorated_function


def super_protected_Route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.cookies.get("token")  # Leer token desde la cookie
            decoded = jwt.decode(token, os.getenv("SECRET_KEY_JWT"), algorithms=["HS256"])
            print(decoded)
            if(decoded['rol'] != str(-1)):
                return redirect('/')
            
            response = f(*args, **kwargs)
            return response
        
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401  # Código 401 para indicar expiración

        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401  # También un 401 en caso de token no válido

    return decorated_function