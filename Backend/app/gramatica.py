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

reservadas = {
    'smallint': 'SMALLINT',
    'integer': 'INTEGER',
    'biginit': 'BIGINIT',
    'decimal': 'DECIMAL',
    'numeric': 'NUMERIC',
    'real': 'REAL',
    'double': 'DOUBLE',
    'precision': 'PRECISION',
    'money': 'MONEY',
    'varchar': 'VARCHAR',
    'character': 'CHARACTER',
    'text': 'TEXT',
    'timestamp': 'TIMESTAMP',
    'without': 'WITHOUT',
    'time': 'TIME',
    'zone': 'ZONE',
    'with': 'WITH',
    'date': 'DATE',
    'interval': 'INTERVAL',
    'year': 'YEAR',
    'month': 'MONTH',
    'day': 'DAY',
    'hour': 'HOUR',
    'minute': 'MINUTE',
    'second': 'SECOND',
    'to': 'TO',
    'boolean': 'BOOLEAN',
    'create': 'CREATE',
    'type': 'TYPE',
    'as': 'AS',
    'enum': 'ENUM',
    'between': 'BETWEEN',
    'in': 'IN',
    'like': 'LIKE',
    'ilike': 'ILIKE',
    'similar': 'SIMILAR',
    'isnull': 'ISNULL',
    'notnull': 'NOTNULL',
    'not': 'NOT',
    'null': 'NULL',
    'and': 'AND',
    'or': 'OR',
    'replace': 'REPLACE',
    'database': 'DATABASE',
    'if': 'IF',
    'exists': 'EXISTS',
    'owner': 'OWNER',
    'mode': 'MODE',
    'show': 'SHOW',
    'databases': 'DATABASES',
    'alter': 'ALTER',
    'rename': 'RENAME',
    'drop': 'DROP',
    'table': 'TABLE',
    'constraint': 'CONSTRAINT',
    'unique': 'UNIQUE',
    'check': 'CHECK',
    'primary': 'PRIMARY',
    'key': 'KEY',
    'references': 'REFERENCES',
    'foreign': 'FOREIGN',
    'add': 'ADD',
    'set': 'SET',
    'delete': 'DELETE',
    'from': 'FROM',
    'where': 'WHERE',
    'inherits': 'INHERITS',
    'insert': 'INSERT',
    'into': 'INTO',
    'update': 'UPDATE',
    'values': 'VALUES',
    'select': 'SELECT',
    'distinct': 'DISTINCT',
    'group': 'GROUP',
    'by': 'BY',
    'having': 'HAVING',
    'sum': 'SUM',
    'count': 'COUNT',
    'avg': 'AVG',
    'max': 'MAX',
    'min': 'MIN',
    'abs': 'ABS',
    'cbrt': 'CBRT',
    'ceil': 'CEIL',
    'ceiling': 'CEILING',
    'degrees': 'DEGREES',
    'div': 'DIV',
    'exp': 'EXP',
    'factorial': 'FACTORIAL',
    'floor': 'FLOOR',
    'gcd': 'GCD',
    'lcm': 'LCM',
    'ln': 'LN',
    'log': 'LOG',
    'log10': 'LOG10',
    'min_scale': 'MIN_SCALE',
    'mod': 'MOD',
    'pi': 'PI',
    'power': 'POWER',
    'radians': 'RADIANS',
    'round': 'ROUND',
    'scale': 'SCALE',
    'sign': 'SIGN',
    'sqrt': 'SQRT',
    'trim_scale': 'TRIM_SCALE',
    'width_bucket': 'WIDTH_BUCKET',
    'random': 'RANDOM',
    'setseed': 'SETSEED',
    'acos': 'ACOS',
    'acosd': 'ACOSD',
    'asin': 'ASIN',
    'asind': 'ASIND',
    'atan': 'ATAN',
    'atand': 'ATAND',
    'atan2': 'ATAN2',
    'atan2d': 'ATAN2D',
    'cos': 'COS',
    'cosd': 'COSD',
    'cot': 'COT',
    'cotd': 'COTD',
    'sin': 'SIN',
    'sind': 'SIND',
    'tan': 'TAN',
    'tand': 'TAND',
    'sinh': 'SINH',
    'cosh': 'COSH',
    'tanh': 'TANH',
    'asinh': 'ASINH',
    'acosh': 'ACOSH',
    'atanh': 'ATANH',
    'length': 'LENGTH',
    'substring': 'SUBSTRING',
    'trim': 'TRIM',
    'get_byte': 'GET_BYTE',
    'md5': 'MD5',
    'set_byte': 'SET_BYTE',
    'sha256': 'SHA256',
    'substr': 'SUBSTR',
    'convert': 'CONVERT',
    'encode': 'ENCODE',
    'decode': 'DECODE',
    'extract': 'EXTRACT',
    'century': 'CENTURY',
    'decade': 'DECADE',
    'dow': 'DOW',
    'doy': 'DOY',
    'epoch': 'EPOCH',
    'isodown': 'ISODOWN',
    'isoyear': 'ISOYEAR',
    'microseconds': 'MICROSECONDS',
    'millennium': 'MILENNIUM',
    'milliseconds': 'MILLISECONDS',
    'quarter': 'QUARTER',
    'timezone': 'TIMEZONE',
    'timezone_hour': 'TIMEZONE_HOUR',
    'timezone_minute': 'TIMEZONE_MINUTE',
    'week': 'WEEK',
    'at': 'AT',
    'current_date': 'CURRENT_DATE',
    'current_time': 'CURRENT_TIME',
    'current_timestamp': 'CURRENT_TIMESTAMP',
    'localtime': 'LOCALTIME',
    'localtimestamp': 'LOCALTIMESTAMP',
    'pg_sleep': 'PG_SLEEP',
    'pg_sleep_for': 'PG_SLEEP_FOR',
    'pg_sleep_until': 'PG_SLEEP_UNTIL',
    'inner': 'INNER',
    'left': 'LEFT',
    'right': 'RIGHT',
    'full': 'FULL',
    'outer': 'OUTER',
    'join': 'JOIN',
    'all': 'ALL',
    'any': 'ANY',
    'some': 'SOME',
    'order': 'ORDER',
    'asc': 'ASC',
    'desc': 'DESC',
    'case': 'CASE',
    'when': 'WHEN',
    'then': 'THEN',
    'else': 'ELSE',
    'end': 'END',
    'greatest': 'GREATEST',
    'least': 'LEAST',
    'limit': 'LIMIT',
    'union': 'UNION',
    'intersect': 'INTERSECT',
    'except': 'EXCEPT',
    'is':   'IS',
    'default':   'DEFAULT',
    'true':   'TRUE',
    'false':   'FALSE',
    'column': 'COLUMN',
    'current_user': 'CURRENT_USER',
    'session_user': 'SESSION_USER',
    'date_part':   'DATE_PART',
    'now':   'NOW',
    'trunc':   'TRUNC',
    'offset':   'OFFSET',
    'nulls':   'NULLS',
    'first':   'FIRST',
    'last':   'LAST',
    'char':   'CHAR',
    'use':    'USE'
}

# list of tokens

tokens = [
    'semicolon', # ;
    'comma', # ,
    'point', # .
    'plus', # + 
    'minus', # -
    'times', # *
    'division', # /
    'exp', # ^
    'mod', # %
    'equal', # =
    # Expresiones Relacionales
    'equals', # ==
    'greater', # >
    'less', # <
    'greater_equal', # >=
    'less_equal', # <=
    'not_equal', # !=
    # Expresiones Logicas
    'and', # &&
    'or', # ||
    'not', # !
    'open_parenthesis', # (
    'close_parenthesis', # )
    'open_square_bracket', # [
    'close_square_bracket', # ]
    'open_bracket', # {
    'close_bracket', # }
    'decimal_number', # 1.0
    'integer_number', # 1
    'string_literal', # 'string'
    'identifier', # name
    'spaces', # \s
    'line_comment', # --
] + list(reservadas.values())

# Regular expression rules for simple tokens

t_semicolon = r';'
t_comma = r','
t_point = r'\.'
t_plus = r'\+'
t_minus = r'-'
t_times = r'\*'
t_division = r'/'
t_exp = r'\^'
t_mod = r'%'
t_equal = r'='
t_greater = r'>'
t_less = r'<'
t_greater_equal = r'>='
t_less_equal = r'<='
t_not_equal = r'!='
t_and = r'&&'
t_or = r'\|\|'
t_not = r'!'
t_open_parenthesis = r'\('
t_close_parenthesis = r'\)'
t_open_square_bracket = r'\['
t_close_square_bracket = r'\]'
t_open_bracket = r'\{'
t_close_bracket = r'\}'
t_decimal_number = r'\d+\.\d+'
t_integer_number = r'\d+'
t_string_literal = r'\'.*?\''
t_identifier = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_spaces = r'\s+'
t_line_comment = r'--.*'

# some actions code

def t_DECIMAL_NUMBER(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error no se puede convertir %d", t.value)
        t.value = 0
    return t

def t_INTEGER_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Error no se puede convertir %d", t.value)
        t.value = 0
    return t

def t_STRING_LITERAL(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas simples
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(),'IDENTIFIER')    # Check for reserved words
    return t

def t_LINE_COMMENT(t):
    r'--.*'
    pass
    # No return value. Token discarded
    
def t_SPACES(t):
    r' |\t'
    global columna
    if t.value == '\t':

        columna = IncColuma(columna+8)
    else:

        columna = IncColuma(columna)


# Caracteres ignorados
t_ignore = "\r"

global columna
columna = 0
numNodo = 0


def incNodo(valor):
    global numNodo
    numNodo = numNodo + 1
    return numNodo


def IncColuma(valor):
    columna = valor + 1
    return columna

    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    global columna
    columna = 0

def t_error(t):
    print("token: '%s'" % t)
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def crear_nodo_general(nombre, valor, fila, column):
    nNodo = incNodo(numNodo)
    nodoEnviar = nodoGeneral.NodoGeneral()
    nodoEnviar.setearValores(fila, columna, nombre, nNodo, valor, [])
    return nodoEnviar

# Build the lexer
lexer = lex.lex(reflags= re.IGNORECASE)

# Operator Association and Precedence
precedence = (
    ('left', 'or'),
    ('left', 'and'),
    ('right', 'not'),
    ('left', 'equals', 'greater', 'less', 'greater_equal', 'less_equal', 'not_equal'),
    ('left', 'plus', 'minus'),
    ('left', 'times', 'division', 'mod'),
    ('left', 'exp'),
)

# Grammar definition

