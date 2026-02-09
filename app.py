import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da Página
# O arquivo 'fi-port.png' deve estar na raiz do seu repositório GitHub
favicon_path = "fi-port.png"

# Verificação simples para garantir que o app não quebre se a imagem sumir
if os.path.exists(favicon_path):
    page_icon = favicon_path
else:
    page_icon = "🪐"

st.set_page_config(
    page_title="Painel Solar Analytics",
    page_icon=page_icon,
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
    .stRadio > label {
        font-weight: bold;
        font-size: 1.1rem;
    }
    /* Estilização para o botão de link para parecer mais integrado */
    .stLinkButton > a {
        width: 100%;
        text-align: center;
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

# --- FUNÇÃO AUXILIAR DE PLOTAGEM ---
def configurar_layout_padrao(fig):
    """Configura o modo Pan e estética dark."""
    fig.update_layout(
        dragmode='pan',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FAFAFA"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- BARRA LATERAL ---
st.sidebar.header("Filtros de Dados")

# Radio Buttons para clique direto
filtro_visual = st.sidebar.radio(
    "Selecionar Categoria:",
    options=["Todos os Planetas", "Rochosos (Terrestres)", "Gigantes Gasosos", "Gigantes Gelados"],
    index=0
)

# Lógica de Filtragem
if filtro_visual == "Todos os Planetas":
    df_filtrado = df
elif filtro_visual == "Rochosos (Terrestres)":
    df_filtrado = df[df["Tipo"] == "Terrestre"]
elif filtro_visual == "Gigantes Gasosos":
    df_filtrado = df[df["Tipo"] == "Gigante Gasoso"]
elif filtro_visual == "Gigantes Gelados":
    df_filtrado = df[df["Tipo"] == "Gigante Gelado"]

st.sidebar.markdown("---")
st.sidebar.markdown("**Links Externos:**")
# Botão para o Portfólio do usuário
st.sidebar.link_button("Acessar meu Portfólio 🚀", "https://brunojsdev.github.io/meu-portfolio/")

# --- CONTEÚDO PRINCIPAL ---

st.title("🪐 Painel Analítico do Sistema Solar")
st.markdown("Dashboard técnico com dados físicos e orbitais consolidados.")

# 1. Correlação Gravidade x Temperatura
st.subheader("🔭 Análise de Dispersão: Gravidade vs Temperatura")
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
fig_bubble.update_traces(textposition='top center')
fig_bubble = configurar_layout_padrao(fig_bubble)
st.plotly_chart(fig_bubble, use_container_width=True)

# 2. Abas Comparativas
st.subheader("📊 Comparativo de Variáveis")
tab1, tab2, tab3, tab4 = st.tabs(["Distância do Sol", "Duração do Dia", "Diâmetro", "Satélites (Luas)"])

with tab1:
    fig1 = px.bar(df_filtrado, x="Nome", y="Distância do Sol (10⁶ km)", color="Distância do Sol (10⁶ km)", 
                 color_continuous_scale="Viridis", text_auto='.1f', template="plotly_dark")
    st.plotly_chart(configurar_layout_padrao(fig1), use_container_width=True)

with tab2:
    fig2 = px.bar(df_filtrado, x="Nome", y="Duração do Dia (horas)", color="Tipo", 
                 text_auto='.1f', template="plotly_dark")
    st.plotly_chart(configurar_layout_padrao(fig2), use_container_width=True)

with tab3:
    fig3 = px.bar(df_filtrado, y="Nome", x="Diâmetro (km)", orientation='h', color="Tipo", 
                 text_auto=True, template="plotly_dark")
    st.plotly_chart(configurar_layout_padrao(fig3), use_container_width=True)

with tab4:
    fig4 = px.bar(df_filtrado.sort_values("Luas", ascending=False), x="Nome", y="Luas", 
                 color="Luas", color_continuous_scale="Magma", text_auto=True, template="plotly_dark")
    st.plotly_chart(configurar_layout_padrao(fig4), use_container_width=True)

# 3. Tabela de Dados
st.markdown("---")
st.subheader("📋 Tabela de Dados Científica")
st.dataframe(
    df_filtrado.drop(columns=["Cor"]),
    use_container_width=True,
    hide_index=True
)
