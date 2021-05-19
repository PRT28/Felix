import sys

sys.path.append(".")

from error import InvalidSyntaxError

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

#NODES

class NumberNode:
    def __init__(self,token):
        self.token=token
        
    def __repr__(self):
        return f'{self.token}'
    
class BinaryOP:
    def __init__(self,left,op,right):
        self.right=right
        self.left=left
        self.op=op
        
    def __repr__(self):
        return f'({self.left},{self.op},{self.right})'
    
class UnaryOP:
	def __init__(self, token, node):
		self.token = token
		self.node = node

	def __repr__(self):
		return f'({self.token}, {self.node})'
    

#PARSE RESULT CHECKER

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None

	def register(self, res):
		if isinstance(res, ParseResult):
			if res.error: self.error = res.error
			return res.node

		return res

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
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
    
    def factor(self):
        res=ParseResult()
        token=self.curr_token
        
        if token.type_ in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOP(token, factor))
        
        elif token.type_ in (TT_INT,TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))
        
        elif token.type_ == TT_LPAREN:
            res.register(self.advance())
            expr= res.register(self.expr())
            if res.error: return res
            if self.curr_token.type_ == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
					self.curr_token.start, self.curr_tokentok.end,
					"Expected ')'"
				))
        else:
            return res.failure(InvalidSyntaxError(token.start,token.end,"Expected int or float" ))
    
    def term(self):
        return self.bIN(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
    	return self.bIN(self.term, (TT_PLUS, TT_MINUS))
    
    def bIN(self,func,op):
        res=ParseResult()
        left=res.register(func())
        if res.error: return res
        
        while self.curr_token.type_ in op:
            o=self.curr_token
            res.register(self.advance())
            right=res.register(func())
            if res.error: return res
            left=BinaryOP(left, o, right)
        
        return res.success(left)