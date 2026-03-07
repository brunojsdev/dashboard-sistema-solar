import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PALETA DE CORES PERSONALIZADA ---
COR_PLANETAS = {
    'Sol': '#FFD700',       # Amarelo/Dourado para o Sol
    'Mercúrio': '#8C8C8C',
    'Vênus': '#E89AB0',
    'Terra': '#0AC269',
    'Marte': '#E63946',
    'Júpiter': '#C65D2E',
    'Saturno': '#EAD7A1',
    'Urano': '#76EEC6',
    'Netuno': '#2A4B9B'
}

COR_TIPOS = {
    'Rochoso': '#8B5E3C',
    'Gasoso': '#D9FFF2',
    'Gelo': '#6EC5E9',
    'Estrela': '#FFD700'
}

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Data Solar",
    page_icon="fi-port.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO CSS AVANÇADO ---
st.markdown("""
<style>
    /* Reset e Fundo */
    .stApp {
        background-color: #040014;
        color: #c9e4ff;
    }
    
    /* Botão Portfolio */
    .portfolio-btn {
        position: absolute;
        top: -50px;
        left: 0;
        color: #5752ff;
        text-decoration: none !important;
        font-weight: 600;
        border: 1px solid #5752ff;
        padding: 5px 20px;
        border-radius: 4px;
        transition: 0.3s;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    .portfolio-btn:hover {
        background-color: #5752ff;
        color: white !important;
        box-shadow: 0px 0px 15px rgba(87, 82, 255, 0.4);
    }

    h1, h2, h3 {
        color: #ffdd00 !important;
        font-family: 'Inter', sans-serif;
    }

    /* FIX: NAVEGAÇÃO HORIZONTAL SEM SOBREPOSIÇÃO */
    div[data-testid="stHorizontalBlock"]:has(button) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        overflow-x: auto;
    }
    
    div[data-testid="stColumn"]:has(button) {
        width: auto !important;
        min-width: fit-content !important;
        flex: 0 0 auto !important;
    }

    .stButton > button {
        background-color: #090024;
        color: #c9e4ff;
        border: 1px solid #150136;
        border-radius: 4px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        width: auto !important;
        white-space: nowrap;
    }

    .stButton > button:hover {
        border-color: #ffdd00;
        color: #ffdd00;
    }

    /* AJUSTE DO MULTISELECT */
    .stMultiSelect div[data-baseweb="select"] {
        min-width: 400px !important;
    }
    
    .planeta-desc {
        font-size: 1.2rem;
        color: #c9e4ff;
        margin-bottom: 25px;
        border-left: 3px solid #5752ff;
        padding-left: 15px;
        font-style: italic;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE ---
@st.cache_data
def get_data():
    data = {
        'Planeta': ['Sol', 'Mercúrio', 'Vênus', 'Terra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Netuno'],
        'Tipo': ['Estrela', 'Rochoso', 'Rochoso', 'Rochoso', 'Rochoso', 'Gasoso', 'Gasoso', 'Gelo', 'Gelo'],
        'Distancia': [0, 57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0],
        'Gravidade': [274.0, 3.7, 8.87, 9.8, 3.71, 24.79, 10.44, 8.69, 11.15],
        'Diametro': [1392700, 4879, 12104, 12742, 6779, 139820, 116460, 50724, 49244],
        'Luas': [0, 0, 0, 1, 2, 95, 146, 27, 14],
        'Temperatura_Media': [5500, 167, 464, 15, -65, -110, -140, -195, -200]
    }
    return pd.DataFrame(data)

df_original = get_data()
df_planetas_apenas = df_original[df_original['Tipo'] != 'Estrela']

# --- HEADER ---
st.markdown(f'<a href="https://brunojsdev.github.io/meu-portfolio/" class="portfolio-btn">Portfolio</a>', unsafe_allow_html=True)
st.title("SISTEMA SOLAR | DATA INSIGHTS")

# --- NAVEGAÇÃO ---
botoes_nomes = ["SISTEMA COMPLETO", "SOL", "MERCÚRIO", "VÊNUS", "TERRA", "MARTE", "JÚPITER", "SATURNO", "URANO", "NETUNO"]

if 'selecao' not in st.session_state:
    st.session_state.selecao = "Geral"

cols = st.columns(len(botoes_nomes))
for idx, nome in enumerate(botoes_nomes):
    with cols[idx]:
        if st.button(nome, key=f"btn_{nome}"):
            st.session_state.selecao = "Geral" if nome == "SISTEMA COMPLETO" else nome.title()

st.markdown("---")

plotly_config = {'displayModeBar': False}

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.selecao == "Geral":
    col_f1, _ = st.columns([4, 6]) 
    with col_f1:
        tipos_disponiveis = df_planetas_apenas['Tipo'].unique()
        filtro_tipo = st.multiselect(
            "Filtrar por Tipo:", 
            options=tipos_disponiveis, 
            default=list(tipos_disponiveis)
        )
    
    df_filtered = df_planetas_apenas[df_planetas_apenas['Tipo'].isin(filtro_tipo)]
    st.write("")

    c1, c2, c3, c4, _ = st.columns([1.2, 2.2, 1.5, 1.2, 2])
    c1.metric("Planetas", len(df_filtered))
    c2.metric("Média de Gravidade", f"{df_filtered['Gravidade'].mean():.2f} m/s²")
    c3.metric("Total de Luas", df_filtered['Luas'].sum())
