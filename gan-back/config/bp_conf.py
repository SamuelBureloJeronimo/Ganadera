from config.app import app

bp = app

#from routes.Dispositivo import BP_dispositivo
from routes.UsersRoutes import BP_UsersRoutes
from routes.PublicRoutes import BP_PublicRoutes

bp.register_blueprint(BP_PublicRoutes)
bp.register_blueprint(BP_UsersRoutes)