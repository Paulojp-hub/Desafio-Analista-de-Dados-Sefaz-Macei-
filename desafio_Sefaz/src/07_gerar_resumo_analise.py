from pathlib import Path
import pandas as pd

# Indicadores de 2024 gerados no script 05
ARQUIVO_INDICADORES_2024 = Path("outputs/tabelas/indicadores_execucao_2024.csv")

# Resumo textual da analise
ARQUIVO_RESUMO = Path("outputs/resumo_analise.txt")


def formatar_percentual(valor):
    # Formata percentuais com duas casas decimais
    if pd.isna(valor):
        return "sem informação"
    return f"{valor:.2f}%"


def formatar_reais(valor):
    # Formata valores monetarios em reais de forma simples
    if pd.isna(valor):
        return "sem informação"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_resumo():
    # Le os indicadores de 2024, ano usado como referencia principal
    df = pd.read_csv(ARQUIVO_INDICADORES_2024)

    # Funcoes principais escolhidas para leitura publica
    funcoes_interesse = ["10 - Saúde", "12 - Educação", "15 - Urbanismo", "04 - Administração"]
    df_funcoes = df[df["Conta"].isin(funcoes_interesse)].copy()

    # Dados especificos de Maceio
    maceio = df_funcoes[df_funcoes["capital"].str.contains("Maceió", case=False, na=False)].copy()

    # Media das demais capitais, sem Maceio
    demais_capitais = df_funcoes[
        ~df_funcoes["capital"].str.contains("Maceió", case=False, na=False)
    ].copy()

    media_demais = (
        demais_capitais.groupby("Conta")["taxa_execucao_percentual"]
        .mean()
        .reset_index()
        .rename(columns={"taxa_execucao_percentual": "media_demais_capitais"})
    )

    comparativo_maceio = maceio.merge(media_demais, on="Conta", how="left")

    # Ranking de Saude por taxa de execucao
    saude = df[df["Conta"] == "10 - Saúde"].copy()
    saude = saude.dropna(subset=["taxa_execucao_percentual"])
    ranking_saude = saude.sort_values("taxa_execucao_percentual", ascending=False)

    melhor_saude = ranking_saude.iloc[0]
    pior_saude = ranking_saude.iloc[-1]

    # Cria a pasta outputs caso necessario
    ARQUIVO_RESUMO.parent.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO_RESUMO, "w", encoding="utf-8") as arquivo:
        arquivo.write("RESUMO DA ANALISE - DESPESAS POR FUNCAO DAS CAPITAIS\n")
        arquivo.write("=" * 60 + "\n\n")

        arquivo.write("Ano principal de comparacao: 2024\n")
        arquivo.write(
            "O ano de 2024 foi usado como referencia principal porque 2025 ainda "
            "esta incompleto, conforme validado pela quantidade de capitais disponiveis.\n\n"
        )

        arquivo.write("Indicador principal:\n")
        arquivo.write(
            "Taxa de execucao financeira = despesas pagas / despesas empenhadas * 100.\n"
        )
        arquivo.write(
            "Em linguagem simples, esse indicador mostra quanto do dinheiro comprometido "
            "foi efetivamente pago dentro do ano.\n\n"
        )

        arquivo.write("Comparacao de Maceio com as demais capitais:\n")
        for _, linha in comparativo_maceio.iterrows():
            arquivo.write(f"- {linha['Conta']}:\n")
            arquivo.write(
                f"  Maceio: {formatar_percentual(linha['taxa_execucao_percentual'])}\n"
            )
            arquivo.write(
                f"  Media das demais capitais: {formatar_percentual(linha['media_demais_capitais'])}\n"
            )

        arquivo.write("\nDestaque em Saude no ano de 2024:\n")
        arquivo.write(
            f"- Maior taxa de execucao: {melhor_saude['capital']} "
            f"({formatar_percentual(melhor_saude['taxa_execucao_percentual'])}).\n"
        )
        arquivo.write(
            f"- Menor taxa de execucao: {pior_saude['capital']} "
            f"({formatar_percentual(pior_saude['taxa_execucao_percentual'])}).\n"
        )

        arquivo.write("\nObservacoes metodologicas:\n")
        arquivo.write(
            "- A analise principal usa apenas linhas classificadas como funcao, "
            "evitando misturar funcoes, subfuncoes e totais agregados.\n"
        )
        arquivo.write(
            "- Maceio foi removida do calculo da media das demais capitais, "
            "para evitar que ela influenciasse o proprio parametro de comparacao.\n"
        )
        arquivo.write(
            "- Valores per capita foram calculados para permitir comparacoes mais justas "
            "entre cidades de tamanhos diferentes.\n"
        )

    print("Resumo da analise gerado em:", ARQUIVO_RESUMO)


if __name__ == "__main__":
    gerar_resumo()