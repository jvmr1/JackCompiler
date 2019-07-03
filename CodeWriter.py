class CodeWriter():
    def __init__(self, filename):
        self.asm=open(filename, 'w')
        self.asm.write("@256\n")
        self.asm.write("D=A\n")
        self.asm.write("@SP\n")
        self.asm.write("M=D\n")
        #self.asm.write(command)
        self.labelcounter = 0

    def writePushPop(self, command, arg1, arg2):
        if command=="C_PUSH":
            if arg1 == "constant":
                self.asm.write("@"+str(arg2)+" // push "+str(arg1)+" "+str(arg2)+"\n")
                self.asm.write("D=A\n")
                self.asm.write("@SP\n")
                self.asm.write("A=M\n")
                self.asm.write("M=D\n")
                self.asm.write("@SP\n")
                self.asm.write("M=M+1\n")
            elif arg1 in  ["local", "argument", "this", "that"]:
                segment = self.mapRegisters(arg1, arg2)
                self.asm.write("@"+segment+" // push "+arg1+" "+str(arg2)+"\n")
                self.asm.write("D=M\n")
                self.asm.write("@"+str(arg2)+"\n")
                self.asm.write("A=D+A\n")
                self.asm.write("D=M\n")
                self.asm.write("@SP\n")
                self.asm.write("A=M\n")
                self.asm.write("M=D\n")
                self.asm.write("@SP\n")
                self.asm.write("M=M+1\n")
            elif arg1 in ["static" ,"temp", "pointer"]:
                segment = self.mapRegisters(arg1, arg2)
                self.asm.write("@"+segment+" // push "+arg1+" "+str(arg2)+"\n")
                self.asm.write("D=M\n")
                self.asm.write("@SP\n")
                self.asm.write("A=M\n")
                self.asm.write("M=D\n")
                self.asm.write("@SP\n")
                self.asm.write("M=M+1\n")

        elif command == "C_POP":
            if arg1 in ["static" ,"temp", "pointer"]:
                segment = self.mapRegisters(arg1, arg2)
                self.asm.write("@SP // pop "+arg1+" "+str(arg2)+"\n")
                self.asm.write("M=M-1\n")
                self.asm.write("A=M\n")
                self.asm.write("D=M\n")
                self.asm.write("@"+segment+"\n")
                self.asm.write("M=D\n")
            else:
                segment = self.mapRegisters(arg1, arg2)
                self.asm.write("@"+segment+" // pop "+arg1+" "+str(arg2)+"\n")
                self.asm.write("D=M\n")
                self.asm.write("@"+str(arg2)+"\n")
                self.asm.write("D=D+A\n")
                self.asm.write("@R13\n")
                self.asm.write("M=D\n")
                self.asm.write("@SP\n")
                self.asm.write("M=M-1\n")
                self.asm.write("A=M\n")
                self.asm.write("D=M\n")
                self.asm.write("@R13\n")
                self.asm.write("A=M\n")
                self.asm.write("M=D\n")

    def writeArithmetic(self, command):
        if command == "add":
            self.writeAdd()
        elif command == "sub":
            self.writeSub()
        elif command == "eq":
            self.writeEq()
        elif command == "lt":
            self.writeLt()
        elif command == "gt":
            self.writeGt()
        elif command == "neg":
            self.writeNeg()
        elif command == "and":
            self.writeAnd()
        elif command == "or":
            self.writeOr()
        elif command == "not":
            self.writeNot()

    def writeAdd(self):
        self.asm.write("@SP // add\n")
        self.asm.write("M=M-1\n")
        self.asm.write("A=M\n")
        self.asm.write("D=M\n")
        self.asm.write("A=A-1\n")
        self.asm.write("M=D+M\n")

    def writeSub(self):
        self.asm.write("@SP // sub\n")
        self.asm.write("M=M-1\n")
        self.asm.write("A=M\n")
        self.asm.write("D=M\n")
        self.asm.write("A=A-1\n")
        self.asm.write("M=M-D\n")

    def writeEq(self):
        label = "JEQ_"+str(self.labelcounter)
        self.asm.write("@SP // eq\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M\n")
        self.asm.write("@SP\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M-D\n")
        self.asm.write("@" + label+"\n")
        self.asm.write("D;JEQ\n")
        self.asm.write("D=1\n")
        self.asm.write("("+label+")\n")
        self.asm.write("D=D-1\n")
        self.asm.write("@SP\n")
        self.asm.write("A=M\n")
        self.asm.write("M=D\n")
        self.asm.write("@SP\n")
        self.asm.write("M=M+1\n")
        self.labelcounter += 1

    def writeLt(self):
        labeltrue = "JLT_TRUE_"+str(self.labelcounter)
        labelfalse = "JLT_FALSE_"+str(self.labelcounter)
        self.asm.write("@SP // lt\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M\n")
        self.asm.write("@SP\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M-D\n")
        self.asm.write("@"+labeltrue+"\n")
        self.asm.write("D;JLT\n")
        self.asm.write("D=0\n")
        self.asm.write("@"+labelfalse+"\n")
        self.asm.write("0;JMP\n")
        self.asm.write("("+labeltrue+")\n")
        self.asm.write("D=-1\n")
        self.asm.write("("+labelfalse+")\n")
        self.asm.write("@SP\n")
        self.asm.write("A=M\n")
        self.asm.write("M=D\n")
        self.asm.write("@SP\n")
        self.asm.write("M=M+1\n")
        self.labelcounter += 1

    def writeGt(self):
        labeltrue = "JGT_TRUE_"+str(self.labelcounter)
        labelfalse = "JGT_FALSE_"+str(self.labelcounter)
        self.asm.write("@SP // gt\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M\n")
        self.asm.write("@SP\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M-D\n")
        self.asm.write("@"+labeltrue+"\n")
        self.asm.write("D;JGT\n")
        self.asm.write("D=0\n")
        self.asm.write("@"+labelfalse+"\n")
        self.asm.write("0;JMP\n")
        self.asm.write("("+labeltrue+")\n")
        self.asm.write("D=-1\n")
        self.asm.write("("+labelfalse+")\n")
        self.asm.write("@SP\n")
        self.asm.write("A=M\n")
        self.asm.write("M=D\n")
        self.asm.write("@SP\n")
        self.asm.write("M=M+1\n")
        self.labelcounter += 1

    def writeNeg(self):
        self.asm.write("@SP // neg\n")
        self.asm.write("A=M\n")
        self.asm.write("A=A-1\n")
        self.asm.write("M=-M\n")

    def writeAnd(self):
        self.asm.write("@SP // and\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M\n")
        self.asm.write("A=A-1\n")
        self.asm.write("M=D&M\n")

    def writeOr(self):
        self.asm.write("@SP // or\n")
        self.asm.write("AM=M-1\n")
        self.asm.write("D=M\n")
        self.asm.write("A=A-1\n")
        self.asm.write("M=D|M\n")

    def writeNot(self):
        self.asm.write("@SP // not\n")
        self.asm.write("A=M\n")
        self.asm.write("A=A-1\n")
        self.asm.write("M=!M\n")

    def mapRegisters(self, segment, i):
        if segment == "local":   
            return "LCL"
        if segment == "argument":
            return "ARG"
        if segment == "this":
            return "THIS"
        if segment == "that":
            return "THAT"
        if segment == "pointer":
            return "R" + str(3 + i)
        if segment == "temp":
            return "R" + str(5 + i)

    def close(self):
        self.asm.close()
