from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session
import jwt
from database.db import *
from config.jwt_conf import SECRET_KEY
from datetime import datetime
from guards.RoutesGuards import with_session
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

BP_Jornalero = Blueprint('BP_Jornalero', __name__ )

# src/routes/JornaleroRoutes.py
@BP_Jornalero.route('/ver_actividades', methods=['GET'])
@with_session
def ver_actividades(cursor):
    """
    Muestra las actividades asignadas al jornalero (rol 3),
    con opción de filtrar por estado via ?filter=pending|completed|reviewed|inconclusa.
    """
    filtro = request.args.get('filter', 'today')
    actividades = []

    # 1) Leer y validar token
    token = request.cookies.get('token')
    if not token:
        flash("Debe iniciar sesión para ver sus actividades.", "warning")
        return render_template(
            'jornalero/activities.html',
            actividades=[],
            filter=filtro,
            es_jornalero=False,
            hoy=date.today()
        )

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        flash("Token inválido o expirado.", "danger")
        return render_template(
            'jornalero/activities.html',
            actividades=[],
            filter=filtro,
            es_jornalero=False,
            hoy=date.today()
        )

    # 2) Verificar rol = 3 (jornalero) o 4 (veterinario) y obtener su RFC
    rol = int(decoded.get('rol', -1))
    if rol == 3:
        rfc_usuario = decoded.get('rfc_jor') or decoded.get('rfc') or decoded.get('rfc_cap')
    elif rol == 4:
        rfc_usuario = decoded.get('rfc_vet') or decoded.get('rfc')
    else:
        flash("No tienes permiso para ver esta sección.", "danger")
        return redirect(url_for('BP_PublicRoutes.login_user'))

    print("TOKEN DECODED:", decoded)
    print("RFC USUARIO USADO:", rfc_usuario)
    if not rfc_usuario:
        flash("No se encontró tu RFC en el token.", "danger")
        return render_template(
            'jornalero/activities.html',
            actividades=[],
            filter=filtro,
            es_jornalero=False,
            hoy=date.today()
        )

    # 3) Construir consulta SQL
    sql = """
        SELECT
          a.id,
          a.titulo,
          a.`desc`    AS descripcion,
          a.observ,
          a.estado,
          a.fech_in,
          a.fech_fi,
          pc.nombre AS nombre_capataz,
          pc.app AS apellido_capataz
        FROM actividades a
        LEFT JOIN personas pc ON a.rfc_cap = pc.rfc
        WHERE a.rfc_jor = %s
    """
    params = [rfc_usuario]

    estados = {
        'pending':    0,
        'completed':  1,
        'reviewed':   2,
        'inconclusa': 3
    }
    if filtro == 'today':
        hoy = date.today()
        sql += " AND (DATE(a.fech_in) <= %s AND DATE(a.fech_fi) >= %s) AND a.estado = 0"
        params.append(hoy)
        params.append(hoy)
     
    elif filtro in estados:
        sql += " AND a.estado = %s"
        params.append(estados[filtro])
    sql += " ORDER BY a.fech_fi ASC"

    # 4) Ejecutar y obtener resultados
    try:
        cursor.execute(sql, tuple(params))
        actividades = cursor.fetchall()
        print("ACTIVIDADES ENCONTRADAS:", actividades)
    except Exception as e:
        flash(f"Error al cargar actividades: {e}", "danger")
        actividades = []

    # 5) Formatear fechas y renombrar campo
    actividades_formateadas = []
    for act in actividades:
        act_dict = {
            'id': act[0],
            'titulo': act[1],
            'desc': act[2],
            'observ': act[3],
            'estado': act[4],
            'fech_in': act[5].strftime('%d/%m/%Y') if act[5] else '',
            'fech_fi': act[6].strftime('%d/%m/%Y') if act[6] else '',
            'nombre_capataz': act[7],
            'apellido_capataz': act[8]
        }
        actividades_formateadas.append(act_dict)

    # 6) Renderizar
    return render_template(
        'jornalero/activities.html',
        actividades=actividades_formateadas,
        filtro=request.args.get('filter', 'today'),  
        es_jornalero=True,
        hoy=date.today().strftime('%d/%m/%Y') 
    )


@BP_Jornalero.route('/actividades/<int:actividad_id>/completar', methods=["POST"])
@with_session
def completar_actividad(cursor, actividad_id):
    try:
        # Verificar autenticación
        token = request.cookies.get('token')
        if not token:
            flash('No se encontró el token de autenticación.', 'danger')
            return redirect(url_for('BP_Jornalero.ver_actividades'))
            
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        rol_usuario = int(decoded_token.get('rol', 0))
        
        # Obtener el RFC correcto según el rol
        if rol_usuario == 3:  # Jornalero
            rfc_usuario = decoded_token.get('rfc_jor') or decoded_token.get('rfc') or decoded_token.get('rfc_cap')
        elif rol_usuario == 4:  # Veterinario
             rfc_usuario = decoded_token.get('rfc_vet') or decoded_token.get('rfc')
        else:
            flash('Solo los jornaleros y veterinarios pueden marcar actividades como realizadas.', 'warning')
            return redirect(url_for('BP_Jornalero.ver_actividades'))

        # Verificar que la actividad pertenece al usuario
        cursor.execute("SELECT id FROM actividades WHERE id=%s AND rfc_jor=%s", (actividad_id, rfc_usuario))
        actividad = cursor.fetchone()
        if not actividad:
            flash('No tienes permiso para modificar esta actividad.', 'danger')
            return redirect(url_for('BP_Jornalero.ver_actividades'))

        # Actualizar estado
        cursor.execute("UPDATE actividades SET estado=%s WHERE id=%s", (1, actividad_id,))
        flash('Actividad marcada como realizada.', 'success')
    except Exception as e:
        flash(f'Error al marcar actividad: {str(e)}', 'danger')
    return redirect(url_for('BP_Jornalero.ver_actividades'))