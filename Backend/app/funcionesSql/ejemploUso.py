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


#crea la tabla y la agrega al archivo
sqlFun.agregar_tabla(nombre_archivo, nombre_tabla, columnas, llave_primaria, llaves_foraneas,not_null_columns)


#agrega una fila a la tabla
#por motivo de bugs de momento asi se tiene que realizar el insert
sqlFun.agregar_fila(nombre_archivo, nombre_tabla, {"id":3, "nombre":"Usuario3", "edad":28})

#otras funciones 

#Alter table para agregar columna
sqlFun.alterar_tabla_agregar(nombre_archivo, nombre_tabla, "agregar", algo="entero")


#Alter table para eliminar columna
sqlFun.alterar_tabla_delete(nombre_archivo, nombre_tabla, "eliminar", algo="entero")


#Truncate table 
sqlFun.truncar_tabla(nombre_archivo,nombre_tabla)



#Select  (equivalente al SELCET * FROM nombretabla)
sqlFun.select_final(nombre_archivo,"*",["usuarios"],["edad > 23.3"])


