import os
import lxml
import pandas as pd
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
df_trabalho = pd.DataFrame({'evento': [],
								'ano':[],
								'qualis': []})
df_artigo = pd.DataFrame({'evento': [],
							'ano':[],
							'qualis': []})


# Manipulando PATH
BASE_DIR = os.getcwd()
os.chdir('./cachexml')


def parse_PRODUCOES_BIBLIOGRAFICAS(item):
	
	#list_trabalho = []
	#list_artigo = []
	dict_trabalho = {'evento':[], 'ano':[], 'qualis':[]}
	dict_artigo = {'evento':[], 'ano':[], 'qualis':[]}

	print("******* Trabalhos ********")
	try:
		trabalhosEventos = item.find('TRABALHOS-EM-EVENTOS')
		for trabalho in trabalhosEventos.findall('TRABALHO-EM-EVENTOS'):
			nodeNaturezaTrabalho = trabalho.find('DADOS-BASICOS-DO-TRABALHO')
			naturezaTrabalho = nodeNaturezaTrabalho.get('NATUREZA')
			nodeTrabalho = trabalho.find('DETALHAMENTO-DO-TRABALHO')

			if (naturezaTrabalho in TRABALHO_COMPLETO):			# Trabalho completo
				'''dict_aux = {'evento':[],'ano':[],'qualis':[]}
				dict_aux['evento'].append(nodeTrabalho.get('NOME-DO-EVENTO'))
				dict_aux['ano'].append(nodeTrabalho.get('ANO-DE-REALIZACAO'))
				dict_aux['qualis'].append('-')
				#list_trabalho.append(dict_aux)
				'''
				dict_trabalho['evento'].append(nodeTrabalho.get('NOME-DO-EVENTO'))
				dict_trabalho['ano'].append(nodeTrabalho.get('ANO-DE-REALIZACAO'))
				dict_trabalho['qualis'].append('-')


	except AttributeError:
		print('Sem trabalhos!')
		pass


	print("******* Artigos ********")
	artigosEventos = item.find('ARTIGOS-PUBLICADOS')
	try:
		for artigo in artigosEventos.findall('ARTIGO-PUBLICADO'):
			nodeNaturezaArtigo = artigo.find('DADOS-BASICOS-DO-ARTIGO')
			naturezaArtigo = nodeNaturezaArtigo.get('NATUREZA')
			nodeArtigo = artigo.find('DETALHAMENTO-DO-ARTIGO')

			if (naturezaArtigo in ARTIGOS):
				'''dict_aux = {'evento':[],'ano':[],'qualis':[]}
				dict_aux['evento'].append(nodeTrabalho.get('NOME-DO-EVENTO'))
				dict_aux['ano'].append(nodeTrabalho.get('ANO-DE-REALIZACAO'))
				dict_aux['qualis'].append('-')
				list_artigo.append(dict_aux)'''
				dict_artigo['evento'].append(nodeTrabalho.get('NOME-DO-EVENTO'))
				dict_artigo['ano'].append(nodeTrabalho.get('ANO-DE-REALIZACAO'))
				dict_artigo['qualis'].append('-')

	except AttributeError:
		print('Sem artigos!')
		pass

	
	#return (pd.DataFrame(list_trabalho, index=df_trabalho.columns)), (pd.DataFrame(list_artigo, index=df_trabalho.columns))
	return pd.DataFrame(dict_trabalho), pd.DataFrame(dict_artigo)



# -------- MAIN ----------
for pasta in os.listdir():
	currentDir = os.getcwd()
	os.chdir(currentDir+ '/' + pasta)
	tree = etree.parse('curriculo.xml')
	myroot = tree.getroot()	
	
	

	#df_tb = pd.DataFrame({'evento': [],
	#							'ano':[],
	#							'qualis': []})
	#df_art = pd.DataFrame({'evento': [],
	#							'ano':[],
	#							'qualis': []})


	for item in myroot:		# maior for: representa cada grande item do curriculo lattes
		
		if (item.tag == 'DADOS-GERAIS'):
			#print('Entrou em DADOS-GERAIS')
			print(item.get('NOME-COMPLETO'))
		
		
		if(item.tag == 'PRODUCAO-BIBLIOGRAFICA'):		# caso prod bibliografica
			df_tb, df_art = parse_PRODUCOES_BIBLIOGRAFICAS(item)
			df_trabalho = pd.concat([df_trabalho, df_tb]).drop_duplicates().reset_index(drop=True)
			df_artigo = pd.concat([df_artigo, df_art]).drop_duplicates().reset_index(drop=True)
			
			#print(df_trabalho)

			

		'''
		if (item.tag == 'PRODUCAO-TECNICA'):
			print('Entrou em PRODUCAO-TECNICA')
		'''
		'''
		if (item.tag == 'OUTRA-PRODUCAO'):
			print('Entrou em OUTRA-PRODUCAO')
		'''
		'''
		if (item.tag == 'DADOS-COMPLEMENTARES'):
			print('Entrou em DADOS-COMPLEMENTARES')
		'''

	# Depois de processar os curriculos
	df_trabalho['categoria'] = 'conferencia'
	df_artigo['categoria'] = 'periodico'
	df_eventos = pd.DataFrame(index=['evento', 'ano', 'qualis', 'categoria'])
	df_eventos = pd.concat([df_trabalho, df_artigo]).drop_duplicates().reset_index(drop=True)

	os.chdir(currentDir)
# fim for pastas

# Extrair e colocar todos os dados em 2 arquivos
os.chdir(BASE_DIR+'/eventos')
#df_trabalho.to_csv('trabalhos.csv')
#df_artigo.to_csv('artigos.csv')
df_eventos.to_csv('eventos.csv')
os.chdir(BASE_DIR)
