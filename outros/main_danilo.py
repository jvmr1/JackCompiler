from JackTokenizer import JackTokenizer

tknz = JackTokenizer('Main.jack')
tknz.advance()
with open('Main.xml', 'w') as xml_file:
  xml_file.write("<tokens>\n")
  print("<tokens>")
  while tknz.hasMoreTokens():
    tokenClass = tknz.tokenType()
    line = '<' + tokenClass + '>' + tknz.getToken() + '<' + tokenClass + '>\n'
    xml_file.write(line)
    print(line)
    tknz.advance()
  xml_file.write('</tokens>')
  print('</tokens>')
