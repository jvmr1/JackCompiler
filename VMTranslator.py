import re
import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter

if __name__ == '__main__':
    parser=Parser('BasicTest.vm')
    codewriter=CodeWriter('BasicTest.asm')
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

    codewriter.close()
