from flask import Blueprint, redirect, render_template, request, url_for
from mysql.connector import Error
from database.db import connect_to_database

# Crear el Blueprint para manejar la búsqueda
BP_buscar = Blueprint('BP_buscar', __name__)

# Ruta para cargar el formulario de búsqueda
@BP_buscar.route('/buscar-form', methods=['GET'])
def buscar_form():
    return render_template('owner/vistas/view-ganados.html', animal=None)

# Ruta para realizar la búsqueda
@BP_buscar.route('/buscar', methods=['GET'])
def buscar():
    connection = None  # Inicializar conexión
    try:
        id = request.args.get('id')

        # Validar que el ID fue proporcionado
        if not id:
            return redirect(url_for('BP_animal.buscar_form', error="Por favor ingrese un número de arete."))

        # Conexión a la base de datos
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        # Consulta SQL para buscar el animal por ID
       # Consulta SQL para buscar el animal por ID
        query = """
            SELECT
                a.especie,
                r.nom AS raza,
                f.nombre AS finca,  -- Corregido el nombre de la columna
                a.fech,
                CASE
                    WHEN a.estado = 1 THEN 'Sano'
                    WHEN a.estado = 2 THEN 'Vendido'
                    WHEN a.estado = 3 THEN 'Muerto'
                    ELSE 'Desconocido'
                END AS estado,
                a.externo
            FROM animales a
            JOIN razas r ON a.raza_id = r.id
            JOIN fincas f ON a.finca_id = f.id
            WHERE a.id = %s;
        """
        cursor.execute(query, (id,))
        animal = cursor.fetchone()

        # Si no se encuentra el animal
        if not animal:
            return redirect(url_for('BP_buscar.buscar_form', error="No se encontró un animal con ese número de arete."))

        # Renderizar resultados
        return render_template('owner/vistas/view-ganados.html', animal=animal)
    except Error as e:
        # Manejo de errores en la base de datos
        return redirect(url_for('BP_buscar.buscar_form', error=f"Error al realizar la búsqueda: {str(e)}"))
    finally:
        if connection:
            cursor.close()
            connection.close()