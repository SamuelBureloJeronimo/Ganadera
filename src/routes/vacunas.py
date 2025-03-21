from collections import namedtuple
import random
from dotenv import load_dotenv
from flask import Blueprint, jsonify, render_template, request, send_from_directory
from database.db import connect_to_database
from config.mail_conf import mail
import os
from mysql.connector import Error

# Cargar variables de entorno
load_dotenv()

BP_vacuna = Blueprint('BP_vacuna',__name__)

@BP_vacuna.route('/')
def vacuna ():
    return render_template('vacuna.html') 