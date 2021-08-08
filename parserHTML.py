# Downloader de HTML's da internet

import requests, os, time
import pandas                 # DataFrame
import re                     # Regex
import bs4
import datetime as date
import genderbr as gender
# Utilização de genderbr:
# $ gender.get_gender(nome)
# nome é uma string contendo APENAS O PRIMEIRO NOME da pessoa à ser classificada
# retorna um caractere 'F' para mulheres e 'M' para homens
# Mais informações:
# Info para linguagem R: https://fmeireles.com/blog/rstats/genderbr-predizer-sexo/
# repositório oficial: https://pypi.org/project/genderbr/
# Instalado com $ pip install genderbr

#pandas.set_option("display.max_colwidth", 150)			# Mostrar todo o texto do pandas

from bs4 import BeautifulSoup

#if (os.getcwd() == ('/content/drive/My Drive/TCC/cache') or os.getcwd() == ('/content/drive/My Drive/TCC/cacheManual')):
#  os.chdir('..')
#else:
#  os.chdir('/content/drive/MyDrive/TCC')

cache = os.listdir('./cacheManual')
#cache = os.listdir('./cache')

#estadosBrasil = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RR', 'RO', 'RN', 'RS', 'SC', 'SE', 'SP', 'TO']
idiomas = ['Inglês', 'Espanhol', 'Português', 'Francês', 'Italiano', 'Russo', 'Alemão']


class webScraping:
  global page
  global f

#	def downloadHTML(self):			# Dummy def para fazer download de um HTML qualquer
#		self.page = requests.get('https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/')
#		print(type(self.page))
#
#		if (self.page.status_code == 200):
#			print("Download feito com sucesso")
#			self.f = open('paginateste.html', 'wb')
#			self.f.write(self.page.content)
#			self.f.close()
			
#		else:
#			print('Houve um problema ao baixar o HTML')

	# Fim method downloadHTML



  def openCachedHTML(self):
    currentPath = os.getcwd() 													# Salva caminho atual para ser recuperado posteriormente
    #os.chdir('./cache')															# Alterar pasta do codigo para pasta cache
    os.chdir('./cacheManual')															# Alterar pasta do codigo para pasta cacheManual (cache baixada do navegador diretamente sem a pasta de source)
    data = {'nome':list(), 'sexo':list(), 'idade':list(), 'estado':list(), 'idlattes':list(), 'idioma':list(), 'formacao':list(), 'endereco':list() ,'descricao':list(), 'producao':list(), 'doutorado':list(), 'mestrado':list(), 'posdoc':list(), 'licenca':list()}				# Dicionario auxiliar
    stringProducoes = str()
    countIter = 0
    MAX = 4 # alterar pra ver quantas vezes executar
    for cv in (cache):
			
      self.page = open(cv, encoding='latin-1')								# Encoding importantissimo, se nao ele nao funciona
			
      soup = BeautifulSoup(self.page, 'html.parser')
			
			# A partir de agora, em soup eu tenho o código HTML aberto

      # achar idlattes
      resultIdlattes = re.findall(r'ID Lattes: .*>(................).*', str(soup.find_all('div', class_='infpessoa')))
      data['idlattes'].append(str(resultIdlattes[0]))
      
#     p a — finds all a tags inside of a p tag
#     body p a — finds all a tags inside of a p tag inside of a body tag
#     html body — finds all body tags inside of an html tag
#     p.outer-text — finds all p tags with a class of outer-text
#     p#first — finds all p tags with an id of first
#     body p.outer-text — finds any p tags with a class of outer-text inside of a body tag
      ##
      # <br class=clear />
      flagEndereco = 0
      listaEndereco = list()
      for item in list(soup.select('div div.layout-cell-pad-5')):
        for itemaux in list(item.children):
          if (re.findall(r'........ - (.*), (..) - .* - .*:', str(itemaux))):
            flagEndereco = 1
            continue
          if (flagEndereco):
            listaEndereco.append(list(item.children))
            flagEndereco = 0
            continue
      listaEnderecoFinal = list()
      if len(listaEndereco):
        for itemitem in listaEndereco[0]:
          if (isinstance(itemitem, bs4.element.NavigableString)):
            listaEnderecoFinal.append(str(itemitem))
      stringEndereco = ' '.join(listaEnderecoFinal)
      stringEndereco = re.sub(' URL da Homepage:', '', stringEndereco)
      data['endereco'].append(stringEndereco)
      #print(stringEndereco)
      #
			

      data['descricao'].append(soup.find_all('p', class_='resumo')[0].get_text())					# Pegar a descricao e colocar no dicionario info			
      data['nome'].append(soup.find_all('h2', class_='nome')[0].get_text())						# Pegar o nome e colocar no dicionario

      # Definição de sexo a partir do primeiro nome
      data['sexo'].append( gender.get_gender((data['nome'][-1].split(' '))[0] ))
      ###

      #pegar producoes

      parserProducoes(soup, data)

      print("Curriculo parcialmente processado: "+ str(data['nome'][-1]))

      if countIter == MAX-1:
        break
      else:
        countIter+=1

      
      continue


      

      data['licenca'].append(0)
      resultLicensas = list()
      for item in soup.find_all('div', class_='layout-cell layout-cell-9'):       # Pegar o estado à partir da RegEx
        result = re.findall(r'.*, (..) - .*', str(list(item.children)[1]))
        if len(result) == 1:
          data['estado'].append(str(result[0]))

        itemLicensas = re.findall(r'Licença Maternidade', str(item))
        if len(itemLicensas) > 0:
          resultLicensas.append(item)  
        
        
      if (len(resultLicensas) == 1):
         data['licenca'][-1] = ((re.findall(r'/>(.* dias)', str(resultLicensas[0])))[0])
      elif (len(resultLicensas) > 1):
        data['licenca'].pop()
        licencaAux = list()
        for c in resultLicensas:
          licencaAux.append( (re.findall(r'/>(.* dias)', str(c) )[0] ) )
        data['licenca'].append(licencaAux)
      # Fim for estado e licenca

      # Verificacao de titulos
      data['posdoc'].append(0)
      data['doutorado'].append(0)
      data['mestrado'].append(0)

      flagFormacao = 1
      flagTitulo = 1
      stringGraduacao = ''
      grauFormacao = 0;
      for item in soup.find_all('div', class_='layout-cell-pad-5'):
        if flagTitulo:
          resultGraduacaoOrientador = re.search(r'Título: (.+)|Orientador: (.+)', str(item))
          if resultGraduacaoOrientador:
            #print(resultGraduacaoOrientador.group())
            flagTitulo = 0
            #resultGraduacaoOrientador = re.search(r'Orientador: ([a-zA-Z\s]+)', str(item))

        if flagFormacao:
          resultGraduacao = re.search(r'Graduação em (.+)', str(item))
          if resultGraduacao:
            stringGraduacao = re.sub('<span class="ajaxCAPES" data-param="&amp;codigoCurso=&amp;nivelCurso="></span>. <br class="clear"/>',' - ',resultGraduacao.group())
            data['formacao'].append(stringGraduacao)
            flagFormacao = 0


        resultPosdoc = re.findall(r'.*>(Pós-Doutorado.) <.*', str(item))
        if len(resultPosdoc) == 1:
          data['posdoc'][-1] = 1
          continue
          
        resultDoc = re.findall(r'(Doutorado).*', str(item))
        if len(resultDoc) == 1:
          grauFormacao += 1;
          data['doutorado'][-1] = 1
          continue
                  
        resultMestre = re.findall(r'(Mestrado).*', str(item))
        if len(resultMestre) == 1:
          grauFormacao += 1;
          data['mestrado'][-1] = 1
          continue
      # Fim verificacao titulos

      ## Formação
      for resultFormacao in soup.find_all('div', class_='layout-cell layout-cell-12 data-cell'):

        result = re.findall(r'([0-9]{4} - [0-9]{4})</b>\n</div>\n</div>\n<div class="layout-cell layout-cell-9">\n<div class="layout-cell-pad-5">Graduação em ', str(resultFormacao))
        if (result):
          resultAux = re.findall(r'([0-9]{4} - [0-9]{4})', str(result))
          for cont in resultAux:
            data['formacao'][-1] = str(data['formacao'][-1]) + ' Período: ' + str(cont)
          #print(result)
        # Aqui também tem participação em eventos


      # Cálculo da idade baseado em formação 
      stringIdade = data['formacao'][-1].split(' ')[-1]
      anoAtual = date.datetime.now()
      data['idade'].append( (anoAtual.year - int(stringIdade)) )   # Cálculo grosseiro da idade fazendo 23 + # anos após formatura da graduação

      # Orientações
      #[print(item.children) for item in soup.find_all('div', class_='title-wrapper')]
      


      # Busca de idiomas 
      idiomasAux = list()
      periodoLicenca = list()
      for item in soup.find_all('div', class_='layout-cell-pad-5 text-align-right'):
        periodolicenca = re.findall(r'([0-9]{2}/[0-9]{2}/[0-9]{4} a [0-9]{2}/[0-9]{2}/[0-9]{4})', str(item))
        if periodolicenca:
          periodoLicenca.append(str(periodolicenca))

        #dataGraduacao = re.search(r'[0-9]{4} - [0-9]{4}', str(item))
        #if dataGraduacao:
        #  0+0
          #print(dataGraduacao.group())
        resultIdioma = re.findall(r'<b>(.*)</b>', str(item))[0]
        if resultIdioma in idiomas:
          idiomasAux.append(resultIdioma)   
      data['idioma'].append(idiomasAux)
      if periodoLicenca:
        #indexlicenca=0
        for itemli in range(len(data['licenca'][-1])):
          data['licenca'][-1][itemli] += periodoLicenca[itemli]
          #indexlicenca+=1
          #print(itemli)
          

      #Para cargos: <div class="layout-cell-pad-5">Conselhos, Comissões e Consultoria, Faculdade de Computação, . </div>
      # Para trabalhos que pesquisador ja participou: [print(resultFormacao.get_text()) for resultFormacao in soup.find_all('div', class_='layout-cell layout-cell-12 data-cell')]

      ##### A partir daqui, ja esta retirando nome do autor, sexo(gênero),  lattesid, descricao, trabalhos (artigos completos publicados), estado, titulos (mestre, doutor e pos doutor) e licença maternidade (mais de uma se tiver); idioma
      # data['nome']; data['sexo'];data['idade']; data['lattesid'];  data['producao']; data['descricao']; data['estado']; data['posdoc']; data['doutorado']; data['mestrado']; data[licenca]; data['idioma']

      print("Curriculo processado: "+ str(data['nome'][-1]))

      self.page.close()
			#time.sleep(2)
			
    #df = pandas.DataFrame(data)																		# Transformar o dicionario data em um DataFrame
		
    #printDici(data)
    os.chdir(currentPath)


	# fim openCachedHTML method

def parserProducoes(soup, data):
  # Link com info para pegr: https://linuxhint.com/find_children_nodes_beautiful_soup/
  # Dar uma olhada em descendants
  # Forma alternativa de utilizar
  # https://stackoverflow.com/questions/22217713/how-to-select-a-class-of-div-inside-of-a-div-with-beautiful-soup
  stringProducoes = str()
  for item in list(soup.find_all('div', class_='artigo-completo')):             # Pegar os nomes de artigos completos publicados em periodicos  
    soupProducao = BeautifulSoup(str(list(item.children)[3]), 'html.parser')
    for itemProducao in list(soupProducao.find_all('div', class_='layout-cell-pad-5')):
      stringProducoes += (str(itemProducao.get_text())+'\n')

    #print(stringProducoes)
    data['producao'].append(stringProducoes)
    stringProducoes = str()
    # até aqui pega artigos completos publicados em periodicos


    # para pegar " Trabalhos completos publicados em anais de congressos "
    # Produção de maquina de estados
    TCPAC = True  # Trabalhos completos publicados em anais de congresso
    REPAC = True  # Resumos expandidos publicados em anais de congresso
    RPAC = True   # Resumos publicados em anais de congresso


    
    for item in list(soup.find_all('div', class_='layout-cell layout-cell-11')):
      print(item.text)  # Aqui está imprimindo os nomes do jeito que eu queroooooooooooooooooooooooo
      data['producao'].append(item.text)
      #print("#################### PULA LINHA ########################")


      #item_descendants = item.descendants
      #for d in item_descendants:
      #  if d.name == 'div' and d.get('class', '') == ['layout-cell-pad-5']:
      #    print(d.text)

def printDici(data):
  
  for i in range(len(data['nome'])):
    print(data['nome'][i])
    print(data['sexo'][i])
    print('Idade acadêmica: '+str(data['idade'][i]) + ' anos')
    print(data['estado'][i])
    #print('LattesID: '+ data['idlattes'][i])
    if (data['endereco'][i]):
      print('Endereco : '+data['endereco'][i])
    print(data['formacao'][i])
    #print(data['descricao'][i])
    #print(data['producao'][i])
    #if data['idioma'][i]:
    #  for c in data['idioma'][i]:
    #    print(str(c))
    #print()
    #if data['posdoc'][i]:
    #  print('Pós-Doutorado')
    #if data['doutorado'][i]:
    #  print('Doutorado')
    #if data['mestrado'][i]:
    #  print('Mestrado')
    
    if data['licenca'][i]:
      for c in data['licenca'][i]:
        print('Licença Maternidade: '+ str(c))
    print()

if __name__ == "__main__":

  scrapper = webScraping()
	
  #scraper.downloadHTML()
  scrapper.openCachedHTML()