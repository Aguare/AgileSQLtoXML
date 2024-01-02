import controller.AST
from flask import jsonify
from controller.manageErrors import *


manejador_json = ManageErrors()

def analizar_codigo(codigo):
    reiniciarVariables()  # Reinicia las variables globales antes de analizar el código
    mensajes = []


    try:
        lista = controller.AST.Analizar(codigo)  # Aquí ejecutas el análisis del código
        lista_errores = manejador_json.leer_archivo()
        lista.extend(lista_errores) #unir lista de output y la de errores
        
        controller.AST.generarAST();
        
        json_reporte = controller.AST.generarTSReporte();

        # Convierte los mensajes a un formato JSON
        # mensajes_json = [msg.to_dict() for msg in outputTxt]
        return jsonify({"message": ["OK", ], "mensajes": lista, "type": ["exito"]}), 200

    except Exception as e:
        # Maneja errores generales y retorna una respuesta con el error
        return jsonify({"message": str(e), "tipo": "error"}), 500

def reiniciarVariables():
    global outputTxt
    outputTxt = []
    global Errores_Semanticos
    Errores_Semanticos = []
    global manejador_json
    manejador_json.vaciar_archivo()

# Agrega esta protección al final del archivo
if __name__ == "__main__":
    app.run(debug=True)