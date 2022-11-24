Bem vindo ao LattesAnalyst! (Nome informal escolhido para este projeto)

Este projeto foi desenvolvido como trabalho de conclusão de curso em Engenharia de Computação na UFMS 2022

Seu opjetivo é realizar uma análise completa dos dados de currículos Lattes em seu formato XML, fazendo desde a raspagem dos dados, armazenamento, modelagem e transformação até a visualização de informações úteis.

As bbliotecas necessárias para execução são:
 - pandas: $ pip install pandas
 - matplotlib: $ sudo apt-get install python-matplotlib
 - Levenshtein: $ pip install Levenshtein
 - genderbr: $ pip install genderbr
 - FuzzyWuzzy: $ pip install fuzzywuzzy
 - lxml: $pip install lxml


 Para executar o script, fazer:

 $ python3 LattesAnalyst.py

 Isto irá gerar o arquivo _pesquisadores.csv_ e _eventos.csv_ dentro da pasta _eventos_
 
 
Para executar o script de processamento dos eventos e periódicos, fazer:

$ python3 Eventos.py 


- Este código resulta em um arquivo _'eventos_gabarito.csv'_ contendo todas as produções dos pesquisadores com mapeamento de Qualis e outras informações.
