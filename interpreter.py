from error import RTError
from constants import *

# SYMBOL TABLE

class SymbolTable:
	def __init__(self):
		self.symbols = {}
		self.parent = None

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

class Number:
    def __init__(self,value):
        self.value=value
        self.set_pos()
        self.set_context()
        
    def set_pos(self,start=None,end=None):
        self.start=start
        self.end=end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def add(self,other):
        if isinstance(other, Number):
            return Number(self.value+other.value).set_context(self.context),None
        
    def sub(self,other):
        if isinstance(other, Number):
            return Number(self.value-other.value).set_context(self.context),None
        
    def mul(self,other):
        if isinstance(other, Number):
            return Number(self.value*other.value).set_context(self.context),None
        
    def power(self,other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context),None
        
    def div(self,other):
        if isinstance(other, Number):
            if other.value==0:
                return None,RTError(other.start,other.end,"Division by zero",self.context)
            else:
                return Number(self.value/other.value).set_context(self.context),None
            
    def ee(self,other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context),None
    def ne(self,other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context),None
    def lt(self,other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context),None
    def lte(self,other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context),None
    def gt(self,other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context),None
    def gte(self,other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context),None
    def andd(self,other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context),None
    def orr(self,other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context),None
    def nott(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
            
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.start, self.end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value != 0
        
    def __repr__(self):
        return str(self.value)



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

        value = value.copy().set_pos(node.start, node.end)
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
        