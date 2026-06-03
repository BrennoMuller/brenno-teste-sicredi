import os
import pandas as pd

pasta_brutos = r'../dados/brutos/'

paths = [
    os.path.abspath(os.path.join(pasta_brutos, arquivo))
    for arquivo in os.listdir(pasta_brutos)
    if os.path.isfile(os.path.join(pasta_brutos, arquivo))
]

df_final = pd.DataFrame()
for arq in paths:

  if arq.endswith('.csv') and not 'tx_desemprego.csv' in arq:

    df = pd.read_csv(arq, sep=',')

    codigo = df['codigo'].unique()[0]

    df = df.drop('codigo', axis=1)

    df[codigo] = (
                df[codigo]
                .astype(str)
                .str.replace(',', '.')
                .astype(float)
            )

    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')


    if codigo == 'Taxa_Selic':
      # como selic é diario, vou trazer para minha tabela a media mensal
      df = (
          df.set_index('data')
          .resample('ME')
          .mean()
          .reset_index()
      )

    df['data'] = df['data'].dt.strftime('%m/%Y')

    if df_final.empty:
      df_final = df
    else:
      df_final = df_final.merge(df, how='right', on='data')


desemprego = [arq for arq in paths if 'tx_desemprego.csv' in arq.lower()]
df_desemprego = pd.read_csv(desemprego[0], sep=',')

df_desemprego['D3C'] = df_desemprego['D3C'].astype(str)

df_desemprego['ano'] = df_desemprego['D3C'].str[:4].astype(int)
df_desemprego['mes'] = df_desemprego['D3C'].str[4:].astype(int)

df_desemprego['data'] = pd.to_datetime(
    dict(
        year=df_desemprego['ano'],
        month=df_desemprego['mes'],
        day=1
    )
)

df_desemprego['data'] = df_desemprego['data'].dt.strftime('%m/%Y')

df_desemprego = df_desemprego[['data', 'Taxa_Desemprego']]

df_final = df_final.merge(
    df_desemprego,
    on='data',
    how='left'
)

# adicioando novas colunas

# juros reais
df_final["juro_real"] = (
    df_final["Taxa_Selic"] - df_final["IPCA"]
)

# Índice de Pressão Financeira (Serve para criar rankings de meses mais críticos.)
df_final["pressao_financeira"] = (
    df_final["IPCA"] *
    df_final["Taxa_Selic"] *
    df_final["Taxa_de_Inadimplência"]
)

#Razão Spread/Selic
df_final['Spread_Selic'] = (
    df_final['Spread_do_Crédito']
    / df_final['Taxa_Selic']
)

# Z-Score
df_final["inadimplência_zscore"] = (
    (df_final["Taxa_de_Inadimplência"] -
     df_final["Taxa_de_Inadimplência"].mean())
    /
    df_final["Taxa_de_Inadimplência"].std()
)

df_final = df_final.round(2)

df_final.to_csv('./tratados/dados_tratados.csv', sep=',', index=False)
