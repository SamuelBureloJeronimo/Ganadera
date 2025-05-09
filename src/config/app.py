import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

app = Flask(__name__,template_folder='../templates', static_folder='../../static')

# Cargar variables de entorno
load_dotenv()
""
# Configurar la clave secreta desde las variables de entorno
app.secret_key = os.getenv('SECRET_KEY_JWT')

# Cargar variables desde el archivo .env'load_dotenv()

    
from config.jwt_conf import jwt
from config.bp_conf import bp
from config.mail_conf import mail

app = bp

# Habilitar CORS para todos los orígenes y rutas
CORS(app)