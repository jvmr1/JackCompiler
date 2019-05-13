import re
from CompilationEngine import CompilationEngine

compEng = CompilationEngine('Main.jack')
xml_string = compEng.compileClass()
print(xml_string)
with open('Main.xml', 'w') as xml:
    if type(xml_string) == str:
        xml.write(xml_string)
