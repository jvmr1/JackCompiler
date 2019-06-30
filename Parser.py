import re

class Parser (object):
    def __init__(self, path):
        with open(path) as in_file:
            commands = in_file.read()
        pattern_comment = '\/(\*|)\*(.|\n)*?\*\/|\/\/.*'
        commands = re.sub(pattern_comment, '', commands)
        self.commands=commands.split()
        self.asm_string=''
        self.currCommand = None

    def Printar(self):
        for command in self.commands:
            self.asm_string+=command+'\n'
        return self.asm_string

	def hasMoreCommands(self):
		if self.commands:
			return True
		return False

	def advance(self):
		if self.hasMoreCommands():
            if self.commandType() in ["C_ARITHMETIC", "C_RETURN"]:
			    self.currCommand = self.commands.pop(0)
            elif self.commandType() in ["C_LABEL", "C_GOTO", "C_IF"]:
                self.commands.pop(0)
                self.currCommand = self.commands.pop(0)
            elif self.commandType() in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
                self.commands.pop(0)
                self.commands.pop(0)
                self.currCommand = self.commands.pop(0)


    def commandType(self):
        if self.currCommand in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        elif self.currCommand == "push":
            return "C_PUSH"
        elif self.currCommand == "pop":
            return "C_POP"
        elif self.currCommand == "label":
            return "C_LABEL"
        elif self.currCommand == "goto":
            return "C_GOTO"
        elif self.currCommand == "if-goto":
            return "C_IF"
        elif self.currCommand == "function":
            return "C_FUNCTION"
        elif self.currCommand == "return":
            return "C_RETURN"
        elif self.currCommand == "call":
            return "C_CALL"
        else:
            return None

    def arg1(self):
		if self.hasMoreCommands():
            if self.commandType() in ["C_ARITHMETIC"]:
                return str(self.currCommand)
            elif self.commandType() in ["C_RETURN"]:
                return None
            else:
			    return str(self.commands[0])

    def arg2(self):
		if self.hasMoreCommands():
            if self.commandType() in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
			    return int(self.commands[1])
            else:
                return None
