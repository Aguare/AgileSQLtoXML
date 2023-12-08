from flask import Flask, jsonify, request
from gramatica import ejecutar_parser 
import sys
sys.path.append('.')


app = Flask(__name__)

@app.route('/procesar-expresion', methods=['POST'])
def procesar_expresion():
    datos = request.json
    expresion = datos.get('expresion', '')
    
    # Ejecuta el parser con la expresión proporcionada
    resultado = ejecutar_parser(expresion)
    
    # Devuelve el resultado como JSON
    return jsonify({'resultado': resultado})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
