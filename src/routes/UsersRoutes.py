from flask import Blueprint, request, jsonify
from database.db import *

import os

# Cargar variables desde el archivo .env
load_dotenv()

BP_UsersRoutes = Blueprint('BP_UsersRoutes', __name__, url_prefix='/user')
