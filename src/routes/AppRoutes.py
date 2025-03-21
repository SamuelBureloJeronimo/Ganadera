from flask import Blueprint, render_template
from database.db import *

from guards.SuperuserGuard import super_protected

# Cargar variables desde el archivo .env
load_dotenv()

AppRoutes = Blueprint('AppRoutes', __name__)

@AppRoutes.route('/')
def index():
    images = ["/slide/img1.png", "/slide/img2.webp", "/slide/img3.png", "/slide/img4.png"]  # Agrega más imágenes si es necesario
    return render_template("home.html", images=images)

@AppRoutes.route('/login')
def login():
    return render_template('login.html')

@AppRoutes.route('/sales')
def sales():
    return render_template('sale.html')


@AppRoutes.route('/contact')
def contact():
    return render_template('contact.html')


@AppRoutes.route('/dashboard/superuser/metrics', methods=["GET"])
@super_protected
def metrics():
    return render_template('superuser/metrics.html')

@AppRoutes.route('/dashboard/superuser/register', methods=["GET"])
@super_protected
def register():
    return render_template('superuser/register.html')

@AppRoutes.route('/dashboard/superuser/settings', methods=["GET"])
@super_protected
def settings():
    return render_template('superuser/settings.html')
