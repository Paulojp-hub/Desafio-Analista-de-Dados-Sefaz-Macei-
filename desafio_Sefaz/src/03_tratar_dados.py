from pathlib import Path
import re
import pandas as pd

# Arquivo consolidado gerado pelo script 02_consolidar_dados.py
ARQUIVO_ENTRADA = Path("dados_processados/finbra_consolidado.csv")

# Arquivos de saida com a base tratada
ARQUIVO_SAIDA_CSV = Path("dados_processados/finbra_tratado.csv")
ARQUIVO_SAIDA_PARQUET = Path("dados_processados/finbra_tratado.parquet")


def classificar_conta(conta):
    """
    Classifica a coluna Conta em funcao, subfuncao, demais subfuncoes ou total/outros.
    Isso evita misturar linhas detalhadas com linhas agregadas e gerar dupla contagem.
    """
    conta = str(conta).strip()

    if re.match(r"^\d{2} - ", conta):
        return "funcao"

    if re.match(r"^\d{2}\.\d{3} - ", conta):
        return "subfuncao"

    if re.match(r"^FU\d{2} - ", conta):
        return "demais_subfuncoes"

    return "total_ou_outros"


def extrair_codigo_conta(conta):
    """
    Extrai o codigo inicial da conta.
    Exemplos: 10 - Saude -> 10 | 10.301 - Atencao Basica -> 10.301
    """
    conta = str(conta).strip()
    resultado = re.match(r"^([A-Z]{2}\d{2}|\d{2}\.\d{3}|\d{2})", conta)

    if resultado:
        return resultado.group(1)

    return ""


def extrair_nome_conta(conta):
    """
    Extrai o nome da conta retirando o codigo inicial.
    Exemplo: 10 - Saude -> Saude
    """
    conta = str(conta).strip()

    if " - " in conta:
        return conta.split(" - ", 1)[1]

    return conta


def tratar_valor(df):
    """
    Garante que a coluna Valor esteja como numero.
    Essa etapa permite somar valores e calcular indicadores.
    """
    if df["Valor"].dtype == "object":
        df["Valor"] = (
            df["Valor"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    return df


def tratar_dados():
    # Le a base consolidada
    df = pd.read_csv(ARQUIVO_ENTRADA, encoding="utf-8-sig")

    # Remove espacos extras dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Trata a coluna de valores monetarios
    df = tratar_valor(df)

    # Classifica a conta para evitar dupla contagem nas analises
    df["tipo_conta"] = df["Conta"].apply(classificar_conta)

    # Cria colunas auxiliares para facilitar filtros e graficos
    df["codigo_conta"] = df["Conta"].apply(extrair_codigo_conta)
    df["nome_conta"] = df["Conta"].apply(extrair_nome_conta)

    # Simplifica o nome da instituicao para obter apenas o nome da capital
    df["capital"] = (
    df["Instituição"]
    .astype(str)
    .str.strip()
    .str.replace(r" - [A-Z]{2}$", "", regex=True)
    .str.replace("Prefeitura Municipal de ", "", regex=False)
    .str.replace("Prefeitura Municipal do ", "", regex=False)
    .str.replace("Prefeitura Municipal da ", "", regex=False)
    .str.replace("Municipal de ", "", regex=False)
    .str.strip()
)

# Correção pontual identificada na validação de 2020
    df["capital"] = df["capital"].replace({
    "nicipal de Rio Branco": "Rio Branco"
})



    # Salva a base tratada em CSV e Parquet
    df.to_csv(ARQUIVO_SAIDA_CSV, index=False, encoding="utf-8-sig")
    df.to_parquet(ARQUIVO_SAIDA_PARQUET, index=False)

    # Resumo de conferencia
    print("Base tratada salva em:", ARQUIVO_SAIDA_CSV)
    print("Base em Parquet salva em:", ARQUIVO_SAIDA_PARQUET)
    print("Total de linhas:", len(df))
    print("Tipos de conta encontrados:")
    print(df["tipo_conta"].value_counts())
    print("Valores nulos na coluna Valor:", df["Valor"].isna().sum())


if __name__ == "__main__":
    tratar_dados()