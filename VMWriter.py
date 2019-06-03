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
        elif (command=='-'):
            return 'sub'+'\n'
        elif (command=='<'):
            return 'lt'+'\n'
        elif (command=='>'):
            return 'gt'+'\n'
        elif (command=='='):
            return 'eq'+'\n'
        elif (command=='&'):
            return 'and'+'\n'
        elif (command=='|'):
            return 'or'+'\n'
        elif (command=='*'):
            return 'Math.multiply'
        elif (command=='/'):
            return 'Math.divide'
        elif (command == 'unary~'):
            return 'not\n'
        elif (command == 'unary-'):
            return 'neg\n'

    def writeLabel(self, label):
        return 'label ' + label + '\n'

    def writeGoto(self, label):
        return 'goto ' + label + '\n'

    def writeIf(self, label):
        return 'if-goto ' + label + '\n'

    def writeCall(self, name, nArgs):
        return 'call ' + name + ' ' + str(nArgs) + '\n'

    def writeFunction(self, name, nLocals):
        return 'function ' + name + ' ' + str(nLocals) + '\n'

    def writeReturn(self):
        return 'return'+'\n'

    def close(self):
        return
