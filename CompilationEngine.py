from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable

class CompilationEngine():

    #Constructor
    def __init__(self, input_file):
        self.st=SymbolTable()
        self._vm_string = ''
        self.tknz = JackTokenizer(input_file)
        self.tknz.advance()


    def eat(self, vetor):
        if (self.tknz.getToken() in vetor):
            self._vm_string += '<' + self.tknz.tokenType() + '> ' + self.tknz.getToken() + ' </' + self.tknz.tokenType() + '>\n'
            self.tknz.advance()
        else:
            raise Exception ("Esperado '"+str(vetor)+"' encontrado '"+self.tknz.getToken()+"'")

    def eatType(self, vetor):
        if (self.tknz.tokenType() in vetor):
            self._vm_string += '<' + self.tknz.tokenType() + '> ' + self.tknz.getToken() + ' </' + self.tknz.tokenType() + '>\n'
            self.tknz.advance()
        else:
            raise Exception ("Esperado '"+str(vetor)+"' encontrado '"+self.tknz.tokenType()+"'")

    def compileClass(self):
        # 'class' className '{' classVarDec* subroutineDec* '}'
        #self._vm_string += '<class>\n'
        self.eat('class')
        self.compileClassName()
        self.eat('{')
        self.compileClassVarDec()
        for keys,values in self.st.classTable.items():
            print(keys)
            print(values)
        self.compileSubroutineDec()
        self.eat('}')
        self._vm_string += '</class>\n'
        return self._vm_string

    def compileClassVarDec(self):
        #( 'static' | 'field' ) type varName ( ',' varName)* ';'
        if (self.tknz.getToken() in ['static', 'field']):
            #self._vm_string += '<classVarDec>\n'
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

            #self._vm_string += '</classVarDec>\n'
            self.compileClassVarDec()

    def compileSubroutineDec(self):
        #( 'constructor' | 'function' | 'method' ) ( 'void' | type) subroutineName '(' parameterList ')' subroutineBody
        if (self.tknz.getToken() in ['constructor', 'function', 'method']):
            self._vm_string += '<subroutineDec>\n'
            self.eat(['constructor', 'function', 'method'])
            if self.tknz.getToken() == 'void':
                self.eat('void')
            else:
                self.compileType()
            self.compileSubroutineName()
            self.eat('(')
            self.compileParameterList()
            self.eat(')')
            self.compileSubroutineBody()
            self._vm_string += '</subroutineDec>\n'
            self.compileSubroutineDec()

    def compileParameterList(self):
        #((type varName) ( ',' type varName)*)?
        self._vm_string += '<parameterList>\n'
        while self.tknz.getToken() != ')':
            self.compileType()
            self.compileVarName()
            if (self.tknz.getToken()==','):
                self.eat(',')
        self._vm_string += '</parameterList>\n'

    def compileSubroutineBody(self):
        #'{' varDec* statements '}'
        self._vm_string += '<subroutineBody>\n'
        self.eat('{')
        while self.tknz.getToken()=='var':
            self.compileVarDec()
        self.compileStatements()
        self.eat('}')
        self._vm_string += '</subroutineBody>\n'

    def compileVarDec(self):
        #'var' type varName ( ',' varName)* ';'
        self._vm_string += '<varDec>\n'
        self.eat('var')
        self.compileType()
        self.compileVarName()
        while self.tknz.getToken() == ',':
            self.eat(',')
            self.compileVarName()
        self.eat(';')
        self._vm_string += '</varDec>\n'

    def compileStatements(self):
        # statement*
        self._vm_string += '<statements>\n'
        while self.tknz.getToken()!='}':
            self.compileStatement()
        self._vm_string += '</statements>\n'

    def compileStatement(self):
        #letStatement | ifStatement | whileStatement | doStatement | returnStatement
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
        #'let' varName ( '[' expression ']' )? '=' expression ';'
        self._vm_string += '<letStatement>\n'
        self.eat('let')
        self.compileVarName()
        if (self.tknz.getToken()=='['):
            self.eat('[')
            self.compileExpression()
            self.eat(']')
        self.eat('=')
        self.compileExpression()
        self.eat(';')
        self._vm_string += '</letStatement>\n'

    def compileIf(self):
        #'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
        self._vm_string += '<ifStatement>\n'
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
        self._vm_string += '</ifStatement>\n'

    def compileWhile(self):
        #'while' '(' expression ')' '{' statements '}'
        self._vm_string += '<whileStatement>\n'
        self.eat('while')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')
        self.compileStatements()
        self.eat('}')
        self._vm_string += '</whileStatement>\n'

    def compileDo(self):
        #'do' subroutineCall ';'
        self._vm_string += '<doStatement>\n'
        self.eat('do')
        self.compileSubroutineCall()
        self.eat(';')
        self._vm_string += '</doStatement>\n'

    def compileReturn(self):
        #'return' expression? ';'
        self._vm_string += '<returnStatement>\n'
        self.eat('return')
        if (self.tknz.getToken()!=';'):
            self.compileExpression()
        self.eat(';')
        self._vm_string += '</returnStatement>\n'

    def compileExpression(self):
        #term (op term)*
        self._vm_string += '<expression>\n'
        self.compileTerm()
        while self.tknz.getToken() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.compileOp()
            self.compileTerm()
        self._vm_string += '</expression>\n'

    def compileTerm(self):
        # integerConstant | stringConstant | keywordConstant |
        # varName ('[' expression ']')? |
        # subroutineCall |
        # '(' expression ')' |
        # unaryOp term
        #print('<term>')
        self._vm_string += '<term>\n'
        if (self.tknz.tokenType() in ['intConst', 'stringConst', 'keyword']):
            self._vm_string += '<' + self.tknz.tokenType() + '> ' + self.tknz.getToken() + ' </' + self.tknz.tokenType() + '>\n'
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
        self._vm_string += '</term>\n'

    def compileExpressionList(self):
        #(expression ( ',' expression)* )?
        self._vm_string += '<expressionList>\n'
        while self.tknz.getToken()!=')':
            self.compileExpression()
            if (self.tknz.getToken()==','):
                self.eat(',')
        #print('</expressionList>')
        self._vm_string += '</expressionList>\n'

    #outros
    def compileType(self):
        #'int' | 'char' | 'boolean' | className
        vetor = ['int','char','boolean', 'String', 'Array', 'Square', 'SquareGame']
        if (self.tknz.getToken() in vetor ):
            self._vm_string += '<' + self.tknz.tokenType() + '> ' + self.tknz.getToken() + ' </' + self.tknz.tokenType() + '>\n'
            self.tknz.advance()
        else:
            raise Exception ("Esperado 'int' | 'char' | 'boolean' | className encontrado '"+self.tknz.getToken()+"'")

    def compileClassName(self):
        #identifier
        self.eatType('identifier')
        self.ClassName=self.tknz.getToken()


    def compileSubroutineName(self):
        #identifier
        self.eatType('identifier')

    def compileVarName(self):
        #identifier
        self.eatType('identifier')

    def compileSubroutineCall(self):
        #subroutineName '(' expressionList ')' | (className|varName) '.' subroutineName '(' expressionList ')'
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
        # '+' | '-' | '* | '/' | '&' | '|' | '<' | '>' | '='
        vetor = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        if (self.tknz.getToken() in vetor ):
            self._vm_string += '<' + self.tknz.tokenType() + '> ' + self.tknz.getToken() + ' </' + self.tknz.tokenType() + '>\n'
            self.tknz.advance()
        else:
            raise Exception ("Esperado '+' | '-' | '* | '/' | '&' | '|' | '<' | '>' | '=' encontrado '"+self.tknz.getToken()+"'")

    def compileUnaryOp(self):
        # '-' | '~'
        vetor = ['-', '~']
        if (self.tknz.getToken() in vetor ):
            self._vm_string += '<' + self.tknz.tokenType() + '> ' + self.tknz.getToken() + ' </' + self.tknz.tokenType() + '>\n'
            self.tknz.advance()
        else:
            raise Exception ("Esperado '-' | '~' encontrado '"+self.tknz.getToken()+"'")


    def compileKeywordConstant(self):
        # 'true' | 'false' | 'null' | 'this'
        vetor = ['true', 'false', 'null', 'this']
        if (self.tknz.getToken() in vetor ):
            self._vm_string += '<' + self.tknz.tokenType() + '> ' + self.tknz.getToken() + ' </' + self.tknz.tokenType() + '>\n'
            self.tknz.advance()
        else:
            raise Exception ("Esperado 'true' | 'false' | 'null' | 'this' encontrado '"+self.tknz.getToken()+"'")
