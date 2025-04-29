from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session
import jwt
from database.db import *
from config.jwt_conf import SECRET_KEY
from datetime import datetime
from guards.RoutesGuards import with_session

BP_Jornalero = Blueprint('BP_Jornalero', __name__ )

@BP_Jornalero.route('/ver_actividades', methods=["GET", "POST"])
@with_session
def ver_actividades(cursor):
    filter = request.args.get('filter', 'all')

    try:
        # Verificar autenticación
        token = request.headers.get('Authorization').split(" ")[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        rfc_usuario = decoded_token.get('rfc')
        rol_usuario = decoded_token.get('role')  # Ahora es un número (ej: 2 para capataz)
        es_capataz = (rol_usuario == 2)  # Verificar si el rol es capataz

        # Si es POST y es capataz, procesar el formulario de creación
        if request.method == 'POST' and es_capataz:
            # ... (código para insertar actividad, igual que antes)

        # Consulta dinámica
            query = "SELECT id, titulo, desc, estado, fech_in, fech_fi, rfc_cap, rfc_jor FROM actividades WHERE "
            params = []

        if es_capataz:
            query += "rfc_cap = %s"  # Actividades asignadas POR el capataz
            params.append(rfc_usuario)

            if filter == 'pending':
                query += " AND estado = 'pendiente'"
            elif filter == 'completed':
                query += " AND estado = 'completada'"
            elif filter == 'reviewed':
                query += " AND estado = 'revisada'"
        else:
            query += "rfc_jor = %s"  # Actividades asignadas AL usuario
            params.append(rfc_usuario)

            if filter == 'pending':
                query += " AND estado = 'pendiente'"
            elif filter == 'completed':
                query += " AND estado = 'completada'"

        # ... (resto del código: ordenamiento, renderizado)
        
        return render_template('jornalero/activities.html', 
                               actividades=actividades,
                               filter=filter,
                               es_capataz=es_capataz,  # Enviar variable es_capataz en lugar de es_asignador
                               hoy=hoy)

    except Exception as e:
        flash(f'Error al cargar actividades: {str(e)}', 'danger')
        return render_template('jornalero/activities.html', actividades=[], filter=filter)