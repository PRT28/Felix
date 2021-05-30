import string
from interpreter import Number,BuiltIn

#CONSTANTS

DIGITS = "01234566789"
LETTERS = string.ascii_letters
L_D=LETTERS+DIGITS


Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)

BuiltIn.print       = BuiltIn("print")
BuiltIn.print_ret   = BuiltIn("print_ret")
BuiltIn.input       = BuiltIn("input")
BuiltIn.input_int   = BuiltIn("input_int")
BuiltIn.clear       = BuiltIn("clear")
BuiltIn.is_number   = BuiltIn("is_number")
BuiltIn.is_string   = BuiltIn("is_string")
BuiltIn.is_list     = BuiltIn("is_list")
BuiltIn.is_function = BuiltIn("is_function")
BuiltIn.append      = BuiltIn("append")
BuiltIn.pop         = BuiltIn("pop")
BuiltIn.extend      = BuiltIn("extend")

#KEYWORDS

KEYWORDS=[
    'var',
    'and',
    'or',
    'not',
    'if',
    'else',
    'ifel',
    'for',
    'while',
    'function'
    ]

#TOKENS

TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_IDENTIFIER= 'IDENTIFIER'
TT_KEYWORD  = 'KEYWORD'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EQ       = 'EQ'
TT_EOF      = 'EOF'
TT_POW      = 'POW'
TT_EE       = 'EE'
TT_NE       = 'NE'
TT_LT       = 'LT'  
TT_GT       = 'GT'
TT_LTE      = 'LTE'
TT_GTE      = 'GTE'
TT_LCURL    = 'LCURL'
TT_RCURL    = 'RCURL'
TT_COL      = 'COL'
TT_SEMCOL   = 'SEMCOL'
TT_COM     = 'COM'
TT_STRING = 'STRING'
TT_LSQ = 'LSQ'
TT_RSQ = 'RSQ'