Pasta "meuprojeto" contem a virtualenv para executar o script. Os principais programas instalados são:
 - mechanize: $ pip install mechanize
 - simplejson: $ pip install simplejson
 - Pillow: $ pip install Pillow

 Arquivo "numero_identificador_lattes_18052020.csv" contem lista dos Lattes
 - Para ter acesso à este arquivo, descompactar o comprimido pois o GitHub limita o tamanho máximo do arquivo à 100MB

 Para executar o script, fazer:

 $ python baixaDados.py numero_identificador_lattes_18052020.csv	# Atualmente não funcionando por conta do captcha do Lattes

 Após isto, na pasta CSV conterão todos os arquivos Lattes separados por LattesID
 
 
 ############# Segundo script (script de parser HTML) ############
O segundo script utiliza arquivos (curriculos) armazenados na pasta cache.
  
Para executá-lo (funciona em Python 3), fazer:
$ python3 parserHTML.py	# Ainda está em desenvolvimento
