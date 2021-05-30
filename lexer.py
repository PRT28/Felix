import sys

sys.path.append(".")

from position import Position
from error import IllegalCharError
from constants import *

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
    
    def match(self,t,v):
        return self.type_==t and self.val==v 
        
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
            elif self.curr_char in LETTERS:
                tokens.append(self.make_id())
            elif self.curr_char == '"':
                tokens.append(self.make_string())
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
            elif self.curr_char == '^':
                tokens.append(Token(TT_POW,start=self.pos))
                self.advance()
            elif self.curr_char == '(':
                tokens.append(Token(TT_LPAREN,start=self.pos))
                self.advance()
            elif self.curr_char == ')':
                tokens.append(Token(TT_RPAREN,start=self.pos))
                self.advance()
            elif self.curr_char == '[':
                tokens.append(Token(TT_LSQ,start=self.pos))
                self.advance()
            elif self.curr_char == ']':
                tokens.append(Token(TT_RSQ,start=self.pos))
                self.advance()
            elif self.curr_char == '{':
                tokens.append(Token(TT_LCURL,start=self.pos))
                self.advance()
            elif self.curr_char == '}':
                tokens.append(Token(TT_RCURL,start=self.pos))
                self.advance()
            elif self.curr_char == ':':
                tokens.append(Token(TT_COL,start=self.pos))
                self.advance()
            elif self.curr_char == ';':
                tokens.append(Token(TT_SEMCOL,start=self.pos))
                self.advance()
            elif self.curr_char == ',':
                tokens.append(Token(TT_COM,start=self.pos))
                self.advance()
            elif self.curr_char == '!':
                token, err=self.make_not()
                if err: return [],err
                tokens.append(token)
            elif self.curr_char == '=':
                tokens.append(self.make_eq())
            elif self.curr_char == '<':
                tokens.append(self.less())
            elif self.curr_char == '>':
                tokens.append(self.great())
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
        
    def make_string(self):
        string=''
        start=self.pos.cp()
        esc_char=False
        self.advance()
        esc={'n':'\n','t':'\t'}
        
        while self.curr_char != None and (self.curr_char != '"' or esc_char):
            if esc_char:
                string += esc.get(self.curr_char, self.curr_char)
            else:
                if self.curr_char == '\\':
                    esc_char = True
                else:
                    string += self.curr_char
                
            self.advance()
            esc_char = False
            
        self.advance()
        return Token(TT_STRING, string,start,self.pos)
        
    def make_id(self):
        id_str=''
        start=self.pos.cp()
        
        while self.curr_char != None and self.curr_char in L_D + '_':
            id_str+=self.curr_char
            self.advance()
            
        token= TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(token,id_str,start,self.pos)
    def make_not(self):
        start=self.pos.cp()
        self.advance()
        
        if self.curr_char == "=":
            self.advance()
            return Token(TT_NE,start=start,end=self.pos),None
        
        return None,ExpectedCharErr(start,self.pos,"'=' after '!'")
    
    def make_eq(self):
        token=TT_EQ
        start=self.pos.cp()
        self.advance()
        
        if self.curr_char == "=":
            self.advance()
            token=TT_EE
            
        return Token(token,start=start,end=self.pos)
    
    def less(self):
        token=TT_LT
        start=self.pos.cp()
        self.advance()
        
        if self.curr_char == "=":
            self.advance()
            token=TT_LTE
            
        return Token(token,start=start,end=self.pos)
    
    def great(self):
        token=TT_GT
        start=self.pos.cp()
        self.advance()
        
        if self.curr_char == "=":
            self.advance()
            token=TT_GTE
            
        return Token(token,start=start,end=self.pos)
    
        
        