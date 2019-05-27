import re
from CompilationEngine import CompilationEngine

#implementar caso pra rodar em varios arquivos de uma pasta

compEng = CompilationEngine('Teste.jack')
vm_string = compEng.compileClass()
#print(vm_string) #opcional
with open('Teste.vm', 'w') as vm:
    vm.write(vm_string)
