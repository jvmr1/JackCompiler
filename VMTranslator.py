import re
import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter

if __name__ == '__main__':
    parser=Parser('BasicTest.vm')
    codewriter=CodeWriter('BasicTest.asm')
    while parser.hasMoreCommands():
        ctype = parser.commandType()
        arg1 = parser.arg1()
        arg2 = parser.arg2()
        #print(ctype, arg1, arg2,'\n')
        if ctype == "C_ARITHMETIC":
<<<<<<< HEAD
            codewriter.writeArithmetic(parse.currCommand[0])
=======
            writer.writeArithmetic(parse.currCommand[0])
>>>>>>> 444c56bfe8f7c2f3ffc79cab50c20a8c23788f9d
        elif ctype == "C_PUSH" or ctype == 'C_POP':
            codewriter.writePushPop(ctype, arg1, arg2)
        parser.advance()
    codewriter.close()
