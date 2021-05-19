import sys

sys.path.append(".")

from lexer import Lexer
from parse import Parser

#CONSTANTS
DIGITS = "01234566789"

#TOKENS

TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EOF      = 'EOF'





#RUN

def run(fname,text):
    lexer=Lexer(fname,text)
    tokens,err = lexer.make_tokens()
    if err:return None,err
    
    else:
        parser=Parser(tokens)
        ast=parser.parse()
        
    
    return ast.node,ast.error