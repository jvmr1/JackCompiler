class CodeWriter():
    def __init__(self, filename):
        self.asm=open(filename, 'w')
        #self.asm.write(command)

    def writeArithmetic(self, command):
        return 0

    def writePushPop(self, command, arg1, arg2):
        return 0

    def close(self):
        self.asm.close()
