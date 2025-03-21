from collections import namedtuple
import random
from dotenv import load_dotenv
from flask import Blueprint, jsonify, render_template, request, send_from_directory
from database.db import connect_to_database
from config.mail_conf import mail
import os
from mysql.connector import Error 

BP_raza= Blueprint('BP_raza',__name__)

@BP_raza.route('/raza')
def razas():
    return render_template('raza.html')