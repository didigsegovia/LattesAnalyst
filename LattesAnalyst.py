import os
import lxml
import pandas as pd
import numpy as np
import genderbr as gender
import datetime as date
import Avaliador
import requests
import time
from lxml import etree as etree

"""
Tuto basico:
root.attrib: retorna um dicionario com os atributos da tag
root.tag: retorna string contendo o nome da tag em questao
item.findall('tag'): retorna todos os elementos filhos que tenham essa tag especifica (usar em for)
item.find('tag'): retorna o primeiro filho com aquela tag
item.get('attrib').text: retorna o conteudo daquele atributo

- myroot
#print(myroot)			# retorna objeto da tag
#print(myroot.tag)		# retorna string da tag
#print(myroot.attrib)	# returna atributos da tag
"""

# Declaração de macros (tipos de producoes)
TRABALHO_COMPLETO = ['COMPLETO', 'RESUMO', 'RESUMO_EXPANDIDO']
ARTIGOS = ['COMPLETO']
PROCESSA_PRODUCOES = True								# Para processar produções bibliográficas, definir como true

df_trabalho = pd.DataFrame({'evento': [],
								'ano':[],
								'qualis': []})
df_artigo = pd.DataFrame({'evento': [],
							'ano':[],
							'qualis': []})

df_pesquisador = {	'id_lattes':list(),
					'nome':list(),
				 	'sexo':list(),
				 	'idade_academica':list(),
					'quantidade_producoes':list(),
					'producoes_por_idade':list(),
				   	'nota_qualis':list(),
					'precisao_nota_qualis':list(),
					'softwares_participacao':list(),
					'orientacoes':list(),
					'orientacoes_por_idade':list(),
					'instituicao_trabalho':list(),
					'estado_instituicao_trabalho':list(),
					'graduacao':list(),
					'ano_graduacao':list(),
					'posdoc':list(),
					'ano_posdoc':list(),
					'mestrado':list(),
					'ano_mestrado':list(),
					'doutorado':list(),
					'ano_doutorado':list(),
					'ATIVIDADES_DE_DIRECAO_E_ADMINISTRACAO': list(),
					'ATIVIDADES_DE_PESQUISA_E_DESENVOLVIMENTO':list(),
					'ATIVIDADES_DE_ENSINO':list(),
					'ATIVIDADES_DE_EXTENSAO_UNIVERSITARIA':list(),
					'ATIVIDADES_DE_PARTICIPACAO_EM_PROJETO':list(),
					'grande_area_conhecimento':list(),
					'area_conhecimento':list(),
					'subarea_conhecimento':list()}


eventos_gabarito = pd.read_csv('eventos_gabarito.csv')


# Manipulando PATH
BASE_DIR = os.getcwd()
os.chdir('./cachexml')



def parse_PRODUCOES_BIBLIOGRAFICAS(item):
	
	dict_trabalho = {'evento':[], 'ano':[], 'qualis':[], 'tipo':[]}
	dict_artigo = {'evento':[], 'ano':[], 'qualis':[], 'tipo':[]}


	try:
		trabalhosEventos = item.find('TRABALHOS-EM-EVENTOS')
		for trabalho in trabalhosEventos.findall('TRABALHO-EM-EVENTOS'):
			nodeNaturezaTrabalho = trabalho.find('DADOS-BASICOS-DO-TRABALHO')
			naturezaTrabalho = nodeNaturezaTrabalho.get('NATUREZA')
			nodeTrabalho = trabalho.find('DETALHAMENTO-DO-TRABALHO')

			if (naturezaTrabalho in TRABALHO_COMPLETO):			# Trabalho completo
				dict_trabalho['evento'].append(nodeTrabalho.get('NOME-DO-EVENTO'))
				dict_trabalho['ano'].append(nodeTrabalho.get('ANO-DE-REALIZACAO'))
				dict_trabalho['qualis'].append('-')
				dict_trabalho['tipo'].append('conferencia')


	except AttributeError:
		print('		Sem trabalhos!')
		pass


	artigosEventos = item.find('ARTIGOS-PUBLICADOS')
	try:
		for artigo in artigosEventos.findall('ARTIGO-PUBLICADO'):
			nodeNaturezaArtigo = artigo.find('DADOS-BASICOS-DO-ARTIGO')
			naturezaArtigo = nodeNaturezaArtigo.get('NATUREZA')
			nodeArtigo = artigo.find('DETALHAMENTO-DO-ARTIGO')

			if (naturezaArtigo in ARTIGOS):
				dict_artigo['evento'].append(nodeTrabalho.get('NOME-DO-EVENTO'))
				dict_artigo['ano'].append(nodeTrabalho.get('ANO-DE-REALIZACAO'))
				dict_artigo['qualis'].append('-')
				dict_artigo['tipo'].append('periodico')

	except AttributeError:
		print('		Sem artigos!')
		pass

	
	#return (pd.DataFrame(list_trabalho, index=df_trabalho.columns)), (pd.DataFrame(list_artigo, index=df_trabalho.columns))
	return pd.DataFrame(dict_trabalho), pd.DataFrame(dict_artigo)



# -------- MAIN ----------
CV_SEM_EVENTOS = 0					# Para contabilizar CVS sem eventos registrados
start_time = time.time()

for pasta in os.listdir():
	df_pesquisador['softwares_participacao'].append(0) 			# Correção de erro de CVs
	currentDir = os.getcwd()
	os.chdir(currentDir+ '/' + pasta)
	tree = etree.parse('curriculo.xml')
	myroot = tree.getroot()	

	
	df_pesquisador['id_lattes'].append(myroot.get('NUMERO-IDENTIFICADOR'))
	for item in myroot:		# maior for: representa cada grande item do curriculo lattes
		#print(item.find('CURRICULO-VITAE').get('NUMERO-IDENTIFICADOR'))
		

		if (item.tag == 'DADOS-GERAIS'):
			# Aqui é onde terá a maior parte das produções
			#print('Entrou em DADOS-GERAIS')
			nome_pesquisador = item.get('NOME-COMPLETO')
			print(nome_pesquisador)		# controle na execução
			df_pesquisador['nome'].append(str(nome_pesquisador))
			''' SESSAO DE GENERO '''
			try:
				df_pesquisador['sexo'].append(gender.get_gender(str(nome_pesquisador.split(' ')[0])))
			except requests.exceptions.ConnectionError:
				print('ERRO DE CONEXÃO API IBGE')
				df_pesquisador['sexo'].append('ERRO DE CONEXÃO')
			''' FIM SESSAO DE GENERO '''

			
			# Recuperacao de ano de conclusão
			tag_formacao = item.find('FORMACAO-ACADEMICA-TITULACAO')

			GRADUACAO = tag_formacao.find('GRADUACAO')
			df_pesquisador['graduacao'].append( GRADUACAO.get('NOME-CURSO') )
			df_pesquisador['ano_graduacao'].append( GRADUACAO.get('ANO-DE-CONCLUSAO') )
			df_pesquisador['idade_academica'].append(date.datetime.now().year - int( GRADUACAO.get('ANO-DE-CONCLUSAO')) )
			
			try:
				POSDOC = tag_formacao.find('POS-DOUTORADO')
				df_pesquisador['posdoc'].append( POSDOC.get('NOME-CURSO') )
				df_pesquisador['ano_posdoc'].append(POSDOC.get('ANO-DE-CONCLUSAO') )
			except (AttributeError , ValueError) as e:
				df_pesquisador['posdoc'].append( None )
				df_pesquisador['ano_posdoc'].append( None )

			try:
				DOUTORADO = tag_formacao.find('DOUTORADO')
				df_pesquisador['doutorado'].append( DOUTORADO.get('NOME-CURSO') )
				df_pesquisador['ano_doutorado'].append( DOUTORADO.get('ANO-DE-CONCLUSAO') )
			except (AttributeError , ValueError) as e:
				df_pesquisador['doutorado'].append( None )
				df_pesquisador['ano_doutorado'].append( None )


			try:
				MESTRADO = tag_formacao.find('MESTRADO')
				df_pesquisador['mestrado'].append( MESTRADO.get('NOME-CURSO') )
				df_pesquisador['ano_mestrado'].append( MESTRADO.get('ANO-DE-CONCLUSAO') )
			except (AttributeError , ValueError) as e:
				df_pesquisador['mestrado'].append( None )
				df_pesquisador['ano_mestrado'].append( None )


			# Retirar instiuição de vínculo
			tag_endereco = item.find('ENDERECO')
			INSTITUICAO = tag_endereco.find('ENDERECO-PROFISSIONAL')
			df_pesquisador['instituicao_trabalho'].append(INSTITUICAO.get('NOME-INSTITUICAO-EMPRESA'))
			df_pesquisador['estado_instituicao_trabalho'].append(INSTITUICAO.get('UF'))


			# ATUAÇÕES PROFISSIONAIS: PESQUISA, ATIVIDADES, ETC
			tag_atuacoes = item.find('ATUACOES-PROFISSIONAIS')

			ATUACAO_PROFISSIONAL = tag_atuacoes.find('ATUACAO-PROFISSIONAL')

			ATIVIDADES_DE_DIRECAO_E_ADMINISTRACAO = ATUACAO_PROFISSIONAL.find('ATIVIDADES-DE-DIRECAO-E-ADMINISTRACAO')
			ATIVIDADES_DE_PESQUISA_E_DESENVOLVIMENTO = ATUACAO_PROFISSIONAL.find('ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO')
			ATIVIDADES_DE_ENSINO = ATUACAO_PROFISSIONAL.find('ATIVIDADES-DE-ENSINO')
			ATIVIDADES_DE_EXTENSAO_UNIVERSITARIA = ATUACAO_PROFISSIONAL.find('ATIVIDADES-DE-EXTENSAO-UNIVERSITARIA')
			ATIVIDADES_DE_PARTICIPACAO_EM_PROJETO = ATUACAO_PROFISSIONAL.find('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')

			try:
				df_pesquisador['ATIVIDADES_DE_DIRECAO_E_ADMINISTRACAO'].append(len(ATIVIDADES_DE_DIRECAO_E_ADMINISTRACAO))
			except TypeError:
				df_pesquisador['ATIVIDADES_DE_DIRECAO_E_ADMINISTRACAO'].append(0)
			
			try:
				df_pesquisador['ATIVIDADES_DE_PESQUISA_E_DESENVOLVIMENTO'].append(len(ATIVIDADES_DE_PESQUISA_E_DESENVOLVIMENTO))
			except TypeError:
				df_pesquisador['ATIVIDADES_DE_PESQUISA_E_DESENVOLVIMENTO'].append(0)

			try:
				df_pesquisador['ATIVIDADES_DE_ENSINO'].append(len(ATIVIDADES_DE_ENSINO))
			except TypeError:
				df_pesquisador['ATIVIDADES_DE_ENSINO'].append(0)

			try:
				df_pesquisador['ATIVIDADES_DE_EXTENSAO_UNIVERSITARIA'].append(len(ATIVIDADES_DE_EXTENSAO_UNIVERSITARIA))
			except TypeError:
				df_pesquisador['ATIVIDADES_DE_EXTENSAO_UNIVERSITARIA'].append(0)

			try:
				df_pesquisador['ATIVIDADES_DE_PARTICIPACAO_EM_PROJETO'].append(len(ATIVIDADES_DE_PARTICIPACAO_EM_PROJETO))
			except TypeError:
				df_pesquisador['ATIVIDADES_DE_PARTICIPACAO_EM_PROJETO'].append(0)


			# ÁREAS DE ATUAÇÃO
			try:
				tag_areas = item.find('AREAS-DE-ATUACAO')
				AREA_DE_ATUACAO = tag_areas.find('AREA-DE-ATUACAO')
				try:
					df_pesquisador['grande_area_conhecimento'].append(AREA_DE_ATUACAO.get('NOME-GRANDE-AREA-DO-CONHECIMENTO'))
				except AttributeError:
					df_pesquisador['grande_area_conhecimento'].append(None)
			
				try:
					df_pesquisador['area_conhecimento'].append(AREA_DE_ATUACAO.get('NOME-DA-AREA-DO-CONHECIMENTO'))
				except AttributeError:
					df_pesquisador['area_conhecimento'].append(None)
			
				try:
					df_pesquisador['subarea_conhecimento'].append(AREA_DE_ATUACAO.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO'))
				except AttributeError:
					df_pesquisador['subarea_conhecimento'].append(None)
			except AttributeError:
				df_pesquisador['grande_area_conhecimento'].append(None)
				df_pesquisador['area_conhecimento'].append(None)
				df_pesquisador['subarea_conhecimento'].append(None)
			

			

		
		
		if(item.tag == 'PRODUCAO-BIBLIOGRAFICA'):		# caso prod bibliografica
			df_tb, df_art = parse_PRODUCOES_BIBLIOGRAFICAS(item)
			df_trabalho = pd.concat([df_trabalho, df_tb]).drop_duplicates().reset_index(drop=True)
			df_artigo = pd.concat([df_artigo, df_art]).drop_duplicates().reset_index(drop=True)
			
			#print(df_tb)
			#print(df_art)
			score = 0.0
			df_eventos_auxiliar = pd.concat([df_tb, df_art]).drop_duplicates().reset_index(drop=True)
			if (not df_eventos_auxiliar.empty):
				df_pesquisador['quantidade_producoes'].append(len(df_eventos_auxiliar))
				df_eventos_auxiliar, score, densidade = Avaliador.aplicaNota(eventos_gabarito,df_eventos_auxiliar)
				df_pesquisador['producoes_por_idade'].append(df_pesquisador['quantidade_producoes'][-1]/float(df_pesquisador['idade_academica'][-1]))
			else:		# sem eventos registrados
				df_pesquisador['quantidade_producoes'].append(0)
				df_pesquisador['producoes_por_idade'].append(0)
				densidade = 0.0
				CV_SEM_EVENTOS+=1
				
			
			
			df_pesquisador['nota_qualis'].append(score)						# Define score do pesquisador
			df_pesquisador['precisao_nota_qualis'].append(densidade)		# Define precisão deste score
			df_eventos_auxiliar.to_csv('eventos.csv')
			
			# Aqui também deve ser chamado o avaliador (atribuicao de notas para cada pesquisador)
			

			
		
		if (item.tag == 'PRODUCAO-TECNICA'):
			#print('Entrou em PRODUCAO-TECNICA')
			SOFTWARE = 0
			try:
				tag_software = item.find('SOFTWARE')
				SOFTWARE = len(tag_software)
			except TypeError:
				SOFTWARE = 0
			df_pesquisador['softwares_participacao'][-1] = SOFTWARE
		
		if (item.tag == 'OUTRA-PRODUCAO'):
			ORIENTACOES = 0					# Inicializa como 0 orientações
			#print('Entrou em OUTRA-PRODUCAO')
			try:
				tag_orientacoes = item.find('ORIENTACOES-CONCLUIDAS')
				ORIENTACOES_CONCLUIDAS_MESTRADO = tag_orientacoes.find('ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')
				ORIENTACOES_CONCLUIDAS_DOUTORADO = tag_orientacoes.find('ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')
				OUTRAS_ORIENTACOES_CONCLUIDAS = tag_orientacoes.find('OUTRAS-ORIENTACOES-CONCLUIDAS')
				try:
					ORIENTACOES += len(ORIENTACOES_CONCLUIDAS_MESTRADO)	
				except TypeError:
					ORIENTACOES += 0
					
				try:
					ORIENTACOES += len(ORIENTACOES_CONCLUIDAS_DOUTORADO)	
				except TypeError:
					ORIENTACOES += 0
				
				try:
					ORIENTACOES += len(OUTRAS_ORIENTACOES_CONCLUIDAS)
				except TypeError:
					ORIENTACOES += 0


			except AttributeError:
				print('erro')
			
			#print(ORIENTACOES)
			df_pesquisador['orientacoes'].append(ORIENTACOES)
			df_pesquisador['orientacoes_por_idade'].append(ORIENTACOES/float(df_pesquisador['idade_academica'][-1]))

			

		'''
		if (item.tag == 'DADOS-COMPLEMENTARES'):
			print('Entrou em DADOS-COMPLEMENTARES')
		'''



		#FIM PROCESSA_PRODUCOES
	
	os.chdir(currentDir)
	# Depois de processar os curriculos
	if(PROCESSA_PRODUCOES):
		df_trabalho['categoria'] = 'conferencia'
		df_artigo['categoria'] = 'periodico'
		df_eventos = pd.DataFrame(index=['evento', 'ano', 'qualis', 'categoria'])
		df_eventos = pd.concat([df_trabalho, df_artigo]).drop_duplicates().reset_index(drop=True)
		df_eventos.to_csv('eventos.csv')
	
	#print(df_pesquisador)
	
# fim for pastas
os.chdir('..')



# Casting 

df_pesquisador = pd.DataFrame(df_pesquisador)




# Bloco a ser descomentado
#print(df_pesquisador)
df_pesquisador.to_csv('pesquisadores.csv', sep=';')		# DESCOMENTAR ESSE AQUI QUANDO O CÓDIGO ESTIVER PRONTO

NUMERO_CVS = len(df_pesquisador)

print('\n#### ESTATÍSTICAS ####')
print('Tempo de execução: {:.2f} ({:.2f} segundos)'.format((time.time() - start_time)/60.0, (time.time() - start_time)))
print('Curriculos analisados: {}'.format(NUMERO_CVS))
print('CVs sem eventos registrados: {}'.format(CV_SEM_EVENTOS))
print('Score máximo registrado: {}'.format(df_pesquisador['nota_qualis'].max()))
print('Score mínimo registrado: {}'.format(df_pesquisador['nota_qualis'].min()))
print('Variância de scores: {:.2f}'.format(df_pesquisador['nota_qualis'].var()))
print('Desvio padrão de scores: {:.2f}'.format(df_pesquisador['nota_qualis'].std()))
print('Pesquisadores com Mestrado: {}'.format(df_pesquisador['ano_mestrado'].count()))
print('Pesquisadores com Doutorado: {}'.format(df_pesquisador['ano_doutorado'].count()))
print('Pesquisadores com Pos Doutorado: {}'.format(df_pesquisador['ano_posdoc'].count()))
print('Pesquisadores classificados como masculino: {} ocorrências ({:.2f}%) '.format(df_pesquisador['sexo'].value_counts()['M'],df_pesquisador['sexo'].value_counts()['M']/float(NUMERO_CVS)))
print('Pesquisadores classificados como feminino: {} ocorrências ({:.2f}%) '.format(df_pesquisador['sexo'].value_counts()['F'],df_pesquisador['sexo'].value_counts()['F']/float(NUMERO_CVS)))
#print(df_pesquisador.info(verbose=True))


os.chdir(BASE_DIR)
