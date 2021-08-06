import sys

sys.path.append(".")

from lexer import Lexer
from parse import Parser
from interpreter import  Interpreter,Context,SymbolTable,Number,BuiltIn
from constants import *


global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("print", BuiltIn.print)
global_symbol_table.set("print_r", BuiltIn.print_ret)
global_symbol_table.set("input", BuiltIn.input)
global_symbol_table.set("input_int", BuiltIn.input_int)
global_symbol_table.set("clear", BuiltIn.clear)
global_symbol_table.set("cls", BuiltIn.clear)
global_symbol_table.set("is_num", BuiltIn.is_number)
global_symbol_table.set("is_str", BuiltIn.is_string)
global_symbol_table.set("is_list", BuiltIn.is_list)
global_symbol_table.set("is_func", BuiltIn.is_function)
global_symbol_table.set("append", BuiltIn.append)
global_symbol_table.set("pop", BuiltIn.pop)
global_symbol_table.set("extend", BuiltIn.extend)
global_symbol_table.set("len", BuiltIn.len)
global_symbol_table.set("run", BuiltIn.run)



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