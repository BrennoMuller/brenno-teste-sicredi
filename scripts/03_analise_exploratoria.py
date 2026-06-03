# %% [markdown]
# <h1>Radar de Risco Macroeconômico — Análise Exploratória de Dados (EDA)</h1>
#
# análise exploratória e estatística dos indicadores macroeconômicos e de risco de crédito obtidos a partir das bases de dados do Banco Central do Brasil (BCB/SGS) e do IBGE.
#  O foco principal é avaliar a sensibilidade da inadimplência frente aos ciclos de política monetária (Selic) e inflação (IPCA).

# %% [markdown]
# <h2>Importação de Bibliotecas</h2>

# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# %% [markdown]
# <h2>Carga da Base de Dados Tratada</h2>

# %%
# Lendo dados
df_final = pd.read_csv('../dados/tratados/dados_tratados.csv', sep=',')

df_final

# %% [markdown]
# <h2>verificando a estrutura do DataFrame</h2>

# %%
df_final.info()

# %% [markdown]
# <h2>extrair as medidas de tendência central e dispersão (média, mediana, desvio padrão, mínimos e máximos) de cada indicador econômico</h2>
#

# %%
df_final.describe()

# %% [markdown]
# <h2>verificar dados nulos e se te tiver vou removelos</h2>
#

# %%
df_final.isna().sum()

# %%
df_final.dropna()

# %% [markdown]
# <h2>Matriz de correlação entre as colunas do DF</h2>

# %%
# Matriz de correlação
corr = df_final.corr(numeric_only=True)

plt.figure(figsize=(8, 5))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    linewidths=0.5
)

plt.title("Matriz de Correlação dos Indicadores Econômicos")
plt.tight_layout()
plt.show()

# %% [markdown]
# <h2>Rank de correlação com taxa de Inadimplência</h2>

# %%
corr = (
    df_final
    .corr(numeric_only=True)
    ['Taxa_de_Inadimplência']
    .sort_values(ascending=False)
)

print(corr)

# %% [markdown]
# <h2>correlação emtre taxa de Inadimplência e Taxa Desemprego</h2>
#
# aqui vemos a comprovação do que vemos na matriz que a correlação entre desemprego e inadimplencia é negativa isso sujero que talvez desemprego não seja um fator tão forte
# para Inadimplência como selic

# %%
# Extrai o ano
df_final['ano'] = df_final['data'].str[-4:]

plt.figure(figsize=(10,6))

for ano, grupo in df_final.groupby('ano'):

    plt.scatter(
        grupo['Taxa_de_Inadimplência'],
        grupo['Taxa_Desemprego'],
        label=ano
    )

    # Escreve o mês/ano ao lado de cada ponto
    for _, row in grupo.iterrows():

        plt.annotate(
            '',
            (
                row['Taxa_de_Inadimplência'],
                row['Taxa_Desemprego']
            ),
            fontsize=8
        )

plt.xlabel('Taxa de Inadimplência (%)')
plt.ylabel('Taxa de Desemprego (%)')
plt.title('Desemprego x Inadimplência')
plt.legend(title='Ano')
plt.grid(True)

plt.show()

# %% [markdown]
# <h2>Analise de lag Defasagem, quanto tempo demora para taxa de inadimplecia sofrer alteração a partir de uma mudança na Selic</h2>
#
# vemos que nosso pico fica em 6 meses

# %%
lags = []
correlacoes = []

for lag in range(0, 13):

    corr = (
        df_final['Taxa_Selic']
        .shift(lag)
        .corr(df_final['Taxa_de_Inadimplência'])
    )

    lags.append(lag)
    correlacoes.append(corr)

plt.figure(figsize=(10,5))

plt.plot(
    lags,
    correlacoes,
    marker='o'
)

plt.xlabel('Lag (meses)')
plt.ylabel('Correlação')
plt.title('Correlação entre Selic e Inadimplência por Defasagem')

plt.grid(True)

plt.show()

# %% [markdown]
# <h2>Correlação entre Selic e Inadimplência</h2>

# %%
import matplotlib.pyplot as plt

# Extrai o ano
df_final['ano'] = df_final['data'].str[-4:]

plt.figure(figsize=(8,6))

for ano, grupo in df_final.groupby('ano'):

    plt.scatter(
        grupo['Taxa_de_Inadimplência'],
        grupo['Taxa_Selic'],
        label=ano
    )

    # Escreve o mês/ano ao lado de cada ponto
    for _, row in grupo.iterrows():

        plt.annotate(
            '',
            (
                row['Taxa_de_Inadimplência'],
                row['Taxa_Selic']
            ),
            fontsize=8
        )

plt.xlabel('Taxa de Inadimplência (%)')
plt.ylabel('Taxa_Selic (%)')
plt.title('Selic x Inadimplência')
plt.legend(title='Ano')
plt.grid(True)

# %%
plt.scatter(
    df_final['Taxa_de_Inadimplência'],
    df_final['Spread_do_Crédito']
)
