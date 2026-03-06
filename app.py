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

# --- ESTILO CSS ---
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

    /* Estilização dos Botões de Seleção */
    .stButton>button {
        background-color: #090024;
        color: #c9e4ff;
        border: 1px solid #150136;
        border-radius: 4px;
        width: 100%;
        height: 45px;
        transition: 0.2s;
        font-weight: 600;
        padding: 0;
        font-size: 0.85rem;
    }
    .stButton>button:hover {
        border-color: #ffdd00;
        color: #ffdd00;
    }

    /* Padding para os Filtros */
    .stMultiSelect {
        padding-top: 10px;
    }
    
    /* Estilo do Texto Descritivo */
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
# DataFrame apenas com os planetas para não quebrar os gráficos comparativos
df_planetas = df_original[df_original['Tipo'] != 'Estrela']

# --- HEADER ---
st.markdown(f'<a href="https://brunojsdev.github.io/meu-portfolio/" class="portfolio-btn">Portfolio</a>', unsafe_allow_html=True)

st.title("SISTEMA SOLAR | DATA INSIGHTS")

# --- NAVEGAÇÃO POR BOTÕES (TOP BAR) ---
# Criamos a lista na ordem exata e forçamos 10 colunas iguais para manter espaçamento padronizado
botoes_nav = ["SISTEMA COMPLETO", "SOL"] + df_planetas['Planeta'].tolist()
cols_nav = st.columns(10)

for i, btn_nome in enumerate(botoes_nav):
    if cols_nav[i].button(btn_nome.upper()):
        # Mapeia o botão SISTEMA COMPLETO para a string "Geral"
        st.session_state.selecao = "Geral" if btn_nome == "SISTEMA COMPLETO" else btn_nome

# Inicializar estado
if 'selecao' not in st.session_state:
    st.session_state.selecao = "Geral"

st.markdown("---")

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.selecao == "Geral":
    
    # Área de Filtros mais justa: Coluna 1 ocupa 2.5 (espaço exato para 3 tags) e a vazia ocupa 7.5
    col_f1, _ = st.columns([2.5, 7.5]) 
    with col_f1:
        filtro_tipo = st.multiselect(
            "Filtrar Exibição por Tipo:", 
            options=df_planetas['Tipo'].unique(), 
            default=df_planetas['Tipo'].unique()
        )
    
    df = df_planetas[df_planetas['Tipo'].isin(filtro_tipo)]
    st.write("")

    # KPIs: Espaço 1.8 para a Média de Gravidade garante que o texto não será cortado
    c1, c2, c3, c4, _ = st.columns([1, 1.8, 1, 1, 2.2])
    c1.metric("Planetas Ativos", len(df))
    c2.metric("Média de Gravidade", f"{df['Gravidade'].mean():.2f} m/s²")
    c3.metric("Satélites no Filtro", df['Luas'].sum())
    c4.metric("Escopo Visual", "Completo")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Diâmetro por Planeta (km)")
        fig_diam = px.bar(df.sort_values('Diametro'), x='Diametro', y='Planeta', orientation='h',
                         color='Diametro', color_continuous_scale=['#150136', '#5752ff', '#ffdd00'])
        fig_diam.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#c9e4ff', 
            showlegend=False,
            dragmode='pan'
        )
        st.plotly_chart(fig_diam, use_container_width=True)

    with col_right:
        st.subheader("Composição Planetária")
        fig_pie = px.pie(df, names='Tipo', hole=0.6, 
                         color='Tipo',
                         color_discrete_map={
                             'Rochoso': '#ff9900',   
                             'Gasoso': '#b388ff',    # Roxo Claro
                             'Gelo': '#150136'       
                         })
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#c9e4ff',
            dragmode='pan'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Intensidade Gravitacional por Planeta")
    fig_grav = go.Figure(data=[go.Bar(
        x=df['Planeta'], 
        y=df['Gravidade'],
        marker=dict(
            color=df['Gravidade'],
            colorscale=['#150136', '#5752ff', '#ffdd00'],
            line=dict(color='#5752ff', width=1)
        )
    )])
    fig_grav.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font_color='#c9e4ff',
        xaxis=dict(gridcolor='#150136'), 
        yaxis=dict(gridcolor='#150136'),
        dragmode='pan'
    )
    st.plotly_chart(fig_grav, use_container_width=True)

elif st.session_state.selecao == "Sol":
    # --- VISÃO EXCLUSIVA DO SOL ---
    p_data = df_original[df_original['Planeta'] == 'Sol'].iloc[0]
    
    st.header(f"Exploração: NOSSA ESTRELA ({p_data['Planeta'].upper()})")
    
    st.markdown(f"""
        <div class="planeta-desc">
            O Sol é a estrela central do Sistema Solar. Todos os outros corpos celestes orbitam ao seu redor. 
            Sua gravidade gigantesca é o que mantém o sistema unido, sendo cerca de 28 vezes mais forte que a da Terra.
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas adaptadas
    m1, m2, m3, m4, _ = st.columns([1, 1.2, 1, 1.2, 2.6])
    m1.metric("Tipo", "Estrela (Anã Amarela)")
    m2.metric("Diâmetro", f"{p_data['Diametro']:,} km".replace(',','.'))
    m3.metric("Temp. Superfície", f"{p_data['Temperatura_Media']}°C")
    m4.metric("Gravidade Esmagadora", f"{p_data['Gravidade']} m/s²")

    st.write("")
    g1, g2 = st.columns(2)

    with g1:
        st.subheader("Calor da Superfície")
        fig_temp = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_data['Temperatura_Media'],
            number = {'suffix': "°C", 'font': {'color': '#ff9900'}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 6000], 'tickcolor': "#c9e4ff"},
                'bar': {'color': "#ff3300"},
                'bgcolor': "#090024",
                'borderwidth': 2,
                'bordercolor': "#ff9900",
                'steps': [
                    {'range': [0, 2000], 'color': '#ffdd00'},
                    {'range': [2000, 4500], 'color': '#ff9900'}],
            }
        ))
        fig_temp.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#c9e4ff"}, height=350, dragmode='pan')
        st.plotly_chart(fig_temp, use_container_width=True)

    with g2:
        st.subheader("Potencial Gravitacional (Extremo)")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_data['Gravidade'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 300], 'tickcolor': "#c9e4ff"},
                'bar': {'color': "#ffdd00"},
                'bgcolor': "#090024",
                'borderwidth': 2,
                'bordercolor': "#5752ff",
                'steps': [
                    {'range': [0, 100], 'color': '#150136'},
                    {'range': [100, 250], 'color': '#090024'}],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#c9e4ff"}, height=350, dragmode='pan')
        st.plotly_chart(fig_gauge, use_container_width=True)

else:
    # --- VISÃO DETALHADA DOS PLANETAS ---
    target = st.session_state.selecao
    p_data = df_planetas[df_planetas['Planeta'] == target].iloc[0]
    
    st.header(f"Exploração: {target.upper()}")
    
    comparativo = "superior" if p_data['Gravidade'] > 9.8 else ("igual" if p_data['Gravidade'] == 9.8 else "inferior")
    st.markdown(f"""
        <div class="planeta-desc">
            O planeta {target} é classificado como {p_data['Tipo']}. 
            Sua gravidade é {comparativo} à da Terra.
        </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4, _ = st.columns([1, 1, 1, 1, 3])
    m1.metric("Posição vs Sol", f"{p_data['Distancia']} mi km")
    m2.metric("Temp. Média", f"{p_data['Temperatura_Media']}°C")
    m3.metric("Luas", p_data['Luas'])
    m4.metric("Gravidade", f"{p_data['Gravidade']} m/s²")

    st.write("")
    g1, g2 = st.columns(2)

    with g1:
        st.subheader("Escala de Diâmetro (Comparativa)")
        # Retorno à comparação entre o Alvo, Terra e Júpiter
        comp_df = df_planetas[df_planetas['Planeta'].isin(['Terra', 'Júpiter', target])].drop_duplicates()
        
        cores_mapa = {'Terra': '#5752ff', 'Júpiter': '#150136'}
        if target not in cores_mapa:
            cores_mapa[target] = '#b388ff' if p_data['Tipo'] == 'Gasoso' else '#ffdd00' 
            
        fig_comp = px.bar(comp_df, x='Planeta', y='Diametro', color='Planeta',
                         color_discrete_map=cores_mapa)
        fig_comp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#c9e4ff',
            height=350,       
            dragmode='pan'
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with g2:
        st.subheader("Potencial Gravitacional")
        
        # Limite fixo em 30 para os planetas já é suficiente, Júpiter tem 24.79
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_data['Gravidade'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 30], 'tickcolor': "#c9e4ff"},
                'bar': {'color': "#ffdd00"},
                'bgcolor': "#090024",
                'borderwidth': 2,
                'bordercolor': "#5752ff",
                'steps': [
                    {'range': [0, 10], 'color': '#150136'},
                    {'range': [10, 25], 'color': '#090024'}],
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            font={'color': "#c9e4ff"}, 
            height=350,       
            dragmode='pan'
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption(f"Business Intelligence | BrunoJS Dev | Dados Astronômicos Referenciais")
