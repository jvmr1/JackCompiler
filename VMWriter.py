

class VMWriter():
    #def __init__(self, input_file):
    #criar arquivo .vm pra escrever

    def writePush(self, segment, index):
        return

    def writePop(self):
        return

    def writeArithmetic(self):
        return

    def writeLabel(self):
        return

    def writeGoto(self):
        return

    def writeIf(self):
        return

    def writeCall(self):
        return

    def writeFunction(self, name, nLocals):
        return 'function ' + name + ' ' + str(nLocals) + '\n'

    def writeReturn(self):
        # pop temp 0
        # push constant 0
        # printar essas coisas no vm quando o return nao tiver nada
        return 'return'

    def close(self):
        return
