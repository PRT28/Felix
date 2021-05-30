import sys

sys.path.append(".")

from error import InvalidSyntaxError
from constants import *


#NODES

class NumberNode:
    def __init__(self,token):
        self.token=token
        self.start=self.token.start
        self.end=self.token.end
        
    def __repr__(self):
        return f'{self.token}'
    
class StringNode:
    def __init__(self,token):
        self.token=token
        self.start=self.token.start
        self.end=self.token.end
        
    def __repr__(self):
        return f'{self.token}'
    
class ListNode:
    def __init__(self,elements,start,end):
        self.elements=elements
        self.start=start
        self.end=end

class VarAccNode:
    def __init__(self,token):
        self.token=token
        self.start=token.start
        self.end=token.end
        
class VarAsNode:
    def __init__(self,name,exp):
        self.name=name
        self.exp=exp
        self.start=name.start
        self.end=exp.end

class IfNode:
    def __init__(self,cases,else_case):
        self.cases=cases
        self.else_case=else_case
        self.start=cases[0][0].start
        self.end=(self.else_case or self.cases[len(self.cases) - 1][0]).end
        
class ForNode:
    def __init__(self,name,start_val,end_val,step,body):
        self.name=name
        self.start_val=start_val
        self.end_val=end_val
        self.step=step
        self.body=body
        self.start=self.name.start
        self.end=self.body.end
        
class WhileNode:
    def __init__(self,condition,body):
        self.condition=condition
        self.body=body
        self.start=self.condition.start
        self.end=self.body.end
        
class FunctionNode:
    def __init__(self,name,args,body):
        self.name=name
        self.args=args
        self.body=body
        self.start=self.name.start
        if self.name:
            self.start=self.name.start
        elif len(self.args)>0:
            self.start=self.args[0].start
        else:
            self.start=self.body.start
            
        self.end=self.body.end
        
class CallNode:
    def __init__(self,call_node,args):
        self.call_node=call_node
        self.args=args
        self.start=call_node.start
        if len(self.args)>0:
            self.end=self.args[len(self.args)-1].end
        else:
            self.end=self.call_node.end
    
class BinaryOP:
    def __init__(self,left,op,right):
        self.right=right
        self.left=left
        self.op=op
        self.start=self.left.start
        self.end=self.right.end
        
    def __repr__(self):
        return f'({self.left},{self.op},{self.right})'
    
class UnaryOP:
     def __init__(self, token, node):
        self.token = token
        self.node = node
        self.start=self.token.start
        self.end=self.node.end

     def __repr__(self):
        return f'({self.token}, {self.node})'
    

#PARSE RESULT CHECKER

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.advance_count = 0

	def register_advancement(self):
		self.advance_count += 1

	def register(self, res):
		self.advance_count += res.advance_count
		if res.error: self.error = res.error
		return res.node

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		if not self.error or self.advance_count == 0:
			self.error = error
		return self

    
#PARSER

class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.token_idx=-1
        self.advance()
    
    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.curr_token=self.tokens[self.token_idx]
        return self.curr_token
    
    def parse(self):
        res = self.expr()
        if not res.error and self.curr_token.type_ != TT_EOF:
            return res.failure(InvalidSyntaxError(
				self.curr_token.start, self.curr_token.end,
				"Expected '+', '-', '*' or '/'"
			))
        return res
    
    def call(self):
            res=ParseResult()
            atom=res.register(self.atom())
            if res.error: return res
            
            if self.curr_token.type_ == TT_LPAREN:
                res.register_advancement()
                self.advance()
                args=[]
                
                if self.curr_token.type_ == TT_RPAREN:
                    res.register_advancement()
                    self.advance()
                    
                else:
                    args.append(res.register(self.expr()))
                    if res.error:
                        return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected 'VAR', int, float, identifier, '+', '-' or ')'"))
                    
                    while self.curr_token.type_ == TT_COM:
                        res.register_advancement()
                        self.advance()
                        args.append(res.register(self.expr()))
                        if res.error: return res
                      
                    if self.curr_token.type_ != TT_RPAREN:
                        return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected ',' or ')'"))
        
                    res.register_advancement()
                    self.advance()
                    
                return res.success(CallNode(atom, args))
            return res.success(atom)
    
    def if_expr(self):
        res=ParseResult()
        cases=[]
        else_case=None
        
        if not self.curr_token.match(TT_KEYWORD,'if'):
            return res.faliure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,f"Expected 'if'"))
        res.register_advancement()
        self.advance()
        cond=res.register(self.expr())
        if res.error : return res
        
        if not self.curr_token.type_==TT_LCURL:
            return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '{'"))
        
        res.register_advancement()
        self.advance()
        expr=res.register(self.expr())
        if res.error: return res
        cases.append((cond,expr))
        
        if not self.curr_token.type_==TT_RCURL:
            return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '}'"))
        
        res.register_advancement()
        self.advance()
        
        while self.curr_token.match(TT_KEYWORD,"ifel"):
            res.register_advancement()
            self.advance()
            
            cond=res.register(self.expr())
            if res.error: return res
            
            if not self.curr_token.type_==TT_LCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '{'"))
            
            res.register_advancement()
            self.advance()
            expr=res.register(self.expr())
            if res.error: return res
            cases.append((cond,expr))
        
            if not self.curr_token.type_==TT_RCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '}'"))
            
            res.register_advancement()
            self.advance()
            
        if self.curr_token.match(TT_KEYWORD,'else'):
            res.register_advancement()
            self.advance()
            
            if not self.curr_token.type_==TT_LCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '{'"))
            
            else_case=res.register(self.expr)
            if res.error: return res
            
            if not self.curr_token.type_==TT_RCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '}'"))
            
            res.register_advancement()
            self.advance()
            
        return res.success(IfNode(cases, else_case))
            
    def for_expr(self):
        res=ParseResult()
        
        if not self.curr_token.match(TT_KEYWORD,'for'):
            return res.faliure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected 'for'"))
        
        res.register_advancement()
        self.advance()
        
        if self.curr_token.type_ != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected identifier"))
        
        var_name=self.curr_token
        res.register_advancement()
        self.advance()
        
        if self.curr_token.type_ != TT_EQ:
            return res.faliure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '='"))
        
        res.register_advancement()
        self.advance()
        start_val=res.register(self.expr())
        if res.error: return res
        
        if not self.curr_token.type_ == TT_COL:
            return res.faliure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected ':'"))
        
        res.register_advancement()
        self.advance()
        
        end_val=res.register(self.expr())
        if res.error: return res
        
        if self.curr_token.type_ == TT_SEMCOL:
            res.register_advancement()
            self.advance()
            
            step=res.register(self.expr())
            if res.error: return res
        else:
            step=None
            
        if not self.curr_token.type_==TT_LCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '{'"))
            
        res.register_advancement()
        self.advance()
        
        body=res.register(self.expr())
        if res.error: return res
        
        if not self.curr_token.type_==TT_RCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '}'"))
            
        res.register_advancement()
        self.advance()
        
        return res.success(ForNode(var_name, start_val, end_val, step, body))
    
    def while_expr(self):
        res=ParseResult()
        
        if not self.curr_token.match(TT_KEYWORD,'while'):
            return res.faliure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected 'while'"))
        
        res.register_advancement()
        self.advance()
        
        condition=res.register(self.expr())
        if res.error: return res
        
        if not self.curr_token.type_==TT_LCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '{'"))
            
        res.register_advancement()
        self.advance()
        body=res.register(self.expr())
        if res.error: return res
        
        if not self.curr_token.type_==TT_RCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '}'"))
            
        res.register_advancement()
        self.advance()
        
        return res.success(WhileNode(condition, body))
        
    
    def atom(self):
        res=ParseResult()
        token=self.curr_token
        
        if token.type_ in (TT_INT,TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))
        
        elif token.type_ == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(token))
        
        elif token.type_ == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccNode(token))
        
        elif token.type_ == TT_LSQ:
            li=res.register(self.li())
            if res.error: return res
            return res.success(li)
        
        elif token.type_ == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr= res.register(self.expr())
            if res.error: return res
            if self.curr_token.type_ == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
					self.curr_token.start, self.curr_token.end,
					"Expected ')'"
				))
            
        elif token.match(TT_KEYWORD,'if'):
            if_expr=res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        
        elif token.match(TT_KEYWORD,'for'):
            for_expr=res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)
        
        elif token.match(TT_KEYWORD,'while'):
            while_expr=res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)
        
        elif token.match(TT_KEYWORD,'function'):
            func=res.register(self.func_def())
            if res.error: return res
            return res.success(func)
        
        return res.failure(InvalidSyntaxError(
			token.start, token.end,
			"Expected int, float, identifier, '+', '-' or '('"
		))
    
    def comp(self):
        res=ParseResult()
        
        if self.curr_token.match(TT_KEYWORD, "not"):
            op=self.curr_token
            res.register_advancement()
            self.advance()
            
            exp=res.register(self.comp())
            if res.error: return res
            return res.success(UnaryOP(op, exp))
        
        exp = res.register(self.bIN(self.arith, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error: return res.failure(InvalidSyntaxError(
			self.curr_token.start, self.curr_token.end,
			"Expected int, float, identifier, '+', '-', '(' or 'not'"
		))
        
        return res.success(exp)
        
    def arith(self):
        return self.bIN(self.term, (TT_PLUS,TT_MINUS))
    
    def power(self):
        return self.bIN(self.call, (TT_POW, ), self.factor)
    
    def factor(self):
        res=ParseResult()
        token=self.curr_token
        
        if token.type_ in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOP(token, factor))
        
        
        else:
            return self.power()
    
    def term(self):
        return self.bIN(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        res=ParseResult()
        
        if self.curr_token.match(TT_KEYWORD,'var'):
            res.register_advancement()
            self.advance()
            
            if self.curr_token.type_ != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
					self.curr_token.start, self.curr_token.end,
					"Expected identifier"
				))
            
            var_name=self.curr_token
            res.register_advancement()
            self.advance()
            
            if self.curr_token.type_ != TT_EQ:
                return res.failure(InvalidSyntaxError(
					self.curr_token.start, self.curr_token.end,
					"Expected '='"
				))
            
            res.register_advancement()
            self.advance()
            expr=res.register(self.expr())
            if res.error: return res.error
            return res.success(VarAsNode(var_name,expr))
        
        
        node= res.register(self.bIN(self.comp, ((TT_KEYWORD, "and"), (TT_KEYWORD,"or"))))
        
        if res.error:
            return res.failure(InvalidSyntaxError(
				self.curr_token.start, self.curr_token.end,
				"Expected 'VAR', int, float, identifier, '+', '-' or '('"
			))
        
        return res.success(node)
    
    def bIN(self,func1,op,func2=None):
        if func2==None:
            func2=func1
        
        res=ParseResult()
        left=res.register(func1())
        if res.error: return res
        
        while self.curr_token.type_ in op or (self.curr_token.type_,self.curr_token.val) in op:
            o=self.curr_token
            res.register_advancement()
            self.advance()
            right=res.register(func2())
            if res.error: return res
            left=BinaryOP(left, o, right)
        
        return res.success(left)
    
    def func_def(self):
        res=ParseResult()
        if not self.curr_token.match(TT_KEYWORD,'function'):
            return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected 'function'"))
        
        
        res.register_advancement()
        self.advance()
        
        if self.curr_token.type_ == TT_IDENTIFIER:
            var_name=self.curr_token
            res.register_advancement()
            self.advance()
            if self.curr_token.type_ != TT_LPAREN:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '('"))
            
        else:
            var_name=None
            if self.curr_token.type_ != TT_LPAREN:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '('"))
            
        res.register_advancement()
        self.advance()
        args=[]
        
        if self.curr_token.type_ == TT_IDENTIFIER:
            args.append(self.curr_token)
            res.register_advancement()
            self.advance()
            
            while self.curr_token.type_ == TT_COM:
                res.register_advancement()
                self.advance()
                
                if self.curr_token.type_ != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected 'identifier'"))
                
                args.append(self.curr_token)
                res.register_advancement()
                self.advance()
                
            if self.curr_token.type_ != TT_RPAREN:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected ',' or ')'"))
            
        else:
            if self.curr_token.type_ != TT_RPAREN:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected ')'"))
            
        res.register_advancement()
        self.advance()
            
        if not self.curr_token.type_==TT_LCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '{'"))
            
        res.register_advancement()
        self.advance()
        node_ret=res.register(self.expr())
        if res.error: return res
        
        if not self.curr_token.type_==TT_RCURL:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '}'"))
            
        res.register_advancement()
        self.advance()
        
        return res.success(FunctionNode(var_name, args, node_ret))
        
        
    def li(self):
        res=ParseResult()
        elements=[]
        start=self.curr_token.start.cp()
        
        if self.curr_token.type_ != TT_LSQ:
            res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected '['"))
            
        res.register_advancement()
        self.advance()
        
        if self.curr_token.type_ == TT_RSQ:
            res.register_advancement()
            self.advance()
            
        else:
            elements.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected ']', 'var', 'if', 'for', 'while', 'function', int, float, identifier, '+', '-', '(', '[' or 'not'"))
            
            while self.curr_token.type_ == TT_COM:
                res.register_advancement()
                self.advance()
                
                elements.append(res.register(self.expr()))
                if res.error: return res
                
            if res.error:
                return res.failure(InvalidSyntaxError(self.curr_token.start, self.curr_token.end,"Expected ',' or ']'"))
                
            res.register_advancement()
            self.advance()

        return res.success(ListNode(elements, start, self.curr_token.end.cp()))


