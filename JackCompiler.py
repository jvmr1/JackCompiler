import re
import sys
import os
from CompilationEngine import CompilationEngine

#implementar caso pra rodar em varios arquivos de uma pasta

if __name__ == '__main__':
    args = []
    curr_path = os.getcwd()
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isdir(curr_path + '/' + arg):
            files = os.listdir(curr_path + '/' + arg)
            jack_files = [curr_file for curr_file in files if curr_file.find('.jack') != -1]
            for curr_file in jack_files:
                compEng = CompilationEngine(curr_file)
                vm_string = compEng.compileClass()
                name = re.split('\.', curr_file)[0]
                with open(name + '.vm', 'w') as vm:
                    vm.write(vm_string)
        elif os.path.isfile(curr_path + '/' + arg) and arg.find('.jack') != -1:
            compEng = CompilationEngine(arg)
            vm_string = compEng.compileClass()
            name = re.split('\.', arg)[0]
            with open(name + '.vm', 'w') as vm:
                vm.write(vm_string)
        else:
            print("It is not a directory or a file")