from enum import Enum

class ReturnInstructionType(Enum):
    RETORNO = 1
    NUMBER = 2
    CONTINUE = 3
    NORMAL = 4
    ERROR = 5



class ReturnInstruction():

    def __init__(self, returnType,Sym = None):
        self.returnInstructionType = returnType
        self.ReturnSym = Sym

