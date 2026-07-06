from pathlib import Path
import pandas as pd

# Pasta onde estão os arquivos finbra.csv extraídos por ano
PASTA_EXTRAIDOS = Path("dados_extraidos")

# Pasta onde a base consolidada será salva
PASTA_PROCESSADOS = Path("dados_processados")

# Caminho do arquivo final consolidado
ARQUIVO_SAIDA = PASTA_PROCESSADOS / "finbra_consolidado.csv"


def ler_csv_finbra(caminho_csv):
    """
    Lê um arquivo finbra.csv do Siconfi e adiciona a coluna de ano.

    O arquivo tem algumas particularidades:
    - separador de colunas é ponto e vírgula
    - as 3 primeiras linhas são metadados
    - o encoding é latin-1
    - o decimal usa vírgula
    """

    # O ano está no nome da pasta onde o CSV foi extraído
    # Exemplo: dados_extraidos/2020/finbra.csv -> ano = 2020
    ano = int(caminho_csv.parent.name)

    # Leitura do CSV respeitando o formato brasileiro informado no README
    df = pd.read_csv(
        caminho_csv,
        sep=";",
        skiprows=3,
        encoding="latin-1",
        decimal=","
    )

    # Cria a coluna ano, necessária para comparar os dados ao longo do tempo
    df["ano"] = ano

    return df


def consolidar_dados():
    # Cria a pasta dados_processados caso ela ainda não exista
    PASTA_PROCESSADOS.mkdir(exist_ok=True)

    # Procura todos os arquivos chamados finbra.csv dentro de dados_extraidos
    arquivos_csv = list(PASTA_EXTRAIDOS.rglob("finbra.csv"))

    # Se nenhum CSV for encontrado, encerra o script com uma mensagem clara
    if not arquivos_csv:
        print("Nenhum arquivo finbra.csv encontrado em dados_extraidos.")
        return

    # Lista que vai guardar uma tabela de cada ano
    tabelas = []

    # Lê cada CSV encontrado e adiciona na lista
    for caminho_csv in arquivos_csv:
        print("Lendo arquivo:", caminho_csv)

        df = ler_csv_finbra(caminho_csv)
        tabelas.append(df)

    # Junta todas as tabelas em uma única base
    df_consolidado = pd.concat(tabelas, ignore_index=True)

    # Salva a base consolidada em CSV
    # O encoding utf-8-sig ajuda o Excel a abrir com acentos corretamente
    df_consolidado.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")

    # Mostra um resumo no terminal para conferência
    print("Base consolidada salva em:", ARQUIVO_SAIDA)
    print("Total de linhas:", len(df_consolidado))
    print("Total de colunas:", len(df_consolidado.columns))
    print("Anos encontrados:", sorted(df_consolidado["ano"].unique()))


if __name__ == "__main__":
    consolidar_dados()