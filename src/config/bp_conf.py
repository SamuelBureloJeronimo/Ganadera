from config.app import app

bp = app

from routes.AppRoutes import AppRoutes #Control de rutas para renderizar las plantillas html
from routes.GeneralRoutes import GeneralRoutes #Rutas generales que cualquiera puede acceder


bp.register_blueprint(AppRoutes)
bp.register_blueprint(GeneralRoutes)

#Registro de los BluePrints
from routes.animales import BP_ani 
from routes.SuperUserRoutes import BP_SuperUserRoutes
from routes.OwnerRoutes import BP_Owner
from routes.raza import BP_raza
from routes.buscar import BP_buscar
from routes.veterinaryRoutes import BP_Veterinary

bp.register_blueprint(BP_SuperUserRoutes)
bp.register_blueprint(BP_Owner)
bp.register_blueprint(BP_ani)
bp.register_blueprint(BP_raza)
bp.register_blueprint(BP_buscar)
bp.register_blueprint(BP_Veterinary)