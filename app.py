from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret"

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/ganaderia_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para la tabla de Ventas
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_arete = db.Column(db.String(50), nullable=False)
    comprador = db.Column(db.String(100), nullable=False)
    fecha_venta = db.Column(db.Date, nullable=False)
    peso_kg = db.Column(db.Float, nullable=False)
    precio_kg = db.Column(db.Float, nullable=False)

    @property
    def total(self):
        return self.peso_kg * self.precio_kg

# Ruta principal
@app.route('/')
def index():
    ventas = Venta.query.all()
    return render_template('index.html', ventas=ventas)

# Ruta para agregar venta
@app.route('/agregar_venta', methods=['POST'])
def agregar_venta():
    if request.method == 'POST':
        no_arete = request.form['no_arete']
        comprador = request.form['comprador']
        fecha_venta = request.form['fecha_venta']
        peso_kg = float(request.form['peso_kg'])
        precio_kg = float(request.form['precio_kg'])

        nueva_venta = Venta(no_arete=no_arete, comprador=comprador, fecha_venta=fecha_venta, peso_kg=peso_kg, precio_kg=precio_kg)
        db.session.add(nueva_venta)
        db.session.commit()

        flash("Venta registrada con éxito", "success")
        return redirect(url_for('index'))

# Ruta para eliminar venta
@app.route('/eliminar_venta/<int:id>')
def eliminar_venta(id):
    venta = Venta.query.get(id)
    db.session.delete(venta)
    db.session.commit()
    
    flash("Venta eliminada con éxito", "danger")
    return redirect(url_for('index'))

# Iniciar la aplicación
if __name__ == '__main__':
    db.create_all()  # Crea las tablas en la BD si no existen
    app.run(debug=True)
