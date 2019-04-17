from CompilationEngine import CompilationEngine

compEng = CompilationEngine('Square.jack')
xml_string = compEng.compileClass()
print(xml_string)
with open('Square.xml', 'w') as xml:
    if type(xml_string) == str:
        xml.write(xml_string)
