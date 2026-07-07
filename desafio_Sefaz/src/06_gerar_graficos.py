from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Base tratada usada para validar a quantidade de capitais por ano
ARQUIVO_TRATADO = Path("dados_processados/finbra_tratado.parquet")

# Indicadores de 2024 gerados pelo script 05
ARQUIVO_INDICADORES_2024 = Path("outputs/tabelas/indicadores_execucao_2024.csv")

# Pasta onde os graficos serao salvos
PASTA_GRAFICOS = Path("outputs/graficos")


def configurar_estilo():
    # Define um estilo simples e limpo para facilitar a leitura dos graficos
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (12, 7)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 11


def grafico_capitais_por_ano():
    # Le a base tratada para contar capitais por ano
    df = pd.read_parquet(ARQUIVO_TRATADO)

    capitais_por_ano = (
        df.groupby("ano")["capital"]
        .nunique()
        .reset_index(name="quantidade_capitais")
    )

    plt.figure()
    ax = sns.barplot(
        data=capitais_por_ano,
        x="ano",
        y="quantidade_capitais",
        color="#2E86AB"
    )

    ax.set_title("Quantidade de capitais com dados disponíveis por ano")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Quantidade de capitais")

    # Mostra o valor no topo de cada barra
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f")

    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "capitais_por_ano.png", dpi=300)
    plt.close()


def grafico_taxa_execucao_saude_2024():
    # Le os indicadores de 2024, ano usado como referencia comparavel
    df = pd.read_csv(ARQUIVO_INDICADORES_2024)

    # Filtra a funcao Saude
    saude = df[df["Conta"] == "10 - Saúde"].copy()

    # Remove registros sem taxa de execucao
    saude = saude.dropna(subset=["taxa_execucao_percentual"])

    # Seleciona as 10 maiores taxas de execucao em Saude
    top10 = saude.sort_values(
        "taxa_execucao_percentual",
        ascending=False
    ).head(10)

    plt.figure()
    ax = sns.barplot(
        data=top10,
        y="capital",
        x="taxa_execucao_percentual",
        color="#3A7D44"
    )

    ax.set_title("Top 10 capitais por taxa de execução em Saúde - 2024")
    ax.set_xlabel("Taxa de execução financeira (%)")
    ax.set_ylabel("Capital")

    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "top10_taxa_execucao_saude_2024.png", dpi=300)
    plt.close()


def grafico_maceio_vs_media():
    # Le os indicadores de 2024
    df = pd.read_csv(ARQUIVO_INDICADORES_2024)

    # Filtra Saude e Educacao, duas funcoes relevantes para leitura publica
    funcoes_interesse = ["10 - Saúde", "12 - Educação"]
    df = df[df["Conta"].isin(funcoes_interesse)].copy()

    # Separa Maceio para comparar com as demais capitais
    maceio = df[df["capital"].str.contains("Maceió", case=False, na=False)].copy()

    # Calcula a media sem Maceio
    # Assim a cidade comparada nao influencia o proprio referencial
    outras_capitais = df[~df["capital"].str.contains("Maceió", case=False, na=False)]

    media_capitais = (
        outras_capitais.groupby("Conta")["taxa_execucao_percentual"]
        .mean()
        .reset_index()
    )
    media_capitais["grupo"] = "Média das demais capitais"

    # Mantem apenas as colunas necessarias para o grafico
    maceio = maceio[["Conta", "taxa_execucao_percentual"]]
    maceio["grupo"] = "Maceió"

    comparativo = pd.concat([maceio, media_capitais], ignore_index=True)

    plt.figure()
    ax = sns.barplot(
        data=comparativo,
        x="Conta",
        y="taxa_execucao_percentual",
        hue="grupo"
    )

    ax.set_title("Maceió vs média das demais capitais: Saúde e Educação - 2024")
    ax.set_xlabel("Função")
    ax.set_ylabel("Taxa de execução financeira (%)")
    ax.legend(title="Comparação")

    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "maceio_vs_media_saude_educacao_2024.png", dpi=300)
    plt.close()


def gerar_graficos():
    # Cria a pasta de graficos caso ela ainda nao exista
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

    configurar_estilo()

    grafico_capitais_por_ano()
    grafico_taxa_execucao_saude_2024()
    grafico_maceio_vs_media()

    print("Graficos gerados com sucesso em:", PASTA_GRAFICOS)


if __name__ == "__main__":
    gerar_graficos()