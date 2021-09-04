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

"""	- Para cada produção que não for encontrada (por não constar na planilha Qualis),
contabilizar como "não referenciada", caso contrário, "NA"
"""
def padraoProducoes(stringBusca:str, gramatica:str):
    result = re.search(gramatica, stringBusca)
    if result:
        retorno = stringBusca[result.start(): result.end()]
    else:
        retorno = 'NA'
    return retorno

"""

TODO: Done
- padraoProducoes: Para cada produção que não for encontrada (por não constar na planilha Qualis),
contabilizar como "não referenciada", caso contrário, "NA"

- defineProducoes: Passar para minusculas, tirar tabulações e acentos (da planilha Qualis e dos curriculos)
(padronizar dados para comparação)

"""


def defineProducoes(conferencias, periodicos, strings):		# Retorna um dataframe producoesPesquisador['conferencias', 'periodicos']
	strings = strings[['producoes']]
	strings['producoes'] = strings['producoes'].replace(to_replace='\n', value=' ', regex=True)			# Retira quebra de linha de df de entrada (vindo do parserHTML)
	# Tratamento de DF (passar para minusculo e retirar acentos)
	strings['producoes'] = strings['producoes'].str.lower()
	strings['producoes'] = strings['producoes'].str.normalize('NFKD')\
       														.str.encode('ascii', errors='ignore')\
       														.str.decode('utf-8')
	# Tirar tabs
	strings['producoes'].str.replace("\t","")

	strings.to_csv('producoesTratadas.csv')		# para verificar string de produções entrada sem a quebra de linha

	# Passando tudo para minúsculo
	conferencias['conferencia'] = conferencias['conferencia'].str.lower()

	# Tirar acentos
	conferencias['conferencia'] = conferencias['conferencia'].str.normalize('NFKD')\
       														.str.encode('ascii', errors='ignore')\
       														.str.decode('utf-8')

	# Formar ER de conferencias a serem avaliadas
	listaRegexConferencia = '|'.join(conferencias['conferencia'])

	##### Letras minusculas, sem tabulações e acentos (da planilha Qualis e dos curriculos)

	listaRegexConferencia = listaRegexConferencia.replace('(', '\(')
	listaRegexConferencia = listaRegexConferencia.replace(')', '\)')
	listaRegexConferencia = listaRegexConferencia.replace('.', '\.')
	
	# Tratamento de periodicos agora
	periodicos['periodico'] = periodicos['periodico'].str.lower()
	periodicos['periodico'] = periodicos['periodico'].str.normalize('NFKD')\
       														.str.encode('ascii', errors='ignore')\
       														.str.decode('utf-8')


	listaRegexPeriodicos = '|'.join(periodicos['periodico'])

	listaRegexPeriodicos = listaRegexPeriodicos.replace('(', '\(')
	listaRegexPeriodicos = listaRegexPeriodicos.replace(')', '\)')
	listaRegexPeriodicos = listaRegexPeriodicos.replace('.', '\.')
	


	producoesPesquisador = pd.DataFrame(columns=['conferencias', 'qualis_conferencias', 'periodicos', 'qualis_periodicos'])

	producoesPesquisador['conferencias'] = strings['producoes'].apply(lambda x: padraoProducoes(stringBusca=x, gramatica=listaRegexConferencia))
	producoesPesquisador['periodicos'] = strings['producoes'].apply(lambda x: padraoProducoes(stringBusca=x, gramatica=listaRegexPeriodicos))

	

	# achar uma forma de colocar o qualis ao lado de cada produção encontrada
	#display(listaRegexPeriodicos)
	#display(listaRegexConferencia)
	#periodicos.to_csv('periodicos.csv')
	#conferencias.to_csv('conferencias.csv')

	producoesPesquisador.to_csv('resultadoProvisorio.csv')



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


