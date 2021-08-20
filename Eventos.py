import pandas as pd
from IPython.display import display
import re

""" 
Métodos:
	- baixaPlanilha(): Retorna 'conferencias' e 'periodicos' contendo os respectivos dataframes 
	- padraoProducoes(): Retorna 'stringBusca' ou 'NA' contendo o nome da conferencia ou periódico ou NA 

"""

def baixaPlanilha():
	sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZsntDnttAWGHA8NZRvdvK5A_FgOAQ_tPMzP7UUf-CHwF_3PHMj_TImyXN2Q_Tmcqm2MqVknpHPoT2/pubhtml?gid=0&single=true"
	url_1 = sheet_url.replace("/pubhtml?gid=", "/pub?output=csv&gid=")

	sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTeZuJpry8wjDWn5KBMmWpl0JAEh20SQXZ8SUzswKpwEUHuFB4-4vKIsY238K4uNJga3bRChPIKYTka/pubhtml?gid=0&single=true"
	url_2 = sheet_url.replace("/pubhtml?gid=", "/pub?output=csv&gid=")

	conferencias = pd.read_csv(url_1)
	periodicos = pd.read_csv(url_2)

	#display(conferencias)
	#display(periodicos)

	return conferencias, periodicos

def padraoProducoes(stringBusca:str, gramatica:str):

    result = re.search(gramatica, stringBusca)
    if result:
        retorno = stringBusca[result.start(): result.end()]
    else:
        retorno = 'NA'
    return retorno


def defineProducoes(conferencias, periodicos, strings):		# Retorna um dataframe producoesPesquisador['conferencias', 'periodicos']
	

	#######

	listaRegexConferencia = '|'.join(conferencias['conferencia'])
	listaRegexConferencia = listaRegexConferencia.replace('(', '\(')
	listaRegexConferencia = listaRegexConferencia.replace(')', '\)')
	
	listaRegexPeriodicos = '|'.join(periodicos['periodico'])
	listaRegexPeriodicos = listaRegexPeriodicos.replace('(', '\(')
	listaRegexPeriodicos = listaRegexPeriodicos.replace(')', '\)')
	#listaRegex.append('|\n')
	print(listaRegexPeriodicos)
	print(listaRegexConferencia)

	producoesPesquisador = pd.DataFrame(columns=['conferencias', 'periodicos'])
	# na linha de baixo, o strings['conferencia'] é correspondente à uma coluna de dicionario com todos os valores que eu quero pesquisar

	producoesPesquisador['conferencias'] = strings['producoes'].apply(lambda x: padraoProducoes(stringBusca=x, gramatica=listaRegexConferencia),case=False)
	producoesPesquisador['periodicos'] = strings['producoes'].apply(lambda x: padraoProducoes(stringBusca=x, gramatica=listaRegexPeriodicos),case=False)

	
	display(producoesPesquisador)

	#display(conferencias)

	producoesPesquisador.to_csv('resultadoIntermediario.csv')



# init

conferencias, periodicos = baixaPlanilha()

"""# Entrada teste
teste = open('entradaTeste.txt', 'r')
strings = teste.readlines()
strings = pd.DataFrame(strings,columns=['conferencia'])
teste.close()
"""

strings = pd.read_csv('producoes.csv')
#display(strings)

defineProducoes(conferencias, periodicos, strings)


