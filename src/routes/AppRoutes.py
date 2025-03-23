from flask import Blueprint, render_template, request
from database.db import *

from guards.RoutesGuards import owner_protected, super_protected

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

# RUTAS PARA EL SUPERUSUARIO

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

# RUTAS PARA EL DUEÑO
@AppRoutes.route('/dashboard/owner/panel', methods=["GET", "POST"])
@owner_protected
def panel(decoded):
    return render_template('owner/panel.html')

@AppRoutes.route('/dashboard/owner/register-ganado', methods=["GET", "POST"])
@owner_protected
def regis_ganado(decoded):
    return render_template('owner/registros/regis-ganados.html')

@AppRoutes.route('/dashboard/owner/register-employee', methods=["GET", "POST"])
@owner_protected
def regis_employee(decoded):
    return render_template('owner/registros/regis-empleados.html')

@AppRoutes.route('/dashboard/owner/register-finca', methods=["GET", "POST"])
@owner_protected
def regis_finca(decoded):
    return render_template('owner/registros/regis-fincas.html')



@AppRoutes.route('/dashboard/owner/view-ganados', methods=["GET", "POST"])
@owner_protected
def view_ganados(decoded):
    return render_template('owner/vistas/view-ganados.html')

@AppRoutes.route('/dashboard/owner/view-fincas', methods=["GET", "POST"])
@owner_protected
def view_fincas(decoded):
    return render_template('owner/vistas/view-fincas.html')

@AppRoutes.route('/dashboard/owner/view-employees', methods=["GET", "POST"])
@owner_protected
def view_employees(decoded):
    return render_template('owner/vistas/view-employees.html')




# RUTAS PARA EMPLEADOS
@AppRoutes.route('/dashboard/empleoyes/panelEmpleados', methods=["GET", "POST"])
def panelEmpleados():
    return render_template('empleoyes/panel.html')