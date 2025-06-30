import streamlit as st
import pandas as pd
from tinydb import TinyDB
import plotly.express as px

# === CONFIGURAÇÃO ===
st.set_page_config(page_title="Dashboard Logístico", layout="wide")
DB_PATH = "rotas.json"
CSS_PATH = r"F:\LUIS H\Pipeline-API\dashboard_style.css"

# === INJETAR ESTILO CUSTOM ===
with open(CSS_PATH, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === CARREGAR DADOS ===
@st.cache_data
def carregar_dados():
    db = TinyDB(DB_PATH)
    ctes = pd.DataFrame(db.table("ctes").all())
    filiais = pd.DataFrame(db.table("filiais").all())
    transportadoras = pd.DataFrame(db.table("transportadoras").all())
    clientes = pd.DataFrame(db.table("clientes").all())
    produtos = pd.DataFrame(db.table("produtos").all())
    regioes = pd.DataFrame(db.table("regioes").all())

    if ctes.empty:
        return None

    ctes['frete_valor'] = pd.to_numeric(ctes.get('frete_valor', 0), errors='coerce').fillna(0.0)
    ctes['distancia_km'] = pd.to_numeric(ctes.get('distancia_km', 1), errors='coerce').replace({0: 1})
    ctes['frequencia_semanal'] = pd.to_numeric(ctes.get('frequencia_semanal', 1), errors='coerce').fillna(1)

    ctes['custo_km'] = ctes['frete_valor'] / ctes['distancia_km']
    ctes['custo_mensal'] = ctes['frete_valor'] * ctes['frequencia_semanal'] * 4

    def merge_dim(df, dim, key, nome_col):
        if not dim.empty:
            dim = dim.rename(columns={"id": f"{nome_col}_id_tmp"})
            df = df.merge(dim[[f"{nome_col}_id_tmp", key]], left_on=nome_col, right_on=f"{nome_col}_id_tmp", how='left')
            df = df.rename(columns={key: f"{nome_col}_nome"}).drop(columns=[f"{nome_col}_id_tmp"])
        return df

    ctes = merge_dim(ctes, filiais, "nome", "id_filial")
    ctes = merge_dim(ctes, transportadoras, "nome", "id_transportadora")
    ctes = merge_dim(ctes, clientes, "nome", "id_cliente")
    ctes = merge_dim(ctes, produtos, "nome", "id_produto")
    ctes = merge_dim(ctes, regioes, "nome", "id_regiao")

    return ctes

# === TÍTULO ===
st.title("🚚 Dashboard Logístico Estratégico")

df = carregar_dados()
if df is None:
    st.warning("Nenhum CT-e disponível. Execute o pipeline primeiro.")
    st.stop()

# === FILTROS ===
st.sidebar.header("🎯 Filtros")
filial_op = sorted(df['id_filial_nome'].dropna().unique())
transp_op = sorted(df['id_transportadora_nome'].dropna().unique())
cliente_op = sorted(df['id_cliente_nome'].dropna().unique())
regiao_op = sorted(df['id_regiao_nome'].dropna().unique())

f1 = st.sidebar.multiselect("Filial", filial_op, default=filial_op)
f2 = st.sidebar.multiselect("Transportadora", transp_op, default=transp_op)
f3 = st.sidebar.multiselect("Cliente", cliente_op, default=cliente_op)
f4 = st.sidebar.multiselect("Região", regiao_op, default=regiao_op)

df_filtrado = df[
    df['id_filial_nome'].isin(f1) &
    df['id_transportadora_nome'].isin(f2) &
    df['id_cliente_nome'].isin(f3) &
    df['id_regiao_nome'].isin(f4)
]

# === MÉTRICAS ===
st.subheader("📌 Métricas Gerais")
total_frete = df_filtrado['frete_valor'].sum()
total_km = df_filtrado['distancia_km'].sum()
custo_medio_km = total_frete / total_km if total_km > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total de Fretes", f"R$ {total_frete:,.2f}".replace('.', ','))
col2.metric("🚗 KM Rodados", f"{total_km:,.0f}".replace(',', '.'))
col3.metric("⚖️ Custo Médio por KM", f"R$ {custo_medio_km:,.2f}".replace('.', ','))

# === GRÁFICO 1 ===
st.subheader("📊 Custo Mensal por Filial")
graf1 = px.bar(
    df_filtrado.groupby('id_filial_nome')['custo_mensal'].sum().reset_index(),
    x='id_filial_nome', y='custo_mensal', text_auto='.2s', color='id_filial_nome',
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(graf1, use_container_width=True)

# === GRÁFICO 2 ===
st.subheader("📈 Evolução do Frete por Cliente")
df_filtrado['data_hora'] = pd.to_datetime(df_filtrado['data_hora'], errors='coerce')
df_linha = df_filtrado.groupby([df_filtrado['data_hora'].dt.to_period('M').astype(str), "id_cliente_nome"])["frete_valor"].sum().reset_index()
df_linha = df_linha.rename(columns={"data_hora": "Mês"})
graf2 = px.line(df_linha, x="Mês", y="frete_valor", color="id_cliente_nome", markers=True, line_shape='linear')
st.plotly_chart(graf2, use_container_width=True)

# === GRÁFICO 3 ===
st.subheader("🏆 Top 10 CT-es por Custo")
top10 = df_filtrado.sort_values(by='custo_mensal', ascending=False).head(10)
graf3 = px.bar(
    top10,
    x='cte_numero',
    y='custo_mensal',
    color='id_filial_nome',
    hover_data=['id_cliente_nome', 'frete_valor', 'distancia_km']
)
st.plotly_chart(graf3, use_container_width=True)

# === GRÁFICO 4 ===
st.subheader("📦 Custo Total por Transportadora")
graf4 = px.pie(
    df_filtrado,
    values='custo_mensal',
    names='id_transportadora_nome',
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(graf4, use_container_width=True)

# === TABELA ===
st.subheader("📄 Tabela Detalhada dos CT-es")
st.dataframe(df_filtrado.sort_values(by='custo_mensal', ascending=False), use_container_width=True)

# === EXPORTAÇÃO ===
st.subheader("📤 Exportar Dados Filtrados")
st.download_button(
    label="📥 Baixar CSV",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="dados_logisticos.csv",
    mime="text/csv"
)
