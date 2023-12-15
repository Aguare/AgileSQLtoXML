class Instruccion:
    '''Esta clase representa cualquier instrucción que pueda ir en una lista de instrucciones'''

class CrearBD(Instruccion) :
    def __init__(self,reemplazar,verificacion,nombre, propietario, modo) :
        self.reemplazar = reemplazar
        self.verificacion = verificacion
        self.nombre = nombre 
        self.propietario = propietario
        self.modo = modo

class CrearTabla(Instruccion) :
    def __init__(self, nombre, padre, columnas = []) :
        self.nombre = nombre
        self.columnas = columnas
        self.padre = padre

class CrearType(Instruccion) :
    def __init__(self, nombre, valores = []) :
        self.nombre = nombre
        self.valores = valores

class EliminarTabla(Instruccion) :
    def __init__(self, existencia, nombre) :
        self.nombre = nombre
        self.existencia = existencia        

class EliminarDB(Instruccion) :
    def __init__(self, existencia, nombre) :
        self.nombre = nombre
        self.existencia = existencia    

class columnaTabla(Instruccion) :
    def __init__(self, id, tipo, valor,zonahoraria, atributos = []) :
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.zonahoraria = zonahoraria
        self.atributos = atributos   

class llaveTabla(Instruccion) :
    def __init__(self, tipo,referencia,columnas = [],columnasRef = []) :
        self.tipo = tipo
        self.referencia = referencia
        self.columnas = columnas
        self.columnasRef = columnasRef

class atributoColumna(Instruccion) :
    def __init__(self, default,constraint,null,unique,primary,check) :
        self.default = default
        self.constraint = constraint
        self.null = null
        self.unique = unique
        self.primary = primary
        self.check = check

class Insertar(Instruccion):
    def __init__(self, nombre, columnas, valores=[]) :
        self.nombre = nombre
        self.columnas = columnas
        self.valores = valores

class Actualizar(Instruccion):
    def __init__(self, nombre, condicion, valores=[]) :
        self.nombre = nombre
        self.condicion = condicion
        self.valores = valores

class columna_actualizar(Instruccion):
    def __init__(self, nombre, valor) :
        self.nombre = nombre
        self.valor = valor

class Eliminar(Instruccion): 
    def __init__(self, nombre, condicion):
        self.nombre = nombre
        self.condicion = condicion

class DBElegida(Instruccion):
    def __init__(self,nombre):
        self.nombre = nombre

class MostrarDB(Instruccion):
    '''
        Esta clase representa las base de datos creadas
    '''
class MostrarTB(Instruccion):
    '''
        Esta clase Muestra Tablas de una bd
    '''


class Limite_Select(Instruccion):
    def __init__(self, select, limit, offset):
        self.select=select
        self.limit=limit
        self.offset=offset

class SELECT(Instruccion):
    def __init__(self, cantidad, parametros, cuerpo, funcion_alias):
        self.cantida=cantidad
        self.parametros=parametros
        self.cuerpo=cuerpo
        self.funcion_alias=funcion_alias

class Funcion_Alias(Instruccion):
    def __init__(self, nombre, alias):
        self.nombre=nombre
        self.alias=alias

class CUERPO_SELECT(Instruccion):
    def __init__(self, b_from, b_join, b_where, b_group, b_having, b_order):
        self.b_from=b_from
        self.b_join=b_join
        self.b_where=b_where
        self.b_group=b_group
        self.b_having=b_having
        self.b_order=b_order

class Orden_Atributo(Instruccion):
    def __init__(self, nombre, direccion, rango):
        self.nombre=nombre
        self.direccion=direccion
        self.rango=rango

class SubQuery(Instruccion):
    def __init__(self, condicion, subquery, alias):
        self.condicion=condicion
        self.subquery=subquery
        self.alias=alias

class Valor_From(Instruccion):
    def __init__(self, nombre, subquery, alias):
        self.nombre=nombre
        self.subquery=subquery
        self.alias=alias

class SubQuery_IN(Instruccion):
    def __init__(self, exp, tipo):
        self.exp=exp
        self.tipo=tipo

class Valor_Select(Instruccion):
    def __init__(self, nombre, tipo, alias, fun_exp):
        self.nombre=nombre
        self.tipo=tipo
        self.alias=alias
        self.fun_exp=fun_exp

class Condicion_WHEN_THEN(Instruccion):
    def __init__(self, exp, resultado):
        self.exp=exp
        self.resultado=resultado

class Case(Instruccion):
    def __init__(self, condicion, sino, alias):
        self.condicion=condicion
        self.sino=sino
        self.alias=alias

class ALTERDBO(Instruccion): 
    def __init__(self, Id, TipoCon,valor):
        self.Id = Id
        self.TipoCon = TipoCon
        self.valor = valor

class ALTERTBO(Instruccion): 
    def __init__(self, Id,cuerpo):
        self.Id = Id
        self.cuerpo = cuerpo

class ALTERTBO_RENAME(Instruccion): 
    def __init__(self, Id1,Id2,operacion):
        self.Id1 = Id1
        self.Id2 = Id2
        self.operacion = operacion 

class ALTERTBO_ALTER_PROPIEDADES(Instruccion): 
    def __init__(self, prop1,prop2,prop3,prop4,prop5):
        self.prop1 = prop1
        self.prop2 = prop2
        self.prop3 = prop3 

        self.prop4 = prop4
        self.prop5 = prop5 

class ALTERTBO_ALTER(Instruccion): 
    def __init__(self, instruccion,id,extra):
        self.instruccion = instruccion
        self.id = id
        self.extra = extra 

class ALTERTBO_DROP(Instruccion): 
    def __init__(self, instruccion,id):
        self.instruccion = instruccion
        self.id = id

class ALTERTBO_ADD(Instruccion): 
    def __init__(self, id,tipo,valortipo,instruccion,extra):
        self.id = id
        self.tipo = tipo
        self.valortipo = valortipo

        self.instruccion = instruccion
        self.extra = extra

class ALTERTBO_ADD_EXTRAS(Instruccion): 
    def __init__(self, instruccion,contenido,  id , contenido2):
        self.instruccion = instruccion
        self.contenido = contenido

        self.id = id
        self.contenido2 = contenido2

class ALTERTBO_ALTER_SERIE(Instruccion): 
    def __init__(self, listaval):
        self.listaval = listaval


