from pathlib import Path
import pandas as pd

# Base tratada gerada no script 03
ARQUIVO_ENTRADA = Path("dados_processados/finbra_tratado.parquet")

# Arquivo de saida com o resumo da validacao
ARQUIVO_SAIDA = Path("outputs/resumo_validacao.txt")


def validar_dados():
    # Le a base tratada
    df = pd.read_parquet(ARQUIVO_ENTRADA)

    # Cria a pasta outputs, caso ela ainda nao exista
    ARQUIVO_SAIDA.parent.mkdir(exist_ok=True)

    # Conta quantas capitais aparecem em cada ano
    # Essa validacao e importante porque 2025 esta incompleto
    capitais_por_ano = df.groupby("ano")["capital"].nunique()

    # Conta quantas linhas existem por ano
    linhas_por_ano = df["ano"].value_counts().sort_index()

    # Mostra a distribuicao dos tipos de conta
    # Ajuda a confirmar que funcao, subfuncao e totais foram separados
    tipos_conta = df["tipo_conta"].value_counts()

    # Lista os estagios da despesa encontrados
    estagios_despesa = sorted(df["Coluna"].dropna().unique())

    # Conta valores nulos na coluna Valor
    valores_nulos = df["Valor"].isna().sum()

    # Salva o resumo da validacao em arquivo de texto
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as arquivo:
        arquivo.write("RESUMO DE VALIDACAO DOS DADOS\n")
        arquivo.write("=" * 40 + "\n\n")

        arquivo.write("Capitais por ano:\n")
        arquivo.write(capitais_por_ano.to_string())
        arquivo.write("\n\n")

        arquivo.write("Linhas por ano:\n")
        arquivo.write(linhas_por_ano.to_string())
        arquivo.write("\n\n")

        arquivo.write("Tipos de conta:\n")
        arquivo.write(tipos_conta.to_string())
        arquivo.write("\n\n")

        arquivo.write("Estagios da despesa encontrados:\n")
        for estagio in estagios_despesa:
            arquivo.write(f"- {estagio}\n")

        arquivo.write("\n")
        arquivo.write(f"Valores nulos na coluna Valor: {valores_nulos}\n")

        arquivo.write("\nOBSERVACAO:\n")
        arquivo.write(
            "O ano de 2025 deve ser analisado com cautela, pois o README informa "
            "que ele ainda esta incompleto. Por isso, 2024 sera usado como principal "
            "ano de comparacao entre capitais.\n"
        )

    # Mostra no terminal os principais resultados
    print("Validacao concluida.")
    print("Resumo salvo em:", ARQUIVO_SAIDA)
    print("\nCapitais por ano:")
    print(capitais_por_ano)
    print("\nValores nulos na coluna Valor:", valores_nulos)


if __name__ == "__main__":
    validar_dados()