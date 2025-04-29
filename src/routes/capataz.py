from flask import Blueprint, request, redirect, render_template, url_for, flash, jsonify
from mysql.connector import Error
from database.db import connect_to_database
from datetime import datetime

BP_capataz = Blueprint('BP_capataz', __name__)

# Ruta para obtener información del capataz
@BP_capataz.route('/datos-capataz', methods=['GET'])
def obtener_datos_capataz():
    connection = None
    try:
        rfc_cap = request.args.get('rfc_cap')
        if not rfc_cap:
            return jsonify({"error": "RFC del capataz requerido."}), 400

        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT e.rfc, p.nombre, ps.nombre AS cargo, f.nombre AS finca
            FROM empleados e
            JOIN personas p ON e.rfc = p.rfc
            JOIN puestos ps ON e.puesto_id = ps.id
            JOIN fincas f ON e.finca_id = f.id
            WHERE e.rfc = %s AND ps.nombre = 'Capataz';
        """
        cursor.execute(query, (rfc_cap,))
        datos_capataz = cursor.fetchone()

        if not datos_capataz:
            return jsonify({"error": "No se encontró información del capataz."}), 404

        return jsonify(datos_capataz), 200
    except Error as e:
        return jsonify({"error": f"Error al obtener datos del capataz: {str(e)}"}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

# Ruta para crear actividad
@BP_capataz.route('/crear', methods=['GET', 'POST'])
def crear_actividad():
    connection = None
    if request.method == 'GET':
        return render_template('capataz/act/crear-actividades.html')

    if request.method == 'POST':
        try:
            data = request.form

            if not all([data.get("rfc_cap"), data.get("titulo"), data.get("fech_in"), data.get("fech_fi")]):
                flash("Por favor complete todos los campos.", "error")
                return redirect(url_for('BP_capataz.crear_actividad'))

            fech_in = datetime.strptime(data.get("fech_in"), "%Y-%m-%d")
            fech_fi = datetime.strptime(data.get("fech_fi"), "%Y-%m-%d")
            if fech_in > fech_fi:
                flash("La fecha de inicio debe ser anterior a la fecha de finalización.", "error")
                return redirect(url_for('BP_capataz.crear_actividad'))

            connection = connect_to_database()
            cursor = connection.cursor()

            query = """
                INSERT INTO actividades (rfc_cap, titulo, `desc`, fech_in, fech_fi, estado)
                VALUES (%s, %s, %s, %s, %s, 0)
            """
            cursor.execute(query, (
                data["rfc_cap"], data["titulo"], data.get("desc", None),
                data["fech_in"], data["fech_fi"]
            ))
            connection.commit()

            flash("Actividad creada exitosamente.", "success")
            return redirect(url_for('BP_capataz.listar_actividades'))
        except Error as e:
            flash(f"Error al crear actividad: {str(e)}", "error")
            return redirect(url_for('BP_capataz.listar_actividades'))
        finally:
            if connection:
                cursor.close()
                connection.close()

# Ruta para listar actividades
@BP_capataz.route('/listar', methods=['GET'])
def listar_actividades():
    connection = None
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id, rfc_cap, rfc_jor, titulo, `desc`, fech_in, fech_fi, estado
            FROM actividades
        """
        cursor.execute(query)
        actividades = cursor.fetchall()

        return render_template('capataz/act/listar-actividades.html', actividades=actividades)
    except Error as e:
        flash(f"Error al listar actividades: {str(e)}", "error")
        return redirect(url_for('BP_capataz.listar_actividades'))
    finally:
        if connection:
            cursor.close()
            connection.close()

# Ruta para asignar empleado a actividad
@BP_capataz.route('/asignar', methods=['GET', 'POST'])
def asignar_empleado():
    connection = None
    if request.method == 'GET':
        return render_template('capataz/act/asignar-actividades.html')

    if request.method == 'POST':
        try:
            data = request.form
            actividad_id = data.get("actividad_id")
            rfc_jor = data.get("rfc_jor")
            finca_id = data.get("finca_id")

            if not all([actividad_id, rfc_jor, finca_id]):
                flash("Debe especificarse actividad, empleado y finca.", "error")
                return redirect(url_for('BP_capataz.listar_actividades'))

            connection = connect_to_database()
            cursor = connection.cursor(dictionary=True)

            query_verificar = """
                SELECT 1 FROM empleados WHERE rfc = %s AND finca_id = %s AND estatus = 1
            """
            cursor.execute(query_verificar, (rfc_jor, finca_id))
            if not cursor.fetchone():
                flash("El empleado no pertenece a la finca o no está activo.", "error")
                return redirect(url_for('BP_capataz.listar_actividades'))

            query_asignar = "UPDATE actividades SET rfc_jor = %s WHERE id = %s"
            cursor.execute(query_asignar, (rfc_jor, actividad_id))
            connection.commit()

            flash("Empleado asignado correctamente.", "success")
            return redirect(url_for('BP_capataz.listar_actividades'))
        except Error as e:
            flash(f"Error al asignar empleado: {str(e)}", "error")
            return redirect(url_for('BP_capataz.listar_actividades'))
        finally:
            if connection:
                cursor.close()
                connection.close()

# Ruta para confirmar actividad
@BP_capataz.route('/confirmar/<int:actividad_id>/<int:nuevo_estado>', methods=['POST'])
def confirmar_actividad(actividad_id, nuevo_estado):
    connection = None
    try:
        if nuevo_estado not in [2, 3]:
            flash("Estado no válido.", "error")
            return redirect(url_for('BP_capataz.listar_actividades'))

        connection = connect_to_database()
        cursor = connection.cursor()

        query = "UPDATE actividades SET estado = %s WHERE id = %s"
        cursor.execute(query, (nuevo_estado, actividad_id))
        connection.commit()

        mensaje = "Actividad marcada como Verificada." if nuevo_estado == 2 else "Actividad marcada como Inconclusa."
        flash(mensaje, "success")
        return redirect(url_for('BP_capataz.listar_actividades'))
    except Error as e:
        flash(f"Error al confirmar actividad: {str(e)}", "error")
        return redirect(url_for('BP_capataz.listar_actividades'))
    finally:
        if connection:
            cursor.close()
            connection.close()
