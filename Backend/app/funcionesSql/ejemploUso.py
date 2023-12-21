import funcionesSql as sqlFun


#datos para crear la tabla y el arcvhivo
nombre_archivo = "pruebaFunciones"
nombre_tabla = "usuarios"
columnas = {"id": "entero", "nombre": "cadena", "edad": "entero"}
llave_primaria = "id"
llaves_foraneas = [
    {"columna_local": "id", "tabla_foranea": "otra_tabla", "columna_foranea": "id_foranea"}
]
not_null_columns = ["id", "nombre"]




#crea el archivo xml
sqlFun.crear_base_de_datos(nombre_archivo)
