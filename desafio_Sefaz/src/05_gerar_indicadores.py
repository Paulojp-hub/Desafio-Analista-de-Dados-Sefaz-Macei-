from pathlib import Path
import pandas as pd

# Base tratada gerada no script 03
ARQUIVO_ENTRADA = Path("dados_processados/finbra_tratado.parquet")

# Pasta onde as tabelas finais de indicadores serão salvas
PASTA_OUTPUTS = Path("outputs/tabelas")

# Arquivos de saída
ARQUIVO_INDICADORES_CSV = PASTA_OUTPUTS / "indicadores_execucao_financeira.csv"
ARQUIVO_INDICADORES_PARQUET = PASTA_OUTPUTS / "indicadores_execucao_financeira.parquet"
ARQUIVO_INDICADORES_2024 = PASTA_OUTPUTS / "indicadores_execucao_2024.csv"


def gerar_indicadores():
    # Lê a base tratada em formato Parquet, que é mais rápido e eficiente
    df = pd.read_parquet(ARQUIVO_ENTRADA)

    # Cria a pasta de saída caso ela ainda não exista
    PASTA_OUTPUTS.mkdir(parents=True, exist_ok=True)

    # Filtra apenas as funções orçamentárias
    # Isso evita misturar funções com subfunções e totais agregados
    df_funcoes = df[df["tipo_conta"] == "funcao"].copy()

    # Mantém apenas as duas colunas principais para o indicador:
    # Despesas Empenhadas e Despesas Pagas
    df_execucao = df_funcoes[
        df_funcoes["Coluna"].isin(["Despesas Empenhadas", "Despesas Pagas"])
    ].copy()

    # Transforma as linhas de estágio da despesa em colunas
    # Assim, empenhado e pago ficam lado a lado na mesma linha
    indicadores = df_execucao.pivot_table(
        index=[
            "ano",
            "capital",
            "Instituição",
            "UF",
            "População",
            "Conta",
            "codigo_conta",
            "nome_conta"
        ],
        columns="Coluna",
        values="Valor",
        aggfunc="sum"
    ).reset_index()

    # Remove o nome do eixo criado pelo pivot_table
    indicadores.columns.name = None

    # Renomeia as colunas para nomes mais simples
    indicadores = indicadores.rename(
        columns={
            "Despesas Empenhadas": "valor_empenhado",
            "Despesas Pagas": "valor_pago"
        }
    )

    # Garante que as colunas existam mesmo se algum estágio estiver ausente
    if "valor_empenhado" not in indicadores.columns:
        indicadores["valor_empenhado"] = 0

    if "valor_pago" not in indicadores.columns:
        indicadores["valor_pago"] = 0

    # Calcula a diferença entre o que foi empenhado e o que foi pago
    indicadores["diferenca_empenhado_pago"] = (
        indicadores["valor_empenhado"] - indicadores["valor_pago"]
    )

    # Calcula a taxa de execução financeira
    # Ela mostra quanto foi pago em relação ao que foi empenhado
    indicadores["taxa_execucao_percentual"] = (
        indicadores["valor_pago"] / indicadores["valor_empenhado"] * 100
    )

    # Evita resultados infinitos quando o valor empenhado for zero
    indicadores["taxa_execucao_percentual"] = (
        indicadores["taxa_execucao_percentual"]
        .replace([float("inf"), -float("inf")], pd.NA)
    )

    # Calcula valores por habitante para comparar capitais de tamanhos diferentes
    indicadores["valor_pago_per_capita"] = (
        indicadores["valor_pago"] / indicadores["População"]
    )

    indicadores["valor_empenhado_per_capita"] = (
        indicadores["valor_empenhado"] / indicadores["População"]
    )

    # Separa 2024 como principal ano de comparação
    # O README e o recrutador destacaram que 2025 ainda está incompleto
    indicadores_2024 = indicadores[indicadores["ano"] == 2024].copy()

    # Salva os indicadores completos
    indicadores.to_csv(ARQUIVO_INDICADORES_CSV, index=False, encoding="utf-8-sig")
    indicadores.to_parquet(ARQUIVO_INDICADORES_PARQUET, index=False)

    # Salva também uma base específica de 2024
    indicadores_2024.to_csv(ARQUIVO_INDICADORES_2024, index=False, encoding="utf-8-sig")

    # Resumo no terminal
    print("Indicadores gerados com sucesso.")
    print("Arquivo completo:", ARQUIVO_INDICADORES_CSV)
    print("Arquivo 2024:", ARQUIVO_INDICADORES_2024)
    print("Total de linhas:", len(indicadores))
    print("Total de linhas em 2024:", len(indicadores_2024))
    print("\nColunas geradas:")
    print(indicadores.columns.tolist())


if __name__ == "__main__":
    gerar_indicadores()