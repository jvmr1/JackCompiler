import re

class Parser (object):
    def __init__(self, path):
        with open(path) as in_file:
            commands = in_file.read()
        pattern_comment = '\/(\*|)\*(.|\n)*?\*\/|\/\/.*'
        commands = re.sub(pattern_comment, '', commands)
        self.commands=commands.split()
        self.asm_string=''

    def Printar(self):
        for command in self.commands:
            self.asm_string+=command+'\n'
        return self.asm_string
