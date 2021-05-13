# Downloader de HTML's da internet

import requests, os, time
import pandas

pandas.set_option("display.max_colwidth", 150)			# Mostrar todo o texto do pandas


from bs4 import BeautifulSoup


cache = os.listdir('./cache')


class webScraping:
	global page
	global f

	def downloadHTML(self):			# Dummy def para fazer download de um HTML qualquer
		self.page = requests.get('https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/')
		print(type(self.page))

		if (self.page.status_code == 200):
			print("Download feito com sucesso")
			self.f = open('paginateste.html', 'wb')
			self.f.write(self.page.content)
			self.f.close()
			
		else:
			print('Houve um problema ao baixar o HTML')

	# Fim method downloadHTML



	def openCachedHTML(self):
		currentPath = os.getcwd() 													# Salva caminho atual para ser recuperado posteriormente
		os.chdir('./cache')															# Alterar pasta do codigo para pasta cache
		data = {'nome':list(), 'descricao':list(), 'producao':list()}				# Dicionario auxiliar
		stringProducoes = str()
		for cv in (cache):
			
			self.page = open(cv, encoding='latin-1')								# Encoding importantissimo, se nao ele nao funciona
			
			soup = BeautifulSoup(self.page, 'html.parser')
			
			# A partir de agora, em soup eu tenho o código HTML aberto
			

			data['descricao'].append(soup.find_all('p', class_='resumo')[0].get_text())					# Pegar a descricao e colocar no dicionario info			
			data['nome'].append(soup.find_all('h2', class_='nome')[0].get_text())						# Pegar o nome e colocar no dicionario

			for item in list(soup.find_all('div', class_='artigo-completo')):							# Pegar os nomes de artigos completos publicados em periodicos	
				soupProducao = BeautifulSoup(str(list(item.children)[3]), 'html.parser')
				for itemProducao in list(soupProducao.find_all('div', class_='layout-cell-pad-5')):
					stringProducoes += (str(itemProducao.get_text())+'\n')

			data['producao'].append(stringProducoes)
			stringProducoes = str()

			

			##### A partir daqui, ja esta retirando nome do autor, descricao e trabalhos (artigos completos publicados)

			self.page.close()
			#time.sleep(2)
		print(data)
		#df = pandas.DataFrame(data)																		# Transformar o dicionario data em um DataFrame
		#print(df)



		os.chdir(currentPath)


	# fim openCachedHTML method



if __name__ == "__main__":

	scrapper = webScraping()
	
	#scraper.downloadHTML()
	scrapper.openCachedHTML()