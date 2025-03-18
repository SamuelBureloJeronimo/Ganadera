import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Cargar variables desde el archivo .env
load_dotenv()

# Leer variables del entorno
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# Configuración de la conexión a la base de datos MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,  # Cambia esto por la dirección de tu servidor MySQL
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error al conectar a la base de datos", e)
        return None