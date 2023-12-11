from enum import Enum

class DataTypes(Enum):
    smallInt = 0
    integer = 1
    bigInit = 2
    decimal = 3
    numeric = 4
    real = 5
    double_precision= 6
    money = 7
    varchar = 8
    character = 9
    text = 10    
    date = 11
    time_No_zone = 12
    time_si_zone = 13
    boolean = 14
    columna = 15
    interval = 16    
    timestamp = 17
    nulo = 18
    default = 19
    enum = 20



class ColumnSym():

    def __init__(self,index,nombre,tipoDat):
        if (tipoDat.lower()=="smallint"):
            self.dataType = DataTypes.smallInt
        elif tipoDat.lower() ==  "integer":
            self.dataType = DataTypes.integer
        elif tipoDat.lower() == "biginit":
            self.dataType = DataTypes.bigInit
        elif tipoDat.lower() == "decimal":
            self.dataType = DataTypes.decimal
        elif tipoDat.lower() == "numeric":
            self.dataType = DataTypes.numeric
        elif tipoDat.lower() == "real":
            self.dataType = DataTypes.real
        elif tipoDat.lower() == "double":
            self.dataType = DataTypes.double_precision
        elif tipoDat.lower() == "money":
            self.dataType = DataTypes.money
        elif tipoDat.lower() == "varchar":
            self.dataType = DataTypes.varchar
        elif tipoDat.lower() == "character":
            self.dataType = DataTypes.character
        elif tipoDat.lower() == "text":
            self.dataType = DataTypes.text
        elif tipoDat.lower() == "timestamp":
            self.dataType = DataTypes.time_si_zone
        elif tipoDat.lower() == "time":
            self.dataType = DataTypes.time_No_zone
        elif tipoDat.lower() == "date":
            self.dataType = DataTypes.date
        elif tipoDat.lower() == "boolean":            
            self.dataType = DataTypes.boolean
        elif tipoDat.lower() == "interval":
            self.dataType = DataTypes.interval
        else:
            self.dataType = DataTypes.enum

        self.index = index
        self.nombre = nombre        
        self.defaultValue = None 
        self.null = False
        self.primaryKey = False
        self.unique = False
        self.foreignTable = None
        self.foreignColumn = []
        self.nameConstraint = None
        self.check = None  
        self.tipoDatoNOprimitivo = None


    def createPrimaryKey(self):
        self.null = False
        self.primaryKey = True
        self.unique = True

    def setForeignTable(self, nameForeignTable):
        self.foreignTable = nameForeignTable
    
    def setForeignColumn(self, columnName):
        self.foreignColumn.append(columnName)
    
    def setDefaultValue(self, valorDefault):
        self.defaultValue = valorDefault

    def setNullProperty(self):
        self.null = True
        
    def setNotNullProperty(self):
        self.null = False
    
    def setUniqueProperty(self):
        self.unique = True

    def setConstraintName(self, nameConst):
        self.nameConstraint = nameConst
    
    def setColumnName(self, columnName):
        self.nombre = columnName
    
    def setDataType(self, dataType):
        self.dataType = dataType
    
    def setCheck(self,check):
        self.check = check
        
    def setIndex(self,index):
        self.index = index
    
