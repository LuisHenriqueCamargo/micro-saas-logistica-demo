import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- CONFIGURAÇÃO INICIAL (Streamlit) ---
st.set_page_config(
    page_title="Torre de Controle Logístico Executiva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CORES E CONSTANTES DO TEMA EXECUTIVO C3 ---
# Cores
BG_DARK = "#0e1117"       # Fundo principal
BG_CARD = "#1f2229"       # Fundo dos cards/componentes
C3_BLUE = "#3b82f6"       # Azul principal (Ênfase)
C3_RED = "#ef4444"        # Vermelho (Atenção/Alerta)
TEXT_COLOR = "#e5e7eb"    # Cor do texto
GRAY_BORDER = "#374151"   # Cor da borda
C3_GREEN = "#10b981"      # Verde para delta positivo

# --- DADOS MOCKUP (ATUALIZADO COM OTIF E LEAD TIME) ---
@st.cache_data
def load_and_process_data():
    """Carrega dados mockup em um DataFrame e calcula métricas derivadas."""
    np.random.seed(42)
    
    # Criando mais meses e diversidade de dados para gráficos de linha e barras mais robustos
    dates = pd.date_range(start='2024-01-01', periods=10 * 30, freq='D')
    
    data = []
    transportadoras = ['TransRápida', 'JLLog', 'CargaTotal', 'ExpressoDelta', 'Parceiro Z']
    filiais = ['Filial SP (Leste)', 'Filial PR (Sul)', 'Filial MT (Oeste)']
    clientes = ['Alpha Corp', 'Beta Comércio', 'Gamma Indústria', 'Delta Serviços', 'Epsilon Tech']
    regioes = ['Sudeste', 'Sul', 'Centro-Oeste', 'Nordeste']

    for date in dates:
        for _ in range(np.random.randint(1, 6)): # 1 a 5 CT-es por dia
            frete = np.random.uniform(150, 4500)
            distancia = np.random.uniform(50, 2500)
            peso = np.random.uniform(100, 15000) # Peso da carga em KG
            capacidade = peso * np.random.uniform(1.1, 2.5) # Capacidade do veículo (Sempre maior que o peso)
            
            # NOVOS DADOS DE QUALIDADE E PRAZO
            otif_status = np.random.choice([True, False], p=[0.85, 0.15]) # 85% de sucesso baseline
            lead_time = np.random.uniform(2, 15) # Lead time em dias (2 a 15 dias)
            
            data.append({
                'cte_numero': f'CTE{date.strftime("%y%m%d")}{np.random.randint(100, 999)}', 
                'frete_valor': frete, 
                'distancia_km': distancia, 
                'data_hora': date, 
                'peso_kg': peso, 
                'capacidade_kg': capacidade, 
                'id_filial_nome': np.random.choice(filiais), 
                'id_transportadora_nome': np.random.choice(transportadoras), 
                'id_cliente_nome': np.random.choice(clientes), 
                'id_regiao_nome': np.random.choice(regioes),
                'otif_status': otif_status, # NOVO: Status OTIF da entrega
                'lead_time_dias': lead_time, # NOVO: Lead Time em dias
            })

    df = pd.DataFrame(data)
    df['mes_ano'] = df['data_hora'].dt.to_period('M').astype(str)
    # Custo/KM (Frete / Distância)
    df['custo_km'] = df.apply(lambda row: row['frete_valor'] / row['distancia_km'] if row['distancia_km'] > 0 else 0, axis=1)
    # Custo/KG (Frete / Peso)
    df['custo_unitario_peso'] = df.apply(lambda row: row['frete_valor'] / row['peso_kg'] if row['peso_kg'] > 0 else 0, axis=1)
    # Custo mensal estimado (para fins de ranking e peso)
    df['custo_mensal'] = df['frete_valor'] * np.random.uniform(1, 4) 
    return df

df_base = load_and_process_data()

# --- FUNÇÕES DE FORMATAÇÃO (ATUALIZADO) ---
def format_currency(value):
    """Formata valor para padrão monetário Brasileiro (R$)."""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_custo_km(value):
    """Formata custo/km com 4 casas decimais."""
    return f"{value:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_number(value):
    """Formata número inteiro com separador de milhares."""
    return f"{value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(value):
    """Formata valor para percentual."""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_weight(value):
    """Formata peso em toneladas (T) ou KG."""
    if value >= 1000:
        # Exibe em toneladas se for maior que 1T, senão em KG
        return f"{value / 1000:,.2f} T".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,.0f} KG".replace(",", "X").replace(".", ",").replace("X", ".")


# --- INJEÇÃO DE CSS/TAILWIND E ESTRUTURA GLOBAL (MANTIDO) ---
st.markdown(
    f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Configurações Globais */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
        
        body {{
            background-color: {BG_DARK};
            color: {TEXT_COLOR};
            font-family: 'Inter', sans-serif;
        }}
        
        /* Ajuste do Streamlit: remove margens e padding padrão para o HTML/Tailwind dominar */
        .stApp {{
            background-color: {BG_DARK};
            color: {TEXT_COLOR};
        }}
        .block-container {{
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        
        /* Estilo para os cards Plotly para integrar ao tema */
        [data-testid="stPlotlyChart"] > div {{
            height: 100% !important; 
            width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        .plotly-graph-div {{
            border-radius: 0.75rem; /* rounded-xl */
            border: 1px solid {GRAY_BORDER};
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            background-color: {BG_CARD};
            min-height: 400px; /* Altura padrão mínima */
        }}
        
        /* Oculta o menu e footer do Streamlit para um visual mais limpo */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* AJUSTE PARA O WIDGET st.metric: Garante o fundo do KPI escuro */
        [data-testid="stMetric"] {{
            background-color: {BG_CARD};
            padding: 1rem;
            border-radius: 0.75rem; /* rounded-xl */
            border-left: 5px solid {C3_BLUE}; /* Barra lateral azul */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            height: 100%; /* Garante que todos tenham a mesma altura */
        }}
        
        /* Ajusta o valor principal para ser branco */
        [data-testid="stMetricValue"] {{
            color: {TEXT_COLOR};
            font-size: 1.875rem; /* text-3xl */
            font-weight: 700; /* font-bold */
        }}
        
        /* Ajusta a label do KPI */
        [data-testid="stMetricLabel"] {{
            color: #9ca3af; /* text-gray-400 */
            font-size: 0.875rem; /* text-sm */
            font-weight: 500; /* font-medium */
            text-transform: uppercase;
        }}
        
        /* Ajusta a cor do delta (opcional, pois o Streamlit já gerencia as cores) */
        [data-testid="stMetricDelta"] {{
            font-size: 0.875rem !important; /* text-sm */
            font-weight: 600 !important; /* font-semibold */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR E FILTROS (MANTIDO) ---
st.sidebar.markdown(f'<h2 style="color:{C3_BLUE}; font-size:1.4em;">⚙️ PARÂMETROS DE SEGMENTAÇÃO</h2>', unsafe_allow_html=True)
st.sidebar.markdown('Aplique filtros para análise estratégica de regiões, clientes e parceiros logísticos.')

filiais = df_base['id_filial_nome'].unique()
transportadoras = df_base['id_transportadora_nome'].unique()
clientes = df_base['id_cliente_nome'].unique()
regioes = df_base['id_regiao_nome'].unique()

# Controles de Filtro
selected_filiais = st.sidebar.multiselect('Unidade de Origem (Filial)', filiais, default=filiais)
selected_transportadoras = st.sidebar.multiselect('Parceiro Logístico', transportadoras, default=transportadoras)
selected_clientes = st.sidebar.multiselect('Cliente Faturador', clientes, default=clientes)
selected_regioes = st.sidebar.multiselect('Região de Destino', regioes, default=regioes)

# Filtro de Tempo (usaremos o mês mais recente como padrão)
meses_disponiveis = sorted(df_base['mes_ano'].unique(), reverse=True)
selected_mes = st.selectbox('Período de Análise (Mês/Ano)', meses_disponiveis, index=0)

# --- APLICAÇÃO DOS FILTROS ---
df_filtered_time = df_base[df_base['mes_ano'] == selected_mes]
df_filtered = df_filtered_time[
    df_filtered_time['id_filial_nome'].isin(selected_filiais) &
    df_filtered_time['id_transportadora_nome'].isin(selected_transportadoras) &
    df_filtered_time['id_cliente_nome'].isin(selected_clientes) &
    df_filtered_time['id_regiao_nome'].isin(selected_regioes)
]

if df_filtered.empty:
    st.error(f'⚠️ ALERTA DE DADOS: Nenhum registro de CTe corresponde aos critérios de filtro aplicados para o mês **{selected_mes}**. Por favor, revise os parâmetros de segmentação.')
    st.stop()


# --- CÁLCULOS DE KPIS (ATUALIZADO COM OS NOVOS KPIS) ---
total_frete = df_filtered['frete_valor'].sum()
total_km = df_filtered['distancia_km'].sum()
num_ctes = len(df_filtered)

# Base KPIs
custo_medio_km = total_frete / total_km if total_km > 0 else 0
custo_medio_cte = total_frete / num_ctes if num_ctes > 0 else 0
total_peso = df_filtered['peso_kg'].sum()
total_capacidade = df_filtered['capacidade_kg'].sum()
peso_medio_transportado = total_peso / num_ctes if num_ctes > 0 else 0
taxa_ocupacao_media = (total_peso / total_capacidade) * 100 if total_capacidade > 0 else 0
custo_medio_kg = df_filtered['custo_unitario_peso'].mean() if num_ctes > 0 else 0 

# NOVOS KPIS DE QUALIDADE E PRAZO (OTIF, SLA, Lead Time)
otif_total = df_filtered['otif_status'].sum()
otif_percentual = (otif_total / num_ctes) * 100 if num_ctes > 0 else 0
sla_meta = 96.0 # 96% fixo conforme pedido
lead_time_medio = df_filtered['lead_time_dias'].mean() if num_ctes > 0 else 0


# Cálculo do Mês Anterior para Delta (ATUALIZADO PARA INCLUIR NOVOS CAMPOS)
mes_atual_index = meses_disponiveis.index(selected_mes)
if mes_atual_index < len(meses_disponiveis) - 1:
    mes_anterior = meses_disponiveis[mes_atual_index + 1]
    df_anterior = df_base[df_base['mes_ano'] == mes_anterior]
    
    # Filtra dados do mês anterior com base nos mesmos filtros de dimensão
    df_anterior_filtered = df_anterior[
        df_anterior['id_filial_nome'].isin(selected_filiais) &
        df_anterior['id_transportadora_nome'].isin(selected_transportadoras) &
        df_anterior['id_cliente_nome'].isin(selected_clientes) &
        df_anterior['id_regiao_nome'].isin(selected_regioes)
    ]
    
    # Valores do Mês Anterior (Existentes)
    total_frete_ant = df_anterior_filtered['frete_valor'].sum()
    total_km_ant = df_anterior_filtered['distancia_km'].sum()
    num_ctes_ant = len(df_anterior_filtered)
    custo_medio_km_ant = total_frete_ant / total_km_ant if total_km_ant > 0 else 0
    total_peso_ant = df_anterior_filtered['peso_kg'].sum()
    total_capacidade_ant = df_anterior_filtered['capacidade_kg'].sum()
    custo_medio_cte_ant = total_frete_ant / num_ctes_ant if num_ctes_ant > 0 else 0
    peso_medio_transportado_ant = total_peso_ant / num_ctes_ant if num_ctes_ant > 0 else 0
    taxa_ocupacao_media_ant = (total_peso_ant / total_capacidade_ant) * 100 if total_capacidade_ant > 0 else 0
    custo_medio_kg_ant = df_anterior_filtered['custo_unitario_peso'].mean() if num_ctes_ant > 0 else 0

    # Valores do Mês Anterior (Novos KPIS)
    otif_total_ant = df_anterior_filtered['otif_status'].sum()
    otif_percentual_ant = (otif_total_ant / num_ctes_ant) * 100 if num_ctes_ant > 0 else 0
    lead_time_medio_ant = df_anterior_filtered['lead_time_dias'].mean() if num_ctes_ant > 0 else 0


else:
    # Simulação para o primeiro mês (sem histórico)
    total_frete_ant = total_frete * 0.95 
    total_km_ant = total_km * 1.05 
    num_ctes_ant = int(num_ctes * 1.02)
    custo_medio_km_ant = custo_medio_km * 1.1 
    total_peso_ant = total_peso * 0.90
    total_capacidade_ant = total_capacidade * 1.10
    custo_medio_cte_ant = custo_medio_cte * 1.05
    custo_medio_kg_ant = custo_medio_kg * 1.15
    # Simulação para os novos KPIS
    otif_percentual_ant = otif_percentual * 0.95 
    lead_time_medio_ant = lead_time_medio * 1.15 

# --- CÁLCULO DOS DELTAS DE VARIAÇÃO (%) (ATUALIZADO PARA INCLUIR NOVOS KPIS) ---
def calculate_delta(current, previous, inverse=False):
    """Calcula delta percentual e define o tipo de cor."""
    if previous == 0:
        return 0, 'off' 
    delta_abs = (current - previous)
    delta_percent = (delta_abs / previous) * 100
    
    # Se inverse=True, um valor POSITIVO (aumento) é ruim (inverse) e NEGATIVO (queda) é bom (normal)
    delta_color = "inverse" if inverse else "normal"
    
    return delta_percent, delta_color

# KPIS EXISTENTES
delta_percentual_frete, delta_type_frete = calculate_delta(total_frete, total_frete_ant, inverse=True)
delta_percentual_km, delta_type_km = calculate_delta(total_km, total_km_ant, inverse=False)
delta_percentual_custo_km, delta_type_custo_km = calculate_delta(custo_medio_km, custo_medio_km_ant, inverse=True)
delta_percentual_ctes, delta_type_ctes = calculate_delta(num_ctes, num_ctes_ant, inverse=False)
delta_percentual_pmt, delta_type_pmt = calculate_delta(peso_medio_transportado, peso_medio_transportado_ant, inverse=False)
delta_percentual_tom, delta_type_tom = calculate_delta(taxa_ocupacao_media, taxa_ocupacao_media_ant, inverse=False)
delta_percentual_cmc, delta_type_cmc = calculate_delta(custo_medio_cte, custo_medio_cte_ant, inverse=True)
delta_percentual_custo_kg, delta_type_custo_kg = calculate_delta(custo_medio_kg, custo_medio_kg_ant, inverse=True)

# NOVOS KPIS
# 9. OTIF (%)
delta_percentual_otif, delta_type_otif = calculate_delta(otif_percentual, otif_percentual_ant, inverse=False) # Aumento é bom

# 10. LEAD TIME MÉDIO (Dias)
delta_percentual_lead_time, delta_type_lead_time = calculate_delta(lead_time_medio, lead_time_medio_ant, inverse=True) # Aumento é ruim


# --- INÍCIO DA ESTRUTURA DO DASHBOARD ---

# Cabeçalho Executivo (Mantido em HTML/Tailwind)
st.markdown(
    f"""
    <header class="bg-[#10141b] shadow-xl py-4 mb-8 border-b border-gray-700">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 class="text-3xl font-extrabold tracking-tight text-white">
                <span class="text-4xl" style="color:{C3_BLUE};">DAXLOG</span> TORRE DE CONTROLE LOGÍSTICA INTEGRADA
            </h1>
            <div class="flex items-center space-x-4">
                <span class="text-xs font-semibold uppercase px-3 py-1 rounded-full bg-blue-600 text-white shadow-lg">
                    {selected_mes}
                </span>
                <span class="text-sm font-semibold text-green-400">
                    STATUS: Online ✅ | Dados Sincronizados
                </span>
            </div>
        </div>
    </header>
    """, unsafe_allow_html=True
)

# 1. KPIs (Usando st.metric nativo)
st.markdown(
    f"""
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <h2 class="text-2xl font-semibold text-white mb-4 border-b border-gray-700 pb-2">
            📊 MÉTRICAS DE FOCO E CONTROLE
        </h2>
    </div>
    """, unsafe_allow_html=True
)

# --- PRIMEIRA LINHA DE KPIS (CUSTO E VOLUME) ---
with st.container():
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    # KPI 1: CUSTO TOTAL DE FRETE
    with col_kpi1:
        delta_label = f"{format_percent(abs(delta_percentual_frete))}% vs. Período Anterior"
        st.metric(
            label="CUSTO TOTAL DE FRETE",
            value=f"R$ {format_currency(total_frete)}",
            delta=delta_label,
            delta_color=delta_type_frete # 'inverse' (vermelho)
        )

    # KPI 2: DISTÂNCIA TOTAL PERCORRIDA
    with col_kpi2:
        delta_label = f"{format_percent(abs(delta_percentual_km))}% vs. Período Anterior"
        st.metric(
            label="DISTÂNCIA TOTAL PERCORRIDA",
            value=f"{format_number(total_km)} KM",
            delta=delta_label,
            delta_color=delta_type_km # 'normal' (verde)
        )

    # KPI 3: CUSTO/KM MÉDIO
    with col_kpi3:
        delta_label = f"{format_percent(abs(delta_percentual_custo_km))}% vs. Período Anterior"
        st.metric(
            label="CUSTO/KM MÉDIO",
            value=f"R$ {format_custo_km(custo_medio_km)}",
            delta=delta_label,
            delta_color=delta_type_custo_km # 'inverse' (vermelho)
        )

    # KPI 4: VOLUME DE DOCUMENTOS (CT-es)
    with col_kpi4:
        delta_label = f"{format_percent(abs(delta_percentual_ctes))}% vs. Período Anterior"
        st.metric(
            label="VOLUME DE DOCUMENTOS",
            value=f"{format_number(num_ctes)} CT-es",
            delta=delta_label,
            delta_color=delta_type_ctes # 'normal' (verde)
        )
        
# --- SEGUNDA LINHA DE KPIS (EFICIÊNCIA E CUSTO UNITÁRIO) ---
st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True) # Espaçamento entre linhas
with st.container():
    col_kpi5, col_kpi6, col_kpi7, col_kpi8 = st.columns(4)
    
    # KPI 5: PESO MÉDIO TRANSPORTADO (PMT)
    with col_kpi5:
        delta_label = f"{format_percent(abs(delta_percentual_pmt))}% vs. Período Anterior"
        st.metric(
            label="PESO MÉDIO TRANSPORTADO",
            value=format_weight(peso_medio_transportado),
            delta=delta_label,
            delta_color=delta_type_pmt # 'normal' (verde)
        )
        
    # KPI 6: TAXA DE OCUPAÇÃO MÉDIA (TOM)
    with col_kpi6:
        delta_label = f"{format_percent(abs(delta_percentual_tom))}% vs. Período Anterior"
        st.metric(
            label="TAXA DE OCUPAÇÃO MÉDIA",
            value=f"{format_percent(taxa_ocupacao_media)} %",
            delta=delta_label,
            delta_color=delta_type_tom # 'normal' (verde)
        )
        
    # KPI 7: CUSTO MÉDIO POR CT-e (CMC)
    with col_kpi7:
        delta_label = f"{format_percent(abs(delta_percentual_cmc))}% vs. Período Anterior"
        st.metric(
            label="CUSTO MÉDIO POR CT-e",
            value=f"R$ {format_currency(custo_medio_cte)}",
            delta=delta_label,
            delta_color=delta_type_cmc # 'inverse' (vermelho)
        )

    # KPI 8: CUSTO MÉDIO POR KG (CMKG)
    with col_kpi8:
        delta_label = f"{format_percent(abs(delta_percentual_custo_kg))}% vs. Período Anterior"
        st.metric(
            label="CUSTO/KG MÉDIO",
            value=f"R$ {format_custo_km(custo_medio_kg)}", # Reuso format_custo_km para 4 casas
            delta=delta_label,
            delta_color=delta_type_custo_kg # 'inverse' (vermelho)
        )

# --- TERCEIRA LINHA DE KPIS (QUALIDADE E PRAZO) ---
st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True) # Espaçamento
with st.container():
    # Usar 4 colunas para manter o alinhamento visual
    col_kpi9, col_kpi10, col_kpi11, col_kpi_empty = st.columns(4)

    # KPI 9: OTIF (On-Time, In-Full)
    with col_kpi9:
        delta_label = f"{format_percent(abs(delta_percentual_otif))}% vs. Período Anterior"
        st.metric(
            label="OTIF (ON-TIME, IN-FULL)",
            value=f"{format_percent(otif_percentual)} %",
            delta=delta_label,
            delta_color=delta_type_otif # 'normal' (verde)
        )

    # KPI 10: SLA (FIXO 96%) - Compara OTIF Real vs Meta
    with col_kpi10:
        sla_delta_diff = otif_percentual - sla_meta
        sla_delta_color = 'normal' if sla_delta_diff >= 0 else 'inverse'
        # Usar emoji de forma condicional para melhor visual
        if sla_delta_diff >= 0:
            sla_delta_label = f"🚀 +{format_percent(abs(sla_delta_diff))}% ACIMA DA META"
        else:
            sla_delta_label = f"🔻 -{format_percent(abs(sla_delta_diff))}% ABAIXO DA META"
            
        st.metric(
            label="SLA - META ESTABELECIDA",
            value=f"{format_percent(sla_meta)} %",
            delta=sla_delta_label,
            delta_color=sla_delta_color # 'normal' se acima da meta, 'inverse' se abaixo
        )

    # KPI 11: LEAD TIME MÉDIO
    with col_kpi11:
        delta_label = f"{format_percent(abs(delta_percentual_lead_time))}% vs. Período Anterior"
        st.metric(
            label="LEAD TIME MÉDIO",
            value=f"{lead_time_medio:,.2f} Dias".replace(",", "X").replace(".", ",").replace("X", "."), # Formatação customizada para float
            delta=delta_label,
            delta_color=delta_type_lead_time # 'inverse' (vermelho, pois menos dias é melhor)
        )
    
    # A quarta coluna fica vazia para manter o alinhamento das três linhas
    with col_kpi_empty:
        st.markdown('<div style="height: 100%; visibility: hidden;">.</div>', unsafe_allow_html=True)


# --- GERAÇÃO E INJEÇÃO DOS GRÁFICOS PLOTLY (MANTIDO) ---
# Função para configurar layout base do Plotly
def configure_plotly_layout(fig, height=400):
    fig.update_layout(
        plot_bgcolor=BG_CARD,
        paper_bgcolor=BG_CARD,
        font=dict(color=TEXT_COLOR, family='Inter'),
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor=GRAY_BORDER),
        legend=dict(
            orientation="h", 
            yanchor="bottom",
            xanchor="right", 
            y=-0.2, 
            x=1
        ), 
        height=height,
        hovermode="x unified",
        modebar_remove=['autoscale', 'lasso', 'select', 'pan', 'zoomIn', 'zoomOut', 'resetview'], 
    )
    return fig

# 1. Custo por Filial (Barra)
df_custo_filial = df_filtered.groupby('id_filial_nome')['custo_mensal'].sum().reset_index().rename(columns={'custo_mensal': 'Custo Mensal Estimado (R$)'})
fig_filial = px.bar(
    df_custo_filial,
    x='id_filial_nome',
    y='Custo Mensal Estimado (R$)',
    color='id_filial_nome',
    color_discrete_sequence=[C3_BLUE, C3_RED, '#eab308', '#10b981', '#1d4ed8'],
    text_auto='.2s' 
)
fig_filial = configure_plotly_layout(fig_filial)
fig_filial.update_traces(
    hovertemplate='Unidade: %{x}<br>Custo: %{y:,.2f} R$<extra></extra>',
    marker_line_width=0, 
    textposition='outside'
)
fig_filial.update_xaxes(title=None)
fig_filial.update_yaxes(title="Custo Estimado", showgrid=True)


# 2. Evolução Temporal (Linha)
df_evolucao_total = df_base.groupby('mes_ano')['frete_valor'].sum().reset_index()
df_evolucao_total = df_evolucao_total[df_evolucao_total['mes_ano'] <= selected_mes].sort_values(by='mes_ano')

fig_evolucao = px.line(
    df_evolucao_total,
    x='mes_ano',
    y='frete_valor',
    color_discrete_sequence=[C3_RED],
    markers=True,
)
fig_evolucao = configure_plotly_layout(fig_evolucao)
fig_evolucao.update_yaxes(title="Frete Total (R$)", tickformat=".2s")
fig_evolucao.update_xaxes(title="Período", showgrid=True)
fig_evolucao.update_traces(
    hovertemplate='Mês: %{x}<br>Frete: %{y:,.2f} R$<extra></extra>',
    line=dict(width=3) 
)


# 3. Top 5 CT-e (Barra de Concentração)
df_top_5 = df_filtered.sort_values(by='custo_mensal', ascending=False).head(5)
fig_top_5 = px.bar(
    df_top_5,
    x='cte_numero',
    y='custo_mensal',
    color='custo_mensal',
    color_continuous_scale='Plasma',
    text_auto='.2s'
)
fig_top_5 = configure_plotly_layout(fig_top_5)
fig_top_5.update_yaxes(title="Custo Estimado (R$)", tickformat=".2s", showgrid=True)
fig_top_5.update_xaxes(title="Nº CT-e")
fig_top_5.update_traces(
    hovertemplate='CT-e: %{x}<br>Custo: %{y:,.2f} R$<extra></extra>',
    marker_line_width=0,
    textposition='outside'
)
fig_top_5.update_layout(coloraxis_showscale=False)


# 4. Participação (Rosca/Pie)
df_share = df_filtered.groupby('id_transportadora_nome')['custo_mensal'].sum().reset_index()
total_custo = df_share['custo_mensal'].sum()
df_share['share_percent'] = (df_share['custo_mensal'] / total_custo) * 100
threshold = 5 # Agrupa quem tem menos de 5%
df_share['Parceiro Agrupado'] = np.where(df_share['share_percent'] < threshold, 'Outros', df_share['id_transportadora_nome'])
df_share_agrupado = df_share.groupby('Parceiro Agrupado')['custo_mensal'].sum().reset_index()

fig_share = px.pie(
    df_share_agrupado,
    names='Parceiro Agrupado',
    values='custo_mensal',
    color_discrete_sequence=[C3_BLUE, C3_RED, '#eab308', '#10b981', '#1d4ed8', '#065f46'],
    hole=0.6,
)
fig_share = configure_plotly_layout(fig_share)
fig_share.update_traces(
    textinfo='percent+label', 
    marker=dict(line=dict(color=BG_CARD, width=2)),
    textposition='inside' 
)
fig_share.update_layout(
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", title=None),
    showlegend=True
)

# --- ESTRUTURA PARA GRÁFICOS E INJEÇÃO (MANTIDO) ---

st.markdown(
    f"""
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <h2 class="text-2xl font-semibold text-white mb-4 border-b border-gray-700 pb-2 mt-8">
            📈 VISÃO ANALÍTICA ESTRATÉGICA
        </h2>
    </div>
    """, unsafe_allow_html=True
)

# Geração dos gráficos dentro das colunas Streamlit
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h3 class="text-xl font-semibold text-blue-400 mb-2">CUSTO TOTAL POR UNIDADE DE ORIGEM</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_filial, use_container_width=True, theme=None, key="filial_chart")
    
    st.markdown('<h3 class="text-xl font-semibold text-blue-400 mb-2 mt-6">CONCENTRAÇÃO DE CUSTO: TOP CT-ES DE ALTO IMPACTO</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_top_5, use_container_width=True, theme=None, key="top5_chart")

with col2:
    st.markdown('<h3 class="text-xl font-semibold text-blue-400 mb-2">EVOLUÇÃO MENSAL DO FRETE TOTAL (TENDÊNCIA)</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_evolucao, use_container_width=True, theme=None, key="evolucao_chart")
    
    st.markdown('<h3 class="text-xl font-semibold text-blue-400 mb-2 mt-6">PARTICIPAÇÃO DE MERCADO POR PARCEIRO LOGÍSTICO (SHARE)</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_share, use_container_width=True, theme=None, key="share_chart")


# --- SEÇÃO DE DETALHES E EXPORTAÇÃO (ATUALIZADO COM AS NOVAS COLUNAS E AJUSTE NATIVO) ---

st.markdown(
    """
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <h2 class="text-2xl font-semibold text-white mb-4 border-b border-gray-700 pb-2">
            📄 DETALHAMENTO E AUDITORIA DA BASE
        </h2>
    </div>
    """, unsafe_allow_html=True
)

with st.expander("Expandir Relatório de Auditoria e Base Detalhada", expanded=False):
    # Seleção de colunas e renomeação para a tabela final (prof.)
    df_report = df_filtered[[
        'cte_numero', 'id_filial_nome', 'id_transportadora_nome', 'id_cliente_nome', 
        'id_regiao_nome', 'frete_valor', 'distancia_km', 'peso_kg', 'capacidade_kg', 
        'custo_km', 'custo_unitario_peso', 'custo_mensal', 'otif_status', 'lead_time_dias', 'data_hora'
    ]].sort_values(by='custo_mensal', ascending=False)

    df_report.columns = [
        'Nº CT-e', 'Unidade', 'Parceiro Logístico', 'Cliente Faturador', 
        'Região', 'Frete (R$)', 'Dist. (KM)', 'Peso (KG)', 'Capacidade (KG)',
        'Custo/KM (R$)', 'Custo/KG (R$)', 'Custo Mensal (R$)',
        'OTIF', 'Lead Time (Dias)', 'Data Emissão'
    ]

    # Formatação de exibição do DataFrame
    st.dataframe(
        df_report.style
        .format({
            'Frete (R$)': format_currency, 
            'Custo/KM (R$)': format_custo_km, 
            'Custo/KG (R$)': format_custo_km, 
            'Custo Mensal (R$)': format_currency,
            'Peso (KG)': format_number,
            'Capacidade (KG)': format_number,
            # Formatação dos novos KPIS
            'OTIF': lambda x: '✅ Sim' if x else '❌ Não',
            # CORREÇÃO: usar lambda para formatar número e depois ajustar separadores e texto "dias"
            'Lead Time (Dias)': lambda x: (f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " dias") if pd.notnull(x) else "",
        })
        .set_properties(**{'background-color': BG_CARD, 'color': TEXT_COLOR, 'border-color': GRAY_BORDER}),
        use_container_width=True
    )

    # EXPORTAÇÃO DE DADOS
    st.markdown("---")
    
    # 📌 AJUSTE APLICADO AQUI: Usando st.caption nativo em vez de st.markdown com HTML.
    st.caption('Opções de Exportação') 
    
    csv = df_report.to_csv(index=False, sep=';', encoding='utf-8')

    st.download_button(
        label="📥 BAIXAR BASE DE DADOS FILTRADA (CSV)",
        data=csv,
        file_name=f'relatorio_logistico_executivo_{selected_mes}.csv',
        mime='text/csv',
        key='download_csv',
        type='primary' 
    )

