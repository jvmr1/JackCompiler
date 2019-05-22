from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable

class CompilationEngine():
    def __init__(self, input_file):
        self.st=SymbolTable()
        self._vm_string = ''
        self.tknz = JackTokenizer(input_file)
        self.tknz.advance()

    def eat(self, vetor):
        if (self.tknz.getToken() in vetor):
            self.tknz.advance()
        # else:
        #     raise Exception ("Esperado '"+str(vetor)+"' encontrado '"+self.tknz.getToken()+"'")

    def eatType(self, vetor):
        if (self.tknz.tokenType() in vetor):
            self.tknz.advance()
        # else:
        #     raise Exception ("Esperado '"+str(vetor)+"' encontrado '"+self.tknz.tokenType()+"'")

    def compileClass(self):
        self.eat('class')
        self.compileClassName()
        self.eat('{')
        self.compileClassVarDec()
        # for keys,values in self.st.classTable.items():
        #     print(keys)
        #     print(values)
        self.compileSubroutineDec()
        self.eat('}')
        return self._vm_string

    def compileClassVarDec(self):
        if (self.tknz.getToken() in ['static', 'field']):
            self.kind=self.tknz.getToken()
            self.eat(['static', 'field'])
            self.type=self.tknz.getToken()
            self.compileType()
            self.name=self.tknz.getToken()
            self.compileVarName()
            self.st.define(self.name, self.type, self.kind) #com kind, type e name da variavel definidos, inserir entrada na symboltable
            while self.tknz.getToken() == ',':
                self.eat(',')
                self.name=self.tknz.getToken()
                self.compileVarName()
                self.st.define(self.name, self.type, self.kind)
            self.eat(';')
            self.compileClassVarDec()

    def compileSubroutineDec(self):
        if (self.tknz.getToken() in ['constructor', 'function', 'method']):
            self.st.startSubroutine()
            # self.type = self.className
            # self.kind = 'arg'
            # self.name = 'this'
            # self.st.define(self.name, self.type, self.kind)
            self.subroutineKind=self.tknz.getToken()
            self.eat(['constructor', 'function', 'method'])
            self.subroutineType=self.tknz.getToken()
            if self.tknz.getToken() == 'void':
                self.eat('void')
            else:
                self.compileType()
            self.subroutineName=self.tknz.getToken()
            self.compileSubroutineName()
            self.eat('(')
            self.compileParameterList()
            self.eat(')')
            self.compileSubroutineBody()
            self.compileSubroutineDec()

    def compileParameterList(self):
        while self.tknz.getToken() != ')':
            # self.type = self.className
            # self.kind = 'arg'
            # self.name = 'this'
            # self.st.define(self.name, self.type, self.kind)
            self.compileType()
            self.compileVarName()
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
        self.compileType()
        self.compileVarName()
        while self.tknz.getToken() == ',':
            self.eat(',')
            self.compileVarName()
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
        self.eat('while')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')
        self.compileStatements()
        self.eat('}')

    def compileDo(self):
        self.eat('do')
        self.compileSubroutineCall()
        self.eat(';')

    def compileReturn(self):
        self.eat('return')
        if (self.tknz.getToken()!=';'):
            self.compileExpression()
        self.eat(';')

    def compileExpression(self):
        self.compileTerm()
        while self.tknz.getToken() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.compileOp()
            self.compileTerm()

    def compileTerm(self):
        if (self.tknz.tokenType() in ['intConst', 'stringConst', 'keyword']):
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

    def compileExpressionList(self):
        while self.tknz.getToken()!=')':
            self.compileExpression()
            if (self.tknz.getToken()==','):
                self.eat(',')

    def compileType(self):
        vetor = ['int','char','boolean', 'String', 'Array', 'Square', 'SquareGame']
        if (self.tknz.getToken() in vetor ):
            self.tknz.advance()
        else:
            raise Exception ("Esperado 'int' | 'char' | 'boolean' | className encontrado '"+self.tknz.getToken()+"'")

    def compileClassName(self):
        self.eatType('identifier')
        self.ClassName=self.tknz.getToken()


    def compileSubroutineName(self):
        self.eatType('identifier')

    def compileVarName(self):
        self.eatType('identifier')

    def compileSubroutineCall(self):
        self.compileClassName()
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
        vetor = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        if (self.tknz.getToken() in vetor ):
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
