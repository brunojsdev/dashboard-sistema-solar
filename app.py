import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Sistema Solar | Deep Space UI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJEÇÃO DE CSS CUSTOMIZADO ---
# Adicionei estilos específicos para o link de retorno e botões
st.markdown("""
<style>
    /* Estilização Geral */
    .stApp {
        background-color: #040014;
        color: #c9e4ff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #090024;
        border-right: 1px solid #5752ff;
    }
    
    /* Link de Retorno (Botão Voltar) */
    .back-link {
        display: inline-flex;
        align-items: center;
        text-decoration: none;
        color: #5752ff;
        font-weight: bold;
        padding: 8px 16px;
        border: 1px solid #5752ff;
        border-radius: 30px;
        transition: 0.3s;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
    .back-link:hover {
        background-color: #5752ff;
        color: white;
        box-shadow: 0px 0px 15px rgba(87, 82, 255, 0.5);
    }

    /* Títulos Neon */
    h1, h2, h3 {
        color: #ffdd00 !important;
        text-shadow: 0px 0px 15px rgba(255, 221, 0, 0.3);
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #ffdd00 !important;
        text-shadow: 0px 0px 10px rgba(255, 221, 0, 0.4);
    }
    
    /* Botões nativos do Streamlit */
    .stButton>button {
        background-color: #150136;
        color: #ffdd00;
        border: 1px solid #5752ff;
        border-radius: 20px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS ---
@st.cache_data
def load_data():
    data = {
        'Planeta': ['Mercúrio', 'Vênus', 'Terra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Netuno'],
        'Tipo': ['Rochoso', 'Rochoso', 'Rochoso', 'Rochoso', 'Gasoso', 'Gasoso', 'Gelo', 'Gelo'],
        'Distancia': [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0],
        'Gravidade': [3.7, 8.87, 9.8, 3.71, 24.79, 10.44, 8.69, 11.15],
        'Diametro': [4879, 12104, 12742, 6779, 139820, 116460, 50724, 49244],
        'Luas': [0, 0, 1, 2, 95, 146, 27, 14]
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR (Terminal) ---
with st.sidebar:
    # BOTÃO DE VOLTAR AO PORTFÓLIO
    st.markdown(f"""
        <a href="https://brunojsdev.github.io/meu-portfolio/" target="_self" class="back-link">
            ← Voltar ao Portfólio
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>🛰️ Terminal</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    selecao = st.selectbox("Escolha o alvo:", ["Sistema Solar"] + list(df['Planeta']))
    
    st.markdown("---")
    st.info("Status da Missão: Ativa")
    st.caption("BrunoJS Dev | Exploration Unit")

# --- CONTEÚDO PRINCIPAL ---
if selecao == "Sistema Solar":
    st.markdown("<h1>🌌 Sistema Solar: Visão Telemétrica</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Corpos Escaneados", "8 Planetas")
    col2.metric("Total de Luas", f"{df['Luas'].sum()}")
    col3.metric("Estrela Host", "Sol (G2V)")

    st.write("")
    
    tab1, tab2 = st.tabs(["🚀 Comparativo de Escala", "📈 Gravidade Relativa"])
    
    with tab1:
        fig1 = px.scatter(df, x="Distancia", y="Diametro", size="Diametro", color="Tipo",
                         hover_name="Planeta", size_max=60,
                         color_discrete_map={'Rochoso': '#ffaa00', 'Gasoso': '#5752ff', 'Gelo': '#c9e4ff'})
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          font_color='#c9e4ff', xaxis=dict(gridcolor='#150136'), yaxis=dict(gridcolor='#150136'))
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.bar(df, x="Planeta", y="Gravidade", color="Gravidade",
                     color_continuous_scale=['#150136', '#5752ff', '#ffdd00'])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff')
        st.plotly_chart(fig2, use_container_width=True)

else:
    p = df[df['Planeta'] == selecao].iloc[0]
    st.markdown(f"<h1>🪐 Planeta: {selecao}</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Tipo", p['Tipo'])
    c2.metric("Diâmetro", f"{p['Diametro']:,} km")
    c3.metric("Gravidade", f"{p['Gravidade']} m/s²")
    
    st.markdown(f"### Análise de {selecao}")
    st.write(f"Os dados telemétricos confirmam que **{selecao}** possui uma composição do tipo **{p['Tipo']}** e orbita a uma distância média de **{p['Distancia']} milhões de km** do Sol.")
    
    if st.button("Simular Pouso"):
        st.toast(f"Iniciando manobra de inserção orbital em {selecao}...")
        st.balloons()
