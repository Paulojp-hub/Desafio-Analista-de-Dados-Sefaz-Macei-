# Desafio Técnico — Estágio em Análise de Dados | Sefaz Maceió

Solução desenvolvida para o desafio técnico da vaga de estágio em Análise de Dados
da Secretaria Municipal da Fazenda de Maceió (Sefaz Maceió). O enunciado original
está disponível em [`DESAFIO.md`](./DESAFIO.md).

## 🎯 Objetivo

Comparar como as 26 capitais brasileiras executam seus gastos públicos por função,
olhando a diferença entre o que foi **empenhado** (comprometido) e o que foi
efetivamente **pago**, usando dados do FINBRA/Siconfi de 2020 a 2025.

## 🛠️ Como rodar o projeto

```bash
# 1. Clone o repositório e entre na pasta
git clone <url-do-seu-fork>
cd <pasta-do-projeto>

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o pipeline completo, na ordem
python src/01_extrair.py
python src/02_consolidar_dados.py
python src/03_tratar_dados.py
python src/04_validar_dados.py
python src/05_gerar_indicadores.py
python src/06_gerar_graficos.py
python src/07_gerar_resumo.py
```

> ⚠️ Importante: os scripts têm dependência sequencial. Sempre que um script
> anterior (ex: `03_tratar_dados.py`) for alterado, rode-o novamente antes dos
> scripts seguintes, para garantir que o Parquet consolidado reflita a versão
> mais recente do tratamento.

## 📂 Estrutura do pipeline

| Script | O que faz |
|---|---|
| `01_extrair.py` | Descompacta os `.zip` de `dados_compactos/` para `dados_extraidos/`, identificando o ano pela pasta de origem. |
| `02_consolidar_dados.py` | Lê os 6 CSVs (tratando encoding Latin-1, separador `;` e decimal `,`) e consolida em um único DataFrame com a coluna `ano`. |
| `03_tratar_dados.py` | Classifica cada linha em função/subfunção/total (evitando dupla contagem), extrai código e nome da conta, e limpa o nome da capital. |
| `04_validar_dados.py` | Confere quantas capitais existem por ano, tipos de conta e valores nulos — gera `outputs/resumo_validacao.txt`. |
| `05_gerar_indicadores.py` | Calcula a Taxa de Execução Financeira (Pago/Empenhado) por capital e função, incluindo valores per capita. |
| `06_gerar_graficos.py` | Gera os gráficos comparativos em `outputs/graficos/`. |
| `07_gerar_resumo.py` | Gera o resumo textual da análise em `outputs/resumo_analise.txt`. |

## 🧠 Decisões técnicas

- **Parquet como formato de saída**: escolhido por ser colunar, comprimido e
  muito mais rápido de reler do que os CSVs originais, além de preservar os
  tipos de dado (evitando reconverter `Valor` para número a cada leitura).
- **DuckDB para consultas agregadas**: usado sobre o Parquet consolidado para
  aproveitar performance em SQL nas comparações entre as 26 capitais, mantendo
  o pandas para a etapa de leitura/limpeza inicial (mais flexível para tratar
  encoding e formatos brasileiros).
- **Classificação de `tipo_conta` via regex**: cada linha da coluna `Conta` é
  classificada como função, subfunção, "demais subfunções" ou total/outros,
  evitando somar a mesma despesa duas vezes (ex: função `10 - Saúde` e sua
  subfunção `10.301 - Atenção Básica` não são somadas juntas).
- **Exclusão de Maceió no cálculo da "média das demais capitais"**: garante
  que a cidade comparada não influencie o próprio parâmetro de comparação.
- **2024 como ano principal de comparação**: 2025 está incompleto (apenas 11
  das 26 capitais reportaram até o momento), então comparações anuais usam
  2024 como o ano mais recente com dados completos.

## 📊 Principais conclusões

### Maceió executa bem em Saúde e Administração, mas fica atrás em Educação e Urbanismo

Comparando a Taxa de Execução Financeira (quanto do que foi comprometido em 2024
realmente saiu do caixa) entre Maceió e a média das outras 25 capitais:

| Função | Maceió | Média das demais capitais |
|---|---|---|
| 04 - Administração | 97,85% | 93,69% |
| 10 - Saúde | 97,36% | 94,12% |
| 12 - Educação | 85,52% | 93,15% |
| 15 - Urbanismo | 80,89% | 88,91% |

**Uma leitura possível:** áreas com gastos mais "correntes" (folha de pagamento,
serviços continuados), como Saúde e Administração, tendem a ser pagas com mais
regularidade. Já Educação e Urbanismo costumam concentrar despesas de investimento
e obras, mais suscetíveis a atrasos contratuais, ficando como "restos a pagar" —
dinheiro comprometido, mas não pago no ano. Essa é uma hipótese razoável à luz do
padrão observado, não uma conclusão definitiva comprovada pelos dados.

### Em Saúde, Maceió está entre as melhores capitais do país

Belém lidera a execução em Saúde entre as capitais (99,93%), seguida de perto por
Salvador e Recife. Maceió aparece em 5º lugar (97,36%), à frente de Curitiba,
Aracaju, Rio Branco, Porto Velho e Teresina. Cuiabá tem a menor taxa de execução
em Saúde entre as 26 capitais (85,32%).

### Sobre os dados de 2025

Até o momento, apenas 11 das 26 capitais entregaram seus dados de 2025 (Belo
Horizonte, Belém, Florianópolis, Fortaleza, Goiânia, Manaus, Porto Velho, Rio
Branco, Rio de Janeiro, Salvador e São Luís). Por isso, 2024 foi usado como o ano
principal de comparação — mas entre as capitais que já reportaram, é possível
observar tendências preliminares, sujeitas a mudança conforme mais capitais
completem sua declaração.

## ⚠️ Limitações e observações encontradas

- **1 valor nulo na coluna `Valor`** após o tratamento (de 50.335 linhas totais,
  cerca de 0,002% da base) — não impacta as conclusões, mas é registrado aqui
  por transparência.
- Durante a validação, uma execução fora de ordem do pipeline (rodar a
  validação antes de atualizar o script de tratamento) gerou uma contagem
  temporária incorreta de 27 capitais em 2020. Após rodar o pipeline completo
  na ordem correta, a contagem foi confirmada em 26 capitais por ano (exceto
  2025, incompleto) — um lembrete de como pipelines dependentes exigem
  execução sequencial completa antes de qualquer validação final.

## 💬 Esclarecimentos obtidos com o recrutador (grupo do WhatsApp)

- A organização dos dados é anual; não há necessidade de validar estrutura por mês.
- Para comparações entre anos, 2024 é a referência mais completa; 2025 está
  parcial, mas ainda assim é possível (e desejável) extrair conclusões sobre
  as capitais que já reportaram.
- O resultado final deve priorizar clareza para um público não-técnico, com
  visualizações e conclusões em linguagem acessível.
