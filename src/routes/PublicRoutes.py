from flask import Blueprint, render_template, request, jsonify, send_from_directory
from database.db import *

import os

# Cargar variables desde el archivo .env
load_dotenv()

BP_PublicRoutes = Blueprint('BP_PublicRoutes', __name__, url_prefix='/')

@BP_PublicRoutes.route('/img/<path:filename>')
def public_files(filename):
    return send_from_directory(os.getenv("UPL_FOL_ROUTES"), filename)

@BP_PublicRoutes.route('/')
def index():
    return render_template('index.html')