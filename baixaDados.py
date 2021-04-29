from baixaLattes import baixaCVLattes

import os
import sys




## Este eh um dummy code para exemplificar o uso do codigo baixaLattes

# Entradas: um ID Lattes do tipo "str"
# Saidas: um HTML completo em relatorio em referencia ao ID Lattes aplicado

# Forneco ID Lattes para o baixaCVLattes(id_Lattes)

def executa(documento):

	arquivo = open(documento, 'r')

	for linha in arquivo:
		print(linha)
		cvLattesHTML = baixaCVLattes(linha)
		file = open(linha, 'w')
		file.write(cvLattesHTML)
		file.close()

	arquivo.close()





if __name__ == "__main__":
	# em sys.args temos os argumentos por linha de comando

	executa(sys.argv[1])