import pandas as pd
import re
import os
from fuzzywuzzy import fuzz
import time

def baixaPlanilha():
	sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZsntDnttAWGHA8NZRvdvK5A_FgOAQ_tPMzP7UUf-CHwF_3PHMj_TImyXN2Q_Tmcqm2MqVknpHPoT2/pubhtml?gid=0&single=true"
	url_1 = sheet_url.replace("/pubhtml?gid=", "/pub?output=csv&gid=")

	#sheet_url = "https://docs.google.com/spreadsheets/d/10sObNyyL7veHGFbOyizxM8oVsppQoWV-0ALrDr8FxQ0/edit#gid=204503454"
	#url_2 = sheet_url.replace("/pubhtml?gid=", "/pub?output=csv&gid=")

	conferencias = pd.read_csv(url_1)
	#periodicos = pd.read_csv(url_2)

	#periodicos.to_csv('backup_periodicos.csv')

#	return conferencias, periodicos
	return conferencias


def padraoProducoes(stringBusca, gramatica):
    #result = re.search(gramatica, stringBusca, flags=re.I|re.S)
    result = re.search(gramatica, stringBusca, flags=re.I)
    if result:
        retorno = stringBusca[result.start(): result.end()]
    else:
        retorno = '-'
    return retorno

def fuzzRatioScore(evento, categoria, conferencias, periodicos):
	score = 0
	evento_score = ''
	if (categoria == 'conferencia'):
		for conferencia in conferencias['conferencia']:
			score_aux = fuzz.ratio(evento, conferencia)
			if score_aux > score:
				score = score_aux
				evento_score = conferencia

	elif (categoria == 'periodico'):
		for periodico in periodicos['periodico']:
			#score_aux = fuzz.token_sort_ratio(y, conferencia)
			score_aux = fuzz.ratio(evento, periodico)
			if score_aux > score:
				score = score_aux
				evento_score = periodico

	return str(evento_score)+';'+str(score)

def fuzzPartialScore(evento, categoria, conferencias, periodicos):
	score = 0
	evento_score = ''
	if (categoria == 'conferencia'):
		for conferencia in conferencias['conferencia']:
			#score_aux = fuzz.token_sort_ratio(y, conferencia)
			score_aux = fuzz.partial_ratio(evento, conferencia)
			if score_aux > score:
				score = score_aux
				evento_score = conferencia

	elif (categoria == 'periodico'):
		for periodico in periodicos['periodico']:
			#score_aux = fuzz.token_sort_ratio(y, conferencia)
			score_aux = fuzz.partial_ratio(evento, periodico)
			if score_aux > score:
				score = score_aux
				evento_score = periodico

	return str(evento_score)+';'+str(score)

def fuzzSortScore(evento, categoria, conferencias, periodicos):
	score = 0
	evento_score = ''
	if (categoria == 'conferencia'):
		for conferencia in conferencias['conferencia']:
			#score_aux = fuzz.token_sort_ratio(y, conferencia)
			score_aux = fuzz.token_sort_ratio(evento, conferencia)
			if score_aux > score:
				score = score_aux
				evento_score = conferencia

	elif (categoria == 'periodico'):
		for periodico in periodicos['periodico']:
			#score_aux = fuzz.token_sort_ratio(y, conferencia)
			score_aux = fuzz.token_sort_ratio(evento, periodico)
			if score_aux > score:
				score = score_aux
				evento_score = periodico

	return str(evento_score)+';'+str(score)

def fuzzSetScore(evento, categoria, conferencias, periodicos):
	score = 0
	evento_score = ''
	if (categoria == 'conferencia'):
		for conferencia in conferencias['conferencia']:
			#score_aux = fuzz.token_sort_ratio(y, conferencia)
			score_aux = fuzz.token_set_ratio(evento, conferencia)
			if score_aux > score:
				score = score_aux
				evento_score = conferencia

	elif (categoria == 'periodico'):
		for periodico in periodicos['periodico']:
			#score_aux = fuzz.token_sort_ratio(y, conferencia)
			score_aux = fuzz.token_set_ratio(evento, periodico)
			if score_aux > score:
				score = score_aux
				evento_score = periodico

	return str(evento_score)+';'+str(score)

def aplicaBarraB(k):
	return '\\b'+k+'\\b'

def trataConferencias(conferencias):
	# Passando tudo para minúsculo
	conferencias['conferencia'] = conferencias['conferencia'].str.lower()

	# Tirar acentos
	conferencias['conferencia'] = conferencias['conferencia'].str.normalize('NFKD')\
       														.str.encode('ascii', errors='ignore')\
       														.str.decode('utf-8')

	# Formar ER de conferencias a serem avaliadas
	conferencias['sigla'] = conferencias['sigla'].str.lower()

	conferencias['sigla'] = conferencias['sigla'].apply(lambda k: aplicaBarraB(k))

	listaRegexConferencia = '|'.join(conferencias['sigla'])

	
	listaRegexConferencia = "r'"+listaRegexConferencia+"'"
	
	return conferencias['conferencia'], conferencias['sigla'], listaRegexConferencia

def trataPeriodico(periodicos):
	# Tratamento de periodicos agora
	periodicos['periodico'] = periodicos['periodico'].str.lower()
	periodicos['periodico'] = periodicos['periodico'].str.normalize('NFKD')\
       														.str.encode('ascii', errors='ignore')\
       														.str.decode('utf-8')


	listaRegexPeriodicos = '|'.join(periodicos['periodico'])

	listaRegexPeriodicos = listaRegexPeriodicos.replace('(', '\(')
	listaRegexPeriodicos = listaRegexPeriodicos.replace(')', '\)')
	listaRegexPeriodicos = listaRegexPeriodicos.replace('.', '\.')

	listaRegexPeriodicos = "r'"+listaRegexPeriodicos+"'"

	return periodicos['periodico'], listaRegexPeriodicos

def formataEventos(df_eventos):
	eventos = pd.DataFrame(columns=['evento', 'categoria'])
	eventos['evento'] = df_eventos['evento'].str.lower()
	eventos['categoria'] = df_eventos['categoria']

	# Tratamento de DF (passar para minusculo e retirar acentos)
	eventos['evento'] = eventos['evento'].str.normalize('NFKD')\
											.str.encode('ascii', errors='ignore')\
											.str.decode('utf-8')

	return eventos

def aplicaQualis(categoria, score, evento_match, conferencias, periodicos):	# retorna qualis referente na planilha oficial
	if (categoria == 'conferencia'):
		if (int(score) >= 80):
			return conferencias.loc[conferencias['conferencia'] == evento_match, 'Qualis_Final'].iloc[0]

	elif (categoria == 'periodico'):
		if (int(score) >= 80):
			return periodicos.loc[periodicos['periodico'] == evento_match, 'Qualis_Final'].iloc[0]
		
def defineProducoes(conferencias, periodicos, df_eventos):		# Retorna um dataframe producoesPesquisador['conferencias', 'periodicos']
	# Formatação de trabalhos e artigos
	#trabalhos, artigos = formataTrabalhosArtigos(df_trabalho, df_artigo)
	eventos = formataEventos(df_eventos)

	# Tratamento de nome de eventos e formatação de gramatica
	conferencias['conferencia'], conferencias['sigla'], listaRegexConferencia = trataConferencias(conferencias)
	periodicos['periodico'], listaRegexPeriodicos = 							trataPeriodico(periodicos)	


	
	########### Até aqui: formatação do meu dataframe + formatacao gramatica periodicos e conferencias



	# Resolver questão do REGEX (siglas parciais sendo encontradas): como fazer regex com match whole word
	df_eventos['match_sigla'] = eventos['evento'].apply(lambda x:padraoProducoes(x, listaRegexConferencia))

	print('-- Entrou no calculo score decorridos {:.2f} minutos --'.format((time.time() - start_time)/60.0))

	
	# Aplica algoritmo de achar string match e mostra o score
	print('- Ratio: {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	eventos['aux_score_ratio'] = eventos.apply(lambda y:fuzzRatioScore(y['evento'], y['categoria'] , conferencias, periodicos), axis=1)	# linha maluca
	print('- Partial: {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	eventos['aux_score_partial'] = eventos.apply(lambda y:fuzzPartialScore(y['evento'], y['categoria'] , conferencias, periodicos), axis=1)	# linha maluca
	print('- Sort: {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	eventos['aux_score_sort'] = eventos.apply(lambda y:fuzzSortScore(y['evento'], y['categoria'] , conferencias, periodicos), axis=1)	# linha maluca
	print('- Set: {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	eventos['aux_score_set'] = eventos.apply(lambda y:fuzzSetScore(y['evento'], y['categoria'] , conferencias, periodicos), axis=1)	# linha maluca

	print('-- Entrou no tratamento nome evento decorridos {:.2f} minutos --'.format((time.time() - start_time)/60.0))

	#df_trabalho['conferencia_score'], df_trabalho['fuzz_token_sort_ratio'] = trabalhos['aux_score'].apply(lambda z: z.split(';'))
	df_eventos['evento_match_ratio'] = eventos['aux_score_ratio'].apply(lambda a: a.split(';')[0])
	df_eventos['evento_match_partial'] = eventos['aux_score_partial'].apply(lambda a: a.split(';')[0])
	df_eventos['evento_match_sort'] = eventos['aux_score_sort'].apply(lambda a: a.split(';')[0])
	df_eventos['evento_match_set'] = eventos['aux_score_set'].apply(lambda a: a.split(';')[0])
	#df_eventos['fuzz_token_sort_ratio'] = eventos['aux_score'].apply(lambda b: b.split(';')[1])

	print()
	print('-- Entrou no tratamento score decorridos {:.2f} minutos --'.format((time.time() - start_time)/60.0))

	df_eventos['fuzz_ratio'] = eventos['aux_score_ratio'].apply(lambda b: b.split(';')[1])
	df_eventos['fuzz_partial_ratio'] = eventos['aux_score_partial'].apply(lambda b: b.split(';')[1])
	df_eventos['fuzz_sort_ratio'] = eventos['aux_score_sort'].apply(lambda b: b.split(';')[1])
	df_eventos['fuzz_set_ratio'] = eventos['aux_score_set'].apply(lambda b: b.split(';')[1])

	print()
	print('-- Entrou no qualis decorridos {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	
	# Agora é necessário aplicar qualis encontrada
	#df_eventos['qualis'] = df_eventos.apply(lambda z: aplicaQualis(z.categoria, z.fuzz_partial_ratio, z.evento_match, conferencias, periodicos), axis=1)
	df_eventos['qualis_ratio'] = df_eventos.apply(lambda z: aplicaQualis(z.categoria, z.fuzz_ratio, z.evento_match_ratio, conferencias, periodicos), axis=1)
	print('- Ratio: {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	df_eventos['qualis_partial'] = df_eventos.apply(lambda z: aplicaQualis(z.categoria, z.fuzz_partial_ratio, z.evento_match_partial, conferencias, periodicos), axis=1)
	print('- Partial: {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	df_eventos['qualis_sort'] = df_eventos.apply(lambda z: aplicaQualis(z.categoria, z.fuzz_sort_ratio, z.evento_match_sort, conferencias, periodicos), axis=1)
	print('- Sort: {:.2f} minutos --'.format((time.time() - start_time)/60.0))
	df_eventos['qualis_set'] = df_eventos.apply(lambda z: aplicaQualis(z.categoria, z.fuzz_set_ratio, z.evento_match_set, conferencias, periodicos), axis=1)
	print('- Set: {:.2f} minutos --'.format((time.time() - start_time)/60.0))



	df_eventos.to_csv('eventosTratados.csv')



# init
start_time = time.time()

BASE_DIR = os.getcwd()
os.chdir('./eventos')

#conferencias, periodicos = baixaPlanilha()			# Baixar planilhas de qualis
conferencias = baixaPlanilha()			# Baixar planilhas de qualis
periodicos = pd.DataFrame({'periodico':['empty']})

df_eventos = pd.read_csv('eventos.csv')

#defineProducoes(conferencias, periodicos, df_trabalho, df_artigo)
defineProducoes(conferencias, periodicos, df_eventos)

segundos = (time.time() - start_time)
print('Execução levou : {:.2f} minutos ({:.2f} segundos)'.format((segundos/60.0), segundos))


