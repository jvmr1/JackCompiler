from JackTokenizer import JackTokenizer

tknz = JackTokenizer('Main.jack')
print ("<tokens>")
while tknz.hasMoreTokens():
	token = tknz.getToken()
	tipo = tknz.tokenType(token)
	print ("<" + tipo + ">"+token+"</" + tipo + ">") #fazer a alteraçao de <, >, &, e " aqui na main, não no tokenizer
													#eh preciso o simbolo no analisador sintatico
	tknz.advance()
print ("</tokens>")


