from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine():
    def __init__(self, input_file):
        self.st=SymbolTable()
        self.vmW = VMWriter()
        self.tknz = JackTokenizer(input_file)
        self._vm_string = ''
        self.tknz.advance()
        self.Op=[]

    def eat(self, vetor):
        if (self.tknz.getToken() in vetor):
            self.tknz.advance()
        else:
            raise Exception ("Esperado '"+str(vetor)+"' encontrado '"+self.tknz.getToken()+"'")

    def eatType(self, vetor):
        if (self.tknz.tokenType() in vetor):
            self.tknz.advance()
        else:
            raise Exception ("Esperado '"+str(vetor)+"' encontrado '"+self.tknz.tokenType()+"'")

    def compileClass(self):
        self.eat('class')
        self.compileClassName()
        self.eat('{')
        self.compileClassVarDec()
        self.compileSubroutineDec()
        self.eat('}')
        return self._vm_string

    def compileClassVarDec(self):
        if (self.tknz.getToken() in ['static', 'field']):
            kind=self.tknz.getToken()
            self.eat(['static', 'field'])
            tokenType=self.tknz.getToken()
            self.compileType()
            name=self.tknz.getToken()
            self.compileVarName()
            self.st.define(name, tokenType, kind) #com kind, type e name da variavel definidos, inserir entrada na symboltable
            while self.tknz.getToken() == ',':
                self.eat(',')
                name=self.tknz.getToken()
                self.compileVarName()
                self.st.define(name, tokenType, kind)
            self.eat(';')
            self.compileClassVarDec()

    def compileSubroutineDec(self):
        if (self.tknz.getToken() in ['constructor', 'function', 'method']):
            self.st.startSubroutine()
            if self.tknz.getToken() == 'method':
                tokenType = self.className
                kind = 'arg'
                name = 'this'
                self.st.define(name, tokenType, kind)
            subroutineKind=self.tknz.getToken()
            self.eat(['constructor', 'function', 'method'])
            subroutineType=self.tknz.getToken()
            if self.tknz.getToken() == 'void':
                self.eat('void')
            else:
                self.compileType()
            self.compileSubroutineName()
            self.eat('(')
            self.compileParameterList()
            self.eat(')')
            self._vm_string += self.vmW.writeFunction(self.functionName, self.st.varCount('arg'))
            self.compileSubroutineBody()
            self.compileSubroutineDec()

    def compileParameterList(self):
        while self.tknz.getToken() != ')':
            tokenType = self.tknz.getToken()
            self.compileType()
            name = self.tknz.getToken()
            self.compileVarName()
            kind = 'arg'
            self.st.define(name, tokenType, kind)
            if (self.tknz.getToken()==','):
                self.eat(',')

    def compileSubroutineBody(self):
        self.eat('{')
        while self.tknz.getToken()=='var':
            self.compileVarDec()
        self.compileStatements()
        self.eat('}')

    def compileVarDec(self):
        self.eat('var')
        tokenType = self.tknz.getToken()
        self.compileType()
        name = self.tknz.getToken()
        self.compileVarName()
        kind = 'var'
        self.st.define(name, tokenType, kind)
        while self.tknz.getToken() == ',':
            self.eat(',')
            name = self.tknz.getToken()
            self.compileVarName()
            self.st.define(name, tokenType, kind)
        self.eat(';')

    def compileStatements(self):
        while self.tknz.getToken()!='}':
            self.compileStatement()

    def compileStatement(self):
        if (self.tknz.getToken()=='let'):
            self.compileLet()
        elif (self.tknz.getToken()=='if'):
            self.compileIf()
        elif (self.tknz.getToken()=='while'):
            self.compileWhile()
        elif (self.tknz.getToken()=='do'):
            self.compileDo()
        elif (self.tknz.getToken()=='return'):
            self.compileReturn()
        else:
            raise Exception ("Esperado 'let | if | while | do | return' encontrado '"+self.tknz.getToken()+"'")

    def compileLet(self):
        #writePop
        self.eat('let')
        self.compileVarName()
        if (self.tknz.getToken()=='['):
            self.eat('[')
            self.compileExpression()
            self.eat(']')
        self.eat('=')
        self.compileExpression()
        self.eat(';')

    def compileIf(self):
        #writeIf
        #writeGoto
        #writeLabel
        self.eat('if')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')
        self.compileStatements()
        self.eat('}')
        if (self.tknz.getToken()=='else'):
            self.eat('else')
            self.eat('{')
            self.compileStatements()
            self.eat('}')

    def compileWhile(self):
        #writeIf
        #writeGoto
        #writeLabel
        self.eat('while')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')
        self.compileStatements()
        self.eat('}')

    def compileDo(self):
        self.eat('do')
        self.compileClassName()
        self.compileSubroutineCall()
        self.eat(';')

    def compileReturn(self):
        self.eat('return')
        if (self.tknz.getToken()!=';'):
            self.compileExpression() #caso seja tipo return 0; é preciso printar esse 0 no vm?
        self.eat(';')
        self._vm_string += self.vmW.writeReturn()

    def compileExpression(self):
        self.compileTerm()
        while self.tknz.getToken() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.compileOp()
            self.compileTerm()
            if (self.Op[-1] in ['+', '-']):
                op=self.Op.pop(-1)
                self._vm_string += self.vmW.writeArithmetic(op)
            elif (self.Op[-1] in ['*', '/']):
                op=self.Op.pop(-1)
                self._vm_string += self.vmW.writeCall(self.vmW.writeArithmetic(op), 2)

    def compileTerm(self):
        #writePush
        if (self.tknz.tokenType() in ['intConst', 'stringConst', 'keyword']):
            if (self.tknz.tokenType() == 'intConst'): #desnecessario, talvez
                self._vm_string += self.vmW.writePush('constant', self.tknz.getToken())
            self.tknz.advance()
        elif (self.tknz.getToken()=='('):
            self.eat('(')
            self.compileExpression()
            self.eat(')')
        elif (self.tknz.getToken()=='-' or self.tknz.getToken()=='~'):
            self.compileUnaryOp()
            self.compileTerm()
        else:
            self.compileVarName()
            if (self.tknz.getToken()=='['):
                self.eat('[')
                self.compileExpression()
                self.eat(']')
            elif (self.tknz.getToken()=='.'):
                self.compileSubroutineCall()

    def compileExpressionList(self):
        while self.tknz.getToken()!=')':
            self.compileExpression()
            if (self.tknz.getToken()==','):
                self.eat(',')

    def compileType(self):
        vetor = ['int','char','boolean', 'String']
        if (self.tknz.getToken() in vetor or self.tknz.tokenType() == 'identifier'):
            self.tknz.advance()
        else:
            raise Exception ("Esperado 'int' | 'char' | 'boolean' | className encontrado '"+self.tknz.getToken()+"'")

    def compileClassName(self):
        self.className=self.tknz.getToken()
        self.eatType('identifier')

    def compileSubroutineName(self):
        self.subroutineName=self.tknz.getToken()
        self.functionName = self.className + '.' + self.subroutineName
        self.eatType('identifier')

    def compileVarName(self):
        self.eatType('identifier')

    def compileSubroutineCall(self):
        #writeCall
        if (self.tknz.getToken()=='.'):
            self.eat('.')
            self.compileSubroutineName()
            self.eat('(')
            self.compileExpressionList()
            self.eat(')')
        else:
            self.eat('(')
            self.compileExpressionList()
            self.eat(')')

    def compileOp(self):
        #writeCall
        #writeArithmetic
        #self._vm_string += self.vmW.writeFunction(self.functionName, self.st.varCount('arg'))
        vetor = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        if (self.tknz.getToken() in vetor ):
            # if (self.tknz.getToken() in ['+', '-']):
            #     self._vm_string += self.vmW.writeArithmetic(self.tknz.getToken())
            # elif (self.tknz.getToken() in ['*', '/']):
            #     self._vm_string += self.vmW.writeCall(self.vmW.writeArithmetic(self.tknz.getToken()), 2)
            self.Op.append(self.tknz.getToken())
            self.tknz.advance()
        else:
            raise Exception ("Esperado '+' | '-' | '* | '/' | '&' | '|' | '<' | '>' | '=' encontrado '"+self.tknz.getToken()+"'")

    def compileUnaryOp(self):
        vetor = ['-', '~']
        if (self.tknz.getToken() in vetor ):
            self.tknz.advance()
        else:
            raise Exception ("Esperado '-' | '~' encontrado '"+self.tknz.getToken()+"'")

    def compileKeywordConstant(self):
        vetor = ['true', 'false', 'null', 'this']
        if (self.tknz.getToken() in vetor ):
            self.tknz.advance()
        else:
            raise Exception ("Esperado 'true' | 'false' | 'null' | 'this' encontrado '"+self.tknz.getToken()+"'")
