from arrows import arrows

#ERROR

class Error:
    def __init__(self,start,end,err,cont):
        self.start=start
        self.end=end
        self.err=err
        self.cont=cont
    
    def error(self):
        result= f'{self.err}:{self.cont}\n'
        result += f'File {self.start.fname}, line {self.start.ln + 1}'
        result += '\n\n' + arrows(self.start.fcont, self.start, self.end)
        return result
    
class IllegalCharError(Error):
    def __init__(self,start,end,cont):
        super().__init__(start,end,"IllegarChar",cont)
        
class InvalidSyntaxError(Error):
		def __init__(self, start, end, cont=''):
				super().__init__(start, end, 'Invalid Syntax', cont)



