import re

symbols = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']

keywords=['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']

class JackTokenizer (object):
	
	data=[]
	pos=0
	string_warning=0
	xml_tag_warning=0

	def __init__(self, path):
		file = open(path)
		data1 = file.read()
		file.close()

		data2=data1.split('\n')

		data3 = []
		for i in range (len(data2)):

			data2[i]=data2[i].lstrip() #excluir identacao

			for j in range (len(data2[i])): #excluir comentarios
				if data2[i][j:j+2]=='//':
					data2[i]=data2[i][:j]
	
			if data2[i]!='': #excluir linhas vazias
				data3.append(data2[i])

		data4=[]
		for i in data3:
			i = re.split('(\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~|\ |\:|\?)',i) #separar por simbolos, mantendo eles
			data4=data4+i

		data4 = [x for x in data4 if x != '' and x != ' '] #excluir espacos vazios apos split
	
		self.data = data4

	def advance(self):
		self.pos=self.pos+1

	def hasMoreTokens(self):
		if self.pos < len(self.data):
			return True
		else:
			return False

	def getToken(self):
		aux=self.data[self.pos]
		if aux[0] == '"':
			aux=''
			while self.data[self.pos] != '"':
				aux=aux+self.data[self.pos]+' '
				self.advance()
			aux=aux[1:-1]
			self.string_warning=1
		elif aux == '<':
			self.xml_tag_warning=1
			return '&lt;'
		elif aux == '>':
			self.xml_tag_warning=1
			return '&gt;'
		elif aux == '&':
			self.xml_tag_warning=1
			return '&amp;'
		return aux

	def tokenType(self, token):
		if self.string_warning == 1:
			self.string_warning=0
			return 'stringConst'
		elif self.xml_tag_warning == 1:
			self.xml_tag_warning = 0
			return 'symbol'
		elif token in symbols:
			return 'symbol'
		elif token in keywords:
			return 'keyword'
		elif token[0] not in ['0','1','2','3','4','5','6','7','8','9']:
			return 'identifier'
		elif token.isdigit():
			return 'intConst'
		else:
			return 'error'
