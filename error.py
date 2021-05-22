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

class RTError(Error):
    def __init__(self, start, end, cont,context):
        super().__init__(start, end, 'Runtime Error', cont)
        self.context=context
        
    def error(self):
        result=self.gen_traceback()
        result += f'{self.err}:{self.cont}\n'
        result += '\n\n' + arrows(self.start.fcont, self.start, self.end)
        return result
        
    def gen_traceback(self):
        result=''
        pos=self.start
        ctx=self.context
        
        while ctx:
            result=f'   File {pos.fname}, Line {str(pos.ln+1)}, in {ctx.display_name}\n'
            pos=ctx.parent_entry_pos
            ctx=ctx.parent
            
        return 'Traceback (most recent call last):\n'+result

class ExpectedCharErr(Error):
	def __init__(self, start, end, cont):
		super().__init__(start, end, 'Expected Character', cont)