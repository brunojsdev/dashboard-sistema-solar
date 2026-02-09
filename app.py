import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(
    page_title="Painel Solar Analytics",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #FAFAFA;
        font-family: 'Helvetica', sans-serif;
    }
    /* Ajuste para deixar o radio button mais espaçado e legível */
    .stRadio > label {
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CAMADA DE DADOS ---
@st.cache_data
def load_data():
    data = [
        {"Nome": "Mercúrio", "Tipo": "Terrestre", "Diâmetro (km)": 4879, "Distância do Sol (10⁶ km)": 57.9, "Gravidade (m/s²)": 3.7, "Duração do Dia (horas)": 4222.6, "Luas": 0, "Temperatura Média (°C)": 167, "Cor": "#A5A5A5"},
        {"Nome": "Vênus", "Tipo": "Terrestre", "Diâmetro (km)": 12104, "Distância do Sol (10⁶ km)": 108.2, "Gravidade (m/s²)": 8.87, "Duração do Dia (horas)": 2802.0, "Luas": 0, "Temperatura Média (°C)": 464, "Cor": "#E3BB76"},
        {"Nome": "Terra", "Tipo": "Terrestre", "Diâmetro (km)": 12742, "Distância do Sol (10⁶ km)": 149.6, "Gravidade (m/s²)": 9.8, "Duração do Dia (horas)": 24.0, "Luas": 1, "Temperatura Média (°C)": 15, "Cor": "#2B32B2"},
        {"Nome": "Marte", "Tipo": "Terrestre", "Diâmetro (km)": 6779, "Distância do Sol (10⁶ km)": 227.9, "Gravidade (m/s²)": 3.71, "Duração do Dia (horas)": 24.7, "Luas": 2, "Temperatura Média (°C)": -65, "Cor": "#D14A28"},
        {"Nome": "Júpiter", "Tipo": "Gigante Gasoso", "Diâmetro (km)": 139820, "Distância do Sol (10⁶ km)": 778.6, "Gravidade (m/s²)": 24.79, "Duração do Dia (horas)": 9.9, "Luas": 79, "Temperatura Média (°C)": -110, "Cor": "#BCAFB2"},
        {"Nome": "Saturno", "Tipo": "Gigante Gasoso", "Diâmetro (km)": 116460, "Distância do Sol (10⁶ km)": 1433.5, "Gravidade (m/s²)": 10.44, "Duração do Dia (horas)": 10.7, "Luas": 82, "Temperatura Média (°C)": -140, "Cor": "#C5AB6E"},
        {"Nome": "Urano", "Tipo": "Gigante Gelado", "Diâmetro (km)": 50724, "Distância do Sol (10⁶ km)": 2872.5, "Gravidade (m/s²)": 8.69, "Duração do Dia (horas)": 17.2, "Luas": 27, "Temperatura Média (°C)": -195, "Cor": "#ADD8E6"},
        {"Nome": "Netuno", "Tipo": "Gigante Gelado", "Diâmetro (km)": 49244, "Distância do Sol (10⁶ km)": 4495.1, "Gravidade (m/s²)": 11.15, "Duração do Dia (horas)": 16.1, "Luas": 14, "Temperatura Média (°C)": -200, "Cor": "#5B5DDF"}
    ]
    return pd.DataFrame(data)

df = load_data()

# --- FUNÇÃO AUXILIAR DE PLOTAGEM (PADRÃO PAN) ---
def configurar_layout_padrao(fig):
    """Aplica o modo 'Pan' como padrão e remove fundo."""
    fig.update_layout(
        dragmode='pan',  # FORÇA O MODO PAN
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FAFAFA")
    )
    return fig

# --- BARRA LATERAL (FIXA E SIMPLES) ---
st.sidebar.header("Painel de Controle")

# Opções fixas de filtragem (Radio Button ao invés de Multiselect)
filtro_visual = st.sidebar.radio(
    "Categoria de Visualização:",
    options=["Visão Geral (Todos)", "Terrestres (Rochosos)", "Gigantes Gasosos", "Gigantes Gelados"],
    index=0
)

# Lógica de Filtragem
if filtro_visual == "Visão Geral (Todos)":
    df_filtrado = df
elif filtro_visual == "Terrestres (Rochosos)":
    df_filtrado = df[df["Tipo"] == "Terrestre"]
elif filtro_visual == "Gigantes Gasosos":
    df_filtrado = df[df["Tipo"] == "Gigante Gasoso"]
elif filtro_visual == "Gigantes Gelados":
    df_filtrado = df[df["Tipo"] == "Gigante Gelado"]

st.sidebar.markdown("---")
st.sidebar.info("Utilize as abas no painel principal para alternar entre as métricas comparativas.")

# --- CONTEÚDO PRINCIPAL ---

st.title("🪐 Painel Analítico do Sistema Solar")
st.markdown("Análise quantitativa das características físicas e orbitais dos corpos celestes.")

# 1. Visualização Avançada: Comparativo 3D (Scatter Plot)
st.subheader("🔭 Correlação: Tamanho, Gravidade e Temperatura")

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

# Ajuste fino das labels para não ficarem em cima das bolhas
fig_bubble.update_traces(textposition='top center')
fig_bubble = configurar_layout_padrao(fig_bubble)
fig_bubble.update_layout(height=450, showlegend=False)

st.plotly_chart(fig_bubble, use_container_width=True)


# 2. Análise Comparativa (Abas)
st.subheader("📊 Comparativo Técnico")
tab1, tab2, tab3, tab4 = st.tabs(["Distância", "Rotação (Dia)", "Diâmetro", "Satélites Naturais (Luas)"])

with tab1:
    fig_dist = px.bar(
        df_filtrado,
        x="Nome",
        y="Distância do Sol (10⁶ km)",
        color="Distância do Sol (10⁶ km)",
        color_continuous_scale="Magma",
        text_auto='.1f',
        title="Distância Média ao Sol (Milhões de km)",
        template="plotly_dark"
    )
    fig_dist = configurar_layout_padrao(fig_dist)
    st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    fig_day = px.bar(
        df_filtrado,
        x="Nome",
        y="Duração do Dia (horas)",
        color="Tipo",
        text_auto='.1f',
        title="Duração de um Dia (Horas de Rotação)",
        template="plotly_dark"
    )
    fig_day = configurar_layout_padrao(fig_day)
    st.plotly_chart(fig_day, use_container_width=True)

with tab3:
    fig_dia = px.bar(
        df_filtrado,
        y="Nome",
        x="Diâmetro (km)",
        orientation='h',
        color="Tipo",
        text_auto=True,
        title="Diâmetro Equatorial (km)",
        template="plotly_dark"
    )
    fig_dia = configurar_layout_padrao(fig_dia)
    st.plotly_chart(fig_dia, use_container_width=True)

with tab4:
    # Novo gráfico solicitado: Luas
    fig_luas = px.bar(
        df_filtrado.sort_values(by="Luas", ascending=False), # Ordenado do maior para o menor
        x="Nome",
        y="Luas",
        color="Luas",
        color_continuous_scale="Viridis",
        text_auto=True,
        title="Quantidade de Satélites Naturais (Luas)",
        template="plotly_dark"
    )
    fig_luas = configurar_layout_padrao(fig_luas)
    fig_luas.update_layout(yaxis_title="Número de Luas")
    st.plotly_chart(fig_luas, use_container_width=True)


# 3. Tabela de Dados
st.markdown("---")
st.subheader("📋 Tabela de Dados Detalhada")

df_display = df_filtrado.drop(columns=["Cor"])

st.dataframe(
    df_display,
    use_container_width=True,
    column_config={
        "Diâmetro (km)": st.column_config.NumberColumn(format="%d km"),
        "Distância do Sol (10⁶ km)": st.column_config.NumberColumn(format="%.1f M km"),
        "Gravidade (m/s²)": st.column_config.NumberColumn(format="%.2f m/s²"),
        "Temperatura Média (°C)": st.column_config.NumberColumn(format="%d °C"),
    },
    hide_index=True
)
