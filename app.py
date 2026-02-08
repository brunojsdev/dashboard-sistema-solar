import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Configuração da Página (Deve ser o primeiro comando)
st.set_page_config(
    page_title="Explorador do Sistema Solar",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS Customizado para dar uma estética "Espacial"
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #f0f2f6;
    }
    .stMetricValue {
        color: #00ccff !important;
    }
    .highlight {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# 3. Tratamento dos Dados (Baseado no seu texto)
def carregar_dados():
    data = {
        "Planeta": ["Mercúrio", "Vênus", "Terra", "Marte", "Júpiter", "Saturno", "Urano", "Netuno"],
        "Tipo": ["Rochoso", "Rochoso", "Rochoso", "Rochoso", "Gigante Gasoso", "Gigante Gasoso", "Gigante de Gelo", "Gigante de Gelo"],
        "Diâmetro (km)": [4879, 12104, 12742, 6779, 140000, 116000, 51000, 49000],
        "Periodo Orbital (Texto)": ["3 meses", "7 meses", "1 ano", "2 anos", "12 anos", "29 anos", "84 anos", "165 anos"],
        "Periodo Orbital (Anos Terrestres)": [0.24, 0.62, 1.0, 1.88, 11.86, 29.45, 84.0, 164.8],
        "Distancia Sol (UA)": [0.4, 0.7, 1.0, 1.5, 5.2, 9.5, 19.8, 30.0], # Unidades Astronômicas aproximadas
        "Cor": ["#A5A5A5", "#E3BB76", "#2271B3", "#E27B58", "#D39C7E", "#C5AB6E", "#BBE1E4", "#3e54e8"],
        "Fato Divertido": [
            "Dia super quente, noite gelada; cheio de buracos como a Lua.",
            "Mais quente que forno; gira ao contrário.",
            "Só com vida, água e ar bom; Lua como companheira.",
            "Maior vulcão e canyon do sistema; rios no passado?",
            "Maior de todos; olho vermelho é uma tempestade gigante.",
            "Anéis de gelo como brinco; lua Titã tem lagos de gasolina.",
            "Deita de lado (gira torto); super frio.",
            "Ventos mais fortes do sistema; outra mancha escura de tempestade."
        ],
        "Luas": [0, 0, 1, 2, 95, 146, 27, 14]
    }
    return pd.DataFrame(data)

df = carregar_dados()

# 4. Barra Lateral de Navegação
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Solar_sys8.jpg", caption="Nossa Casa Cósmica")
st.sidebar.title("Painel de Controle 🚀")

modo_visualizacao = st.sidebar.radio(
    "Escolha a visão:",
    ["Visão Geral do Sistema", "Detalhes do Planeta", "Comparativo de Dados"]
)

# Filtro de tipo (apenas para curiosidade na sidebar)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔭 Filtros Rápidos")
filtro_tipo = st.sidebar.multiselect(
    "Filtrar por tipo:", 
    options=df["Tipo"].unique(),
    default=df["Tipo"].unique()
)

# 5. Conteúdo Principal

# --- TELA 1: VISÃO GERAL ---
if modo_visualizacao == "Visão Geral do Sistema":
    st.title("☀️ O Sistema Solar: Nossa Família Cósmica")
    
    st.markdown("""
    > "Tudo começou há 4,6 bilhões de anos, quando uma nuvem gigante de gás e poeira se juntou pela gravidade."
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("O Sol: O Chefe da Família")
        st.write("""
        Imagine o Sol como uma enorme bola de fogo gigante (**1,4 milhão de km de diâmetro**). 
        Ele representa **99,8% de toda a massa** do Sistema Solar e mantém tudo unido com sua gravidade.
        Lá no fundo, átomos de hidrogênio viram hélio, criando a luz que chega até nós.
        """)
    
    with col2:
        st.info("🌟 **Curiosidade:** O Sol é maior que 1 milhão de Terras juntas!")

    st.markdown("---")
    
    st.subheader("🪐 Mapa Orbital (Representação)")
    st.caption("A escala de distância está adaptada para visualização (logarítmica).")
    
    # Criando um gráfico de órbita simulado com Plotly
    fig_orbit = go.Figure()
    
    # Adicionar o Sol
    fig_orbit.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers', 
        marker=dict(size=40, color='yellow', line=dict(width=2, color='orange')),
        name='Sol'
    ))
    
    # Adicionar Planetas (Simulando posição em círculo para estética)
    # Usamos np.log para a distância não ficar impossível de ver na tela
    for i, row in df.iterrows():
        dist = np.log10(row['Distancia Sol (UA)'] * 10 + 1) * 10 
        angle = np.random.uniform(0, 2 * np.pi) # Posição aleatória na órbita
        x = dist * np.cos(angle)
        y = dist * np.sin(angle)
        
        # Desenhar órbita
        theta = np.linspace(0, 2*np.pi, 100)
        x_orbit = dist * np.cos(theta)
        y_orbit = dist * np.sin(theta)
        
        fig_orbit.add_trace(go.Scatter(
            x=x_orbit, y=y_orbit, mode='lines', 
            line=dict(color='gray', width=0.5, dash='dot'), 
            hoverinfo='skip', showlegend=False
        ))
        
        # Desenhar Planeta
        fig_orbit.add_trace(go.Scatter(
            x=[x], y=[y], mode='markers',
            marker=dict(size=row['Diâmetro (km)']/4000 + 5, color=row['Cor']), # Tamanho relativo ajustado
            name=row['Planeta'],
            text=f"{row['Planeta']}<br>{row['Fato Divertido']}",
            hoverinfo='text'
        ))

    fig_orbit.update_layout(
        template="plotly_dark",
        showlegend=True,
        height=600,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_orbit, use_container_width=True)

    # Seção de Outros Corpos
    with st.expander("☄️ Ver outros membros da família (Luas, Cometas, Asteroides)"):
        c1, c2, c3 = st.columns(3)
        c1.markdown("**Luas & Satélites**\nJúpiter tem 95 e Saturno 146! Algumas escondem oceanos sob o gelo.")
        c2.markdown("**Cinturão de Asteroides**\nPedras entre Marte e Júpiter, sobras da 'construção' do sistema.")
        c3.markdown("**Cometas & Cinturão de Kuiper**\nBolas de gelo sujo distantes. Plutão mora aqui!")

# --- TELA 2: DETALHES DO PLANETA ---
elif modo_visualizacao == "Detalhes do Planeta":
    st.title("🔭 Explorador Planetário")
    
    planeta_selecionado = st.selectbox("Selecione um planeta para investigar:", df["Planeta"])
    
    # Filtrar dados
    dados_planeta = df[df["Planeta"] == planeta_selecionado].iloc[0]
    
    # Layout de colunas
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        # Simulando uma "imagem" com um gráfico circular colorido
        fig_p = go.Figure(go.Scatter(
            x=[0], y=[0], mode='markers',
            marker=dict(size=150, color=dados_planeta['Cor'])
        ))
        fig_p.update_layout(
            template="plotly_dark", xaxis_visible=False, yaxis_visible=False, 
            margin=dict(l=0,r=0,t=0,b=0), height=300, bg_color='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_p, use_container_width=True)
    
    with col_info:
        st.subheader(f"{dados_planeta['Planeta']} ({dados_planeta['Tipo']})")
        st.markdown(f"**Fato Divertido:** _{dados_planeta['Fato Divertido']}_")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Diâmetro", f"{dados_planeta['Diâmetro (km)']:,.0f} km")
        m2.metric("Ano (Translação)", dados_planeta['Periodo Orbital (Texto)'])
        m3.metric("Luas Conhecidas", dados_planeta['Luas'])
        
        st.progress(dados_planeta['Distancia Sol (UA)'] / 30.0)
        st.caption(f"Distância relativa ao Sol (Comparado a Netuno)")

    st.markdown("### Contexto de Exploração")
    if planeta_selecionado == "Marte":
        st.success("Robôs em Marte caçam sinais de vida antiga e exploram o maior vulcão do sistema!")
    elif planeta_selecionado in ["Júpiter", "Saturno", "Urano", "Netuno"]:
        st.info("As naves Voyager voaram por aqui e tiraram fotos incríveis antes de sair do sistema.")
    elif planeta_selecionado == "Terra":
        st.success("O único lugar conhecido com vida, água líquida e ar respirável. Cuide bem dele! 🌍")
    else:
        st.warning("Um ambiente hostil e fascinante esperando para ser melhor compreendido.")

# --- TELA 3: COMPARATIVO ---
elif modo_visualizacao == "Comparativo de Dados":
    st.title("📊 Dados Comparativos")
    st.markdown("Veja como os planetas se comparam em tamanho e tempo.")
    
    tab1, tab2 = st.tabs(["Tamanho (Diâmetro)", "Duração do Ano"])
    
    with tab1:
        fig_bar = px.bar(
            df, x="Planeta", y="Diâmetro (km)", color="Planeta",
            color_discrete_sequence=df["Cor"],
            title="Comparação de Tamanho (Diâmetro em km)",
            template="plotly_dark"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with tab2:
        # Gráfico de dispersão para mostrar a relação distância vs tempo
        fig_scat = px.scatter(
            df, x="Distancia Sol (UA)", y="Periodo Orbital (Anos Terrestres)",
            size="Diâmetro (km)", color="Planeta",
            color_discrete_sequence=df["Cor"],
            hover_name="Planeta",
            title="Quanto mais longe, mais o ano demora (Leis de Kepler)",
            template="plotly_dark",
            labels={"Distancia Sol (UA)": "Distância do Sol (Unidades Astronômicas)"}
        )
        st.plotly_chart(fig_scat, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido com Python & Streamlit | Baseado em dados do Sistema Solar 🌌")
```
