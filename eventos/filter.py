import pandas as pd

df = pd.read_csv('eventosTratados.csv')

df = df.drop(['Unnamed: 0'], axis=1)

df.to_csv('eventosTratados.csv')