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
"""	- Para cada produção que não for encontrada (por não constar na planilha Qualis),
contabilizar como "não referenciada", caso contrário, "NA"
"""
    result = re.search(gramatica, stringBusca)
    if result:
        retorno = stringBusca[result.start(): result.end()]
    else:
        retorno = 'NA'
    return retorno

"""def buscaQualisConferencias(stringBusca:str, conferencias):
	if stringBusca is 'NA':
		return 'NA'
	else:
		retorno = 

def buscaQualisPeriodicos(stringBusca:str, periodicos):
	if stringBusca is 'NA':
		return 'NA'
	else:
"""

"""
TODO
- padraoProducoes: Para cada produção que não for encontrada (por não constar na planilha Qualis),
contabilizar como "não referenciada", caso contrário, "NA"

- defineProducoes: Passar para minusculas, tirar tabulações e acentos (da planilha Qualis e dos curriculos)
(padronizar dados para comparação)

"""


def defineProducoes(conferencias, periodicos, strings):		# Retorna um dataframe producoesPesquisador['conferencias', 'periodicos']
	strings = strings.replace(to_replace='\n', value=' ', regex=True)			# Retira quebra de linha de df de entrada (vindo do parserHTML)
	strings.to_csv('producoesSemQuebraLinha.csv')		# para verificar string de produções entrada sem a quebra de linha

	listaRegexConferencia = '|'.join(conferencias['conferencia'])
	##### TODO: Passar para minusculas, tirar tabulações e acentos (da planilha Qualis e dos curriculos)

	listaRegexConferencia = listaRegexConferencia.replace('(', '\(')
	listaRegexConferencia = listaRegexConferencia.replace(')', '\)')
	
	listaRegexPeriodicos = '|'.join(periodicos['periodico'])
	##### TODO: Passar para minusculas, tirar tabulações e acentos

	listaRegexPeriodicos = listaRegexPeriodicos.replace('(', '\(')
	listaRegexPeriodicos = listaRegexPeriodicos.replace(')', '\)')
	


	producoesPesquisador = pd.DataFrame(columns=['conferencias', 'qualis_conferencias', 'periodicos', 'qualis_periodicos'])

	producoesPesquisador['conferencias'] = strings['producoes'].apply(lambda x: padraoProducoes(stringBusca=x, gramatica=listaRegexConferencia))
	producoesPesquisador['periodicos'] = strings['producoes'].apply(lambda x: padraoProducoes(stringBusca=x, gramatica=listaRegexPeriodicos))

	# achar uma forma de colocar o qualis ao lado de cada produção encontrada

	display(strings)
	display(producoesPesquisador)

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


