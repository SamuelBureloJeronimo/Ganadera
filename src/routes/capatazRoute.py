from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session
import jwt
from database.db import *
from config.jwt_conf import SECRET_KEY
from datetime import datetime
from guards.RoutesGuards import with_session
from flask_jwt_extended import jwt_required, get_jwt_identity

BP_Capataz = Blueprint('BP_Capataz', __name__ )

@BP_Capataz.route('/capataz/registrar-actividad', methods=["GET", "POST"])
@with_session
def registrar_actividad(cursor=None, db=None):  # <-- Asegúrate de recibir db si tu decorador lo permite
    try:
        # Obtener el RFC del capataz desde el token
        token = request.cookies.get('token')
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        rfc_capataz = decoded_token.get('rfc_cap')
        rfc_comp = decoded_token.get('rfc_comp')
        
        # Consulta modificada para obtener solo los jornaleros de la misma finca que el capataz
        query_jornaleros = """
            SELECT p.rfc, p.nombre, p.app, p.apm
            FROM personas p
            INNER JOIN usuarios u ON p.rfc = u.rfc
            INNER JOIN empleados e ON p.rfc = e.rfc
            WHERE e.puesto_id = 3 
            AND u.rfc_comp = %s
        """
        cursor.execute(query_jornaleros, [rfc_comp])
        jornaleros = cursor.fetchall()

        if request.method == "GET":
            return render_template('capataz/registrar_actividad.html', 
                                  jornaleros=jornaleros,
                                  rfc_capataz=rfc_capataz,
                                  rfc_comp=rfc_comp)
        elif request.method == "POST":
            titulo = request.form.get('titulo')
            desc = request.form.get('desc')
            observ = request.form.get('observ')
            fech_fi = request.form.get('fech_fi')
            rfc_jor = request.form.get('rfc_jor')
            error = False
            if not rfc_capataz:
                flash('Error: El token no contiene el RFC del capataz (rfc_cap).', 'danger')
                error = True
            elif not (titulo and desc and fech_fi and rfc_jor):
                flash('Todos los campos obligatorios deben ser completados.', 'danger')
                error = True
            else:
                fech_in = datetime.now().date()
                try:
                    query_insert = """
                        INSERT INTO actividades (rfc_cap, rfc_jor, titulo, `desc`, fech_in, fech_fi, estado, observ)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_insert, (rfc_capataz, rfc_jor, titulo, desc, fech_in, fech_fi, 0, observ))
                    
                    # Confirmar cambios
                    if db:
                        db.commit()
                    else:
                        cursor.connection.commit()
                    flash('Actividad creada y asignada exitosamente.','success')
                    return redirect('/capataz/ver-actividades')
                except Exception as e:
                    flash(f'Error al insertar actividad: {str(e)}', 'danger')
                    error = True
            # Si hubo error, mostrar el formulario de nuevo con jornaleros y mensajes
            return render_template('capataz/registrar_actividad.html', 
                                  jornaleros=jornaleros,
                                  rfc_capataz=rfc_capataz,
                                  rfc_comp=rfc_comp)
    except Exception as e:
        flash(f'Error al procesar la solicitud: {str(e)}', 'danger')
        return render_template('capataz/registrar_actividad.html', jornaleros=[], rfc_capataz=None, rfc_comp=None)

@BP_Capataz.route('/capataz/ver-actividades', methods=["GET"])
@with_session
def ver_actividades(cursor=None): # Nombre de la función coincide con url_for
    try:
    
        token = request.cookies.get('token')
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        rfc_capataz = decoded_token.get('rfc_cap')
        
        flash(f"RFC del Capataz (desde token): {rfc_capataz}", "info") # Mensaje de depuración

        # Lógica para obtener y filtrar actividades
        filtro_estado = request.args.get('filter', 'all')
        
        query_base = """SELECT a.*, p_jor.nombre as nombre_jor, p_jor.app as app_jor, p_jor.apm as apm_jor
         FROM actividades 
         a JOIN personas p_jor ON a.rfc_jor = p_jor.rfc WHERE a.rfc_cap = %s"""
        params = [rfc_capataz]
        
        if filtro_estado == 'pending':
            query_base += " AND a.estado = 0"
        elif filtro_estado == 'completed':
            query_base += " AND a.estado = 1"
        elif filtro_estado == 'reviewed':
            query_base += " AND a.estado = 2"
        elif filtro_estado == 'inconclusa': # Asumiendo que 3 es inconclusa
            query_base += " AND a.estado = 3"
            
        query_base += " ORDER BY a.fech_fi DESC, a.id DESC"
        
        flash(f"Consulta SQL: {query_base}", "info") # Mensaje de depuración
        flash(f"Parámetros SQL: {params}", "info") # Mensaje de depuración

        cursor.execute(query_base, params)
        actividades = cursor.fetchall()
        
        flash(f"Actividades encontradas: {len(actividades)}", "info") # Mensaje de depuración
        if not actividades:
            flash("La lista de actividades está vacía después de la consulta.", "warning") # Mensaje de depuración
        else:
            flash(f"Primer actividad (muestra): {str(actividades[0]) if actividades else 'N/A'}", "debug")


        return render_template('capataz/ver_actividades.html', actividades=actividades, filter=filtro_estado)

    except Exception as e:
        flash(f'Error al cargar las actividades: {str(e)}', 'danger')
        return render_template('capataz/ver_actividades.html', actividades=[], filter='all')

# Mantener la ruta original para compatibilidad
@BP_Capataz.route('/capataz/actividades', methods=["GET", "POST"])
@with_session
def actividades_capataz(cursor):
    if request.method == "POST":
       
        return redirect('/capataz/registrar-actividad')
    else:
      
        return redirect('/capataz/ver-actividades')
