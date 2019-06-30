import re
import sys
import os
from Parser import Parser

if __name__ == '__main__':
    args = []
    curr_path = os.getcwd()
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isdir(curr_path + '/' + arg):
            files = os.listdir(curr_path + '/' + arg)
            vm_files = [curr_file for curr_file in files if curr_file.find('.vm') != -1]
            for curr_file in vm_files:
                parser = Parser(curr_file)
                asm_string=parser.Printar()
                name = re.split('\.', curr_file)[0]
                with open(name + '.asm', 'w') as asm:
                    asm.write(asm_string)
        elif os.path.isfile(curr_path + '/' + arg) and arg.find('.vm') != -1:
            parser = Parser(arg)
            asm_string=parser.Printar()
            name = re.split('\.', arg)[0]
            with open(name + '.asm', 'w') as asm:
                asm.write(asm_string)
        else:
            print("It is not a directory or a file")
