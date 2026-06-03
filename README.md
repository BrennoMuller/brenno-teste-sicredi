# brenno-teste-sicredi

# Radar de Risco Macroeconômico

### _Data Pipeline_

---

## 1. Introdução, Contexto e Objetivo

O **Radar de Risco Macroeconômico** é uma solução ponta a ponta (_end-to-end_) de engenharia e análise avançada de dados desenvolvida para monitorar, auditar e projetar os impactos econômicos na carteira de crédito.

### Objetivos do Projeto:

- **Automatizar** a extração, traansformação e enriquecimento de dados macroeconômicos estruturados de fontes oficiais.
- **Identificar** anomalias e desvios de comportamento histórico em indicadores de crédito utilizando modelagem estatística (Z-Score).
- **Dashboard** Desenvolver um dashboard para visualização desses dados de forma estrategica.

---

## 2. Arquitetura de Dados & APIs Utilizadas

A base de dados compreende o período de **janeiro de 2020 a maio de 2026**, capturando o comportamento econômico desde os impactos severos da pandemia até as projeções e fechamentos do ano corrente. O pipeline de dados realiza o consumo automatizado via scripts em Python das seguintes fontes:

### Banco Central do Brasil (API SGS)

- **IPCA (Série 433):** Variação mensal percentual utilizada para monitoramento da inflação.
- **Spread do Crédito:** Indicador da diferença entre o custo de captação bancária e a taxa cobrada final ao cliente, essencial para análise de compressão de margens de risco.
- **Taxa de Inadimplência:** Percentual de saldo de operações de crédito com atraso superior a 90 dias (variável dependente do modelo de risco).
- **Taxa Selic (Série 4390):** Taxa básica de juros acumulada ao mês, balizadora do custo do dinheiro na economia.

### 🗺️ IBGE (API de Metadados)

- **Taxa de Desemprego Total:** Indicador de capacidade de renda da população, crucial para correlacionar o risco de crédito de varejo com fatores de macrofricção.

---

## 3. O Dashboard: Escolhas de Visualização e Design

O painel foi desenhado adotando um layout focado em escaneabilidade, alto contraste e hierarquia visual para facilitar a tomada de decisão executiva.

### 📈 Visuais Utilizados:

- **Cartões Dinâmicos (KPIs Superiores):** Incluem métricas de desvio padrão e Z-Score para contextualizar de forma rápida a severidade do período atual em relação à média histórica.
- **Gráfico de Linhas de Duplo Eixo (Histórico x Projeção):** Escolhido por ser o padrão analítico ideal para tendências temporais. O duplo eixo vertical permite correlacionar diretamente na mesma janela temporal o movimento da Selic (Política Monetária) com a velocidade de resposta da Taxa de Inadimplência da carteira.
- **Tabela:** alem do grafico de linhas trouxe uma tabela para acompanhemento dos valores macroeconomicos para facilitar e deixar mais intuitiva a visualização.
- **Filtro de ano:** podendo ver o avanço da metrica atraves de todos os anos ou somente de um periodo escolhido
- **Filtro de risco:** traz 3 segmentos de dados que classifiquei com critico, desvio, normal, esse filtro é baseado no zscore da inadimplencia
- **Slicer da taxa selic:** para poder visualizar e segmentar periodos em que a taxa selic estava em um valor determinado pelo usuario
- **Link para acesso ao Dashboard:** https://app.powerbi.com/links/P-QkLwex1D?ctid=97d4d0bc-d3bd-40c1-b259-11f70211c133&pbi_source=linkShare    caso não for possivel acessar o arquivo fonte esta em dashboards/arquivo_fonte e as imagens do dashboard está em dashboards/exports
---

## 4. Duvidas

- **codigo do IPCA:** reparei que no pdf do desafio temos um codigo para o IPCA porem quando verificado no SGS do banco central ele retorna outra serie temporal, para esse projeo eu usei o codigo 433 mas puxei atravez do ETL ambos.

---

## 4. Projetos Futuros

- Com mais tempo, implementaria mais analises na automação proposta e faria um painel What-if com slicer para identificar o quanto a Selic impactaria na inadimplencia nos proximos anos.

---


## 5. Como Executar o Projeto

1. Instale as dependências necessárias:
   ```bash
   pip install pandas matplotlib seaborn pyyaml requests Path
   ```
