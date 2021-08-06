from error import RTError
from constants import *
import os
from lexer import Lexer
from parse import Parser




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
TT_COM     = 'COM'
TT_STRING = 'STRING'
TT_LSQ = 'LSQ'
TT_RSQ = 'RSQ'
TT_SEMCOL= 'SEMCOL'

#Function Values

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, start=None, end=None):
		self.start = start
		self.end = end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def add(self, other):
		return None, self.illegal_operation(other)

	def sub(self, other):
		return None, self.illegal_operation(other)

	def mul(self, other):
		return None, self.illegal_operation(other)

	def div(self, other):
		return None, self.illegal_operation(other)

	def power(self, other):
		return None, self.illegal_operation(other)

	def ee(self, other):
		return None, self.illegal_operation(other)

	def ne(self, other):
		return None, self.illegal_operation(other)

	def lt(self, other):
		return None, self.illegal_operation(other)

	def gt(self, other):
		return None, self.illegal_operation(other)

	def lte(self, other):
		return None, self.illegal_operation(other)

	def gte(self, other):
		return None, self.illegal_operation(other)

	def andd(self, other):
		return None, self.illegal_operation(other)

	def ore(self, other):
		return None, self.illegal_operation(other)

	def nott(self, other):
		return None, self.illegal_operation(other)

	def execute(self, args):
		return RTResult().failure(self.illegal_operation())

	def copy(self):
		raise Exception('No copy method defined')

	def is_true(self):
		return False

	def illegal_operation(self, other=None):
		if not other: other = self
		return RTError(
			self.start, other.end,
			'Illegal operation',
			self.context
		)

# SYMBOL TABLE

class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]

#CONTEXT

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
         self.display_name = display_name
         self.parent = parent
         self.parent_entry_pos = parent_entry_pos
         self.symbol=None

#RUNTIME RESULT

class RTResult:
	def __init__(self):
         self.reset()
            
	def reset(self):
		self.value = None
		self.error = None
		self.func_ret_val=None
		self.loop_continue=False
		self.loop_break=False

    
	def register(self, res):
		self.error = res.error
		self.func_ret_val=res.func_ret_val
		self.loop_continue=res.loop_continue
		self.loop_break=res.loop_break
		return res.value

	def success(self, value):
		self.reset()
		self.value = value
		return self
    
	def success_return(self, value):
		self.reset()
		self.func_ret_val = value
		return self
      
	def success_continue(self):
		self.reset()
		self.loop_continue = True
		return self
    
	def success_break(self):
		self.reset()
		self.loop_break = True
		return self

	def failure(self, error):
		self.reset()
		self.error = error
		return self
    
	def should_return(self):
		return(self.error or
      self.func_ret_val or
      self.loop_continue or
      self.loop_break)


#VALLUES

class Number(Value):
    def __init__(self,value):
        super().__init__()
        self.value=value
    
    def add(self,other):
        if isinstance(other, Number):
            return Number(self.value+other.value).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
        
    def sub(self,other):
        if isinstance(other, Number):
            return Number(self.value-other.value).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
        
    def mul(self,other):
        if isinstance(other, Number):
            return Number(self.value*other.value).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
        
    def power(self,other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
        
    def div(self,other):
        if isinstance(other, Number):
            if other.value==0:
                return None,RTError(other.start,other.end,"Division by zero",self.context)
            else:
                return Number(self.value/other.value).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
            
    def ee(self,other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def ne(self,other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def lt(self,other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def lte(self,other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def gt(self,other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def gte(self,other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def andd(self,other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def orr(self,other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context),None
        else:
            return None, Value.illegal_operation(self,other)
    def nott(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
            
    def cp(self):
        copy = Number(self.value)
        copy.set_pos(self.start, self.end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value != 0
        
    def __repr__(self):
        return str(self.value)

#FUNCTION CLASS

class BaseFunc(Value):
    def __init__(self,name):
        super().__init__()
        self.name=name or "<anonymous>"
        
    def gen_new_cont(self):
        new_cont=Context(self.name,self.context,self.start)
        new_cont.symbol= SymbolTable(new_cont.parent.symbol)
        return new_cont
    
    def check_args(self,arg_names,args):
        res=RTResult()
        if len(args)>len(arg_names):
            return res.failure(RTError(self.start,self.end,f"{len(args) - len(arg_names)} too many args passed into '{self.name}'"),self.context)

        if len(args)<len(arg_names):
            return res.failure(RTError(self.start,self.end,f"{len(arg_names) - len(args)} too few args passed into '{self.name}'"),self.context)
        
        return res.success(None)
    
    def populate_args(self,arg_names,args,cont):
        for i in range(len(args)):
            arg=arg_names[i]
            arg_val=args[i]
            arg_val.set_context(cont)
            cont.symbol.set(arg,arg_val)
            
    def check_and_populate_args(self,arg_names,args,cont):
        res=RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, cont)
        return res.success(None)

class Function(BaseFunc):
    def __init__(self,name,body,arg_names, ret):
        super().__init__(name)
        self.body=body
        self.arg_names=arg_names
        self.ret=ret
        
    def execute(self,args):
        res=RTResult()
        interpreter=Interpreter()
        new_cont=self.gen_new_cont()
        
        res.register(self.check_and_populate_args(self.arg_names,args,new_cont))
        if res.should_return(): return res
            
        value= res.register(interpreter.visit(self.body,new_cont))
        if res.should_return() and res.func_ret_val==None: return res
        ret_value = (value if self.ret else None) or res.func_ret_val or Number.null
        return res.success(ret_value)
    
    def cp(self):
        copy= Function(self.name, self.body, self.arg_names, self.ret)
        copy.set_context(self.context)
        copy.set_pos(self.start,self.end)
        return copy
    
    def __repr__(self):
        return f"<function {self.name}>"
    
Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
    
class BuiltIn(BaseFunc):
    def __init__(self,name):
        super().__init__(name)
        
    def execute(self,args):
        res=RTResult()
        new_cont=self.gen_new_cont()
        
        method_name=f'execute_{self.name}'
        method=getattr(self, method_name, self.no_visit_method)
        res.register(self.check_and_populate_args(method.arg_names, args, new_cont))
        if res.should_return(): return res
        return_value = res.register(method(new_cont))
        if res.should_return(): return res
        return res.success(return_value)
    
    def no_visit_method(self):
         raise Exception(f'No execute_{self.name} method defined')
         
    def cp(self):
        copy= BuiltIn(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.start,self.end)
        return copy
    
    def __repr__(self):
        return f"<Built-in function {self.name}>"
    
    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol.get('value')))
        return RTResult().success(Number.null)
    execute_print.arg_names = ['value']
    
    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol.get('value'))))
    execute_print_ret.arg_names = ['value']
  
    def execute_input(self, exec_ctx):
        text = input()
        return RTResult().success(String(text))
    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        while True:
            text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
                return RTResult().success(Number(number))
    execute_input_int.arg_names = []
    
    def execute_clear(self, exec_ctx):
      os.system('cls' if os.name == 'nt' else 'clear') 
      return RTResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol.get("value"), String)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
       is_number = isinstance(exec_ctx.symbol.get("value"), List)
       return RTResult().success(Number.true if is_number else Number.false)
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol.get("value"), BaseFunc)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol.get("list")
        value = exec_ctx.symbol.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
                ))

        list_.elements.append(value)
        return RTResult().success(Number.null)
    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol.get("list")
        index = exec_ctx.symbol.get("index")
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
                ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
                ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
                ))
        return RTResult().success(element)
    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol.get("listA")
        listB = exec_ctx.symbol.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
                ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
                ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)
    execute_extend.arg_names = ["listA", "listB"]
    
    def execute_len(self,exec_ctx):
        list_ = exec_ctx.symbol.get("list")
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
        self.start, self.end,
        "Argument must be list",
        exec_ctx
      ))
        return RTResult().success(Number(len(list_.elements)))
    execute_len.arg_names = ["list"]
        
    
    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol.get("fn")
    
        if not isinstance(fn, String):
          return RTResult().failure(RTError(
            self.start, self.end,
            "Second argument must be string",
            exec_ctx
          ))
    
        fn = fn.value
    
        try:
          with open(fn, "r") as f:
            script = f.read()
        except Exception as e:
          return RTResult().failure(RTError(
            self.start, self.end,
            f"Failed to load script \"{fn}\"\n" + str(e),
            exec_ctx
          ))
    
        _, error = run(fn, script)
        
        if error:
          return RTResult().failure(RTError(
            self.start, self.end,
            f"Failed to finish executing script \"{fn}\"\n" +
            error.as_string(),
            exec_ctx
          ))
    
        return RTResult().success(Number.null)
    execute_run.arg_names = ["fn"]

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
BuiltIn.len         = BuiltIn("len")
BuiltIn.run         = BuiltIn("run")

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
    
class String(Value):
    def __init__(self,value):
        super().__init__()
        self.value=value
        
    def add(self, other):
        if isinstance(other, String):
            return String(self.value+other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def mul(self, other):
        if isinstance(other, Number):
            return String(self.value*other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def is_true(self):
        return len(self.value)>0
    
    def cp(self):
        copy= String(self.value)
        copy.set_context(self.context)
        copy.set_pos(self.start,self.end)
        return copy
    
    def __repr__(self):
        return f"{self.value}"
    
class List(Value):
    def __init__(self,elements):
        super().__init__()
        self.elements=elements
        
    def add(self, other):
        l=self.cp()
        l.elements.append(other)
        return l, None
        
    def sub(self, other):
        if isinstance(other, Number):
            l=self.cp()
            
            try:
                l.elements.pop(other.value)
                return l, None
            except:
                return None, RTError(other.start,other.end,'Index Out of Bounds',self.context)
            
        else:
            return None, Value.illegal_operation(self, other)
        
    def mul(self,other):
        if isinstance(other, List):
            l=self.cp()
            l.elements.extend(other.elements)
            return l, None
        else:
            return None, Value.illegal_operation(self, other)
        
    def div(self,other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(other.start,other.end,'Index Out of Bounds',self.context)
            
        else:
            return None, Value.illegal_operation(self, other)
        
    def cp(self):
        copy= List(self.elements)
        copy.set_context(self.context)
        copy.set_pos(self.start,self.end)
        return copy
    
    def __repr__(self):
        return f'[{",".join([str(x) for x in self.elements])}]'

#INTERPRETER

class Interpreter:
    def visit(self,node,context):
        name=f'visit_{type(node).__name__}'
        method=getattr(self, name,self.no_visit_method)
        return method(node,context)
    
    def no_visit_method(self,node,context):
        raise Exception("No visit method defined")
        
    def visit_VarAccNode(self, node, context):
        res = RTResult()
        var_name = node.token.val
        value = context.symbol.get(var_name)

        if not value:
            return res.failure(RTError(
				node.start, node.end,
				f"'{var_name}' is not defined",
				context
			))

        value = value.cp().set_pos(node.start, node.end).set_context(context)
        return res.success(value)

    def visit_VarAsNode(self, node, context):
        res = RTResult()
        var_name = node.name.val
        value = res.register(self.visit(node.exp, context))
        if res.should_return(): return res

        context.symbol.set(var_name, value)
        return res.success(value)
        
    def visit_NumberNode(self,node,context):
        return RTResult().success(Number(node.token.val).set_context(context).set_pos(node.start,node.end))
    
    def visit_StringNode(self,node,context):
        return RTResult().success(String(node.token.val).set_context(context).set_pos(node.start,node.end))
    
    def visit_BinaryOP(self,node,context):
        res = RTResult()
        left=res.register(self.visit(node.left,context))
        if res.should_return(): return res
        right=res.register(self.visit(node.right,context))
        if res.should_return(): return res
        result=Number(None)
        
        if node.op.type_ == TT_PLUS:
            result,error=left.add(right)
        elif node.op.type_ == TT_MINUS:
            result,error=left.sub(right)
        elif node.op.type_ == TT_MUL:
            result,error=left.mul(right)
        elif node.op.type_ == TT_DIV:
            result,error=left.div(right)
        elif node.op.type_ == TT_POW:
            result,error=left.power(right)
        elif node.op.type_ == TT_EE:
            result,error=left.ee(right)
        elif node.op.type_ == TT_NE:
            result,error=left.ne(right)
        elif node.op.type_ == TT_LT:
            result,error=left.lt(right)
        elif node.op.type_ == TT_LTE:
            result,error=left.lte(right)
        elif node.op.type_ == TT_GT:
            result,error=left.gte(right)
        elif node.op.type_ == TT_GTE:
            result,error=left.gte(right)
        elif node.op.match(TT_KEYWORD,"and"):
            result,error=left.andd(right)
        elif node.op.match(TT_KEYWORD,"or"):
            result,error=left.orr(right)
        
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.start,node.end))

    def visit_UnaryOP(self,node,context):
        res=RTResult()
        num=res.register(self.visit(node.node,context))
        if res.should_return(): return res
        
        error=None
        
        if node.token.type_ == TT_MINUS:
            num,error=num.mul(Number(-1))
        elif node.token.match(TT_KEYWORD,"not"):
            num, error=num.nott()
            
        if error: return res.faliure(error)
        else:
            return res.success(num.set_pos(node.start,node.end))
        
    def visit_IfNode(self,node,context):
        res=RTResult()
        
        for cond,expr,ret_null in node.cases:
            cond_val= res.register(self.visit(cond, context))
            if res.should_return() : return res
            
            if cond_val.is_true():
                expr_val= res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if ret_null else expr_val)
            
            if node.else_case:
                expr, ret_null=node.else_case
                else_val=res.register(self.visit(expr,context))
                if res.should_return(): return res
                return res.success(Number.null if ret_null else else_val)
            
            return res.success(Number.null)
        
    def visit_ForNode(self,node,context):
        res=RTResult()
        li=[]
        
        start_val=res.register(self.visit(node.start, context))
        if res.should_return(): return res
        
        end_val=res.register(self.visit(node.end_val,context))
        if res.should_return(): return res
        
        if node.step:
            step=res.register(self.visit(node.step, context))
            if res.should_return(): return res
        else:
            step=Number(1)
        
        i=start_val.value
        if step.value>=0:
            condition=lambda: i<end_val.value
        else:
            condition=lambda: i>end_val.value
            
        while condition():
            context.symbol.set(node.name.val,Number(i))
            i += step.value
            
            value= res.register(self.visit(node.body, context))
            if res.should_return() and res.loop_continue == False and res.loop_break == False: return res
            if res.loop_continue: continue
            if res.loop_break: break
            li.append(value)
            
        return res.success(Number.null if node.ret_null else List(li).set_context(context).set_pos(node.start,node.end))
    
    def visit_WhileNode(self,node,context):
        res=RTResult()
        li=[]
        
        while True:
            condition=res.register(self.visit(node.condition, context))
            if res.should_return(): return res
            
            if not condition.is_true(): break
            
            value=res.register(self.visit(node.body, context))
            if res.should_return() and res.loop_continue == False and res.loop_break == False: return res
            if res.loop_continue: continue
            if res.loop_break: break
            li.append(value)
            
        return res.success(Number.null if node.ret_null else List(li).set_context(context).set_pos(node.start,node.end))
    
    def visit_FunctionNode(self,node,context):
        res=RTResult()
        
        name=node.name.val if node.name else None
        body=node.body
        args= [arg.val for arg in node.args]
        value = Function(name, body, args, node.ret).set_context(context).set_pos(node.start, node.end)
        
        if node.name:
            context.symbol.set(name,value)
            
        return res.success(value)
    
    def visit_CallNode(self,node,context):
        res=RTResult()
        args=[]
        
        val_cal= res.register(self.visit(node.call_node, context))
        if res.should_return(): return res
        val_cal= val_cal.cp().set_pos(node.start, node.end)
        
        for arg in node.args:
            args.append(res.register(self.visit(arg, context)))
            if res.should_return(): return res
            
        return_val= res.register(val_cal.execute(args))
        if res.should_return(): return res
        return_val = return_val.cp().set_pos(node.start, node.end).set_context(context)
        return res.success(return_val)
    
    def visit_ListNode(self,node,context):
        res= RTResult()
        el=[]
        
        for e in node.elements:
            el.append(res.register(self.visit(e,context)))
            if res.should_return(): return res
            
        return res.success(List(el).set_context(context).set_pos(node.start,node.end))
    
    def visit_ReturnNode(self,node,context):
        res=RTResult()
        
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value=Number.null
            
        return res.success_return(value)
    
    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()
    
    def visit_BreakNode(self, node, context):
        return RTResult().success_break()
    
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
    
    
        