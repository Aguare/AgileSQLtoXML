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
    
     #  root = ET.Element("base_de_datos")
      #  tree = ET.ElementTree(root)
       # tree.write("archivosBD/"+nombre_archivo+".xml", encoding="utf-8", xml_declaration=True)
            # Crear un DataFrame vacío y guardarlo como XML


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
    
def seleccionar_filas(nombre_archivo, nombre_tabla, condiciones=None):
    tree = ET.parse("archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

    # Buscar la tabla y sus columnas
    tabla_existente = root.find(nombre_tabla)
    if tabla_existente is None:
        print(f"Error: La tabla '{nombre_tabla}' no existe.")
        return

    columnas_tabla = [columna.get("nombre") for columna in tabla_existente.findall("columna")]

    # Crear una lista de diccionarios para almacenar los datos seleccionados
    datos_seleccionados = []

    # Iterar sobre las filas y verificar las condiciones
    for fila_existente in tabla_existente.findall("fila"):
        datos_fila = {}
        for columna in columnas_tabla:
            valor_columna = fila_existente.find(columna)
            datos_fila[columna] = None if valor_columna is None else valor_columna.text

        # Verificar las condiciones, si se proporcionan
        if condiciones is None or evaluar_condiciones(datos_fila, condiciones):
            datos_seleccionados.append(datos_fila)

    return datos_seleccionados

def evaluar_condiciones(datos_fila, condiciones):
    for columna, condicion in condiciones.items():
        valor_columna = datos_fila.get(columna)

        if valor_columna is None:
            return False  # La columna no existe en la fila

        # Verificar la condición
        if not eval(f"{valor_columna} {condicion}"):
            return False

    return True



def leer_datos_panda(nombre_archivo, nombre_tabla):
    tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

     # Verificar si la tabla existe
    if root.find(nombre_tabla) is None:
        print(f"Error: La tabla '{nombre_tabla}' no existe en el archivo '{nombre_archivo}'.")
        return None

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

def select_final(baseActiva,columnas,tablas,condiciones=None):
    print(columnas)
    print(len(columnas))
    print("Cantidad de tablas "+str(len(tablas)))
    print(tablas)
    print(condiciones)
    condicionesIniciadas = False
    erroEncontrado=False
    datos_df=""
    talbasFrame= []
    comparaciones = []
    comparacionesNumericas=[]
    listaIndices=[]
    
    
    if verificar_existencia_base_de_datos(baseActiva):
        print("Base activa existente")
        
        #creando frames de tablas y validando la cantidad 
        
        #valida si solo viene una tabla
        if tablas:
            #cuando solo viene una tabla y varias tablas
            if len(tablas)==1:
                dataFrame1 = leer_datos_panda(baseActiva,tablas[0])
                talbasFrame.append(dataFrame1)
                
                
            elif len(tablas) > 1:
                for i, tabla in enumerate(tablas):
                    dataFrameTemp = leer_datos_panda(baseActiva,tabla)
                    talbasFrame.append(dataFrameTemp)
                    listaIndices.append({tabla:i})
                    
        # condiciones 
            if condiciones:
                for i, condicion in enumerate(condiciones):
                    textoDividido = condicion.split()
                    
                    if '.' in textoDividido[0] and '.' in textoDividido[2]:
                        
                        
                        if(es_numero(textoDividido[2])):
                            comparacionesNumericas.append(textoDividido)
                        else:    
                            print( "Estructura con referencia a tabla y columna en ambos casos")
                            
                            
                            nombreColumna=textoDividido[0].split(".")
                            nombreColumna2 = textoDividido[2].split(".")

                            nombreTalba=textoDividido[0].split(".")
                            tabla2 = textoDividido[2].split(".")

                            print("Columna 1 "+nombreColumna[1])

                            print("Columna 2 "+nombreColumna2[1])
                        
                        #claves = list(listaIndices.keys())
                        # Obtener el valor asociado a la clave 'maeterias'
                            valor_uno = next((item[nombreTalba[0]] for item in listaIndices if nombreTalba[0] in item), None)
                            print("valor uno "+str(valor_uno))
                        # Obtener el valor asociado a la clave 'usuarios'
                            valor_dos = next((item[tabla2[0]] for item in listaIndices if tabla2[0] in item), None)
                            print("valor dos "+str(valor_dos))

                            comparaciones.append([(nombreColumna[1], valor_uno), (nombreColumna2[1], valor_dos)])
                    #comparaciones.append([('nombre', 3), ('nombre', 4)]
                        
                    
                    elif '.' in textoDividido[0]:
                        print( "Estructura con referencia solo a tabal y columna")
                        print(textoDividido)
                        print("Texto unido "+textoUnido)
                        
                        print("Texto unido + anterior "+textoDividido)
                        textoUnido = [textoDividido[0], textoDividido[1],' '.join(textoDividido[2:])]
                        
                        comparacionesNumericas.append(textoUnido)
                        
                    else:
                        print( "Estructura simple ")
                        print(textoDividido)
                        
                        textoUnido = [textoDividido[0], textoDividido[1],' '.join(textoDividido[2:])]
                        #print("Texto unido "+textoUnido)

                        comparacionesNumericas.append(textoUnido)
                        
                        
                if comparaciones :
                    resultado = comparar_columnas(talbasFrame,comparaciones)
                    if comparacionesNumericas:
                        for condicionNum in comparacionesNumericas:
                            nombreTablayCol = condicionNum[0].split(".")
                            print(nombreTablayCol)
                            valor_tabla = next((item[nombreTablayCol[0]] for item in listaIndices if nombreTablayCol[0] in item), None)
                            print("valor uno "+str(valor_uno))
                    
                            resultado = filtrar_por_condicion(resultado,nombreTablayCol[1]+"_df"+str(valor_tabla),condicionNum[1],condicionNum[2])
                        print("-----------Resultado pre final comparacion y numericos------------")
                        print(resultado)
                        columnaSeleccionadas = []
                        if columnas!= "*":
                            for columna in columnas:
                                print("Inciando for para seleccionar columnas")
                                if "." in columna:
                                    columnaDividia = columna.split(".")
                                    valor_tabla = next((item[columnaDividia[0]] for item in listaIndices if columnaDividia[0] in item), None)
                                    columnaSeleccionadas.append(columnaDividia[columnaDividia[1]+"_df"+str(valor_tabla)])
                                else:
                                    columnaSeleccionadas.append(columna)
                            
                           
                            finalFrame = resultado[columnaSeleccionadas]
                            print("--------Resultado supuestamente final xd final --------")
                            print(finalFrame)
                        
                        else:
                            print("-----------Resultado supuestamente final sin elegir------------")
                            print(resultado)
                        
                else :
                    if comparacionesNumericas:
                        resultado = talbasFrame[0];
                        for condicionNum in comparacionesNumericas:
                            
                            print(condicionNum)
                            nombreTablayCol = condicionNum[0].split()                        
                            print("condicion simple xd probando que sale")
                            print(nombreTablayCol)
                            #dataFrame1=talbasFrame[0]
                            resultado = filtrar_por_condicion(resultado,condicionNum[0],condicionNum[1],condicionNum[2])
                            print("--------Resultado pre final solo numerico --------")
                            print(resultado)
                        columnaSeleccionadas = []
                        if columnas!= "*":
                            for columna in columnas:
                                print("Inciando for para seleccionar columnas")
                                if "." in columna:
                                    columnaDividia = columna.split(".")
                                    valor_tabla = next((item[columnaDividia[0]] for item in listaIndices if columnaDividia[0] in item), None)
                                    columnaSeleccionadas.append(columnaDividia[columnaDividia[1]+"_df"+str(valor_tabla)])
                                else:
                                    columnaSeleccionadas.append(columna)
                            
                           
                            finalFrame = resultado[columnaSeleccionadas]
                            print("--------Resultado supuestamente final xd final --------")
                            print(finalFrame)
                        
                        else:
                            print("-----------Resultado supuestamente final sin elegir------------")
                            print(resultado)
                            
                        
            
            else:
                print("sin condicion")
                #falta armar ejecucion aqui , cunado no haya condiciones 
                #primero hacer unir todas las tablas y luego validar las columnsa nuevamente 
                if len(talbasFrame)>1:
                    merge_resultado = pd.concat(talbasFrame, axis=1)
                    columnaSeleccionadas = []
                    if columnas!= "*":
                        for columna in columnas:
                            print("Inciando for para seleccionar columnas")
                            if "." in columna:
                                columnaDividia = columna.split(".")
                                valor_tabla = next((item[columnaDividia[0]] for item in listaIndices if columnaDividia[0] in item), None)
                                columnaSeleccionadas.append(columnaDividia[columnaDividia[1]+"_df"+str(valor_tabla)])
                            else:
                                columnaSeleccionadas.append(columna)
                            
                           
                            finalFrame = merge_resultado[columnaSeleccionadas]
                            print("--------Resultado supuestamente final xd final --------")
                            print(finalFrame)
                        
                        else:
                            print("-----------Resultado supuestamente final sin elegir------------")
                            print(merge_resultado)
                
                elif len(talbasFrame)==1:
                    #validar que si existan las columnas
                    print(talbasFrame[0][columnas])
                    #falta seleccionar columnas
            
    
         #bloque en donde no hay condiciones   
            
        else :
            print("error no hay tablas para la seleccion")
    else:
        print("Base activa NO EXISTE")
    
    
    
#validacion para los decimales     
def es_numero(s):
    try:
        float(s)
        return True
    except ValueError:
        return False    





#equivale a  tbcreditoobligacion.Credito = tbcreditoSaldo.credito  && tbcliente.codigocliente = tbcreditoobligacion.codigocliente

def comparar_columnas(dataframes, comparaciones):
    # Renombrar columnas antes de la unión
    for i, df in enumerate(dataframes):
        df.columns = [f'{col}_df{i}' for col in df.columns]

    # Realizar la unión de los DataFrames
        print("comparacions desde la fun ")
        print(comparaciones)
        merge_resultado = pd.concat(dataframes, axis=1)

    # Iterar sobre las comparaciones y filtrar el resultado
    for i, (columna1_info, columna2_info) in enumerate(comparaciones):
        columna1, dataframe1 = columna1_info
        columna2, dataframe2 = columna2_info

        # Asegurarse de que las columnas existan en el resultado
        if columna1 + f'_df{dataframe1}' not in merge_resultado.columns:
            print(f'Error: La columna {columna1} no existe en el DataFrame {dataframe1}.')
            continue
        if columna2 + f'_df{dataframe2}' not in merge_resultado.columns:
            print(f'Error: La columna {columna2} no existe en el DataFrame {dataframe2}.')
            continue

        # Realizar la comparación y filtrar el resultado
        merge_resultado = merge_resultado[merge_resultado[columna1 + f'_df{dataframe1}'] == merge_resultado[columna2 + f'_df{dataframe2}']]

    # Imprimir columnas disponibles después de la unión
    print(f'\nColumnas disponibles después de la unión:\n{merge_resultado.columns}')

    # Imprimir sufijos generados para las comparaciones
    sufijos_generados = [f'_df{i}' for i in range(len(dataframes))]
    print(f'Sufijos generados para las comparaciones: {sufijos_generados}')

    return merge_resultado



#verificar que sea numerico

def filtrar_por_condicion(dataframe, columna, operador, valor):
    """
    Filtra un DataFrame según una condición dada.

    Parámetros:
    - dataframe: DataFrame de pandas.
    - columna: Nombre de la columna a utilizar en la comparación.
    - operador: Operador de comparación (<, >, ==, >=, <=).
    - valor: Valor a comparar.

    Retorna:
    - DataFrame filtrado según la condición.
    """
    # Verificar que la columna exista en el DataFrame
    if columna not in dataframe.columns:
        print(f"Error: La columna '{columna}' no existe en el DataFrame.")
        return None


        

    # Convertir la columna a valores numéricos ignorando errores
    if valor.isdigit():
        print("valor tipo numerico")
        dataframe[columna] = pd.to_numeric(dataframe[columna], errors='coerce')
        
            # Realizar la comparación según el operador dado
        if operador == '<':
            resultado = dataframe[dataframe[columna] < int(valor)]
        elif operador == '>':
            resultado = dataframe[dataframe[columna] > int(valor)]
        elif operador == '=':
            resultado = dataframe[dataframe[columna] == int(valor)]
        elif operador == '>=':
            resultado = dataframe[dataframe[columna] >= int(valor)]
        elif operador == '<=':
            resultado = dataframe[dataframe[columna] <= int(valor)]
        else:
            print("Error: Operador no válido. Utilice '<', '>', '==', '>=', '<='. ")
            return None

        return resultado
    
    elif es_numero(valor):
        print("xd")
        print("valor tipo decimal")
        dataframe[columna] = pd.to_numeric(dataframe[columna], errors='coerce')
        
            # Realizar la comparación según el operador dado
        if operador == '<':
            resultado = dataframe[dataframe[columna] < float(valor)]
        elif operador == '>':
            resultado = dataframe[dataframe[columna] > float(valor)]
        elif operador == '=':
            resultado = dataframe[dataframe[columna] == float(valor)]
        elif operador == '>=':
            resultado = dataframe[dataframe[columna] >= float(valor)]
        elif operador == '<=':
            resultado = dataframe[dataframe[columna] <= float(valor)]
        else:
            print("Error: Operador no válido. Utilice '<', '>', '==', '>=', '<='. ")
            return None

        return resultado
     
    else:
        if operador == '=':
            resultado = dataframe[dataframe[columna] == valor]
            return resultado
        else:
            print("Error: Operador no válido en strings.")
            return None
        print("")
    
    
#funciones de UPDATE 
def actualizar_datos(nombre_archivo, nombre_tabla, condiciones, datos_nuevos):
    tree = ET.parse("archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

    # Obtener un DataFrame de pandas a partir de datos XML
    df = leer_datos_panda(nombre_archivo, nombre_tabla)

    # Obtener índices de las filas que cumplen con las condiciones
    indices_filas = obtener_indices_filas(df, condiciones)
#    if not indices_filas:
    if len(indices_filas) == 0:
        print("Error: No hay filas que cumplan con las condiciones de actualización.")
        return 2

    # Actualizar los datos en el DataFrame
    for indice in indices_filas:
        for columna, valor in datos_nuevos.items():
            df.at[indice, columna] = valor

    # Guardar el DataFrame actualizado de nuevo en el archivo XML
    guardar_datos_panda(df, nombre_archivo, nombre_tabla)


def parsear_condicion(condicion):
    """
    Parsea una condición en la forma columna operador valor.
    """
    if isinstance(condicion, tuple) and len(condicion) == 3:
        return condicion
    else:
        print("Error: Condición mal formada.")
        return None, None, None

def obtener_indices_filas(dataframe, condiciones):
    indices_filas = dataframe.index
    print(f"DataFrame original:\n{dataframe}")
    for condicion in condiciones:
        columna, operador, valor = parsear_condicion(condicion)
        try:
            print(f"Condición: {columna} {operador} {valor}")
            print(f"Columna antes de aplicar la condición:\n{dataframe[columna]}")
            dataframe[columna] = pd.to_numeric(dataframe[columna], errors='coerce')
            mask = comparar_condicion(dataframe[columna], operador, valor)
            print(f"Mask después de aplicar la condición:\n{mask}")
            indices_filas = indices_filas[mask]
            print(f"Índices después de aplicar la condición: {indices_filas}")
        except KeyError:
            print(f"Error: La columna '{columna}' no existe en el DataFrame.")
            return []
    return indices_filas.tolist()


def comparar_condicion(columna, operador, valor):
    if operador == "=":
        return columna == valor
    elif operador == "!=":
        return columna != valor
    elif operador == "<":
        return columna < valor
    elif operador == ">":
        return columna > valor
    elif operador == "<=":
        return columna <= valor
    elif operador == ">=":
        return columna >= valor
    else:
        print(f"Error: Operador no válido: {operador}")
        return None

def comparar_valores(valor1, operador, valor2):
    """
    Compara dos valores según el operador especificado.
    Devuelve True si la comparación es verdadera, False en caso contrario.
    """
    if operador == "=":
        return valor1 == valor2
    elif operador == "!=":
        return valor1 != valor2
    elif operador == "<":
        return valor1 < valor2
    elif operador == ">":
        return valor1 > valor2
    elif operador == "<=":
        return valor1 <= valor2
    elif operador == ">=":
        return valor1 >= valor2
    else:
        print("Error: Operador no válido.")
        return False



def guardar_datos_panda(dataframe, nombre_archivo, nombre_tabla):
    # Obtener el elemento de la tabla en el archivo XML
    tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()
    tabla_existente = root.find(nombre_tabla)

    # Eliminar las filas antiguas de la tabla en el XML
    for fila_existente in tabla_existente.findall("fila"):
        tabla_existente.remove(fila_existente)

    # Agregar las filas actualizadas al XML
    for indice, fila in dataframe.iterrows():
        nueva_fila = ET.SubElement(tabla_existente, "fila")
        nueva_fila.tail = "\n"
        for columna, valor in fila.items():
            ET.SubElement(nueva_fila, columna).text = str(valor)
            nueva_fila[-1].tail = "\n"

    # Guardar el árbol XML actualizado
    tree.write("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml", encoding="utf-8", xml_declaration=True)

  

#funcion para complementar el insert
def insert_primitivo_columnas(BaseActiva,tabla,columnas,valores):
    if columnas != "X":

        if len(columnas) == len(valores):
            print("validacion de tamanio exitoso")
        #preparar para el insert de formar into ____ values ____
            columnasPreparadas = {}
        
            for i, columna in enumerate(columnas):
                columnasPreparadas[columna]=valores[i]


            print(columnasPreparadas)        
       # agregar_fila(nombre_archivo, nombre_tabla, {"id": 5, "nombre": "Maestro 5","salario": 6000,"id_materia": 3})
        else:
            error="tamaño de columnas distinto al de valores a ingresar"
        
            mensaje ={"message": [error], "type": ["error", "error"]}
            print(mensaje)
    else:
        columnasGet= obtener_columnas(BaseActiva,tabla)
        print(columnasGet)
        columnasPreparadas2 = {}
        if len(columnasGet) == len(valores):
            for i, columna in enumerate(columnasGet):
                columnasPreparadas2[columna]=valores[i]

            print(columnasPreparadas2)
            # agregar_fila(nombre_archivo, nombre_tabla,columnasPreparadas2)
        else:
            error="tamaño de columnas distinto al de valores a ingresar"

            mensaje ={"message": [error], "type": ["error", "error"]}
            print(mensaje)
     




def obtener_columnas(nombre_archivo, nombre_tabla):
    tree = ET.parse("Backend/app/funcionesSql/archivosBD/"+nombre_archivo+".xml")
    root = tree.getroot()

    # Buscar la tabla y sus columnas
    tabla_existente = root.find(nombre_tabla)
    if tabla_existente is None:
        error=f"Error: La tabla '{nombre_tabla}' no existe."
        mensaje ={"message": [error], "type": ["error", "error"]}
        print(mensaje)
        return []

    # Obtener las columnas de la tabla
    columnas = [columna.get("nombre") for columna in tabla_existente.findall("./columna")]

    return columnas
  

