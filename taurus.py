import sys

sys.path.append(".")

from lexer import Lexer
from parse import Parser
from interpreter import  Interpreter,Context,SymbolTable,Number


global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))
global_symbol_table.set("FALSE", Number(0))
global_symbol_table.set("TRUE", Number(1))



#RUN

def run(fname,text):
    lexer=Lexer(fname,text)
    tokens,err = lexer.make_tokens()
    if err:return None,err
    
    parser=Parser(tokens)
    ast=parser.parse()
    if ast.error: return None,ast.error
    
    interpreter = Interpreter()
    context=Context('<program>')
    context.symbol=global_symbol_table
    result=interpreter.visit(ast.node,context)    
    
    return result.value,result.error