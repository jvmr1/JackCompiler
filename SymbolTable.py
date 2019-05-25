class SymbolTable():
    def __init__(self):
        #criar um dict?
        self.classTable={}
        self.subroutineTable={}
        self.kindIndex = {'static':0, 'field':0, 'arg':0, 'var':0}

    def startSubroutine(self):
        self.subroutineTable.clear()
        self.kindIndex['arg'] = 0
        self.kindIndex['var'] = 0

    def define(self, name, tokenType, kind):
        if kind in ('static', 'field'):
            self.classTable[name] = (tokenType, kind, self.kindIndex[kind])
            print(name, self.classTable[name])

        elif kind in ('arg', 'var'):
            self.subroutineTable[name] = (tokenType, kind, self.kindIndex[kind])
            print(name, self.subroutineTable[name])

        self.kindIndex[kind]=self.kindIndex[kind]+1

    def varCount(self, kind):
        return self.kindIndex[kind]

    def kindOf(self, name):
        if name in self.subroutineTable:
            return self.subroutineTable[name][1]

        elif name in self.classTable:
            if self.classTable[name][1] == 'field':
                return 'this'
            else:
                return self.classTable[name][1]
        else:
            return 'NONE'

    def typeOf(self, name):
        if name in self.classTable:
            return self.classTable[name][0]

        elif name in self.subroutineTable:
            return self.subroutineTable[name][0]

    def indexOf(self, name):
        if name in self.classTable:
            return self.classTable[name][2]

        elif name in self.subroutineTable:
            return self.subroutineTable[name][2]

    def findTable(self, name):
        if name in self.classTable:
            return 'class'

        elif name in self.subroutineTable:
            return 'subroutine'
