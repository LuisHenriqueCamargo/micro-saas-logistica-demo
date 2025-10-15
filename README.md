🚚 Micro-SaaS Logístico — Motor de Decisão Tática e Otimização de Fretes
Este projeto é um Protótipo de Conceito (POC) que demonstra a arquitetura para uma Torre de Controle Tática. Desenvolvido com Python e Streamlit, seu foco principal é transformar dados brutos de frete em Decisão Prescritiva e Otimização de Custos (OPEX).

Ele atua como um Data Mart leve e um motor de visualização, permitindo a auditoria e o mapeamento de exceções logísticas em tempo real.

🔗 Demo pública: https://micro-saas-logistica-demo-emhmpvqmxwadso3jmm7bb3.streamlit.app/

📈 Entregáveis Estratégicos (Impacto no Negócio)
Este sistema não apenas visualiza, ele permite a ação imediata através de indicadores claros:

✅ Auditoria e Otimização de Custo por KM: Identifica e quantifica desvios de frete por rota, permitindo a redução imediata de custos de transporte.
✅ Visão de Performance Gerencial: Compara o desempenho de Filiais, Clientes e Transportadoras, fornecendo dados concretos para renegociação e melhoria do Nível de Serviço (SLA).
✅ Rastreabilidade de Exceções: Gera o Ranking dos Top 10 CT-es de maior impacto financeiro, permitindo a investigação tática focada onde o prejuízo é maior.
✅ Agilidade na Decisão (POC): Por rodar 100% localmente via TinyDB, demonstra a capacidade de implantar soluções de análise tática com zero latência e baixo custo de infraestrutura (ideal para POCs e MVPs).

🏗️ Arquitetura e Stack Técnica
O projeto utiliza uma micro-arquitetura orientada a dados focada em desempenho e simplicidade para ambientes de POC/MVP.

Categoria

Ferramentas

Foco de Engenharia

Linguagem Core

Python 3.11+

Lógica de processamento e estruturação de dados.

Pipeline & Data Mart

Pandas, TinyDB

Processamento de dados em memória e armazenamento de dados em schema local (JSON).

Visualização & API

Streamlit, Plotly

Front-end interativo com baixa curva de desenvolvimento e alta velocidade de entrega (Rapid Prototyping).

Customização

HTML / CSS

Refinamento da interface para alinhamento com a identidade corporativa (UX/UI).

⚙️ Configuração e Execução Local
Este projeto foi projetado para demonstrar a execução rápida e a lógica do motor de regras.

Pré-requisitos
Certifique-se de ter o Python 3.11+ instalado.

1. Instalação das Dependências
Clone o repositório e instale as bibliotecas necessárias:

git clone [https://github.com/LuisHenriqueCamargo/micro-saas-logistica-demo](https://github.com/LuisHenriqueCamargo/micro-saas-logistica-demo)
cd micro-saas-logistica-demo
pip install -r requirements.txt # (Ou instale manualmente: streamlit, pandas, tinydb, plotly)

2. Execução do Dashboard
Inicie a aplicação via Streamlit:

streamlit run dashboard.py

A aplicação será aberta automaticamente no seu navegador, consumindo os dados do arquivo rotas.json.

🧠 Aplicações Futuras (Visão 5.0)
Esta arquitetura pode ser facilmente escalada e integrada:

Evolução do Data Mart: Migração de TinyDB para PostgreSQL ou AWS RDS para suportar volumes maiores.

Microserviços: Adaptação da lógica do dashboard para uma API Flask dedicada (como a do projeto DAXLOG) para consumo por múltiplos dashboards (Power BI, Metabase, etc.).

Integração: Conexão direta via API REST com sistemas TMS/WMS, eliminando a ingestão manual de arquivos.
