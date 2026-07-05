from pathlib import Path
import zipfile

# Pasta onde estão os arquivos .zip organizados por ano
PASTA_COMPACTOS = Path("dados_compactos")

# Pasta onde os arquivos extraídos serão salvos
PASTA_EXTRAIDOS = Path("dados_extraidos")


def extrair_arquivos_zip():
    # Cria a pasta dados_extraidos caso ela ainda não exista
    PASTA_EXTRAIDOS.mkdir(exist_ok=True)

    # Procura todos os arquivos .zip dentro de dados_compactos e suas subpastas
    arquivos_zip = list(PASTA_COMPACTOS.rglob("*.zip"))

    # Se nenhum arquivo .zip for encontrado, mostra uma mensagem e encerra a função
    if not arquivos_zip:
        print("Nenhum arquivo .zip encontrado em dados_compactos.")
        return

    # Percorre cada arquivo .zip encontrado
    for arquivo_zip in arquivos_zip:
        # Pega o ano pelo nome da pasta onde o arquivo .zip está
        # Exemplo: dados_compactos/2020/arquivo.zip -> ano = 2020
        ano = arquivo_zip.parent.name

        # Define a pasta de destino da extração para aquele ano
        # Exemplo: dados_extraidos/2020
        destino = PASTA_EXTRAIDOS / ano

        # Cria a pasta do ano dentro de dados_extraidos, se ainda não existir
        destino.mkdir(parents=True, exist_ok=True)

        # Abre o arquivo .zip em modo de leitura
        with zipfile.ZipFile(arquivo_zip, "r") as zip_ref:
            # Extrai todo o conteúdo do .zip para a pasta de destino
            zip_ref.extractall(destino)

        # Mostra no terminal qual arquivo foi extraído e para onde ele foi enviado
        print("Arquivo extraido:", arquivo_zip.name, "->", destino)


# Esse bloco faz o script rodar apenas quando executado diretamente
# Ou seja, quando usamos: python src/01_extrair_dados.py
if __name__ == "__main__":
    extrair_arquivos_zip()