import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PALETA DE CORES PERSONALIZADA (VIBRANTE / NEON / ARCO-ÍRIS) ---
COR_PLANETAS = {
    'Sol': '#FFF100',       # Amarelo super brilhante
    'Mercúrio': '#FF4D00',  # Laranja/Vermelho vívido
    'Vênus': '#FF00E6',     # Rosa Neon / Magenta
    'Terra': '#00FF87',     # Verde Menta / Neon Green
    'Marte': '#FF003C',     # Vermelho Neon
    'Júpiter': '#FF8C00',   # Laranja Vibrante
    'Saturno': '#FFE600',   # Dourado Brilhante
    'Urano': '#00E5FF',     # Ciano Neon / Azul Elétrico
    'Netuno': '#651FFF'     # Roxo Elétrico / Índigo
}

COR_TIPOS = {
    'Rochoso': '#FF3366',   # Coral/Rosa Vibrante
    'Gasoso': '#CCFF00',    # Verde Limão Elétrico
    'Gelo': '#00BFFF',      # Azul Celeste Brilhante
    'Estrela': '#FFF100'    # Amarelo Brilhante
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
# Botão adaptado para fechar a aba ou voltar para a Vercel
st.markdown(
    f'<a href="https://brunojsilveira.vercel.app/" onclick="window.close();" class="portfolio-btn" target="_self">Voltar ao Portfólio</a>', 
    unsafe_allow_html=True
)

st.title("DASHBOARD SISTEMA SOLAR")

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
    c4.metric("Escopo", "Completo")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Diâmetro por Planeta (km)")
        # Alterado para colorir pelos Planetas usando o novo dicionário
        fig_diam = px.bar(df_filtered.sort_values('Diametro'), x='Diametro', y='Planeta', orientation='h',
                          color='Planeta', color_discrete_map=COR_PLANETAS)
        fig_diam.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', showlegend=False, dragmode='pan')
        st.plotly_chart(fig_diam, use_container_width=True, config=plotly_config)

    with col_right:
        st.subheader("Distribuição por Composição")
        # Alterado para usar o dicionário de cores dos Tipos
        fig_pie = px.pie(df_filtered, names='Tipo', hole=0.6, 
                         color='Tipo',
                         color_discrete_map=COR_TIPOS)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', dragmode='pan')
        st.plotly_chart(fig_pie, use_container_width=True, config=plotly_config)

    st.subheader("Intensidade Gravitacional")
    # Alterado para pegar a cor exata do planeta no gráfico de barras
    cores_gravidade = [COR_PLANETAS.get(p, '#ffffff') for p in df_filtered['Planeta']]
    fig_grav = go.Figure(data=[go.Bar(
        x=df_filtered['Planeta'], y=df_filtered['Gravidade'],
        marker=dict(color=cores_gravidade)
    )])
    fig_grav.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', dragmode='pan')
    st.plotly_chart(fig_grav, use_container_width=True, config=plotly_config)

elif st.session_state.selecao == "Sol":
    p_data = df_original[df_original['Planeta'] == 'Sol'].iloc[0]
    st.header(f"Exploração: {p_data['Planeta'].upper()}")
    
    st.markdown(f'<div class="planeta-desc">O Sol contém 99.8% da massa do Sistema Solar. É uma estrela de tipo espectral G2V.</div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4, _ = st.columns([1, 1.2, 1, 1.2, 2.6])
    m1.metric("Tipo", "Estrela")
    m2.metric("Diâmetro", f"{p_data['Diametro']:,}".replace(',','.'))
    m3.metric("Temperatura", f"{p_data['Temperatura_Media']}°C")
    m4.metric("Gravidade", f"{p_data['Gravidade']} m/s²")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Temperatura da Superfície")
        fig_t = go.Figure(go.Indicator(mode="gauge+number", value=p_data['Temperatura_Media'], number={'suffix':"°C"},
                                     gauge={'axis':{'range':[None, 6000]}, 'bar':{'color':COR_PLANETAS['Sol']}, 'bgcolor':"#090024"}))
        fig_t.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=350)
        st.plotly_chart(fig_t, use_container_width=True, config=plotly_config)
    with g2:
        st.subheader("Potencial Gravitacional")
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=p_data['Gravidade'],
                                     gauge={'axis':{'range':[None, 300]}, 'bar':{'color':COR_PLANETAS['Sol']}}))
        fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=350)
        st.plotly_chart(fig_g, use_container_width=True, config=plotly_config)

else:
    target = st.session_state.selecao
    try:
        p_data = df_planetas_apenas[df_planetas_apenas['Planeta'] == target].iloc[0]
        st.header(f"Exploração: {target.upper()}")
        
        comparativo = "superior" if p_data['Gravidade'] > 9.8 else "inferior"
        st.markdown(f'<div class="planeta-desc">Planeta {p_data["Tipo"]} com gravidade {comparativo} à da Terra.</div>', unsafe_allow_html=True)
        
        m1, m2, m3, m4, _ = st.columns([1, 1, 1, 1, 3])
        m1.metric("Distância Sol", f"{p_data['Distancia']}M km")
        m2.metric("Temp. Média", f"{p_data['Temperatura_Media']}°C")
        m3.metric("Luas", p_data['Luas'])
        m4.metric("Gravidade", f"{p_data['Gravidade']} m/s²")

        g1, g2 = st.columns(2)
        with g1:
            st.subheader("Diâmetro Comparativo (Terra/Júpiter)")
            comp_df = df_planetas_apenas[df_planetas_apenas['Planeta'].isin(['Terra', 'Júpiter', target])].drop_duplicates()
            # Usando o dicionário global para garantir que Terra, Júpiter e o Alvo usem as novas cores
            fig_comp = px.bar(comp_df, x='Planeta', y='Diametro', color='Planeta',
                             color_discrete_map=COR_PLANETAS)
            fig_comp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', height=350, dragmode='pan', showlegend=False)
            st.plotly_chart(fig_comp, use_container_width=True, config=plotly_config)
        with g2:
            st.subheader("Potencial Gravitacional")
            cor_alvo = COR_PLANETAS.get(target, '#ffdd00')
            # Barra do Gauge alterada para a cor específica do planeta selecionado
            fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=p_data['Gravidade'],
                                             gauge={'axis':{'range':[None, 30]}, 'bar':{'color': cor_alvo}}))
            fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=350)
            st.plotly_chart(fig_gauge, use_container_width=True, config=plotly_config)
    except IndexError:
        st.error("Erro ao carregar dados. Regresse ao Sistema Completo.")

st.markdown("---")
st.caption("Business Intelligence | BrunoJS Dev | Dados Astronômicos Referenciais")
