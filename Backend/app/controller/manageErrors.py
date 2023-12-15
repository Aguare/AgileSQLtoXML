import json

class ManageErrors:
    def __init__(self):
        self.nombre_archivo = "errors.json"

    def agregar_textos(self, textos):
        try:
            # Validar la entrada
            if not textos:
                raise ValueError("La entrada no puede estar vacía.")

            # Convertir a lista si es un solo string
            textos = [textos] if isinstance(textos, str) else textos

            # Cargar el contenido actual del archivo (si existe)
            try:
                with open(self.nombre_archivo, 'r') as archivo_existente:
                    contenido_existente = json.load(archivo_existente)
            except FileNotFoundError:
                contenido_existente = []

            # Asegurarse de que el contenido existente sea una lista
            if not isinstance(contenido_existente, list):
                contenido_existente = []

            # Agregar los nuevos textos al contenido existente
            contenido_existente.extend(textos)

            # Escribir el contenido actualizado en el archivo JSON
            with open(self.nombre_archivo, 'w') as archivo:
                json.dump(contenido_existente, archivo, indent=2)

            print("Textos agregados al archivo JSON con éxito.")
        except Exception as e:
            print(f"Error al agregar textos al archivo JSON: {str(e)}")
            
    def vaciar_archivo(self):
        try:
            # Escribir una lista vacía en el archivo JSON
            with open(self.nombre_archivo, 'w') as archivo:
                json.dump([], archivo, indent=2)

            print("Contenido del archivo JSON vaciado con éxito.")
        except Exception as e:
            print(f"Error al vaciar el archivo JSON: {str(e)}")
            
    def leer_archivo(self):
        try:
            # Leer el contenido del archivo JSON
            with open(self.nombre_archivo, 'r') as archivo:
                contenido = json.load(archivo)

            return contenido
        except Exception as e:
            print(f"Error al leer el archivo JSON: {str(e)}")
            return None