from error import RTError
from constants import *

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

	def nott(self):
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
			self.pos_start, other.pos_end,
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
		self.value = None
		self.error = None

	def register(self, res):
		if res.error: self.error = res.error
		return res.value

	def success(self, value):
		self.value = value
		return self

	def failure(self, error):
		self.error = error
		return self


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

class Function(Value):
    def __init__(self,name,body,args):
        super().__init__()
        self.name=name or "<anonymous>"
        self.body=body
        self.args=args
        
    def execute(self,args):
        res=RTResult()
        interpreter=Interpreter()
        new_cont=Context(self.name,self.context,self.start)
        new_cont.symbol= SymbolTable(new_cont.parent.symbol)
        
        if len(args)>len(self.args):
            return res.failure(RTError(self.start,self.end,f"{len(args) - len(self.args)} too many args passed into '{self.name}'"),self.context)

        if len(args)<len(self.args):
            return res.failure(RTError(self.start,self.end,f"{len(args) - len(self.args)} too few args passed into '{self.name}'"),self.context)
        
        for i in range(len(args)):
            arg=self.args[i]
            arg_val=args[i]
            arg_val.set_context(new_cont)
            new_cont.symbol.set(arg,arg_val)
            
        value= res.register(interpreter.visit(self.body,new_cont))
        if res.error: return res
        return res.success(value)
    
    def cp(self):
        copy= Function(self.name, self.body, self.args)
        copy.set_context(self.context)
        copy.set_pos(self.start,self.end)
        return copy
    
    def __repr__(self):
        return f"<function {self.name}>"

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

        value = value.cp().set_pos(node.start, node.end)
        return res.success(value)

    def visit_VarAsNode(self, node, context):
        res = RTResult()
        var_name = node.name.val
        value = res.register(self.visit(node.exp, context))
        if res.error: return res

        context.symbol.set(var_name, value)
        return res.success(value)
        
    def visit_NumberNode(self,node,context):
        return RTResult().success(Number(node.token.val).set_context(context).set_pos(node.start,node.end))
    
    def visit_BinaryOP(self,node,context):
        res = RTResult()
        left=res.register(self.visit(node.left,context))
        if res.error: return res
        right=res.register(self.visit(node.right,context))
        if res.error: return res
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
        if res.error: return res
        
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
        
        for cond,expr in node.cases:
            cond_val= res.register(self.visit(cond, context))
            if res.error : return res
            
            if cond_val.is_true():
                expr_val= res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_val)
            
            if node.else_case:
                else_val=res.register(self.visit(node.else_case,context))
                if res.error: return res
                return res.success(else_val)
            
            return res.success(None)
        
    def visit_ForNode(self,node,context):
        res=RTResult()
        
        start_val=res.register(self.visit(node.start_val, context))
        if res.error: return res
        
        end_val=res.register(self.visit(node.end_val,context))
        if res.error: return res
        
        if node.step:
            step=res.register(self.visit(node.step, context))
            if res.error: return res
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
            
            res.register(self.visit(node.body, context))
            if res.error: return res
            
        return res.success(None)
    
    def visit_WhileNode(self,node,context):
        res=RTResult()
        
        while True:
            condition=res.register(self.visit(node.condition, context))
            if res.error: return res
            
            if not condition.is_true(): break
            
            res.register(self.visit(node.body, context))
            if res.error: return res
            
        return res.success(None)
    
    def visit_FunctionNode(self,node,context):
        res=RTResult()
        
        name=node.name.val if node.name else None
        body=node.body
        args= [arg.val for arg in node.args]
        value = Function(name, body, args).set_context(context).set_pos(node.start, node.end)
        
        if node.name:
            context.symbol.set(name,value)
            
        return res.success(value)
    
    def visit_CallNode(self,node,context):
        res=RTResult()
        args=[]
        
        val_cal= res.register(self.visit(node.call_node, context))
        if res.error: return res
        val_cal= val_cal.cp().set_pos(node.start, node.end)
        
        for arg in node.args:
            args.append(res.register(self.visit(arg, context)))
            if res.error: return res
            
        return_val= res.register(val_cal.execute(args))
        if res.error: return res
        return res.success(return_val)
    
    
    
    
        