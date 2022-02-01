## Os principais programas instalados são:
 - mechanize: $ pip install mechanize
 - simplejson: $ pip install simplejson
 - Pillow: $ pip install Pillow
 - lxml: $pip install lxml

 Arquivo "numero_identificador_lattes_18052020.csv" contem lista dos Lattes
 - Para ter acesso à este arquivo, descompactar o comprimido pois o GitHub limita o tamanho máximo do arquivo à 100MB

 ## Para executar o primeiro script, fazer:

 $ python baixaDados.py numero_identificador_lattes_18052020.csv    # Atualmente não funcionando por conta do captcha do Lattes

 Após isto, na pasta CSV conterão todos os arquivos Lattes separados por LattesID
 
 ---
 
## Segundo script (script de parser HTML: meu trabalho atual) ############
O segundo script utiliza arquivos (curriculos) armazenados na pasta cache.
  
Para executá-lo (funciona em Python 3), fazer:
$ python3 parserHTML.py # Ainda está em desenvolvimento

 - OBS: Parametro MAX contem o numero de curriculos a serem processados, este numero vai de 1 a 56

 - Este código resulta em um arquivo 'producoes.csv' contendo todas as produções de pesquisadores
definidos no código parserHTML.py. O código Eventos.py está tratando este CSV e gerando um arquivo
'resultadoProvisorio.csv' com as produções encontradas. Este código contem todo o tratamento de dados
e aplicação de expressões regulares para realizar esta busca.

Para executá-lo, fazer (necessita de 'producoes.csv' na mesma pasta):
$ python3 Eventos.py 

---
## Script funcional de Eventos
Este script irá alocar na pasta 'eventos' 2 arquivos: trabalhos.csv e artigos.csv, cada um contendo os eventos referentes a cada produção 
