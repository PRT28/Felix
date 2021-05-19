import sys

sys.path.append(".")

from position import Position
from error import IllegalCharError

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

class Token:
    def __init__(self,type_,val=None,start=None,end=None):
        self.type_=type_
        self.val=val
        
        if start:
            self.start=start.cp()
            self.end=start.cp()
            self.end.advance()
            
        if end:
            self.end=end.cp()
        
    def __repr__(self):
        if self.val:
            return f'{self.type_}:{self.val}'
        else:
            return f'{self.type_}'
        
#LEXER

class Lexer:
    def __init__(self,fname,text):
        self.fname=fname
        self.text=text
        self.pos= Position(-1, 0, -1,fname,text)
        self.curr_char=None
        self.advance()
        
    def advance(self):
        self.pos.advance(self.curr_char)
        self.curr_char=self.text[self.pos.index] if self.pos.index<len(self.text) else None
        
    def make_tokens(self):
        tokens=[]
        
        while self.curr_char != None:
            if self.curr_char in ' \t':
                self.advance()
            elif self.curr_char in DIGITS:
                tokens.append(self.make_num())
            elif self.curr_char == '+':
                tokens.append(Token(TT_PLUS,start=self.pos))
                self.advance()
            elif self.curr_char == '-':
                tokens.append(Token(TT_MINUS,start=self.pos))
                self.advance()
            elif self.curr_char == '*':
                tokens.append(Token(TT_MUL,start=self.pos))
                self.advance()
            elif self.curr_char == '/':
                tokens.append(Token(TT_DIV,start=self.pos))
                self.advance()
            elif self.curr_char == '(':
                tokens.append(Token(TT_LPAREN,start=self.pos))
                self.advance()
            elif self.curr_char == ')':
                tokens.append(Token(TT_RPAREN,start=self.pos))
                self.advance()
            else:
                start=self.pos.cp()
                char=self.curr_char
                self.advance()
                return [], IllegalCharError(start,self.pos,"'" + char + "'")
        
        tokens.append(Token(TT_EOF,start=self.pos))
        return tokens,None
    
    def make_num(self):
        num=''
        start=self.pos.cp()
        
        while self.curr_char != None and self.curr_char in DIGITS + '.':
            if self.curr_char == '.':
                if self.curr_char in num:
                    break
                else:
                    num += '.'
            else:
                num += self.curr_char
            self.advance()
        
        if '.' in num:
            return Token(TT_FLOAT, float(num),start,self.pos)
        else:
            return Token(TT_INT, int(num),start,self.pos)
