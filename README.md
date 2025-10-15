# 🚚 Micro-SaaS Logístico — Dashboard Estratégico de Performance

Este projeto é um **dashboard interativo e inteligente**, desenvolvido com [Streamlit](https://streamlit.io/) e **focado em análise logística estratégica**.  
Permite **visualizar, comparar e otimizar custos logísticos**, identificando padrões de frete, rotas, filiais, clientes e transportadoras — tudo de forma automatizada e acessível.

🔗 **Demo pública:**  
[https://micro-saas-logistica-demo-emhmpvqmxwadso3jmm7bb3.streamlit.app/](https://micro-saas-logistica-demo-emhmpvqmxwadso3jmm7bb3.streamlit.app/)

---

## 🔍 Funcionalidades Principais

- 📦 Análise de custo mensal por **filial, cliente e transportadora**  
- 📈 Evolução temporal dos **fretes e custos operacionais**  
- 🏆 Ranking dos **Top 10 CT-es de maior impacto financeiro**  
- 📊 **Gráficos interativos** e filtros dinâmicos (filial, cliente, região etc.)  
- 📤 **Exportação de dados filtrados** (CSV, Power BI, Excel ou PDF)  
- 🎨 Interface **visual moderna e personalizável** (CSS customizado)  
- 🔐 **Execução 100% local** via TinyDB — sem dependência de nuvem  

---

## 💡 Benefícios Estratégicos

✅ **Reduza custos por km** com análise automatizada de fretes  
✅ **Otimize negociações** com transportadoras através de dados reais  
✅ **Compare desempenho entre filiais e rotas** em tempo real  
✅ **Melhore a tomada de decisão** com KPIs logísticos centralizados  

---

## 🧠 Aplicações Corporativas

Este projeto pode ser:
- Implantado **localmente** como ferramenta de gestão de fretes  
- Adaptado para **multiusuário** em ambiente cloud  
- Integrado via **API** com ERPs, WMS e TMS  
- Incorporado a **torres de controle logístico (DAXLOG)** para monitoramento centralizado  

---

## ⚙️ Tecnologias Utilizadas

| Categoria | Ferramentas |
|------------|-------------|
| Linguagem | **Python 3.11+** |
| Visualização | **Streamlit**, **Plotly** |
| Banco de Dados | **TinyDB** (banco local em JSON) |
| Processamento | **Pandas** |
| Front-end | **HTML / CSS (customização visual)** |

---

## 🗂️ Estrutura do Projeto

```bash
📁 micro-saas-logistica-demo/
├── dashboard.py             → Código principal (lógica e interface Streamlit)
├── dashboard_style.css      → Customização visual (tema azul DAXLOG)
├── rotas.json               → Banco de dados TinyDB (dados de rotas e fretes)
└── .streamlit/
    └── config.toml          → Configuração de deploy no Streamlit Cloud

