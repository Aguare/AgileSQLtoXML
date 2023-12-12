import ply.yacc as yacc
import ply.lex as lex
import re
from ply import *

# here start grammar
# ----------------------------------------------------------------------------------------
# 07-12-2023: Created by Luis Emilio Maldonado Rodriguez & Marcos Andres Aguare Bravo    #
# Project 1 ORGANIZACION DE LENGUAJES Y COMPILADORES 2                                   #             
# ----------------------------------------------------------------------------------------


# words reserved
global_arr = []

Reservadas = {  
    'create':'CREATE',
    'database':'DATABASE',
    'table': 'TABLE',
    'replace':'REPLACE',
    'if':'IF',
    'exists':'EXISTS',
    'owner':'OWNER',
    'mode':'MODE',
    'smallint':'smallint',
    'integer':'integer',
    'bigint':'bigint',
    'decimal':'decimal',
    'numeric':'numeric',
    'real':'real',
    'double':'double',
    'precision':'precision',
    'money':'money',
    'default':'DEFAULT',
    'null':'NULL',
    'unique':'UNIQUE',
    'constraint':'CONSTRAINT',
    'primary':'PRIMARY',
    'key':'KEY',
    'foreign':'FOREIGN',
    'references':'REFERENCES',
    'inherits':'INHERITS',
    'insert':'INSERT',
    'into':'INTO',
    'values':'VALUES',
    'update':'UPDATE',
    'set':'SET',
    'where':'WHERE',
    'delete':'DELETE',
    'from':'FROM',
    'and':'AND',
    'not':'NOT',
    'or':'OR',
    'character':'character',
    'varying':'varying',
    'varchar':'varchar',
    'char':'char',
    'text':'text',
    'timestamp':'timestamp',
    'with':'with',
    'time':'time',
    'zone':'zone',
    'date':'date',
    'interval':'interval',
    'boolean':'boolean',
    'year':'YEAR',
    'month':'MONTH',
    'day':'DAY',
    'hour':'HOUR',
    'minute':'MINUTE',
    'second':'SECOND',
    'select':'SELECT',
    'distinct':'DISTINCT',
     'group':'GROUP',
    'by':'BY',
    'having':'HAVING',
    'order':'ORDER',
    'as':'AS',
    'asc':'ASC',
    'desc':'DESC',
    'nulls':'NULLS',
    'first':'FIRST',
    'last':'LAST',
    'type':'TYPE',
    'enum':'ENUM',
    'check':'CHECK',
    'show':'SHOW',
    'databases':'DATABASES',
    'drop':'DROP',
    'column':'COLUMN',
    'rename':'RENAME',
    'alter':'ALTER',
    'data':'DATA',
    'to':'TO',
    'add':'ADD',
    'abs':'ABS',
    'cbrt':'CBRT',
    'ceil':'CEIL',
    'ceiling':'CEILING',
    'degrees':'DEGREES',
    'div':'DIV',
    'exp':'EXP',
    'factorial':'factorial',
    'floor':'FLOOR',
    'gcd':'GCD',
    'ln':'LN',
    'log':'LOG',
    'mod':'MOD',
    'pi':'PI',
    'power':'POWER',
    'radians':'RADIANS',
    'round':'ROUND',
    'min_scale':'min_scale',
    'scale':'scale',
    'sign':'sign',
    'sqrt':'sqrt',
    'trim_scale':'trim_scale',
    'trunc':'TRUNC',
    'random':'random',
    'setseed':'setseed',
    'acos':'ACOS',
    'acosd':'ACOSD',
    'asin':'ASIN',
    'asind':'ASIND',
    'atan':'ATAN',
    'atand':'ATAND',
    'atan2':'ATAN2',
    'atan2d':'ATAN2D',
    'cos':'COS',
    'cosd':'COSD',
    'cot':'COT',
    'cotd':'COTD',
    'sin':'SIN',
    'sind':'SIND',
    'tan':'TAN',
    'tand':'TAND',
    'sinh':'SINH',
    'cosh':'COSH',
    'tanh':'TANH',
    'asinh':'ASINH',
    'acosh':'ACOSH',
    'atanh':'ATANH',
    'length':'length',
    'substring':'substring',
    'trim':'trim',
    'leading':'leading',
    'trailing':'trailing',
    'both':'both',
    'sha256':'sha256',
    'decode':'decode',
    'get_byte':'get_byte',
    'bytea':'bytea',
    'set_byte':'set_byte',
    'substr':'substr',
    'convert':'CONVERT',
    'encode':'encode',
    'width_bucket':'width_bucket',
    'current_user':'CURRENT_USER',
    'session_user':'SESSION_USER',
    'natural':'NATURAL',
    'join':'JOIN',
    'inner':'INNER',
    'left':'LEFT',
    'right':'RIGHT',
    'full':'FULL',
    'outer':'OUTER',
    'using':'USING',
    'on':'ON',
    'in':'IN',
    'any':'ANY',
    'all':'ALL',
    'some':'SOME',
    'union':'UNION',
    'intersect':'INTERSECT',
    'except':'EXCEPT' , 
    'case':'CASE',
    'when':'WHEN',
    'else':'ELSE',
    'end':'END',
    'then':'THEN' ,
    'limit':'LIMIT',
    'similar':'SIMILAR',
    'like':'LIKE',
    'ilike':'ILIKE',
    'between':'BETWEEN',
    'offset':'OFFSET',
    'greatest':'GREATEST', 
    'least':'LEAST',
    'md5':'MD5',
    'extract':'EXTRACT',
    'now':'NOW',
    'date_part':'DATE_PART', 
    'current_date':'CURRENT_DATE', 
    'current_time':'CURRENT_TIME',
    'use':'USE',
    'count':'COUNT',
    'sum':'SUM',
    'avg':'AVG',
    'max':'MAX',
    'min':'MIN'
}

# list of tokens

tokens = [ 
    'ID', #identificador
    'PTCOMA', #;
    'IGUAL', #=
    'DECIMAL', #0.1
    'ENTERO', #1
    'PAR_A', #(
    'PAR_C', #)
    'PUNTO', #.
    'COMA', #,
    'CADENA1', # ' hola '
    'CADENA2', # " hola "
    'BOOLEAN', # true | false
    'DESIGUAL', # <>
    'DESIGUAL2', # !=
    'MAYORIGUAL', # >=
    'MENORIGUAL', # <=
    'MAYOR', # >
    'MENOR', # <
    'ASTERISCO', # *
    'RESTA', # -
    'SUMA', # +
    'DIVISION', # /
    'POTENCIA', # ^
    'MODULO', # %
    'DOSPUNTOS', # :
    'SQRT2', # ||
    'CBRT2', # &&
    'AND2', # &
    'NOT2', # ~
    'XOR', # #
    'SH_LEFT', # <<
    'SH_RIGHT' # >>
] + list(Reservadas.values())


# Regular expression rules for simple tokens

t_PTCOMA = r';'
t_PAR_A = r'\('
t_PAR_C = r'\)'
t_COMA = r'\,'
t_PUNTO = r'\.'
t_ASTERISCO = r'\*'
t_DOSPUNTOS =r'::'
t_SQRT2 = r'\|'
t_CBRT2 = r'\|\|'
t_AND2 = r'\&'
t_NOT2 = r'\~'
t_XOR = r'\#'
t_SH_LEFT = r'\<\<'
t_SH_RIGHT = r'\>\>'

#Comparision operators
t_IGUAL = r'\='
t_DESIGUAL = r'\!\='
t_DESIGUAL2 = r'\<\>'
t_MAYORIGUAL = r'\>\='
t_MENORIGUAL = r'\<\='
t_MAYOR = r'\>'
t_MENOR = r'\<'


#arithmetic operators
t_RESTA = r'-'
t_SUMA = r'\+'
t_DIVISION = r'\/'
t_POTENCIA = r'\^'
t_MODULO = r'\%'

# some actions code

def t_DECIMAL(t):
     r'\d+\.\d+'
     try:
          t.value = float(t.value)
     except ValueError:
          print("Valor no es parseable a decimal %d",t.value)
          t.value = 0
     return t    


def t_ENTERO(t):
     r'\d+'
     try:
        t.value = int(t.value)
     except ValueError:
        print('Int valor muy grande %d', t.value)
        t.value = 0
     return t

def t_BOOLEAN(t):
     r'(true|false)'
     mapping = {"true": True, "false": False}
     t.value = mapping[t.value]
     return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = Reservadas.get(t.value.lower(),'ID')
     return t

def t_CADENA1(t):
     r'\".*?\"'
     t.value = t.value[1:-1]
     return t

def t_CADENA2(t):
     r'\'.*?\''
     t.value = t.value[1:-1] 
     return t 

def t_COMENT_MULTI(t):
     r'/\*(.|\n)*?\*/'
     t.lexer.lineno += t.value.count('\n')

def t_COMENT_SIMPLE(t):
     r'--.*\n'
     t.lexer.lineno += 1

t_ignore = " \t"

def t_newline(t):
     r'\n+'
     t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
     print("Caracter Invalido '%s'" % t.value[0])
     Error_Lex.append("Error Lexico: "+t.value[0]+" en la Fila: "+str(int(t.lexer.lineno)))
     t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()


# Operator Association and Precedence
precedence = (
    ('right','NOT'),
    ('left', 'AND', 'OR'),
    ('left', 'IGUAL', 'DESIGUAL'),
    ('left', 'DESIGUAL2', 'MAYORIGUAL'),
    ('left', 'MENORIGUAL', 'MAYOR'),
    ('left', 'MENOR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'ASTERISCO', 'DIVISION'),
    ('left', 'POTENCIA', 'MODULO'),
    ('right', 'UMENOS', 'USQRT2'),
    ('right', 'CBRT2', 'NOT2'),
    ('left', 'SQRT2', 'AND2'),
    ('left', 'XOR', 'SH_LEFT'),
    ('left', 'SH_RIGHT')
)

# Grammar definition

