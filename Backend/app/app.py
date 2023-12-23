from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from backend import *


app = Flask(__name__)
CORS(app)  # Habilita CORS

# Lista global para almacenar mensajes
outputTxt = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analizar', methods=['POST'])
def api_analizar():
    global outputTxt
    reiniciarVariables()

    data = request.get_json()
    try:
        respuesta = analizar_codigo(data['codigo'])
        return respuesta  # Devuelve directamente la respuesta JSON generada

    except Exception as e:
        return jsonify({"mensaje": str(e), "tipo": "error"}), 500

@app.route('/api/arbol', methods=['GET'])
def descargar_pdf():
    try:
        # Aqui se envia el archivo pdf
        pdf_path = 'reporte_AST.pdf'

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        return jsonify({"mensaje": str(e), "tipo": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
