import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Data Solar | BrunoJS Dev",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO CSS REFINADO ---
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

    /* Ajuste para botões em linha com espaçamento uniforme */
    [data-testid="stHorizontalBlock"] {
        gap: 0.5rem;
    }

    .stButton>button {
        background-color: #090024;
        color: #c9e4ff;
        border: 1px solid #150136;
        border-radius: 4px;
        transition: 0.2s;
        font-weight: 600;
        width: auto;
        min-width: 80px;
        white-space: nowrap;
    }
    
    .stButton>button:hover {
        border-color: #ffdd00;
        color: #ffdd00;
    }

    .stMultiSelect {
        padding-top: 10px;
    }
    
    .planeta-desc {
        font-size: 1.2rem;
        color: #c9e4ff;
        margin-bottom: 25px;
        border-left: 3px solid #5752ff;
        padding-left: 15px;
        font-style: italic;
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
df_planetas = df_original[df_original['Tipo'] != 'Estrela']

# --- HEADER ---
st.markdown(f'<a href="https://brunojsdev.github.io/meu-portfolio/" class="portfolio-btn">Portfolio</a>', unsafe_allow_html=True)
st.title("SISTEMA SOLAR | DATA INSIGHTS")

# --- NAVEGAÇÃO (TOP BAR) ---
# Usando colunas proporcionais ao texto para evitar o visual aleatório
botoes_nav = ["SISTEMA COMPLETO", "SOL"] + df_planetas['Planeta'].tolist()
# Criamos 10 colunas, mas o Streamlit agora lida melhor com o CSS injetado acima
cols_nav = st.columns([1.5, 0.8, 1, 1, 1, 1, 1, 1, 1, 1])

for i, btn_nome in enumerate(botoes_nav):
    if cols_nav[i].button(btn_nome.upper()):
        st.session_state.selecao = "Geral" if btn_nome == "SISTEMA COMPLETO" else btn_nome

if 'selecao' not in st.session_state:
    st.session_state.selecao = "Geral"

st.markdown("---")

# Configuração padrão para remover a Modebar dos gráficos
plotly_config = {'displayModeBar': False}

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.selecao == "Geral":
    
    col_f1, _ = st.columns([2.2, 7.8]) 
    with col_f1:
        filtro_tipo = st.multiselect(
            "Filtrar por Tipo:", 
            options=df_planetas['Tipo'].unique(), 
            default=df_planetas['Tipo'].unique()
        )
    
    df = df_planetas[df_planetas['Tipo'].isin(filtro_tipo)]
    st.write("")

    # KPIs com espaçamento otimizado para não cortar o texto
    c1, c2, c3, c4, _ = st.columns([1, 2, 1, 1, 2])
    c1.metric("Planetas", len(df))
    c2.metric("Média de Gravidade", f"{df['Gravidade'].mean():.2f} m/s²")
    c3.metric("Total de Luas", df['Luas'].sum())
    c4.metric("Escopo", "Completo")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Diâmetro por Planeta (km)")
        fig_diam = px.bar(df.sort_values('Diametro'), x='Diametro', y='Planeta', orientation='h',
                         color='Diametro', color_continuous_scale=['#150136', '#5752ff', '#ffdd00'])
        fig_diam.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', showlegend=False, dragmode='pan')
        st.plotly_chart(fig_diam, use_container_width=True, config=plotly_config)

    with col_right:
        st.subheader("Distribuição por Composição")
        fig_pie = px.pie(df, names='Tipo', hole=0.6, 
                         color='Tipo',
                         color_discrete_map={'Rochoso': '#ff9900', 'Gasoso': '#b388ff', 'Gelo': '#150136'})
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', dragmode='pan')
        st.plotly_chart(fig_pie, use_container_width=True, config=plotly_config)

    st.subheader("Intensidade Gravitacional")
    fig_grav = go.Figure(data=[go.Bar(
        x=df['Planeta'], y=df['Gravidade'],
        marker=dict(color=df['Gravidade'], colorscale=['#150136', '#5752ff', '#ffdd00'])
    )])
    fig_grav.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', dragmode='pan')
    st.plotly_chart(fig_grav, use_container_width=True, config=plotly_config)

elif st.session_state.selecao == "Sol":
    p_data = df_original[df_original['Planeta'] == 'Sol'].iloc[0]
    st.header(f"Exploração: {p_data['Planeta'].upper()}")
    
    st.markdown(f'<div class="planeta-desc">O Sol contém 99.8% da massa do Sistema Solar. É uma esfera quase perfeita de plasma quente.</div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4, _ = st.columns([1, 1.2, 1, 1.2, 2.6])
    m1.metric("Tipo", "Estrela G2V")
    m2.metric("Diâmetro", f"{p_data['Diametro']:,}".replace(',','.'))
    m3.metric("Temperatura", f"{p_data['Temperatura_Media']}°C")
    m4.metric("Gravidade", f"{p_data['Gravidade']} m/s²")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Temperatura da Superfície")
        fig_t = go.Figure(go.Indicator(mode="gauge+number", value=p_data['Temperatura_Media'], number={'suffix':"°C"},
                                     gauge={'axis':{'range':[None, 6000]}, 'bar':{'color':"#ff3300"}, 'bgcolor':"#090024"}))
        fig_t.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=350)
        st.plotly_chart(fig_t, use_container_width=True, config=plotly_config)
    with g2:
        st.subheader("Gravidade Solar")
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=p_data['Gravidade'],
                                     gauge={'axis':{'range':[None, 300]}, 'bar':{'color':"#ffdd00"}}))
        fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=350)
        st.plotly_chart(fig_g, use_container_width=True, config=plotly_config)

else:
    target = st.session_state.selecao
    p_data = df_planetas[df_planetas['Planeta'] == target].iloc[0]
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
        comp_df = df_planetas[df_planetas['Planeta'].isin(['Terra', 'Júpiter', target])].drop_duplicates()
        fig_comp = px.bar(comp_df, x='Planeta', y='Diametro', color='Planeta',
                         color_discrete_map={'Terra': '#5752ff', 'Júpiter': '#150136', target: '#ffdd00'})
        fig_comp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', height=350, dragmode='pan')
        st.plotly_chart(fig_comp, use_container_width=True, config=plotly_config)
    with g2:
        st.subheader("Potencial Gravitacional")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=p_data['Gravidade'],
                                         gauge={'axis':{'range':[None, 30]}, 'bar':{'color':"#ffdd00"}}))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=350)
        st.plotly_chart(fig_gauge, use_container_width=True, config=plotly_config)

st.markdown("---")
st.caption("Business Intelligence | BrunoJS Dev | Dados Astronômicos Referenciais")
