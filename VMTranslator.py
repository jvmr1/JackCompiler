import re
import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter

if __name__ == '__main__':

    if len(sys.argv) > 1:
        vm_files = []
        asm_name = ""
        arg = sys.argv[1]
        if os.path.isdir(arg):
            files = os.listdir(arg)
            vm_files = [arg+curr_file for curr_file in files if curr_file.find('.vm') != -1]
            asm_name = arg + re.split('\/', arg)[-2] + '.asm'
            '''for curr_file in vm_files:
                compEng = CompilationEngine(arg+curr_file)
                vm_string = compEng.compileClass()
                name = re.split('\.', curr_file)[0]
                with open(arg + name + '.vm', 'w') as vm:
                    vm.write(vm_string)'''
        elif os.path.isfile(arg) and arg.find('.vm') != -1:
            vm_files.append(arg)
            asm_name = arg
            '''compEng = CompilationEngine(arg)
            vm_string = compEng.compileClass()
            name = re.split('\.', arg)[0]
            with open(name + '.vm', 'w') as vm:
                vm.write(vm_string)'''
        else:
            print("It is not a directory or a file")
        
        if vm_files:
            #print(vm_files)
            #print(asm_name)

            codewriter=CodeWriter(asm_name)

            if len(vm_files) > 1:
                codewriter.writeInit()

            for vm_file in vm_files:
                parser=Parser(vm_file)
                codewriter.setModuleName(vm_file)
                while parser.hasMoreCommands():
                    parser.advance()
                    ctype = parser.commandType()
                    arg1 = parser.arg1()
                    arg2 = parser.arg2()
                    #print(ctype, arg1, arg2,'\n')
                    if ctype == "C_ARITHMETIC":
                        codewriter.writeArithmetic(parser.currCommand[0])
                    elif ctype == "C_PUSH" or ctype == 'C_POP':
                        codewriter.writePushPop(ctype, arg1, arg2)
                    elif ctype == "C_LABEL":
                        codewriter.writeLabel(arg1)
                    elif ctype == "C_GOTO":
                        codewriter.writeGoto(arg1)
                    elif ctype == "C_IF":
                        codewriter.writeIf(arg1) 
                    elif ctype == "C_FUNCTION":
                        codewriter.writeFunction(arg1, arg2)
                    elif ctype == "C_CALL":
                        codewriter.writeCall(arg1, arg2)
                    elif ctype == "C_RETURN":
                        codewriter.writeReturn()

            codewriter.close()
