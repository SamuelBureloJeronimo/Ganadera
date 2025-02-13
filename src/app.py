from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="../static")
CORS(app)

@app.route('/img/<path:filename>')
def public_files(filename):
    return send_from_directory('../public/', filename)

@app.route('/')
def index():
    return render_template('home/home.html')

if __name__ == '__main__':
    app.run(debug=True)