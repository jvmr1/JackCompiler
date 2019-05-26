

class VMWriter():
    #def __init__(self, input_file):
    #criar arquivo .vm pra escrever

    def writePush(self, segment, index):
        if segment == 'var':
            return 'push ' + 'local' + ' ' + str(index)+ '\n'
        elif segment == 'arg':
            return 'push ' + 'argument' + ' ' + str(index)+ '\n'
        else:
            return 'push ' + segment + ' ' + str(index)+ '\n'

    def writePop(self, segment, index):
        return

    def writeArithmetic(self, command):
        return

    def writeLabel(self, label):
        return

    def writeGoto(self, label):
        return

    def writeIf(self, label):
        return

    def writeCall(self, name, nArgs):
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
