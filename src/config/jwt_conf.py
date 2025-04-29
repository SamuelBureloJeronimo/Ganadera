from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from config.app import app
import os

# Cargar variables desde el archivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_JWT")

# Configuración de la clave secreta para JWT
app.config["JWT_SECRET_KEY"] = SECRET_KEY  # Cambia esto en producción
jwt = JWTManager(app)
