import string

#CONSTANTS

DIGITS = "01234566789"
LETTERS = string.ascii_letters
L_D=LETTERS+DIGITS

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