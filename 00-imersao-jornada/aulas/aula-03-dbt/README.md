# Dia 3: dbt & Camada Analitica | Jornada de Dados

Projeto dbt com arquitetura Medalhao (Bronze -> Silver -> Gold) usando PostgreSQL.

**11 modelos** organizados em 3 camadas e 3 Data Marts.

---

## Estrutura do Projeto

```
aula-03-dbt/
├── dbt_project.yml              # Configuracoes centralizadas (materializacao, schemas, variaveis)
├── profiles.yml                 # Conexao com o banco PostgreSQL
├── models/
│   ├── _sources.yml             # Definicao das 4 tabelas raw
│   ├── bronze/                  # 4 views  - Dados brutos
│   │   ├── bronze_vendas.sql
│   │   ├── bronze_clientes.sql
│   │   ├── bronze_produtos.sql
│   │   └── bronze_preco_competidores.sql
│   ├── silver/                  # 4 tables - Colunas calculadas
│   │   ├── silver_vendas.sql
│   │   ├── silver_clientes.sql
│   │   ├── silver_produtos.sql
│   │   └── silver_preco_competidores.sql
│   └── gold/                    # 3 tables - 1 por Data Mart
│       ├── sales/
│       │   └── gold_sales_vendas_temporais.sql
│       ├── customer_success/
│       │   └── gold_customer_success_clientes_segmentacao.sql
│       └── pricing/
│           └── gold_pricing_precos_competitividade.sql
├── macros/
└── tests/
```

---

## Fluxo de Dados

```
RAW (public)                BRONZE (views)                SILVER (tables)                  GOLD (tables)
────────────                ──────────────                ───────────────                  ──────────────

raw.vendas ──────────────► bronze_vendas ──────────────► silver_vendas ──────────────────► gold_sales_vendas_temporais
                                                         (+ receita_total,           │
                                                          dimensoes temporais,        ├──► gold_customer_success_clientes_segmentacao
                                                          preco_venda)                │
                                                                                      └──► gold_pricing_precos_competitividade
                                                                                                ▲
raw.clientes ────────────► bronze_clientes ────────────► silver_clientes ────────────────────────┤
                                                                                                │
raw.produtos ────────────► bronze_produtos ────────────► silver_produtos ────────────────────────┤
                                                         (+ faixa_preco)                        │
                                                                                                │
raw.preco_competidores ──► bronze_preco_competidores ──► silver_preco_competidores ─────────────┘
                                                         (+ data_coleta_date)
```

### Dependencias dos Gold Models

| Gold Model | Silver Models usados |
|-----------|---------------------|
| `gold_sales_vendas_temporais` | `silver_vendas` |
| `gold_customer_success_clientes_segmentacao` | `silver_vendas` + `silver_clientes` |
| `gold_pricing_precos_competitividade` | `silver_produtos` + `silver_preco_competidores` + `silver_vendas` |

---

## Schemas por Camada

### BRONZE - Dados Brutos (4 views)

Copia exata das tabelas raw. Materializado como **view**. Contrato minimo do dado.

#### bronze_vendas

| Coluna | Origem |
|--------|--------|
| id_venda | raw.vendas |
| data_venda | raw.vendas |
| id_cliente | raw.vendas |
| id_produto | raw.vendas |
| canal_venda | raw.vendas |
| quantidade | raw.vendas |
| preco_unitario | raw.vendas |

#### bronze_clientes

| Coluna | Origem |
|--------|--------|
| id_cliente | raw.clientes |
| nome_cliente | raw.clientes |
| estado | raw.clientes |
| pais | raw.clientes |
| data_cadastro | raw.clientes |

#### bronze_produtos

| Coluna | Origem |
|--------|--------|
| id_produto | raw.produtos |
| nome_produto | raw.produtos |
| categoria | raw.produtos |
| marca | raw.produtos |
| preco_atual | raw.produtos |
| data_criacao | raw.produtos |

#### bronze_preco_competidores

| Coluna | Origem |
|--------|--------|
| id_produto | raw.preco_competidores |
| nome_concorrente | raw.preco_competidores |
| preco_concorrente | raw.preco_competidores |
| data_coleta | raw.preco_competidores |

---

### SILVER - Colunas Calculadas (4 tables)

Mesmas colunas do bronze + **novas colunas calculadas**. Materializado como **table**. Sem JOINs.

#### silver_vendas

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id_venda | original | ID da venda |
| id_cliente | original | FK cliente |
| id_produto | original | FK produto |
| quantidade | original | Quantidade vendida |
| **preco_venda** | **renomeado** | preco_unitario renomeado |
| data_venda | original | Data/hora da venda |
| canal_venda | original | Canal de venda |
| **receita_total** | **calculado** | quantidade * preco_unitario |
| **data_venda_date** | **calculado** | DATE(data_venda) |
| **ano_venda** | **calculado** | EXTRACT(YEAR) |
| **mes_venda** | **calculado** | EXTRACT(MONTH) |
| **dia_venda** | **calculado** | EXTRACT(DAY) |
| **dia_semana** | **calculado** | EXTRACT(DOW) - 0=Domingo, 6=Sabado |
| **hora_venda** | **calculado** | EXTRACT(HOUR) |

#### silver_clientes

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id_cliente | original | ID do cliente |
| nome_cliente | original | Nome do cliente |
| estado | original | Estado |
| pais | original | Pais |
| data_cadastro | original | Data de cadastro |

#### silver_produtos

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id_produto | original | ID do produto |
| nome_produto | original | Nome do produto |
| categoria | original | Categoria |
| marca | original | Marca |
| preco_atual | original | Preco atual |
| data_criacao | original | Data de criacao |
| **faixa_preco** | **calculado** | PREMIUM (>1000), MEDIO (>500), BASICO |

#### silver_preco_competidores

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id_produto | original | FK produto |
| nome_concorrente | original | Nome do concorrente |
| preco_concorrente | original | Preco do concorrente |
| data_coleta | original | Data/hora da coleta |
| **data_coleta_date** | **calculado** | DATE(data_coleta) |

---

### GOLD - KPIs (3 tables, 1 por Data Mart)

JOINs entre tabelas silver + agregacoes. Materializado como **table**. Dados prontos para dashboards.

#### gold_sales_vendas_temporais

**Pergunta:** Qual foi minha receita por data?

Metricas de venda agregadas por data/hora. Fonte: `silver_vendas`

| Coluna | Descricao |
|--------|-----------|
| data_venda | Data da venda |
| ano_venda | Ano |
| mes_venda | Mes |
| dia_venda | Dia |
| dia_semana_nome | Domingo, Segunda, ..., Sabado |
| hora_venda | Hora |
| receita_total | SUM(receita_total) |
| quantidade_total | SUM(quantidade) |
| total_vendas | COUNT(DISTINCT id_venda) |
| total_clientes_unicos | COUNT(DISTINCT id_cliente) |
| ticket_medio | AVG(receita_total) |

---

#### gold_customer_success_clientes_segmentacao

**Pergunta:** Quais sao meus melhores clientes?

Segmentacao de clientes por receita. JOIN: `silver_vendas` + `silver_clientes`

| Coluna | Descricao |
|--------|-----------|
| cliente_id | ID do cliente |
| nome_cliente | Nome |
| estado | Estado |
| receita_total | SUM(receita_total) |
| total_compras | COUNT(DISTINCT id_venda) |
| ticket_medio | AVG(receita_total) |
| primeira_compra | MIN(data_venda_date) |
| ultima_compra | MAX(data_venda_date) |
| segmento_cliente | VIP (>=R$10k), TOP_TIER (>=R$5k), REGULAR |
| ranking_receita | ROW_NUMBER por receita |

---

#### gold_pricing_precos_competitividade

**Pergunta:** Como estamos em relacao a concorrencia?

Analise de preco vs concorrentes. JOIN: `silver_produtos` + `silver_preco_competidores` + `silver_vendas`

| Coluna | Descricao |
|--------|-----------|
| produto_id | ID do produto |
| nome_produto | Nome |
| categoria | Categoria |
| marca | Marca |
| nosso_preco | Nosso preco atual |
| preco_medio_concorrentes | AVG dos concorrentes |
| preco_minimo_concorrentes | MIN dos concorrentes |
| preco_maximo_concorrentes | MAX dos concorrentes |
| total_concorrentes | COUNT(DISTINCT concorrente) |
| diferenca_percentual_vs_media | % diferenca vs media |
| diferenca_percentual_vs_minimo | % diferenca vs minimo |
| classificacao_preco | MAIS_CARO_QUE_TODOS / MAIS_BARATO_QUE_TODOS / ACIMA_DA_MEDIA / ABAIXO_DA_MEDIA / NA_MEDIA |
| receita_total | Receita do produto |
| quantidade_total | Quantidade vendida |

---

## Configuracao (dbt_project.yml)

```yaml
models:
  jornada_de_dados:
    bronze:
      +materialized: view       # Views - sempre atualizadas
      +schema: bronze
    silver:
      +materialized: table      # Tables - colunas calculadas persistidas
      +schema: silver
    gold:
      +materialized: table      # Tables - KPIs prontos para consumo
      +schema: gold

vars:
  segmentacao_vip_threshold: 10000    # Receita minima para VIP
  segmentacao_top_tier_threshold: 5000 # Receita minima para TOP_TIER
```

---

## Como Usar

```bash
# Instalar
pip install dbt-core dbt-postgres

# Navegar e testar conexao
cd aulas/aula-03-dbt
dbt debug

# Executar tudo (dbt resolve dependencias)
dbt run

# Executar por camada
dbt run --select tag:bronze
dbt run --select tag:silver
dbt run --select tag:gold

# Executar modelo especifico com suas dependencias
dbt run --select +gold_sales_vendas_temporais

# Documentacao
dbt docs generate
dbt docs serve
```

---

## Resumo da Arquitetura

| Camada | Modelos | Materializacao | O que faz |
|--------|---------|----------------|-----------|
| **Bronze** | 4 | view | Copia exata do raw (contrato do dado) |
| **Silver** | 4 | table | Colunas calculadas (receita_total, faixa_preco, dimensoes temporais) |
| **Gold** | 3 | table | JOINs + agregacoes (1 KPI por Data Mart) |
