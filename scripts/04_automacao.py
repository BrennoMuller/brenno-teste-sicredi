import os
import yaml  # Biblioteca PyYAML
import pandas as pd
import numpy as np
from datetime import datetime


# carregar arquivo de configuração YAML
def carregar_configuracao(caminho_config="../config/config.yaml"):
    if not os.path.exists(caminho_config):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {caminho_config}")

    with open(caminho_config, "r", encoding="utf-8") as f:
        # Loader seguro para evitar execução de código arbitrário no YAML
        return yaml.load(f, Loader=yaml.SafeLoader)


config = carregar_configuracao()

# variáveis vindas do YAML
ARQUIVO_DADOS = config["caminhos"]["arquivo_dados"]
PASTA_RELATORIOS = config["caminhos"]["pasta_relatorios"]
LIMITE_ZSCORE = config["parametros_analise"]["limite_zscore"]
LIMITE_SPREAD = config["parametros_analise"]["limite_spread_minimo"]

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        raise FileNotFoundError(f"A base de dados não foi encontrada em: {ARQUIVO_DADOS}")
    df = pd.read_csv(ARQUIVO_DADOS)
    df['data'] = pd.to_datetime(df['data'])
    return df

def executar_analise(df):
    alertas = []

    # 1. Detecção de Outliers com o limite vindo do YAML
    if 'inadimplência_zscore' not in df.columns:
        media_inad = df['Taxa_de_Inadimplência'].mean()
        std_inad = df['Taxa_de_Inadimplência'].std()
        df['inadimplência_zscore'] = (df['Taxa_de_Inadimplência'] - media_inad) / std_inad

    # Usa a variável dinâmica LIMITE_ZSCORE
    outliers = df[df['inadimplência_zscore'].abs() > LIMITE_ZSCORE]
    for _, row in outliers.iterrows():
        alertas.append(
            f"🚨 **ANOMALIA CRÍTICA**: Mês **{row['data'].strftime('%m/%Y')}** | "
            f"Inadimplência: **{row['Taxa_de_Inadimplência']}%** (Z-Score: **{row['inadimplência_zscore']:.2f}**)."
        )

    # 2. Alerta de Margem com o limite vindo do YAML
    if 'Spread_Selic' in df.columns:
        margens_criticas = df[df['Spread_Selic'] < LIMITE_SPREAD]
        for _, row in margens_criticas.iterrows():
            alertas.append(
                f"⚠️ **ALERTA DE MARGEM**: Mês **{row['data'].strftime('%m/%Y')}** | "
                f"Spread_Selic caiu para **{row['Spread_Selic']:.2f}** (Abaixo do limite prudencial de {LIMITE_SPREAD})."
            )

    # 3. Matriz de Correlação (Se ativado no YAML)
    matriz_corr = None
    if config["relatorio"]["incluir_matriz_correlacao"]:
        colunas_analise = ['Taxa_de_Inadimplência', 'Taxa_Selic', 'juro_real']
        colunas_presentes = [c for c in colunas_analise if c in df.columns]
        matriz_corr = df[colunas_presentes].corr(method='pearson')

    return alertas, matriz_corr, len(df)

def gerar_relatorio_markdown(alertas, matriz_corr, total_registros):
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    nome_arquivo = f"Relatorio_Estatistico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    caminho_final = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    conteudo = []
    conteudo.append(f"# Relatório Automatizado de Análise Estatística e Riscos #")
    conteudo.append(f"**Gerado em:** {data_atual} | **Volume de dados analisado:** {total_registros} meses.\n")
    conteudo.append(f"---")

    # Seção 1: Alertas e Anomalias
    conteudo.append(f"## 📌 1. Painel de Alertas Operacionais")
    if not alertas:
        conteudo.append(f"✅ Nenhum comportamento fora da normalidade ou outlier estatístico foi detectado no período.")
    else:
        for alerta in alertas:
            conteudo.append(f"{alerta}")
    conteudo.append(f"\n---")

    # Seção 2: Correlações Macroeconômicas
    if matriz_corr is not None:
        conteudo.append(f"## 📈 2. Matriz de Correlação entre os dados Macroeconomicos (Pearson)")


        # Transforma a matriz do pandas em uma tabela Markdown bonita (requer pacote 'tabulate')
        conteudo.append(matriz_corr.to_markdown())
        conteudo.append(f"\n\n*Nota de Auditoria: *")

    # Salva o arquivo final
    with open(caminho_final, "w", encoding="utf-8") as f:
        f.write("\n".join(conteudo))

    print(f"[{datetime.now()}] SUCESSO: Relatório estatístico exportado para {caminho_final}")


if __name__ == "__main__":
    try:
        dados_tabela = carregar_dados()
        lista_alertas, matriz_correlacao, total_linhas = executar_analise(dados_tabela)
        gerar_relatorio_markdown(lista_alertas, matriz_correlacao, total_linhas)
    except Exception as e:
        print(f" Falha na execução da análise: {str(e)}")
