#POSTITON

class Position:
    def __init__(self,index,ln,cn,fname,fcont):
        self.index=index
        self.ln=ln
        self.cn=cn
        self.fname=fname
        self.fcont=fcont
        
    def advance(self,curr_char=None):
        self.index += 1
        self.cn += 1
        
        if curr_char == '\n':
            self.ln += 1
            self.cn =0
        
        return self
    
    def cp(self):
        return Position(self.index,self.ln,self.cn,self.fname,self.fcont)
