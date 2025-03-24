from collections import namedtuple
import secrets
import string
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from guards.RoutesGuards import with_session, with_transaction


BP_Veterinary = Blueprint('BP_Veterinary', __name__)

@BP_Veterinary.route('/registro_medicamento', methods=["GET", "POST"])
@jwt_required()
@with_transaction
def registro_medicamento(cursor):
    jwt_data = get_jwt()
    rfc_comp = jwt_data.get("rfc_comp")
    
    required_fields = ["id", "rfc_prov", "nom", "enf_id", "marca", "dur", "unid", "cont", "via_adm", "desc"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
      
    _id = int(request.form.get("id"))
    rfc_prov = request.form.get("rfc_prov")
    nom = request.form.get("nom")
    enf_id = request.form.get("enf_id")
    marca = request.form.get("marca")
    dur = request.form.get("dur")
    unid = request.form.get("unid")
    cont = request.form.get("cont")
    via_adm = request.form.get("via_adm")
    desc = request.form.get("desc")

    # Consulta SQL corregida
    query = """
    INSERT INTO medicamentos (id, rfc_prov, nom, enf_id, marca, dur, unid, cont, via_adm, `desc`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    # Ejecutar la consulta con los valores
    cursor.execute(query, (_id, rfc_prov, nom, enf_id, marca, dur, unid, cont, via_adm, desc))
    
    return jsonify({"success": True, "msg": "Medicamento registrado"}), 200

@BP_Veterinary.route('/registro_alimento',methods=["GET","POST"])
@jwt_required()
@with_transaction
def registro_alimento(cursor):
    jwt_data = get_jwt()
    rfc_comp = jwt_data.get("rfc_comp")
    
    required_fields = ["id", "nombre", "tipo", "calorias", "costo_kg_lt"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
      
    
    id = request.form.get("id")
    nombre=request.form.get("nombre")
    tipo=request.form.get("tipo")
    calorias=request.form.get("calorias")
    costo_kg_lt=request.form.get("costo_kg_lt")
    
    # Consulta SQL corregida
    query = """
    INSERT INTO alimentos (id, nombre, tipo, calorias, costo_kg_lt)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    # Ejecutar la consulta con los valores
    cursor.execute(query, (id, nombre, tipo, calorias, costo_kg_lt))
    
    return jsonify({"success": True, "msg": "Alimento registrado"}), 200
  
@BP_Veterinary.route('/registro_insumo',methods=["GET","POST"])
@jwt_required()
@with_transaction
def registro_insumo(cursor):
    wt_data = get_jwt()
    
    
    required_fields = ["id", "tipo", "rfc_prov", "fech", "cantidad","precio_u","estatus","observ"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
      
    
    id = request.form.get("id")
    tipo=request.form.get("tipo")
    rfc_prov=request.form.get("rfc_prov")
    fech=request.form.get("fech")
    cantidad=request.form.get("cantidad")
    precio_u=request.form.get("precio_u")
    estatus=request.form.get("estatus")
    observ=request.form.get("observ")
    
    # Consulta SQL corregida
    query = """
    INSERT INTO compras_insumos (id, tipo,rfc_prov,fech,cantidad,precio_u,estatus,observ)
    VALUES (%s, %s, %s, %s,%s, %s, %s, %s);
    """
    
    # Ejecutar la consulta con los valores
    cursor.execute(query, (id, tipo,rfc_prov,fech,cantidad,precio_u,estatus,observ))
    
    return jsonify({"success": True, "msg": "Alimento registrado"}), 200