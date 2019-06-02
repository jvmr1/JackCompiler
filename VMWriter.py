

class VMWriter():
    #constructor
    #def __init__(self):

    def writePush(self, segment, index):
        if segment == 'var':
            return 'push ' + 'local' + ' ' + str(index)+ '\n'
        elif segment == 'arg':
            return 'push ' + 'argument' + ' ' + str(index)+ '\n'
        else:
            return 'push ' + segment + ' ' + str(index)+ '\n'

    def writePop(self, segment, index):
        if segment == 'var':
            return 'pop ' + 'local' + ' ' + str(index)+ '\n'
        elif segment == 'arg':
            return 'pop ' + 'argument' + ' ' + str(index)+ '\n'
        else:
            return 'pop ' + segment + ' ' + str(index)+ '\n'

    def writeArithmetic(self, command):
        if (command=='+'):
            return 'add'+'\n'
        if (command=='-'):
            return 'sub'+'\n'
        if (command=='<'):
            return 'lt'+'\n'
        if (command=='>'):
            return 'gt'+'\n'
        if (command=='*'):
            return 'Math.multiply'
        if (command=='/'):
            return 'Math.divide'

    def writeLabel(self, label):
        return

    def writeGoto(self, label):
        return

    def writeIf(self, label):
        return

    def writeCall(self, name, nArgs):
        return 'call ' + name + ' ' + str(nArgs) + '\n'

    def writeFunction(self, name, nLocals):
        return 'function ' + name + ' ' + str(nLocals) + '\n'

    def writeReturn(self):
        return 'return'+'\n'

    def close(self):
        return
