import re

class Parser (object):
    def __init__(self, path):
        self.commands=[]
        with open(path) as in_file:
            commands = in_file.read()
        pattern_comment = '\/(\*|)\*(.|\n)*?\*\/|\/\/.*'
        commands = re.sub(pattern_comment, '', commands)
        commands=commands.split('\n')
        for i in range(len(commands)):
            if len(commands[i])==0:
                pass
            else:
                self.commands.append(commands[i].split())

    def hasMoreCommands(self):
        if self.commands:
            return True
        return False

    def advance(self):
        if self.hasMoreCommands():
            self.currCommand = self.commands.pop(0)

    def commandType(self):
        if self.currCommand[0] in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        elif self.currCommand[0] == "push":
            return "C_PUSH"
        elif self.currCommand[0] == "pop":
            return "C_POP"
        elif self.currCommand[0] == "label":
            return "C_LABEL"
        elif self.currCommand[0] == "goto":
            return "C_GOTO"
        elif self.currCommand[0] == "if-goto":
            return "C_IF"
        elif self.currCommand[0] == "function":
            return "C_FUNCTION"
        elif self.currCommand[0] == "return":
            return "C_RETURN"
        elif self.currCommand[0] == "call":
            return "C_CALL"
        else:
            return None

    def arg1(self):
        if self.commandType() in ["C_ARITHMETIC"]:
            return str(self.currCommand[0])
        elif self.commandType() in ["C_RETURN"]:
            return None
        else:
            return str(self.currCommand[1])

    def arg2(self):
        if self.commandType() in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return int(self.currCommand[2])
        else:
            return None
