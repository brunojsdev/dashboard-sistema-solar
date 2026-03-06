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
        padding: 0 5px;
    }
    .stButton>button:hover {
        border-color: #ffdd00;
        color: #ffdd00;
    }

    /* Padding para os Filtros e ajuste para alinhar em linha */
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

# --- HEADER ---
st.markdown(f'<a href="https://brunojsdev.github.io/meu-portfolio/" class="portfolio-btn">Portfolio</a>', unsafe_allow_html=True)

st.title("SISTEMA SOLAR | DATA INSIGHTS")

# --- NAVEGAÇÃO POR BOTÕES (TOP BAR) ---
planetas_lista = df_original['Planeta'].tolist()
# Cria colunas dinamicamente baseado na quantidade de corpos celestes + 1 (botão Geral)
cols_nav = st.columns(len(planetas_lista) + 1)

if cols_nav[0].button("SISTEMA COMPLETO"):
    st.session_state.selecao = "Geral"

for i, planeta in enumerate(planetas_lista):
    if cols_nav[i+1].button(planeta.upper()):
        st.session_state.selecao = planeta

# Inicializar estado
if 'selecao' not in st.session_state:
    st.session_state.selecao = "Geral"

st.markdown("---")

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.selecao == "Geral":
    
    # Área de Filtros com largura ideal para enfileirar
    col_f1, _, _ = st.columns([5, 2, 3]) 
    with col_f1:
        filtro_tipo = st.multiselect(
            "Filtrar Exibição por Tipo:", 
            options=df_original['Tipo'].unique(), 
            default=df_original['Tipo'].unique()
        )
    
    df = df_original[df_original['Tipo'].isin(filtro_tipo)]
    st.write("")

    # KPIs agrupados à esquerda para não ficarem demasiadamente espaçados
    # A última coluna vazia empurra as outras para perto
    c1, c2, c3, c4, _ = st.columns([1.2, 1.2, 1.2, 1.2, 4])
    c1.metric("Corpos Celestes", len(df))
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
            dragmode='pan' # Inicia com PAN
        )
        st.plotly_chart(fig_diam, use_container_width=True)

    with col_right:
        st.subheader("Composição Planetária")
        fig_pie = px.pie(df, names='Tipo', hole=0.6, 
                         color='Tipo',
                         color_discrete_map={
                             'Estrela': '#ffdd00',   # Amarelo Solar
                             'Rochoso': '#ff9900',   # Laranja
                             'Gasoso': '#b388ff',    # Roxo Claro
                             'Gelo': '#150136'       # Azul Escuro/Roxo profundo
                         })
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#c9e4ff',
            dragmode='pan' # Inicia com PAN
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Intensidade Gravitacional por Corpo Celeste")
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
        dragmode='pan' # Inicia com PAN
    )
    st.plotly_chart(fig_grav, use_container_width=True)

else:
    # --- VISÃO DETALHADA ---
    target = st.session_state.selecao
    p_data = df_original[df_original['Planeta'] == target].iloc[0]
    
    st.header(f"Exploração: {target.upper()}")
    
    comparativo = "superior" if p_data['Gravidade'] > 9.8 else ("igual" if p_data['Gravidade'] == 9.8 else "inferior")
    # Trocado "O planeta" por "O corpo celeste" para englobar o Sol corretamente
    st.markdown(f"""
        <div class="planeta-desc">
            O corpo celeste {target} é classificado como {p_data['Tipo']}. 
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
        # Compara selecionado com Terra e Sol 
        comp_df = df_original[df_original['Planeta'].isin(['Terra', 'Sol', target])].drop_duplicates()
        
        # Mapeamento dinâmico para garantir destaque no alvo
        cores_mapa = {'Terra': '#5752ff', 'Sol': '#ffdd00'}
        if target not in cores_mapa:
            cores_mapa[target] = '#b388ff' # Roxo claro para o alvo selecionado (se não for sol/terra)
            
        fig_comp = px.bar(comp_df, x='Planeta', y='Diametro', color='Planeta',
                         color_discrete_map=cores_mapa)
        fig_comp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#c9e4ff',
            height=350,       # Tamanho idêntico ao velocímetro
            dragmode='pan'    # Inicia com PAN
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with g2:
        st.subheader("Potencial Gravitacional")
        
        # Ajuste dinâmico do range do velocímetro para comportar a gravidade do Sol (274)
        max_gauge = max(30, int(p_data['Gravidade'] * 1.2))
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_data['Gravidade'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, max_gauge], 'tickcolor': "#c9e4ff"},
                'bar': {'color': "#ffdd00"},
                'bgcolor': "#090024",
                'borderwidth': 2,
                'bordercolor': "#5752ff",
                'steps': [
                    {'range': [0, max_gauge*0.33], 'color': '#150136'},
                    {'range': [max_gauge*0.33, max_gauge*0.83], 'color': '#090024'}],
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            font={'color': "#c9e4ff"}, 
            height=350,       # Tamanho idêntico ao gráfico de barras
            dragmode='pan'    # Inicia com PAN
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption(f"Business Intelligence | BrunoJS Dev | Dados Astronômicos Referenciais")
