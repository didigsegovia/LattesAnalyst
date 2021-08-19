import pandas as pd
from IPython.display import display
import re

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

def padraoProducoes(search_str:str, search_list:str):

    result = re.search(search_list, search_str)
    if result:
        retorno = search_str[result.start(): result.end()]
    else:
        retorno = 'NA'
    return retorno


def defineProducoes(conferencias, periodicos):		# Retorna um dataframe producoesPesquisador['conferencias', 'periodicos']
	# Entrada teste
	teste = open('entradaTeste.txt', 'r')

	strings = teste.readlines()
	#'|'.join(strings)
	strings = pd.DataFrame(strings,columns=['conferencia'])

	listaRegex = '|'.join(conferencias['conferencia'])

	producoesPesquisador = pd.DataFrame(columns=['conferencias', 'periodicos'])
	# na linha debaixo, o conferencias['conferencia'] é correspondente à uma coluna de dicionario com todos os valores que eu quero pesquisar



	#conferencias['achou'] = strings['conferencia'].apply(lambda x: padraoConferencia(search_str=x, search_list=listaRegex))
	producoesPesquisador['conferencias'] = strings['conferencia'].apply(lambda x: padraoConferencia(search_str=x, search_list=listaRegex))

	
	display(producoesPesquisador)

	#display(conferencias)

	conferencias.to_csv('resultadoIntermediario.csv')
	teste.close()



# init

conferencias, periodicos = baixaPlanilha()

testaSubstring(conferencias, periodicos)


