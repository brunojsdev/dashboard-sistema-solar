import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Data Solar | Business Intelligence",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO CSS (Sua Paleta + UX Melhorada) ---
st.markdown("""
<style>
    /* Reset e Fundo */
    .stApp {
        background-color: #040014;
        color: #c9e4ff;
    }
    
    /* Botão Portfolio no Topo */
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

    /* Títulos e Labels */
    h1, h2, h3 {
        color: #ffdd00 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Estilização dos Botões de Seleção (Navegação) */
    .stButton>button {
        background-color: #090024;
        color: #c9e4ff;
        border: 1px solid #150136;
        border-radius: 4px;
        width: 100%;
        height: 45px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        border-color: #ffdd00;
        color: #ffdd00;
    }
    .stButton>button:focus {
        background-color: #5752ff !important;
        color: white !important;
    }

    /* Ajuste de métricas */
    [data-testid="stMetricValue"] {
        color: #ffdd00 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE ---
@st.cache_data
def get_data():
    data = {
        'Planeta': ['Mercúrio', 'Vênus', 'Terra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Netuno'],
        'Tipo': ['Rochoso', 'Rochoso', 'Rochoso', 'Rochoso', 'Gasoso', 'Gasoso', 'Gelo', 'Gelo'],
        'Distancia': [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0],
        'Gravidade': [3.7, 8.87, 9.8, 3.71, 24.79, 10.44, 8.69, 11.15],
        'Diametro': [4879, 12104, 12742, 6779, 139820, 116460, 50724, 49244],
        'Luas': [0, 0, 1, 2, 95, 146, 27, 14],
        'Temperatura_Media': [167, 464, 15, -65, -110, -140, -195, -200]
    }
    return pd.DataFrame(data)

df_original = get_data()

# --- HEADER E NAVEGAÇÃO ---
st.markdown(f'<a href="https://brunojsdev.github.io/meu-portfolio/" class="portfolio-btn">Portfolio</a>', unsafe_allow_html=True)

st.title("SISTEMA SOLAR | DATA INSIGHTS")
st.write("Análise comparativa de corpos celestes e métricas gravitacionais.")

# --- BARRA DE FILTROS ---
with st.container():
    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    with col_f1:
        filtro_tipo = st.multiselect("Filtrar por Tipo:", options=df_original['Tipo'].unique(), default=df_original['Tipo'].unique())
    
    # Aplicar Filtros
    df = df_original[df_original['Tipo'].isin(filtro_tipo)]

st.markdown("---")

# --- SISTEMA DE NAVEGAÇÃO POR CLIQUE (SEM ENTER) ---
# Usamos colunas para criar um "menu" de planetas
cols_nav = st.columns(9)
if cols_nav[0].button("SISTEMA TOTAL"):
    st.session_state.selecao = "Geral"

for i, planeta in enumerate(df_original['Planeta']):
    if cols_nav[i+1].button(planeta.upper()):
        st.session_state.selecao = planeta

# Inicializar estado caso não exista
if 'selecao' not in st.session_state:
    st.session_state.selecao = "Geral"

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.selecao == "Geral":
    
    # Dash Principal
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Planetas em Exibição", len(df))
    c2.metric("Média de Gravidade", f"{df['Gravidade'].mean():.2f} m/s²")
    c3.metric("Total de Satélites", df['Luas'].sum())
    c4.metric("Maior Diâmetro", f"{df['Diametro'].max():,} km")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Diâmetro por Planeta (Escala Real)")
        fig_diam = px.bar(df.sort_values('Diametro'), x='Diametro', y='Planeta', orientation='h',
                         color='Diametro', color_continuous_scale=['#150136', '#5752ff', '#ffdd00'])
        fig_diam.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', showlegend=False)
        st.plotly_chart(fig_diam, use_container_width=True)

    with col_right:
        st.subheader("Distribuição por Composição")
        fig_pie = px.pie(df, names='Tipo', hole=0.6, color_discrete_sequence=['#5752ff', '#ffdd00', '#ff9900'])
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Ranking de Gravidade Relativa")
    # Gráfico de barras com gradiente visual via Plotly
    fig_grav = go.Figure(data=[go.Bar(
        x=df['Planeta'], 
        y=df['Gravidade'],
        marker=dict(
            color=df['Gravidade'],
            colorscale=['#150136', '#5752ff', '#ffdd00'],
            line=dict(color='#5752ff', width=1)
        )
    )])
    fig_grav.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff',
                          xaxis=dict(gridcolor='#150136'), yaxis=dict(gridcolor='#150136'))
    st.plotly_chart(fig_grav, use_container_width=True)

else:
    # --- VISÃO DETALHADA DO PLANETA ---
    target = st.session_state.selecao
    p_data = df_original[df_original['Planeta'] == target].iloc[0]
    
    st.header(f"Exploração: {target.upper()}")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Posição vs Sol", f"{p_data['Distancia']} mi km")
    m2.metric("Temp. Média", f"{p_data['Temperatura_Media']}°C")
    m3.metric("Luas", p_data['Luas'])
    m4.metric("Gravidade", f"{p_data['Gravidade']} m/s²")

    g1, g2 = st.columns(2)

    with g1:
        st.subheader("Comparativo de Diâmetro")
        # Gráfico comparando o planeta selecionado com a Terra e Júpiter
        comp_df = df_original[df_original['Planeta'].isin(['Terra', 'Júpiter', target])]
        fig_comp = px.bar(comp_df, x='Planeta', y='Diametro', color='Planeta',
                         color_discrete_map={target: '#ffdd00', 'Terra': '#5752ff', 'Júpiter': '#150136'})
        fig_comp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff')
        st.plotly_chart(fig_comp, use_container_width=True)

    with g2:
        st.subheader("Métricas de Orbita")
        st.info(f"O planeta {target} é classificado como {p_data['Tipo']}. "
                f"Sua gravidade é {'superior' if p_data['Gravidade'] > 9.8 else 'inferior'} à da Terra.")
        
        # Gráfico de Radar ou Simples Gauge para Gravidade
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_data['Gravidade'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Intensidade Gravitacional", 'font': {'color': '#c9e4ff'}},
            gauge = {
                'axis': {'range': [None, 30], 'tickcolor': "#c9e4ff"},
                'bar': {'color': "#ffdd00"},
                'bgcolor': "#090024",
                'borderwidth': 2,
                'bordercolor': "#5752ff",
                'steps': [
                    {'range': [0, 10], 'color': '#150136'},
                    {'range': [10, 20], 'color': '#090024'}],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#c9e4ff"})
        st.plotly_chart(fig_gauge, use_container_width=True)

# Rodapé simples
st.markdown("---")
st.caption(f"Análise de dados gerada para o portfolio de BrunoJS Dev.")
