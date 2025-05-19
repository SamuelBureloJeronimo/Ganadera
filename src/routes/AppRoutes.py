from flask import Blueprint, render_template, request
from database.db import *
from guards.RoutesGuards import owner_protected, super_protected, with_session, veterinary_protected
from routes.GeneralRoutes import convertToObject
from flask import redirect, url_for

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
  
#RUTAS PARA EL VETERINARIO
@AppRoutes.route('/dashboard/veterinary/panel', methods=["GET", "POST"])
@veterinary_protected
def panel_veterinary(decoded):
    return render_template('veterinary/panel.html')

@AppRoutes.route('/dashboard/veterinary/register-medicamento',methods=["GET", "POST"])
@veterinary_protected
def regis_medicamentos(decoded):
    return render_template('veterinary/registros/regis-medicamento.html')
  
@AppRoutes.route('/dashboard/veterinary/register-alimento',methods=["GET","POST"])
@veterinary_protected
def regis_alimentos(decoded):
    return render_template('veterinary/registros/regis-alimento.html')

@AppRoutes.route('/dashboard/veterinary/register-insumo',methods=["GET","POST"])
@veterinary_protected
def regis_insumos(decoded):
  return render_template('veterinary/registros/regis-insumo.html')
  
@AppRoutes.route('/dashboard/veterinary/register-tratamiento',methods=["GET","POST"])
@veterinary_protected
def regis_tratamiento(decoded):
    return render_template('veterinary/registros/regis-tratamiento.html')
  
@AppRoutes.route('/dashboard/veterinary/register-chequeo',methods=["GET","POST"])
@veterinary_protected
def regis_chequeo(decoded):
    return render_template('veterinary/registros/regis-chequeo.html')

# RUTAS PARA EL DUEÑO
@AppRoutes.route('/dashboard/owner/salud-general', methods=["GET", "POST"])
@owner_protected
@with_session
def panel(cursor, decoded):
    query = "SELECT id, nombre FROM fincas WHERE rfc_comp=%s;"
    cursor.execute(query, (decoded['rfc_comp'],))
    fincas = convertToObject(cursor)
    print(fincas)
    return render_template('owner/salud_general/salud_general.html', fincas=fincas)

@AppRoutes.route('/dashboard/owner/contabilidad', methods=["GET", "POST"])
@owner_protected
def conta_own(decoded):
    return render_template('owner/contabilidad/contabilidad.html')

@AppRoutes.route('/dashboard/owner/administracion', methods=["GET", "POST"])
@owner_protected
def admin_own(decoded):
    return render_template('owner/admin/admin.html')

@AppRoutes.route('/dashboard/owner/register-ganado', methods=["GET", "POST"])
@owner_protected
def regis_ganado(decoded):
    return render_template('owner/registros/regis-ganados.html')



@AppRoutes.route('/dashboard/owner/register-finca', methods=["GET", "POST"])
@owner_protected
def regis_finca(decoded):
    return render_template('owner/admin/fincas/regis.html')

@AppRoutes.route('/dashboard/owner/register-razas', methods=["GET", "POST"])
@owner_protected
def regis_razas(decoded):
    return render_template('owner/registros/regis-fincas.html')

@AppRoutes.route('/dashboard/owner/regis-razas', methods=["GET", "POST"])
@owner_protected
def conf_puestos(decoded):
    return render_template('owner/admin/razas/regis.html')

@AppRoutes.route('/dashboard/owner/razas', methods=["GET", "POST"])
@with_session
def razas(cursor):

    query = "SELECT * FROM razas;"
    cursor.execute(query)
    razas = convertToObject(cursor)

    return render_template('owner/admin/razas/view.html', razas=razas)



@AppRoutes.route('/dashboard/owner/view-ganados', methods=["GET", "POST"])
@owner_protected
def view_ganados(decoded):
    return render_template('owner/vistas/view-ganados.html')

@AppRoutes.route('/dashboard/owner/view-fincas', methods=["GET", "POST"])
@owner_protected
@with_session
def view_fincas(cursor, decoded):
    query = "SELECT * FROM fincas WHERE rfc_comp=%s;"
    cursor.execute(query, (decoded['rfc_comp'],))
    fincas = convertToObject(cursor)
    for finca in fincas:
        query = "SELECT nom, mun_id, cp FROM colonias WHERE id=%s;"
        cursor.execute(query, (finca["id_colonia"],))
        colonia = cursor.fetchone()
        
        query = "SELECT nom, est_id FROM municipios WHERE id=%s;"
        cursor.execute(query, (colonia[1],))
        mun = cursor.fetchone()

        query = "SELECT nom FROM estados WHERE id=%s;"
        cursor.execute(query, (mun[1],))
        estado = cursor.fetchone()

        direccion = mun[0] + ", " + estado[0] + ". CP: " + str(colonia[2]) + ". "+ colonia[0] +"."

        finca["id_colonia"] = {"name": direccion, "id": finca["id_colonia"]}
    print(fincas)
    return render_template('owner/admin/fincas/view.html', fincas=fincas)






@AppRoutes.route('/dashboard/owner/config-puestos', methods=["GET","POST"])
@owner_protected
def config_puestos(decoded):
    return render_template('owner/admin/puestosYsalarios/conf-puestos.html')

@AppRoutes.route('/dashboard/owner/panel_empleados', methods=["GET","POST"])
@owner_protected
def panel_empleados(decoded):
    return render_template('owner/trabajadores/trab.html')

@AppRoutes.route('/dashboard/owner/view-employees', methods=["GET", "POST"])
@owner_protected
def view_employees(decoded):
    return render_template('owner/trabajadores/listar/view-employees.html')

@AppRoutes.route('/dashboard/owner/register-employee', methods=["GET", "POST"])
@owner_protected
def regis_employee(decoded):
    return render_template('owner/trabajadores/regis/regis-empleados.html')




@AppRoutes.route("/dashboard/owner/animales",methods=["GET","POST"])
@owner_protected
def view_animal(decoded):
    return render_template('owner/vistas/view-animal.html')

# RUTAS PARA EMPLEADOS
@AppRoutes.route('/dashboard/empleoyes/panelEmpleados', methods=["GET", "POST"])
def panelEmpleados():
    return render_template('contability/panel.html')


#RUTAS PARA JORNALERO
@AppRoutes.route('/dashboard/jornalero/panelJornalero', methods=["GET", "POST"])
def panelJornalero():
    return render_template('jornalero/dash.html')

@AppRoutes.route('/dashboard/jornalero/actividades', methods=["GET", "POST"])
def actividades():
    return redirect('/ver_actividades')

@AppRoutes.route('/dashboard/jornalero/asistencias', methods=["GET", "POST"])
def asistencias():
    return render_template('jornalero/asistencias.html')

# RUTAS PARA CAPATAZ
@AppRoutes.route('/dashboard/capataz/panelCapataz', methods=["GET", "POST"])
def panelCapataz():
    return redirect(url_for('BP_Capataz.actividades_capataz'))

@AppRoutes.route('/dashboard/capataz/registraracti', methods=["GET", "POST"])
def registraractividades():
    return render_template('capataz/registrar_actividades.html')