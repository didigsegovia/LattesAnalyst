import os
import pandas as pd
import re



def abrirArquivos():
    #sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9pKKjSwGjJaztc9yM7VxSbi9lPFbqg4uN3-ccNcyVB7hfh3z6qphKusWpdSX5Ljg5RnuJjfy4Uazt/pubhtml"  # gabarito 
    #sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZsntDnttAWGHA8NZRvdvK5A_FgOAQ_tPMzP7UUf-CHwF_3PHMj_TImyXN2Q_Tmcqm2MqVknpHPoT2/pubhtml?gid=0&single=true"    # gabarito eventos (conferencias)
    #url_1 = sheet_url.replace("/pubhtml?gid=", "/pub?output=csv&gid=")

    #conferencias = pd.read_csv(url_1)
    conferencias = pd.read_csv('eventos/conferenciasTratadas.csv')

    eventos_gabarito = pd.read_csv('eventos_manual_ufms.csv')

    return eventos_gabarito, conferencias

def defineQualis(algoritmo, nome_final, eventos_gabarito, conferencias):
    algoritmo = str(algoritmo)
    nome_final = str(nome_final)
    qualis = '-'

    try:
        qualis = conferencias.loc[(nome_final == conferencias['conferencia'])  , 'Qualis_Final'].iloc[0]
        print(qualis)
    except IndexError:
        print('Não achou qualis')
        
    return qualis



def avaliaPesquisador(eventos_gabarito, conferencias):
    
    eventos_gabarito['qualis_final'] = eventos_gabarito.apply(lambda x: defineQualis(x['algoritmo_match_final'], x['nome_evento_final'], eventos_gabarito, conferencias), axis=1)
    eventos_gabarito.to_csv('eventos_ufms.csv')



def retornaQualis(eventos_gabarito, evento):
    evento = str(evento)
    qualis = None

    #print(evento)
    # Agora usar o loc
    try:
        # Agora utilizando o igual, não é um bom método de comparação: ver uma melhor forma
        qualis = eventos_gabarito.loc[(evento == eventos_gabarito['evento']), 'qualis_final'].iloc[0]
        #print('Achou Qualis')
    except IndexError:
        return None

    return qualis
    
def contaQualis(df_eventos, qualis):
    return (df_eventos[df_eventos == qualis].count())['qualis']


def aplicaNota(eventos_gabarito, df_eventos):           # Aqui a mágica acontece xD
    
    # Passando tudo para minúsculo
    df_eventos['evento'] = df_eventos['evento'].str.lower()

    # Tirar acentos
    df_eventos['evento'] = df_eventos['evento'].str.normalize('NFKD')\
       														.str.encode('ascii', errors='ignore')\
       														.str.decode('utf-8')
    
    eventos_gabarito['evento'] = eventos_gabarito['evento'].str.lower()
    eventos_gabarito['evento'] = eventos_gabarito['evento'].str.normalize('NFKD')\
                                                            .str.encode('ascii', errors='ignore')\
       														.str.decode('utf-8')

    df_eventos['qualis'] = df_eventos['evento'].apply(lambda x: retornaQualis(eventos_gabarito, x))
    '''
        Até aqui ja tenho em df_eventos todos os eventos do pesquisador com a coluna qualis preenchida de valores
        Agora, utilizar a formula do CA-CC (Comitê de Área de Ciência da computação CAPES)
        iGeralTotal = iRestritoTotal + #B1*0.5 + #B2*0.2 + #B3*0.1 + #B4*0.05
        iRestritoTotal = #A1 + #A2*0.875 + #A3*0.75 + #A4*0.625

        Chamar função para contar ocorrências de qualis
    '''
    #contaQualis(df_eventos, 'B4')
    iRestritoTotal = contaQualis(df_eventos, 'A1') + contaQualis(df_eventos, 'A2') * 0.875 + contaQualis(df_eventos, 'A3') * 0.75 + contaQualis(df_eventos, 'A4') * 0.625
    iGeralTotal = iRestritoTotal + contaQualis(df_eventos, 'B1') * 0.5 + contaQualis(df_eventos, 'B2') * 0.2 + contaQualis(df_eventos, 'B3') * 0.1 + contaQualis(df_eventos, 'B4') * 0.05 # score


    # Cálculo da precisão: Precisão = 1-(NaN/Total)
    densidade =  1 - (contaQualis(df_eventos, '-'))/len(df_eventos.index)
    #print('score: {0:.2f}'.format(iGeralTotal))
    #print('densidade: {0:.2f}'.format(densidade))

    return df_eventos, iGeralTotal, densidade
    

def main():
    # Foi feita uma adaptação para o código rodar a partir daqui, a fim de testes
    # Para retornar ao funcionamento que deve ser utilizado:
    # Linha 150 de LattesAnalyst: chamar a função aplicaNota()


    
    #eventos_gabarito, conferencias = abrirArquivos()
    #df = avaliaPesquisador(eventos_gabarito, conferencias)
    print('Olá mundo!')
    df_eventos = pd.read_csv('eventos.csv')
    eventos_gabarito = pd.read_csv('eventos_gabarito.csv')
    df_eventos, score, densidade = aplicaNota(eventos_gabarito, df_eventos)
    df_eventos.to_csv('teste.csv')
    print('Salvo! Score = {0:.2f}'.format(float(score)))

    exit()


if __name__ == '__main__':
    main()


