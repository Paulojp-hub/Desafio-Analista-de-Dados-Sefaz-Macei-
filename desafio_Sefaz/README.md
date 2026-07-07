# Análise de Despesas por Função das Capitais Brasileiras

Projeto desenvolvido para o desafio técnico de Estágio em Análise de Dados da Sefaz Maceió.

O objetivo é analisar dados de despesas das capitais brasileiras, com foco na comparação entre despesas empenhadas e despesas pagas por função orçamentária.

## Objetivo

Comparar como as capitais brasileiras executam suas despesas por função, observando principalmente a diferença entre o valor empenhado e o valor efetivamente pago.

O principal indicador utilizado foi a Taxa de Execução Financeira:

```text
Taxa de Execução = Despesas Pagas / Despesas Empenhadas * 100
```

Em linguagem simples, esse indicador mostra quanto do valor comprometido pela prefeitura foi realmente pago dentro do ano.

## Fonte dos Dados

Os dados utilizados vêm do FINBRA/Siconfi, no relatório Despesas por Função (Anexo I-E), com escopo de capitais brasileiras.

Os arquivos originais estavam organizados por ano, de 2020 a 2025, dentro da pasta `dados_compactos/`.

## Estrutura do Projeto

```text
dados_compactos/      arquivos zip originais por ano
dados_extraidos/      arquivos csv extraídos por código
dados_processados/    bases consolidadas e tratadas
outputs/
  graficos/           gráficos finais da análise
  tabelas/            tabelas de indicadores
notebooks/            espaço para análises exploratórias
src/                  scripts do pipeline de dados
```

## Ordem de Execução

Os scripts foram numerados para indicar a ordem do pipeline:

```text
01_extrair_dados.py
02_consolidar.py
03_tratar_dados.py
04_validar_dados.py
05_gerar_indicadores.py
06_gerar_graficos.py
07_gerar_resumo_analise.py
```

Para rodar o projeto:

```bash
py src/01_extrair_dados.py
py src/02_consolidar.py
py src/03_tratar_dados.py
py src/04_validar_dados.py
py src/05_gerar_indicadores.py
py src/06_gerar_graficos.py
py src/07_gerar_resumo_analise.py
```

## Tratamento dos Dados

Durante a leitura dos arquivos, foram considerados cuidados importantes do formato original do Siconfi:

- separador de colunas com ponto e vírgula;
- encoding `latin-1`;
- três primeiras linhas como metadados;
- valores monetários com vírgula como separador decimal;
- criação da coluna `ano` a partir da pasta de origem.

Também foi criada uma classificação para a coluna `Conta`, separando:

- função;
- subfunção;
- demais subfunções;
- totais/outros.

Essa separação é importante para evitar dupla contagem, já que algumas linhas representam agregações.

## Validação dos Dados

Antes da análise, foi feita uma validação da completude dos anos.

A contagem mostrou que 2025 possui apenas 11 capitais disponíveis, enquanto 2021 a 2024 possuem 26 capitais. Por isso, 2024 foi usado como principal ano de comparação.

Durante a validação, o ano de 2020 apareceu inicialmente com 27 capitais. Ao investigar os nomes únicos, foi encontrada uma inconsistência de padronização relacionada a Rio Branco. A correção foi aplicada no tratamento dos dados.

## Indicadores Gerados

Foram calculados os seguintes indicadores:

- valor empenhado;
- valor pago;
- diferença entre empenhado e pago;
- taxa de execução financeira;
- valor pago per capita;
- valor empenhado per capita.

A análise principal utiliza apenas contas classificadas como função, evitando misturar funções, subfunções e totais agregados.

## Comunicação dos Resultados

Além das tabelas de indicadores, foram gerados gráficos para facilitar a leitura dos resultados por pessoas não técnicas.

A ideia foi transformar os dados em informação acessível, mostrando visualmente:

- quais anos possuem dados completos;
- por que 2025 não deve ser usado como principal comparação;
- quais capitais tiveram melhor execução financeira em Saúde;
- como Maceió se posiciona em relação à média das demais capitais em Saúde e Educação.

Os gráficos foram pensados para responder perguntas simples, como:

```text
O ano analisado tem dados suficientes?
Quanto do valor empenhado foi realmente pago?
Maceió está acima ou abaixo da média das demais capitais?
```

Dessa forma, a análise busca não apenas calcular indicadores, mas comunicar os resultados de maneira clara e útil para tomada de decisão.


## Principais Conclusões

Em 2024, Maceió apresentou um resultado positivo na função Saúde, com taxa de execução financeira acima da média das demais capitais.

Na função Educação, o comportamento foi diferente: Maceió ficou abaixo da média das demais capitais, indicando que uma parcela maior do valor empenhado não foi paga dentro do ano.

Assim, a principal leitura da análise é:

```text
Maceió se destaca na execução financeira em Saúde, mas fica abaixo da média das demais capitais em Educação.
```

Esse contraste mostra que a execução financeira pode variar bastante conforme a área analisada.

## Gráficos Gerados

Os principais gráficos gerados foram:

- quantidade de capitais com dados disponíveis por ano;
- ranking das capitais por taxa de execução em Saúde em 2024;
- comparação entre Maceió e a média das demais capitais em Saúde e Educação.

Os gráficos estão disponíveis em:

```text
outputs/graficos/
```

## Observações

O ano de 2025 foi mantido na base, mas tratado como parcial, pois nem todas as capitais haviam enviado seus dados.

A comparação principal foi feita com 2024 por ser o ano completo mais recente disponível.

## Tecnologias Utilizadas

- Python
- pandas
- pyarrow
- matplotlib
- seaborn

## Uso de IA

Foi permitido o uso de IA durante o desenvolvimento. A IA foi utilizada como apoio para organização, revisão de código e estruturação da análise. As decisões metodológicas, validações e interpretação dos resultados foram estudadas e revisadas durante o desenvolvimento do projeto.
