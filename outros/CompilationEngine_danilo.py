from JackTokenizer import JackTokenizer


class CompilationEngine():
    def __init__(self, file_path):

        self._tokenizer = JackTokenizer(file_path)
        self._xml_string = ''

    def compileToken(self, *tokens):

        tokenizer = self._tokenizer
        if tokenizer.getToken() in tokens:
            self._xml_string += '<' + tokenizer.tokenType() + '>' + tokenizer.getToken() + \
                    '</' + tokenizer.tokenType() + '>\n'
        else:
            raise Exception('Esperado "' + str(list(tokens)) +
                            '" encontrado "' + tokenizer.getToken() + '"')

    def compileTokenType(self, *types):

        tokenizer = self._tokenizer
        if tokenizer.tokenType() in types:
            self._xml_string += '<' + tokenizer.tokenType() + '>' + tokenizer.getToken() + \
                '</' + tokenizer.tokenType() + '>\n'
        else:
            raise Exception('Erro sintático')

    def compileType(self):

        tokenizer = self._tokenizer
        if tokenizer.tokenType() == 'keyword':
            self.compileToken('int', 'char', 'boolean')
        else:
            self.compileTokenType('identifier')

    def compileClass(self):

        tokenizer = self._tokenizer
        tokenizer.advance()
        self._xml_string += '<class>\n'
        self.compileToken('class')
        tokenizer.advance()
        self.compileTokenType('identifier')
        tokenizer.advance()
        self.compileToken('{')
        self.compileClassVarDec()
        self.compileSubroutine()
        tokenizer.advance()
        self.compileToken('}')
        self._xml_string += '</class>'

        return self._xml_string

    def compileClassVarDec(self):

        tokenizer = self._tokenizer
        tokenizer.advance()
        if tokenizer.getToken() in ('field', 'static'):
            self._xml_string += '<classVarDec>\n'
            self.compileToken('field', 'static')
            tokenizer.advance()
            self.compileType()
            tokenizer.advance()
            self.compileTokenType('identifier')
            tokenizer.advance()
            while tokenizer.getToken() == ',':
                self.compileToken(',')
                tokenizer.advance()
                self.compileTokenType('identifier')
                tokenizer.advance()
            self.compileToken(';')
            self._xml_string += '</classVarDec>\n'
            self.compileClassVarDec()

    def compileSubroutine(self):

        tokenizer = self._tokenizer
        if tokenizer.getToken() in ('constructor', 'function', 'method'):
            self._xml_string += '<subroutineDec>\n'
            self.compileToken('constructor', 'function', 'method')
            tokenizer.advance()
            if tokenizer.getToken() == 'void':
                self.compileToken('void')
            else:
                self.compileType()
            tokenizer.advance()
            self.compileTokenType('identifier')
            tokenizer.advance()
            self.compileToken('(')
            tokenizer.advance()
            self.compileParameterList()
            self.compileToken(')')
            tokenizer.advance()
            self._xml_string += '<subroutineBody>\n'
            self.compileToken('{')
            tokenizer.advance()
            self.compileVarDec()
            self.compileStatements()
            self.compileToken('}')
            self._xml_string += '</subroutineBody>\n'
            self._xml_string += '</subroutineDec>\n'
            self.compileSubroutine()

    def compileParameterList(self):

        tokenizer = self._tokenizer
        self._xml_string += '<parameterList>\n'
        if tokenizer.getToken() != ')':
            self.compileType()
            tokenizer.advance()
            self.compileTokenType('identifier')
            tokenizer.advance()
            while tokenizer.getToken() == ',':
                self.compileToken(',')
                tokenizer.advance()
                self.compileType()
                tokenizer.advance()
                self.compileTokenType('identifier')
                tokenizer.advance()
        self._xml_string += '</parameterList>\n'

    def compileVarDec(self):

        tokenizer = self._tokenizer
        if tokenizer.getToken() == 'var':
            self._xml_string += '<varDec>\n'
            self.compileToken('var')
            tokenizer.advance()
            self.compileType()
            tokenizer.advance()
            self.compileTokenType('identifier')
            tokenizer.advance()
            while tokenizer.getToken() == ',':
                self.compileToken(',')
                tokenizer.advance()
                self.compileTokenType('identifier')
                tokenizer.advance()
            self.compileToken(';')
            tokenizer.advance()
            self._xml_string += '</varDec>\n'
            self.compileVarDec()

    def compileStatements(self):

        tokenizer = self._tokenizer
        if tokenizer.getToken() == 'let':
            self.compileLet()
            tokenizer.advance()
            self.compileStatements()

    def compileLet(self):

        tokenizer = self._tokenizer
        if tokenizer.getToken() == 'let':
            self._xml_string += '<letStatement>\n'
            self.compileToken('let')
            tokenizer.advance()
            self.compileTokenType('identifier')
            tokenizer.advance()
            self.compileExpression()
            tokenizer.advance
            self.compileToken('=')
            tokenizer.advance()
            self.compileExpression()
            self.compileToken(';')
            self._xml_string += '</letStatement>\n'

    def compileExpression(self):

        tokenizer = self._tokenizer
        if tokenizer.tokenType() == 'identifier':
            self._xml_string += '<expression>\n'
            self.compileTerm()
            tokenizer.advance()
            while tokenizer.getToken() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
                self.compileToken('+', '-', '*', '/', '&', '|', '<', '>', '=')
                tokenizer.advance()
                self.compileTerm()
                tokenizer.advance()
            self._xml_string += '</expression>\n'

    def compileTerm(self):

        tokenizer = self._tokenizer
        if tokenizer.tokenType() == 'identifier':
            self._xml_string += '<term>\n'
            self.compileTokenType('identifier')
            self._xml_string += '</term>\n'
