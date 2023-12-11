
from .columnSym import DataTypes

class Sym():

    def __init__(self):
        self.nameColumnaIzquierdo = None
        self.nameColumnaDerecho = None
        self.dataTypeReturn = None
        self.returnValue = None
        self.errorDescription = None
        self.tipDatoCasteo = None
        self.tipoOperacion = None 


    def createSimboloPrimitivo(self,dataTypeReturn,returnValue):
        self.dataTypeReturn = dataTypeReturn
        self.returnValue = returnValue
    
    def createColumnSym(self,columnName):
        self.dataTypeReturn = DataTypes.columna
        self.nameColumnaIzquierdo = columnName

    def setDataTypeReturn(self,dataType):
        self.dataTypeReturn = dataType

    def setErrorDescription(self,description):
        self.errorDescription = description
    
    def setTipoDatosCasteo(self, dataType):
        self.tipDatoCasteo = dataType

