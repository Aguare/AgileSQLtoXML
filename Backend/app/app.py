from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "Content-Type"}})  # Habilita CORS

# Lista global para almacenar mensajes
outputTxt = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/compile', methods=['POST'])
def api_analizar():
    global outputTxt
    reiniciarVariables()

    data = request.get_json()
    try:
        respuesta = analizar_codigo(data['codigo'])
        return respuesta  # Devuelve directamente la respuesta JSON generada

    except Exception as e:
        return jsonify({"message": str(e), "type": "error"}), 500


@app.route('/api/generar_reporte_errores', methods=['GET'])
def api_generar_reporte_errores():
    resultado = generar_reporte_errores()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
