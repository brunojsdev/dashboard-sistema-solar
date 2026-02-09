import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuração da Página
st.set_page_config(
    page_title="Painel de Dados do Sistema Solar",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS PERSONALIZADA ---
# Ajuste fino para garantir aparência profissional no modo Dark do Streamlit
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #FAFAFA;
        font-family: 'Helvetica', sans-serif;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #41444C;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CAMADA DE DADOS ---
@st.cache_data
def load_data():
    """
    Carrega e processa os dados dos planetas.
    Utilizamos um dicionário hardcoded para evitar dependências de arquivos externos (CSV)
    no deploy, garantindo robustez.
    """
    data = [
        {
            "Nome": "Mercúrio",
            "Tipo": "Terrestre",
            "Diâmetro (km)": 4879,
            "Distância do Sol (10⁶ km)": 57.9,
            "Gravidade (m/s²)": 3.7,
            "Duração do Dia (horas)": 4222.6,
            "Luas": 0,
            "Temperatura Média (°C)": 167,
            "Cor": "#A5A5A5"
        },
        {
            "Nome": "Vênus",
            "Tipo": "Terrestre",
            "Diâmetro (km)": 12104,
            "Distância do Sol (10⁶ km)": 108.2,
            "Gravidade (m/s²)": 8.87,
            "Duração do Dia (horas)": 2802.0,
            "Luas": 0,
            "Temperatura Média (°C)": 464,
            "Cor": "#E3BB76"
        },
        {
            "Nome": "Terra",
            "Tipo": "Terrestre",
            "Diâmetro (km)": 12742,
            "Distância do Sol (10⁶ km)": 149.6,
            "Gravidade (m/s²)": 9.8,
            "Duração do Dia (horas)": 24.0,
            "Luas": 1,
            "Temperatura Média (°C)": 15,
            "Cor": "#2B32B2"
        },
        {
            "Nome": "Marte",
            "Tipo": "Terrestre",
            "Diâmetro (km)": 6779,
            "Distância do Sol (10⁶ km)": 227.9,
            "Gravidade (m/s²)": 3.71,
            "Duração do Dia (horas)": 24.7,
            "Luas": 2,
            "Temperatura Média (°C)": -65,
            "Cor": "#D14A28"
        },
        {
            "Nome": "Júpiter",
            "Tipo": "Gigante Gasoso",
            "Diâmetro (km)": 139820,
            "Distância do Sol (10⁶ km)": 778.6,
            "Gravidade (m/s²)": 24.79,
            "Duração do Dia (horas)": 9.9,
            "Luas": 79,
            "Temperatura Média (°C)": -110,
            "Cor": "#BCAFB2"
        },
        {
            "Nome": "Saturno",
            "Tipo": "Gigante Gasoso",
            "Diâmetro (km)": 116460,
            "Distância do Sol (10⁶ km)": 1433.5,
            "Gravidade (m/s²)": 10.44,
            "Duração do Dia (horas)": 10.7,
            "Luas": 82,
            "Temperatura Média (°C)": -140,
            "Cor": "#C5AB6E"
        },
        {
            "Nome": "Urano",
            "Tipo": "Gigante Gelado",
            "Diâmetro (km)": 50724,
            "Distância do Sol (10⁶ km)": 2872.5,
            "Gravidade (m/s²)": 8.69,
            "Duração do Dia (horas)": 17.2,
            "Luas": 27,
            "Temperatura Média (°C)": -195,
            "Cor": "#ADD8E6"
        },
        {
            "Nome": "Netuno",
            "Tipo": "Gigante Gelado",
            "Diâmetro (km)": 49244,
            "Distância do Sol (10⁶ km)": 4495.1,
            "Gravidade (m/s²)": 11.15,
            "Duração do Dia (horas)": 16.1,
            "Luas": 14,
            "Temperatura Média (°C)": -200,
            "Cor": "#5B5DDF"
        }
    ]
    return pd.DataFrame(data)

df = load_data()

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Navegação e Filtros")
st.sidebar.markdown("---")

# Filtro Global
tipos_disponiveis = df["Tipo"].unique()
filtro_tipo = st.sidebar.multiselect(
    "Filtrar por Tipo de Planeta:",
    options=tipos_disponiveis,
    default=tipos_disponiveis
)

# Aplicar filtro
df_filtrado = df[df["Tipo"].isin(filtro_tipo)]

if df_filtrado.empty:
    st.warning("Nenhum dado disponível com os filtros selecionados.")
    st.stop()

# --- CONTEÚDO PRINCIPAL ---

st.title("🪐 Painel Analítico do Sistema Solar")
st.markdown("""
Este painel apresenta dados quantitativos sobre os planetas do sistema solar. 
Explore as métricas de massa, diâmetro, gravidade e temperatura através das visualizações interativas abaixo.
""")

st.markdown("---")

# 1. Métricas Principais (KPIs)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total de Planetas Listados", value=len(df_filtrado))
with col2:
    maior_planeta = df_filtrado.loc[df_filtrado['Diâmetro (km)'].idxmax()]['Nome']
    st.metric(label="Maior Diâmetro", value=maior_planeta)
with col3:
    total_luas = df_filtrado['Luas'].sum()
    st.metric(label="Total de Luas (Filtro)", value=int(total_luas))
with col4:
    temp_media = df_filtrado['Temperatura Média (°C)'].mean()
    st.metric(label="Temp. Média", value=f"{temp_media:.1f} °C")

st.markdown("---")

# 2. Visualização Avançada: Comparativo 3D (Scatter Plot)
st.subheader("🔭 Visualização de Escala Relativa (Diâmetro vs Temperatura)")
st.markdown("O gráfico abaixo correlaciona o diâmetro (tamanho da bolha), a temperatura (eixo Y) e a gravidade (eixo X).")

fig_bubble = px.scatter(
    df_filtrado,
    x="Gravidade (m/s²)",
    y="Temperatura Média (°C)",
    size="Diâmetro (km)",
    color="Nome",
    hover_name="Nome",
    text="Nome",
    size_max=60,
    color_discrete_map={row['Nome']: row['Cor'] for index, row in df.iterrows()},
    template="plotly_dark"
)

fig_bubble.update_layout(
    height=500,
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Gravidade (m/s²)",
    yaxis_title="Temperatura Média (°C)"
)
st.plotly_chart(fig_bubble, use_container_width=True)


# 3. Análise Comparativa (Abas)
st.subheader("📊 Comparativo Técnico")
tab1, tab2, tab3 = st.tabs(["Distância do Sol", "Duração do Dia", "Comparativo de Diâmetro"])

with tab1:
    # Gráfico de Barras: Distância
    fig_dist = px.bar(
        df_filtrado,
        x="Nome",
        y="Distância do Sol (10⁶ km)",
        color="Distância do Sol (10⁶ km)",
        color_continuous_scale="Magma",
        title="Distância em relação ao Sol (Milhões de km)",
        template="plotly_dark"
    )
    fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    # Gráfico de Linha/Area: Duração do dia
    fig_day = px.bar(
        df_filtrado,
        x="Nome",
        y="Duração do Dia (horas)",
        color="Tipo",
        title="Duração de um Dia (Rotação em Horas)",
        template="plotly_dark"
    )
    fig_day.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_day, use_container_width=True)

with tab3:
    # Gráfico de Pizza: Proporção de Luas
    # Usando Pie Chart para variar a visualização, focado nas Luas ou Diâmetro
    fig_dia = px.bar(
        df_filtrado,
        y="Nome",
        x="Diâmetro (km)",
        orientation='h',
        color="Tipo",
        title="Diâmetro Equatorial (km)",
        template="plotly_dark"
    )
    fig_dia.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_dia, use_container_width=True)


# 4. Tabela de Dados Brutos
st.markdown("---")
st.subheader("📋 Base de Dados Científica")

# Formatação da tabela para exibição
df_display = df_filtrado.drop(columns=["Cor"]) # Remove a coluna de cor hexadecimal da visualização

st.dataframe(
    df_display,
    use_container_width=True,
    column_config={
        "Diâmetro (km)": st.column_config.NumberColumn(format="%d km"),
        "Distância do Sol (10⁶ km)": st.column_config.NumberColumn(format="%.1f M km"),
        "Gravidade (m/s²)": st.column_config.NumberColumn(format="%.2f m/s²"),
    },
    hide_index=True
)

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>Desenvolvido em Python com Streamlit | Dados aproximados para fins ilustrativos (NASA Planetary Fact Sheet).</small>
    </div>
    """, 
    unsafe_allow_html=True
)
