import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

""" EDA de um dataset disponibilizado pelo Ministério do Turismo. 
O dataset contêm dados de chegadas de turistas internacionais no Brasil ao longo do ano 2023, 
incluindo país de origem, quantidade de chegadas por país, UF por onde a chegada ocorreu. 
URL de dados: https://dados.gov.br/dados/conjuntos-dados/estimativas-de-chegadas-de-turistas-internacionais-ao-brasil  """

# Carregando dataset com dados de chegadas de turistas internacionais no Brasil em 2023

dataset = pd.read_csv(
    "chegadas_2023.csv", sep=";", decimal=",", encoding="ISO-8859-1", engine="c"
)


# Iniciando a análise exploratória de dados

dataset["Mês"] = pd.Categorical(
    dataset["Mês"],
    [
        "Janeiro",
        "Fevereiro",
        "Marco",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ],
    ordered=True,
)

dataset.columns

cheg_por_pais = (
    dataset.groupby(by=["País"])
    .agg({"Chegadas": "sum"})
    .rename(columns={"Chegadas": "Total de Chegadas"})
)

cheg_por_pais = cheg_por_pais.sort_values(by="Total de Chegadas", ascending=False)

top_10_paises = cheg_por_pais["Total de Chegadas"].nlargest(10, keep="all")

cheg_no_ano = (
    dataset.groupby(by="Mês")
    .agg({"Chegadas": "sum"})
    .rename(columns={"Chegadas": "Total de chegadas no mês"})
)

cheg_no_ano.sort_values(axis=0, by="Mês")

##### Visualização de Dados #####

# Plotando os países com maior quantidade de turistas com matplotlib

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 8), layout="constrained")

nomes_pais = list(top_10_paises.keys())
chegadas_pais = list(top_10_paises.values)

largura = 0.30
cores = [
    "tab:orange",
    "tab:green",
    "tab:blue",
    "tab:red",
    "tab:purple",
    "tab:pink",
    "tab:brown",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
]

ax1.bar(
    np.arange(len(nomes_pais)),
    chegadas_pais,
    width=largura,
    linewidth=0.5,
    align="center",
    color=cores,
)

ax1.set_xticks(ticks=np.arange(len(nomes_pais)), labels=nomes_pais, rotation="vertical")
ax1.set_yticks(
    ticks=np.arange(0, 2000000, 200000), labels=np.arange(0, 2000000, 200000)
)
ax1.set_xlabel(xlabel="País")
ax1.set_ylabel(ylabel="Chegadas (milhões)")
ax1.set_ylim(0, 2000000)


# Plotando quantidade de chegadas de turistas por mês com seaborn

sns.set_theme(style="ticks")
ax2 = sns.categorical.barplot(
    data=cheg_no_ano,
    x="Mês",
    y="Total de chegadas no mês",
    width=0.5,
    hue="Mês",
    legend=False,
)
ax2.set_xticks(ticks=cheg_no_ano.index)
ax2.set_xticklabels(labels=cheg_no_ano.index, rotation="vertical")
ax2.set_yticks(
    ticks=np.arange(0, 1100000, 100000), labels=np.arange(0, 1100000, 100000)
)
ax2.set_ylabel(ylabel="Total de chegadas")

fig.align_labels()
fig.align_titles()

fig.savefig(fname="Top_10_paises.png", dpi=200)
