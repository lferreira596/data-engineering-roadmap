# PRD - Case 2: Agente de Relatorios Diarios

## Contexto

Script Python que conecta no banco PostgreSQL (Supabase), consulta os 3 Data Marts gold, usa a API do Claude para interpretar os dados e gera um relatorio diario com insights acionaveis para cada diretor. O relatorio e gerado automaticamente e pode ser agendado para rodar as 8h da manha.

**Banco:** PostgreSQL (Supabase)
**LLM:** Claude (Anthropic API)
**Referencia tecnica:** Ler o arquivo `database.md` para schemas completos, colunas, tipos e regras de negocio.

---

## Arquitetura

```
Supabase (PostgreSQL)
    │
    ├── public_gold_sales.vendas_temporais
    ├── public_gold_cs.clientes_segmentacao
    └── public_gold_pricing.precos_competitividade
            │
            ▼
    agente.py (Python)
    │
    ├── 1. Conecta no banco
    ├── 2. Executa queries de cada Data Mart
    ├── 3. Monta contexto com os dados
    ├── 4. Envia para Claude API com prompt estruturado
    └── 5. Retorna relatorio formatado
            │
            ▼
    Saida: relatorio no terminal + arquivo .md
```

**Stack:**
- Python 3.10+
- anthropic (SDK da Anthropic)
- psycopg2-binary (conexao PostgreSQL)
- pandas
- python-dotenv (variaveis de ambiente)
- schedule (agendamento - opcional)

---

## Conexao

Usar variaveis de ambiente via `.env`:

```
SUPABASE_HOST=seu-host.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=seu-usuario
SUPABASE_PASSWORD=sua-senha
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Fluxo do Agente

### Etapa 1: Extrair dados do banco

Executar 3 queries, uma para cada Data Mart. Cada query retorna um DataFrame do pandas.

**Query 1 - Resumo de Vendas:**

```sql
SELECT
    data_venda,
    dia_semana_nome,
    SUM(receita_total) AS receita,
    SUM(total_vendas) AS vendas,
    SUM(total_clientes_unicos) AS clientes,
    AVG(ticket_medio) AS ticket_medio
FROM public_gold_sales.vendas_temporais
GROUP BY data_venda, dia_semana_nome
ORDER BY data_venda DESC
LIMIT 7
```

Objetivo: ultimos 7 dias de vendas para analise de tendencia.

**Query 2 - Segmentacao de Clientes:**

```sql
SELECT
    segmento_cliente,
    COUNT(*) AS total_clientes,
    SUM(receita_total) AS receita_total,
    AVG(ticket_medio) AS ticket_medio_avg,
    AVG(total_compras) AS compras_avg
FROM public_gold_cs.clientes_segmentacao
GROUP BY segmento_cliente
ORDER BY receita_total DESC
```

Objetivo: visao consolidada por segmento.

**Query 3 - Alertas de Pricing:**

```sql
SELECT
    classificacao_preco,
    COUNT(*) AS total_produtos,
    AVG(diferenca_percentual_vs_media) AS dif_media_pct,
    SUM(receita_total) AS receita_impactada
FROM public_gold_pricing.precos_competitividade
GROUP BY classificacao_preco
ORDER BY total_produtos DESC
```

**Query 4 - Produtos Criticos (detalhamento):**

```sql
SELECT
    nome_produto,
    categoria,
    nosso_preco,
    preco_medio_concorrentes,
    diferenca_percentual_vs_media,
    receita_total
FROM public_gold_pricing.precos_competitividade
WHERE classificacao_preco = 'MAIS_CARO_QUE_TODOS'
ORDER BY diferenca_percentual_vs_media DESC
LIMIT 10
```

Objetivo: lista dos produtos mais criticos para acao imediata.

### Etapa 2: Montar o prompt para o Claude

Criar um prompt estruturado com os dados reais. O prompt deve conter:

**System prompt:**

```
Voce e um analista de dados senior de um e-commerce.
Sua funcao e gerar um relatorio executivo diario para 3 diretores.
Cada diretor tem necessidades diferentes:

1. Diretor Comercial: quer saber sobre receita, vendas, ticket medio e tendencias.
2. Diretora de Customer Success: quer saber sobre segmentacao de clientes, VIPs e riscos.
3. Diretor de Pricing: quer saber sobre posicionamento de preco vs concorrencia e alertas.

Regras do relatorio:
- Seja direto e acionavel. Cada insight deve sugerir uma acao.
- Use numeros reais dos dados fornecidos.
- Formate valores monetarios em reais (R$).
- Destaque alertas criticos no inicio.
- O relatorio deve ter no maximo 1 pagina por diretor.
- Use formato Markdown.
```

**User prompt (template):**

```
Gere o relatorio diario com base nos dados abaixo.

## Dados de Vendas (ultimos 7 dias)
{dados_vendas_formatados}

## Segmentacao de Clientes
{dados_clientes_formatados}

## Posicionamento de Precos
{dados_pricing_formatados}

## Produtos Criticos (mais caros que todos os concorrentes)
{dados_produtos_criticos_formatados}

Gere o relatorio com 3 secoes:
1. Comercial (para o Diretor Comercial)
2. Customer Success (para a Diretora de CS)
3. Pricing (para o Diretor de Pricing)

Comece com um resumo executivo de 3 linhas antes das secoes.
```

Os dados devem ser formatados como tabelas ou listas legíveis. Usar `DataFrame.to_string()` ou `DataFrame.to_markdown()`.

### Etapa 3: Chamar a API do Claude

```python
import anthropic

client = anthropic.Anthropic()  # usa ANTHROPIC_API_KEY do ambiente

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_prompt}
    ]
)

relatorio = message.content[0].text
```

### Etapa 4: Salvar e exibir

1. Imprimir o relatorio no terminal
2. Salvar como arquivo `.md` com data no nome: `relatorio_2026-03-12.md`
3. Imprimir caminho do arquivo salvo

---

## Agendamento (Opcional)

Para rodar automaticamente as 8h da manha, adicionar ao final do script:

**Opcao 1 - Cron (Linux/Mac):**

```bash
# Abrir crontab
crontab -e

# Adicionar linha (ajustar caminhos):
0 8 * * * cd /caminho/para/case-02-agente && /caminho/para/python agente.py >> /tmp/agente.log 2>&1
```

**Opcao 2 - schedule (Python):**

```python
import schedule
import time

schedule.every().day.at("08:00").do(gerar_relatorio)

while True:
    schedule.run_pending()
    time.sleep(60)
```

A opcao do cron e preferivel para producao. A opcao schedule e boa para demonstracao.

---

## Exemplo de Saida Esperada

```markdown
# Relatorio Diario - E-commerce
Data: 12/03/2026

## Resumo Executivo
- Receita dos ultimos 7 dias: R$ 45.230,00 (queda de 8% vs semana anterior)
- 10 clientes VIP respondem por 62% da receita total
- 15 produtos estao mais caros que todos os concorrentes

---

## 1. Comercial

### Tendencia de Receita (ultimos 7 dias)
| Data | Dia | Receita | Vendas | Ticket Medio |
| ---- | --- | ------- | ------ | ------------ |
| 12/03 | Quarta | R$ 6.120 | 42 | R$ 145,71 |
| 11/03 | Terca | R$ 7.340 | 55 | R$ 133,45 |
| ... | ... | ... | ... | ... |

### Insights
- Terca foi o melhor dia da semana (+19% vs media)
- Ticket medio caiu 5% nos ultimos 3 dias -- verificar se ha promocoes ativas
- **Acao sugerida:** Revisar campanhas de quarta e quinta, que estao abaixo da media

---

## 2. Customer Success

### Segmentacao Atual
| Segmento | Clientes | Receita | Ticket Medio |
| -------- | -------- | ------- | ------------ |
| VIP | 10 | R$ 267.000 | R$ 420,00 |
| TOP_TIER | 15 | R$ 98.000 | R$ 310,00 |
| REGULAR | 25 | R$ 42.000 | R$ 180,00 |

### Insights
- 20% dos clientes (VIP) geram 65% da receita
- 3 clientes TOP_TIER estao proximos de virar VIP (receita > R$ 9.000)
- **Acao sugerida:** Ligar para os 3 clientes TOP_TIER proximos do upgrade

---

## 3. Pricing

### Posicionamento Geral
| Classificacao | Produtos | Receita Impactada |
| ------------- | -------- | ----------------- |
| Mais caro que todos | 15 | R$ 12.000 |
| Acima da media | 45 | R$ 35.000 |
| Na media | 20 | R$ 18.000 |
| Abaixo da media | 80 | R$ 55.000 |
| Mais barato que todos | 25 | R$ 22.000 |

### Produtos Criticos
- Necessaire (Xiaomi): R$ 1.139,99 vs mercado R$ 980,00 (+16%)
- Condicionador Hidratante (Asus): R$ 451,90 vs mercado R$ 390,00 (+15%)

### Insights
- 15 produtos estao mais caros que TODOS os concorrentes
- Categoria "Acessorios" tem maior diferenca media (+8.5%)
- **Acao sugerida:** Repricing imediato nos 5 produtos com maior diferenca percentual
```

---

## Arquivos a Gerar

| Arquivo | Descricao |
| ------- | --------- |
| `case-02-agente/agente.py` | Script principal do agente |
| `case-02-agente/requirements.txt` | Dependencias Python |
| `case-02-agente/.env.example` | Template das variaveis de ambiente |

---

## Requisitos Nao Funcionais

- **Tratar erros de conexao com o banco**: se o banco estiver fora, exibir mensagem clara e nao chamar a API
- **Tratar erros da API do Claude**: se a API falhar, exibir mensagem e salvar os dados brutos como fallback
- **Logging**: usar `print` com timestamps para cada etapa (conectou, consultou, enviou para API, salvou)
- **Custo**: usar `claude-sonnet-4-20250514` para manter custo baixo (~$0.01 por execucao)

---

## Como Testar

```bash
cd case-02-agente
cp .env.example .env
# Editar .env com credenciais reais
pip install -r requirements.txt
python agente.py
```

O relatorio deve aparecer no terminal e ser salvo como arquivo `.md` no diretorio atual.
