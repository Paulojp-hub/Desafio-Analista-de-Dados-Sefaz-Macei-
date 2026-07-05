import pandas as pd
from pathlib import Path

# vamos testar com um ano só primeiro
caminho_teste = Path("dados_extraidos/2020/finbra.csv")

df_teste = pd.read_csv(
    caminho_teste,
    sep=";",            # colunas separadas por ponto e vírgula
    skiprows=3,         # pula as 3 linhas de metadados do topo
    encoding="latin-1", # trata os acentos corretamente
    decimal=",",        # vírgula é separador decimal
    thousands=".",      # ponto separa milhar (ex: 1.234.567,89)
)

print(df_teste.head())        # mostra as 5 primeiras linhas
print(df_teste.dtypes)        # mostra o tipo de cada coluna
print(df_teste.shape)         # mostra (linhas, colunas)

print(df_teste[df_teste['Conta'].str.contains('Saúde', na=False)].head(2))