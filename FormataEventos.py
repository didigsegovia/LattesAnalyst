import pandas as pd




unicamp = pd.read_csv('eventos_unicamp.csv')
ufms = pd.read_csv('eventos_ufms.csv')
ufms = ufms.drop(columns=['Column1'])



final = pd.concat([unicamp, ufms], ignore_index=True)         # Ignore index faz com que os indices sejam resetados 

final = final.drop_duplicates(ignore_index = True)
final = final.dropna(subset='nome_evento_final')

final.to_csv('eventos_gabarito.csv')

exit()