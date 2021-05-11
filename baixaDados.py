from baixaLattes import baixaCVLattes

import timeit
import os
import sys
import pandas
from StringIO import StringIO

import datetime as dt

QUANTIDADE_DE_ARQUIVOS = 10



## Este eh um dummy code para exemplificar o uso do codigo baixaLattes

# Entradas: um ID Lattes do tipo "str"
# Saidas: um HTML completo em relatorio em referencia ao ID Lattes aplicado

# Forneco ID Lattes para o baixaCVLattes(id_Lattes)

def executa(documento):
	tempoInicial = timeit.default_timer()
	#arquivo = open(documento, 'r')
	try:
		#arquivo = pandas.read_csv(documento, usecols=['numero', 'ids', 'sigla', 'data', 'area', 'carga'], header=0)

		arquivo = pandas.read_csv(documento, sep=';', dtype=str)
	except:
		#arquivo.close()
		sys.exit("O arquivo nao pode ser carregado corretamente")



	linhasIds = arquivo[arquivo.columns[1]].values
	contador = 0

	

	for linha in linhasIds:
		if contador == QUANTIDADE_DE_ARQUIVOS:
			#arquivo.close()
			print('saiu por quantidade de execucoes')
			break
		print(linha)
		print("progresso: "+str(100*(float(contador)/float(QUANTIDADE_DE_ARQUIVOS)))+"%")
		cvLattesHTML = baixaCVLattes(linha)
		#file = open(('./CVS/'+linha), 'w')
		#file.write(cvLattesHTML)
		#file.close()
		contador +=1

		# Ao tentar baixar o CV e nao conseguir, arquivo contera 3 espacos. "   "

	tempoFinal = timeit.default_timer()

	#dataAtual = str(dt.date.today())
	horaAtual = str(dt.datetime.now())

	arquivoTempo = open('relatorioTempo.txr','a')
	

	arquivoTempo.write("Execucao em "+horaAtual+" horas levou "+str(tempoFinal-tempoInicial)+" de tempo ("+str(contador)+" CVs baixados)\n")

	arquivoTempo.close()
	#arquivo.close()




def executaTxt(documento):
	try:
		arquivo = open(documento, 'r')
	except:
		sys.exit("O arquivo nao pode ser carregado corretamente")

	contador = 0

	for linha in arquivo:
		if contador == 100:
			arquivo.close()
			sys.exit('saiu por quantidade de execucoes')
		print(linha)
		linha = linha.split()
		cvLattesHTML = baixaCVLattes(linha)
		path = './CVS/'+linha
		file = open(path, 'w')
		file.write(cvLattesHTML)
		file.close()
		contador +=1

	arquivo.close()





if __name__ == "__main__":
	# em sys.args temos os argumentos por linha de comando

	executa(sys.argv[1])

	print("Terminou a execucao")