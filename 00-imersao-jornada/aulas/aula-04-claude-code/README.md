# Dia 4: Claude Code & Python | Jornada de Dados

Ultimo dia da imersao. Os dados estao prontos no banco. Agora o desafio e diferente: **como levar esses insights ate quem toma decisao?**

---

## A Situacao

Nos 3 dias anteriores voce construiu um pipeline completo:

| Dia | O que fez | Resultado |
| --- | --------- | --------- |
| Dia 1 - SQL | Entendeu o negocio com queries | Perguntas de negocio respondidas |
| Dia 2 - Python | Ingeriu dados de multiplas fontes | Dados no banco PostgreSQL |
| Dia 3 - dbt | Estruturou camadas Bronze/Silver/Gold | 3 Data Marts prontos para consumo |

O pipeline funciona. Os 3 Data Marts estao no banco:

```
public_gold_sales.vendas_temporais        --> Metricas de vendas por dia/hora
public_gold_cs.clientes_segmentacao       --> Segmentacao VIP/TOP_TIER/REGULAR
public_gold_pricing.precos_competitividade --> Posicionamento vs concorrencia
```

**Mas nenhum diretor acessa o banco de dados.**

---

## O Problema Real

Tres diretores precisam de dados todos os dias. Cada um tem uma dor diferente:

### Diretor Comercial (Vendas)

> "Preciso ver a receita de ontem antes da reuniao das 9h.
> Quero saber se estamos acima ou abaixo da meta.
> Quero ver o ticket medio e quais dias da semana vendem mais."

**Dado que ele precisa:** `vendas_temporais`
**Como ele consome hoje:** Pede pro analista. Demora 2 dias.

### Diretora de Customer Success (Clientes)

> "Preciso saber quantos clientes VIP temos e quanto eles representam.
> Quero ver quem esta comprando menos para ligar antes que cancele.
> Preciso da distribuicao por estado para planejar a equipe regional."

**Dado que ela precisa:** `clientes_segmentacao`
**Como ela consome hoje:** Recebe uma planilha por email. Toda segunda-feira. Ja desatualizada.

### Diretor de Pricing (Precos)

> "Preciso saber quantos produtos estao mais caros que a concorrencia.
> Quero ver quais categorias estao fora do mercado.
> Preciso de alerta quando um produto fica mais caro que todos os concorrentes."

**Dado que ele precisa:** `precos_competitividade`
**Como ele consome hoje:** Nao consome. Ninguem faz essa analise.

---

## A Solucao: 2 Projetos em 30 Minutos

Voce vai usar **Claude Code + Python** para resolver os 3 diretores de uma vez:

```
Projeto 1: Dashboard Streamlit    --> Self-service para os 3 diretores
Projeto 2: Agente de Relatorios   --> Envia insights no email/Slack as 8h da manha
```

### Por que Claude Code?

Claude Code e uma ferramenta de desenvolvimento assistido por IA que:

- Gera codigo Python funcional a partir de instrucoes em linguagem natural
- Le documentacao tecnica (como o `database.md`) para entender o contexto
- Conecta com bancos de dados e cria visualizacoes automaticamente
- Permite iterar rapidamente: "mude o grafico para barras horizontais"

**A ideia:** Voce nao precisa saber Streamlit ou a API do Claude de cor. Voce precisa saber **o que perguntar** e **validar o resultado**. O Claude Code faz o trabalho pesado.

---

## Estrutura do Projeto

```
aula-04-claude-code/
├── README.md                    # Este arquivo
├── database.md                  # Catalogo completo dos 3 Data Marts (contexto para o Claude Code)
├── prd-dashboard.md             # PRD do Case 1: Dashboard
├── prd-agente-relatorios.md     # PRD do Case 2: Agente de Relatorios
├── case-01-dashboard/           # Codigo gerado pelo Claude Code
│   ├── app.py                   # App Streamlit
│   ├── requirements.txt
│   └── .env.example
└── case-02-agente/              # Codigo gerado pelo Claude Code
    ├── agente.py                # Script do agente
    ├── requirements.txt
    └── .env.example
```

---

## O Papel do database.md

O arquivo `database.md` e o **contexto tecnico** que voce entrega para o Claude Code antes de pedir qualquer coisa. Ele contem:

- Schema completo das 3 tabelas gold (colunas, tipos, descricoes)
- Regras de negocio (segmentacao VIP, classificacao de preco)
- Sample data real
- Queries SQL prontas
- Perguntas de negocio que cada tabela responde

**Sem esse arquivo, o Claude Code nao sabe o que existe no banco.**
**Com esse arquivo, ele gera dashboards e agentes que fazem sentido.**

---

## Passo a Passo

### Preparacao (5 minutos)

1. Ter o Claude Code instalado (CLI)
2. Ter o banco Supabase rodando com os 3 Data Marts da aula-03
3. Ter as credenciais do banco (host, user, password)
4. Ter uma chave de API da Anthropic (para o Case 2)

### Case 1: Dashboard (15 minutos)

**Objetivo:** Dashboard Streamlit com 3 paginas (1 por diretor) conectado ao banco.

1. Abra o Claude Code no terminal
2. Passe o `database.md` como contexto
3. Passe o `prd-dashboard.md` como instrucao
4. Valide o resultado
5. Rode o dashboard localmente

```bash
# Depois do Claude Code gerar os arquivos:
cd case-01-dashboard
pip install -r requirements.txt
streamlit run app.py
```

**Entrega:** Dashboard rodando em `localhost:8501` com os dados reais do banco.

### Case 2: Agente de Relatorios (10 minutos)

**Objetivo:** Script Python que gera relatorio diario e pode ser agendado para rodar as 8h.

1. Abra o Claude Code no terminal
2. Passe o `database.md` como contexto
3. Passe o `prd-agente-relatorios.md` como instrucao
4. Valide o resultado
5. Teste o agente manualmente

```bash
# Depois do Claude Code gerar os arquivos:
cd case-02-agente
pip install -r requirements.txt
python agente.py
```

**Entrega:** Relatorio gerado no terminal/arquivo com insights dos 3 diretores.

---

## Conceitos que Voce Aprende

### 1. Prompt Engineering para Codigo

Voce nao escreve codigo do zero. Voce escreve **instrucoes claras** para o Claude Code:

**Instrucao ruim:**
```
Faz um dashboard de vendas.
```

**Instrucao boa:**
```
Crie um dashboard Streamlit com 3 paginas.
Pagina 1 (Vendas): conecte na tabela public_gold_sales.vendas_temporais,
mostre receita total por mes em grafico de linha e ticket medio por dia da semana
em grafico de barras.
Use o database.md como referencia das colunas e tipos.
```

A diferenca e **contexto** e **especificidade**. O PRD faz esse papel.

### 2. Documentacao como Interface

O `database.md` nao e documentacao para humanos lerem uma vez e esquecerem. E uma **interface tecnica** entre o banco de dados e o agente de IA. Quanto melhor a documentacao, melhor o resultado.

### 3. Data Products

Dashboard e agente de relatorios sao **produtos de dados**. O pipeline (SQL + Python + dbt) so tem valor quando alguem consome o resultado. Hoje voce fecha o ciclo:

```
Dados Brutos --> Pipeline --> Data Marts --> Produtos de Dados --> Decisao
   Dia 2         Dia 3        Dia 3            Dia 4              ✓
```

---

## Resultado Final da Imersao

Ao final dos 4 dias, voce construiu:

| Camada | Ferramenta | Entrega |
| ------ | ---------- | ------- |
| Analise | SQL | 21 queries respondendo perguntas de negocio |
| Ingestao | Python | Scripts que coletam dados de CSVs, APIs e bancos |
| Transformacao | dbt | 11 modelos em arquitetura Medalhao (Bronze/Silver/Gold) |
| Consumo | Claude Code + Python | Dashboard + Agente de Relatorios para 3 diretores |

**Isso e um projeto de dados completo. Do dado bruto ate a decisao.**
