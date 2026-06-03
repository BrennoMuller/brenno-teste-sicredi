import requests
import pandas as pd
from pathlib import Path

# Define os parâmetros de busca

def verifica_codigo(codigo):
    if codigo == 432:
        variavel = 'Taxa_Selic'

    if codigo == 433:
        variavel = 'IPCA'

    # Taxa de juros - Selic acumulada no mês anualizada base 252
    if codigo == 4189:
        variavel = 'Taxa_de_juros'

    if codigo == 21082:
        variavel = 'Taxa_de_Inadimplência'

    if codigo == 20783:
        variavel = 'Spread_do_Crédito'

    return variavel

# puxa os dados vindos da api bcb e salva na pasta de dados brutos não processados
def get_data_from_bcb():

    codigos_sgs = [432, 433, 4189, 21082, 20783]
    data_inicial = '01/01/2020'
    data_final = '01/06/2026' # inicio do mes recorrente

    for codigo in codigos_sgs:

        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"

        try:

            response = requests.get(url)

            if response.status_code == 200:

                dados = response.json()
                df = pd.DataFrame(dados)

                codigo_str = verifica_codigo(codigo)

                df['codigo'] = codigo_str

                BASE_DIR = Path(__file__).resolve().parent.parent
                caminho = BASE_DIR / "dados" / "brutos"

                caminho.mkdir(parents=True, exist_ok=True)
                df = df.rename(columns={'valor': codigo_str})


                caminho_salvar = rf"{caminho}/{codigo_str}.csv"

                df.to_csv(caminho_salvar, sep=',', index=False)

            else:
                print("Erro ao conectar à APII")
        except:
            print("Erro ao conectar à API")

# puxa os dados vindos da api IBGE e salva na pasta de dados brutos não processados
def get_data_from_IBGE():
    # Tabela 6381 = PNAD Contínua
    # Variável 4099 = Taxa de desocupação (%)

    url = "https://apisidra.ibge.gov.br/values/t/6381/n1/all/v/4099/p/202001-202604"

    response = requests.get(url)
    dados = response.json()

    # Remove cabeçalho
    df_desemprego = pd.DataFrame(dados[1:])

    # Renomeia colunas
    df_desemprego = df_desemprego.rename(columns={
        'D3N': 'Periodo',
        'V': 'Taxa_Desemprego'
    })

    df_desemprego['Taxa_Desemprego'] = pd.to_numeric(
        df_desemprego['Taxa_Desemprego'].str.replace(',', '.'),
        errors='coerce'
    )


    BASE_DIR = Path(__file__).resolve().parent.parent
    caminho = BASE_DIR / "dados" / "brutos"

    caminho.mkdir(parents=True, exist_ok=True)

    caminho_salvar = rf"{caminho}/tx_desemprego.csv"
    df_desemprego.to_csv(caminho_salvar, sep=',', index=False)


get_data_from_bcb()
get_data_from_IBGE()
