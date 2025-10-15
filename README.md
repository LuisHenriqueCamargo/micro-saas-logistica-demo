# 🚚 Micro-SaaS Logístico — Plataforma de Inteligência Operacional e Estratégica

Este projeto é uma **plataforma de análise logística avançada** desenvolvida em Python, com foco em **monitoramento operacional, otimização de custos e suporte à tomada de decisão estratégica**.  

Construído com [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/python/) e [TinyDB](https://tinydb.readthedocs.io/), o dashboard entrega **insights em tempo real**, integra dados operacionais e fornece **indicadores logísticos críticos** para gestão de transporte, armazenagem e distribuição.

🔗 **Demo pública:**  
[https://micro-saas-logistica-demo-emhmpvqmxwadso3jmm7bb3.streamlit.app/](https://micro-saas-logistica-demo-emhmpvqmxwadso3jmm7bb3.streamlit.app/)

---

## 🧭 Visão Estratégica

Organizações logísticas modernas exigem **alta visibilidade operacional**, **resposta ágil** e **planejamento baseado em dados**.  
Esta solução foi desenhada para fornecer:

- Monitoramento em tempo real de KPIs logísticos.  
- Identificação de gargalos em rotas, SLAs e transportadoras.  
- Redução de custos operacionais via análise comparativa e preditiva.  
- Base escalável para integração com ERPs, TMS e torres de controle.

---

## 📊 Indicadores Logísticos (KPIs)

A plataforma monitora e calcula KPIs logísticos críticos, que são amplamente utilizados por empresas de nível enterprise.

### 🟢 OTIF (On Time In Full)
- **Definição:** Percentual de entregas realizadas no prazo acordado e com pedido completo.  
- **Fórmula:**  
  \[
  OTIF = \frac{\text{Entregas no prazo e completas}}{\text{Total de entregas}} \times 100
  \]
- **Impacto:** Alta confiabilidade operacional, redução de falhas e maior satisfação do cliente.

### 🕒 Lead Time
- **Definição:** Tempo total entre a emissão do pedido e a entrega final.  
- **Cálculo:** Data/Hora de entrega – Data/Hora de emissão.  
- **Impacto:** Lead Times curtos reduzem capital empatado em estoque e aumentam a eficiência da cadeia.

### ⏳ SLA (Service Level Agreement)
- **Definição:** Percentual de entregas realizadas dentro do prazo contratual acordado com clientes ou transportadoras.  
- **Impacto:** Reflete a aderência operacional ao planejamento e contratos logísticos.

📌 *Esses indicadores são disponibilizados em tempo real e podem ser exportados para camadas analíticas externas (Power BI, Tableau ou Data Lake).*

---

## ⚙️ Funcionalidades Principais

- 📦 **Análise financeira e operacional** por filial, cliente, rota e transportadora.  
- 🧭 **Monitoramento de SLA, OTIF e Lead Time** com visualização executiva.  
- 📈 **Evolução temporal** de fretes e KPIs estratégicos.  
- 🏆 Ranking **Top 10 CT-es** com maior impacto financeiro.  
- 📊 Gráficos interativos com filtros dinâmicos (filial, cliente, transportadora etc.).  
- 📤 Exportação de dados para **CSV, Excel, Power BI e PDF**.  
- 🌐 Camada de **API REST (FastAPI)** para integração com sistemas externos (TMS, ERP, WMS).  
- 🔐 Execução local, com base em TinyDB, sem dependências externas.  
- 🧭 Pronto para expansão para Data Lakes ou bancos relacionais.

---

## 🧠 Arquitetura de Dados

A solução foi projetada com **arquitetura modular**, permitindo escalabilidade e integração com pipelines de dados corporativos. 


### ✨ Características da arquitetura:
- **Storage local leve:** TinyDB em JSON — ideal para MVPs e PoCs.  
- **Camada de transformação desacoplada:** Pandas processa KPIs e métricas.  
- **Visualização responsiva:** Gráficos interativos e filtros dinâmicos.  
- **Extensibilidade:** Fácil substituição do TinyDB por bancos SQL ou Data Lake.  
- **API REST nativa:** Suporte para GET/POST, integrando dados externos de pedidos, SLA e frete.

---

## 🧩 Camada de API — Integrações Corporativas

A solução conta com **endpoint de API REST** construído em [FastAPI](https://fastapi.tiangolo.com/), permitindo:

- 📥 Ingestão automática de dados de sistemas TMS, WMS ou ERPs.  
- 📤 Exposição dos indicadores (SLA, OTIF, Lead Time) para Data Warehouses ou plataformas analíticas.  
- 🔐 Suporte para autenticação via token e integração segura.

### 📌 Exemplo de endpoint:

```python
from fastapi import FastAPI
from tinydb import TinyDB

app = FastAPI()
db = TinyDB("rotas.json")

@app.get("/indicadores")
def get_indicadores():
    # Exemplo de retorno simplificado
    return {
        "OTIF": 97.2,
        "LeadTimeMedio": "2.4 dias",
        "SLA": 95.1
    }

| Categoria        | Ferramenta / Tecnologia              |
| ---------------- | ------------------------------------ |
| Linguagem        | Python 3.11+                         |
| Visualização     | Streamlit, Plotly                    |
| Processamento    | Pandas                               |
| Banco de Dados   | TinyDB (JSON local)                  |
| API / Integração | FastAPI                              |
| Front-End        | HTML / CSS (tema customizado DAXLOG) |
| Deploy           | Streamlit Cloud                      |

🧭 Cenários de Aplicação

🏭 Operações logísticas complexas: acompanhamento de OTIF/SLA multi-filiais.

🧰 Centros de distribuição: análise de performance de rotas e transportadoras.

📊 Gestão executiva: dashboards para reuniões estratégicas de nível diretoria.

🧭 Integração com ERPs/TMS: ingestão automática de dados de fretes e pedidos.

🌐 Expansão para Data Lake: arquitetura pronta para escalar para cloud (S3, GCS, BigQuery, etc.).

🧱 Estrutura de Pastas 
📁 micro-saas-logistica-demo/
├── api/
│   └── main.py              # API REST FastAPI
├── dashboard.py             # Código principal do dashboard Streamlit
├── dashboard_style.css      # Customização visual (tema DAXLOG)
├── rotas.json               # Base de dados TinyDB (fretes, SLA, rotas)
├── requirements.txt         # Dependências do projeto
└── .streamlit/
    └── config.toml          # Configuração de deploy
