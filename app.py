import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Configuração da Página
st.set_page_config(
    page_title="Explorador do Sistema Solar",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS Customizado
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #f0f2f6; }
    .stMetricValue { color: #00ccff !important; }
</style>
""", unsafe_allow_html=True)

# 3. Tratamento dos Dados
def carregar_dados():
    data = {
        "Planeta": ["Mercúrio", "Vênus", "Terra", "Marte", "Júpiter", "Saturno", "Urano", "Netuno"],
        "Tipo": ["Rochoso", "Rochoso", "Rochoso", "Rochoso", "Gigante Gasoso", "Gigante Gasoso", "Gigante de Gelo", "Gigante de Gelo"],
        "Diâmetro (km)": [4879, 12104, 12742, 6779, 140000, 116000, 51000, 49000],
        "Periodo Orbital (Texto)": ["3 meses", "7 meses", "1 ano", "2 anos", "12 anos", "29 anos", "84 anos", "165 anos"],
        "Periodo Orbital (Anos Terrestres)": [0.24, 0.62, 1.0, 1.88, 11.86, 29.45, 84.0, 164.8],
        "Distancia Sol (UA)": [0.4, 0.7, 1.0, 1.5, 5.2, 9.5, 19.8, 30.0],
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

# 4. Barra Lateral
st.sidebar.title("Painel de Controle 🚀")
modo_visualizacao = st.sidebar.radio("Escolha a visão:", ["Visão Geral", "Detalhes", "Comparativo"])

# 5. Lógica das Telas
if modo_visualizacao == "Visão Geral":
    st.title("☀️ O Sistema Solar")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("O Sistema Solar é nossa família cósmica de 4,6 bilhões de anos.")
        st.subheader("O Sol: O Chefe da Família")
        st.write("Representa 99,8% de toda a massa do Sistema Solar.")
    
    # Gráfico de Órbita
    fig_orbit = go.Figure()
    fig_orbit.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=40, color='yellow'), name='Sol'))
    for i, row in df.iterrows():
        dist = np.log10(row['Distancia Sol (UA)'] * 10 + 1) * 10
        angle = i * (2 * np.pi / 8)
        fig_orbit.add_trace(go.Scatter(x=[dist * np.cos(angle)], y=[dist * np.sin(angle)], 
                                     mode='markers', marker=dict(size=12, color=row['Cor']), name=row['Planeta']))
    fig_orbit.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig_orbit, use_container_width=True)

elif modo_visualizacao == "Detalhes":
    planeta = st.selectbox("Selecione um planeta:", df["Planeta"])
    dados = df[df["Planeta"] == planeta].iloc[0]
    st.header(f"探索 {planeta}")
    st.metric("Diâmetro", f"{dados['Diâmetro (km)']} km")
    st.info(dados["Fato Divertido"])

else:
    st.title("📊 Comparativo")
    fig = px.bar(df, x="Planeta", y="Diâmetro (km)", color="Planeta", color_discrete_sequence=df["Cor"], template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Desenvolvido com Streamlit")
