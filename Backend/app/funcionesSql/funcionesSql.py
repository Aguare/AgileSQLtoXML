import pandas as pd
import xml.etree.ElementTree as ET
import os



"""    if os.path.exists(nombre_archivo):
        return 2
    else:
        return 0
"""
   # return os.path.exists(nombre_archivo)

def crear_base_de_datos(nombre_archivo):
    if verificar_existencia_base_de_datos(nombre_archivo):
        print("Base de datos Existente")
        return 2
    else:
        root = ET.Element("base_de_datos")
        tree = ET.ElementTree(root)
        tree.write("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
        print("Base de datos creada con éxito.")
        return 0
    




    

def verificar_existencia_base_de_datos(nombre_archivo):
     return os.path.exists("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")     



def agregar_tabla(nombre_archivo, nombre_tabla, columnas, llave_primaria=None, llaves_foraneas=None, not_null_columns=None):
    if not verificar_existencia_base_de_datos(nombre_archivo):
        print("Base de datos no existe")
        return 2
    else:
 
        tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
        root = tree.getroot()

        # Crear la tabla
        tabla = ET.SubElement(root, nombre_tabla)
        tabla.tail = "\n"

    # Agregar metadatos de columnas
        for columna, tipo_dato in columnas.items():
            info_columna = ET.SubElement(tabla, "columna", {"nombre": columna, "tipo": tipo_dato})
            info_columna.tail = "\n"

            # Agregar restricción NOT NULL si está definida
            if not_null_columns and columna in not_null_columns:
                ET.SubElement(info_columna, "not_null")
                info_columna[-1].tail = "\n"
        
    # Agregar llave primaria si está definida
        if llave_primaria is not None:
            info_llave_primaria = ET.SubElement(tabla, "llave_primaria")
            ET.SubElement(info_llave_primaria, "columna").text = llave_primaria
            info_llave_primaria.tail = "\n"

    # Agregar llaves foraneas si están definidas
        if llaves_foraneas is not None:
            for llave_foranea in llaves_foraneas:
                info_llave_foranea = ET.SubElement(tabla, "llave_foranea")
                ET.SubElement(info_llave_foranea, "columna_local").text = llave_foranea["columna_local"]
                ET.SubElement(info_llave_foranea, "tabla_foranea").text = llave_foranea["tabla_foranea"]
                ET.SubElement(info_llave_foranea, "columna_foranea").text = llave_foranea["columna_foranea"]
                info_llave_foranea.tail = "\n"

        tree.write("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml", encoding="utf-8", xml_declaration=True)
        return 0

def agregar_fila(nombre_archivo, nombre_tabla, datos):
    if not verificar_existencia_base_de_datos(nombre_archivo):
        print("Base de datos no existe")
        return 2
    else:
        tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
        root = tree.getroot()

    # Buscar la tabla y sus columnas
        tabla_existente = root.find(nombre_tabla)
        if tabla_existente is None:
            print(f"Error: La tabla '{nombre_tabla}' no existe.")
            return

    # Verificar llave primaria si está definida
        llave_primaria = tabla_existente.find("llave_primaria/columna")
        if llave_primaria is not None:
            nombre_llave_primaria = llave_primaria.text
            valor_llave_primaria = datos.get(nombre_llave_primaria)
            if valor_llave_primaria is not None and any(fila.find(nombre_llave_primaria).text == str(valor_llave_primaria) for fila in tabla_existente.findall("fila")):
                print(f"Error: Ya existe una fila con la llave primaria '{nombre_llave_primaria}' igual a '{valor_llave_primaria}'.")
                return

    # Verificar restricción NOT NULL y llaves foráneas
        for columna, valor in datos.items():
            info_columna = tabla_existente.find(f"./columna[@nombre='{columna}']")
            if info_columna is None:
                print(f"Error: La columna '{columna}' no existe en la tabla '{nombre_tabla}'.")
                return

            not_null = info_columna.find("not_null") is not None

            if valor is None and not_null:
                print(f"Error: La columna '{columna}' tiene restricción NOT NULL y no se proporcionó un valor.")
                return

            tipo_dato_esperado = info_columna.get("tipo")
            if valor is not None and not verificar_tipo_dato(valor, tipo_dato_esperado):
                print(f"Error: Tipo de dato incorrecto para la columna '{columna}'. Se esperaba '{tipo_dato_esperado}'.")
                return

        # Verificar llaves foráneas si están definidas
            for llave_foranea in tabla_existente.findall("llave_foranea"):
                columna_local = llave_foranea.find("columna_local").text
                tabla_foranea = llave_foranea.find("tabla_foranea").text
                columna_foranea = llave_foranea.find("columna_foranea").text

                valor_columna_local = datos.get(columna_local)
                tabla_foranea_existente = root.find(tabla_foranea)
                if tabla_foranea_existente is not None and valor_columna_local is not None and not any(fila.find(columna_foranea).text == str(valor_columna_local) for fila in tabla_foranea_existente.findall("fila")):
                    print(f"Error: No existe una fila en la tabla '{tabla_foranea}' con el valor '{valor_columna_local}' en la columna '{columna_foranea}'.")
                    return

    # Crear una nueva fila con los datos proporcionados, permitiendo valores nulos
        nueva_fila = ET.SubElement(tabla_existente, "fila")
        nueva_fila.tail = "\n"
        for columna, valor in datos.items():
            if valor is not None:
                ET.SubElement(nueva_fila, columna).text = str(valor)
            else:
                ET.SubElement(nueva_fila, columna).text = "none"
            nueva_fila[-1].tail = "\n"

        tree.write("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml", encoding="utf-8", xml_declaration=True)

    

   

def verificar_tipo_dato(valor, tipo_dato):
    # Verificar el tipo de dato del valor
    if tipo_dato == "entero":
        return isinstance(valor, int)
    elif tipo_dato == "cadena":
        return isinstance(valor, str)
    # Agrega más tipos de datos según tus necesidades

    return False

#tuncate table
def truncar_tabla(nombre_archivo, nombre_tabla):
    tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

    # Buscar la tabla
    tabla_existente = root.find(nombre_tabla)
    if tabla_existente is None:
        print(f"Error: La tabla '{nombre_tabla}' no existe.")
        return

    # Eliminar todas las filas de la tabla
    for fila in tabla_existente.findall("fila"):
        tabla_existente.remove(fila)

    tree.write("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml", encoding="utf-8", xml_declaration=True)
    print(f"Tabla '{nombre_tabla}' truncada con éxito.")


def alterar_tabla_delete(nombre_archivo, nombre_tabla, operacion, *columnas):
    tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

    # Buscar la tabla
    tabla_existente = root.find(nombre_tabla)
    if tabla_existente is None:
        print(f"Error: La tabla '{nombre_tabla}' no existe.")
        return

    if operacion == "agregar":
        for nombre_columna, tipo_dato in columnas.items():
            # Validar si la columna ya existe en la tabla
            if tabla_existente.find(f"./columna[@nombre='{nombre_columna}']") is not None:
                print(f"Error: La columna '{nombre_columna}' ya existe en la tabla '{nombre_tabla}'.")
                return

            nueva_columna = ET.SubElement(tabla_existente, "columna", {"nombre": nombre_columna, "tipo": tipo_dato})
            nueva_columna.tail = "\n"

        print(f"Columnas agregadas a la tabla '{nombre_tabla}'.")
    elif operacion == "eliminar":
        for nombre_columna in columnas:
            columna_existente = tabla_existente.find(f"./columna[@nombre='{nombre_columna}']")
            if columna_existente is not None:
                tabla_existente.remove(columna_existente)
                print(f"Columna '{nombre_columna}' eliminada de la tabla '{nombre_tabla}'.")
            else:
                print(f"Error: La columna '{nombre_columna}' no existe en la tabla '{nombre_tabla}'.")
    else:
        print("Error: Operación no válida. Use 'agregar' o 'eliminar'.")

    tree.write("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml", encoding="utf-8", xml_declaration=True)


def alterar_tabla_agregar(nombre_archivo, nombre_tabla, operacion, **columnas):
    tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

    # Buscar la tabla
    tabla_existente = root.find(nombre_tabla)
    if tabla_existente is None:
        print(f"Error: La tabla '{nombre_tabla}' no existe.")
        return

    if operacion == "agregar":
        # Obtener la posición de las llaves primaria y foranea
        idx_llave_primaria = None
        idx_llaves_foraneas = None

        for i, elemento in enumerate(tabla_existente):
            if elemento.tag == "llave_primaria":
                idx_llave_primaria = i
            elif elemento.tag == "llave_foranea":
                idx_llaves_foraneas = i

        for nombre_columna, tipo_dato in columnas.items():
            # Validar si la columna ya existe en la tabla
            if tabla_existente.find(f"./columna[@nombre='{nombre_columna}']") is not None:
                print(f"Error: La columna '{nombre_columna}' ya existe en la tabla '{nombre_tabla}'.")
                return

            nueva_columna = ET.Element("columna", {"nombre": nombre_columna, "tipo": tipo_dato})
            nueva_columna.tail = "\n"

            # Insertar la nueva columna en la posición adecuada
            if idx_llave_primaria is not None:
                tabla_existente.insert(idx_llave_primaria, nueva_columna)
            elif idx_llaves_foraneas is not None:
                tabla_existente.insert(idx_llaves_foraneas, nueva_columna)
            else:
                tabla_existente.append(nueva_columna)

        print(f"Columnas agregadas a la tabla '{nombre_tabla}'.")
    elif operacion == "eliminar":
        for nombre_columna in columnas:
            columna_existente = tabla_existente.find(f"./columna[@nombre='{nombre_columna}']")
            if columna_existente is not None:
                tabla_existente.remove(columna_existente)
                print(f"Columna '{nombre_columna}' eliminada de la tabla '{nombre_tabla}'.")
            else:
                print(f"Error: La columna '{nombre_columna}' no existe en la tabla '{nombre_tabla}'.")
    else:
        print("Error: Operación no válida. Use 'agregar' o 'eliminar'.")

    tree.write("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml", encoding="utf-8", xml_declaration=True)




#funciona como select simple 
def leer_datos_panda(nombre_archivo, nombre_tabla):
    tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

    # Obtener columnas de la tabla
    columnas_tabla = [columna.get("nombre") for columna in root.find(nombre_tabla).findall("columna")]

    # Crear un diccionario para almacenar datos
    datos = {columna: [] for columna in columnas_tabla}

    # Iterar sobre las filas y llenar el diccionario
    for fila_existente in root.find(nombre_tabla).findall("fila"):
        for columna in columnas_tabla:
            valor_columna = fila_existente.find(columna)
            datos[columna].append(None if valor_columna is None else valor_columna.text)

    # Crear un DataFrame de Pandas
    df = pd.DataFrame(datos)

    return df


#en proceso
def select_completo_complejo(baseActiva,columnas,tablas,condiciones):
    print(columnas)
    print(len(columnas))
    print(tablas)
    print(condiciones)

    
    datos_df = leer_datos_panda(baseActiva, tablas)



    selected_columns = datos_df[columnas]




    # Aplicar condiciones si están presentes
    if condiciones:
        for condition in condiciones:
            selected_columns = selected_columns.query(condition)

        # Agregar el resultado al DataFrame final
    result_df = pd.concat([result_df, selected_columns], axis=1)

    return result_df




