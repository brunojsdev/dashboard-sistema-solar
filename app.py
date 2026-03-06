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
    .stApp { background-color: #040014; color: #c9e4ff; }
    
    /* FIX NAVEGAÇÃO: Impede sobreposição e garante leitura */
    div[data-testid="stHorizontalBlock"]:has(button) {
        gap: 8px !important;
    }
    div[data-testid="stColumn"]:has(button) {
        min-width: fit-content !important;
        flex: unset !important;
    }
    .stButton > button {
        background-color: #090024;
        color: #c9e4ff;
        border: 1px solid #150136;
        padding: 4px 12px;
        white-space: nowrap;
    }
    .stButton > button:hover { border-color: #ffdd00; color: #ffdd00; }

    /* FILTROS: Garante os 3 em uma linha */
    .stMultiSelect div[data-baseweb="select"] {
        min-width: 450px !important;
    }
    
    h1, h2, h3 { color: #ffdd00 !important; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
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

df_all = get_data()
df_planets = df_all[df_all['Tipo'] != 'Estrela']

# --- HEADER E NAVEGAÇÃO ---
st.title("SISTEMA SOLAR | DATA INSIGHTS")

botoes = ["SISTEMA COMPLETO", "SOL", "MERCÚRIO", "VÊNUS", "TERRA", "MARTE", "JÚPITER", "SATURNO", "URANO", "NETUNO"]
if 'sel' not in st.session_state: st.session_state.sel = "Geral"

nav_cols = st.columns(len(botoes))
for i, nome in enumerate(botoes):
    with nav_cols[i]:
        if st.button(nome): st.session_state.sel = "Geral" if nome == "SISTEMA COMPLETO" else nome.title()

st.markdown("---")
plotly_config = {'displayModeBar': False}

# --- TELAS ---
if st.session_state.sel == "Geral":
    c_f, _ = st.columns([4.5, 5.5])
    with c_f:
        f_tipo = st.multiselect("Filtrar por Tipo:", options=df_planets['Tipo'].unique(), default=list(df_planets['Tipo'].unique()))
    
    df = df_planets[df_planets['Tipo'].isin(f_tipo)]
    
    k1, k2, k3, k4, _ = st.columns([1, 2, 1, 1, 2])
    k1.metric("Corpos", len(df))
    k2.metric("Média Gravidade", f"{df['Gravidade'].mean():.2f} m/s²")
    k3.metric("Luas", df['Luas'].sum())
    k4.metric("Status", "Online")

    l, r = st.columns(2)
    with l:
        st.subheader("Diâmetro (km)")
        fig = px.bar(df.sort_values('Diametro'), x='Diametro', y='Planeta', orientation='h', color='Diametro', color_continuous_scale='Viridis')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', height=350)
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    with r:
        st.subheader("Tipologia")
        fig = px.pie(df, names='Tipo', hole=0.5)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', height=350)
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

elif st.session_state.sel == "Sol":
    data = df_all[df_all['Planeta'] == 'Sol'].iloc[0]
    st.header("ESTRELA: SOL")
    
    m1, m2, m3, m4, _ = st.columns([1, 1, 1, 1, 2])
    m1.metric("Tipo", "G2V")
    m2.metric("Calor", "5.500°C")
    m3.metric("Massa", "99.8%")
    m4.metric("Gravidade", "274 m/s²")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Temperatura da Superfície")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=data['Temperatura_Media'], number={'suffix':"°C"},
                                     gauge={'axis':{'range':[None, 6000]}, 'bar':{'color':"#ff3300"}}))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=380, margin=dict(t=0, b=0))
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    with g2:
        # TÍTULO INTEGRADO NO PLOTLY PARA ALINHAMENTO ABSOLUTO
        fig = go.Figure(go.Indicator(mode="gauge+number", value=data['Gravidade'],
                                     gauge={'axis':{'range':[None, 300]}, 'bar':{'color':"#ffdd00"}}))
        fig.update_layout(
            title={'text': "Potencial Gravitacional", 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 20, 'color': '#ffdd00'}},
            paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=380, margin=dict(t=60, b=0)
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

else:
    target = st.session_state.sel
    data = df_planets[df_planets['Planeta'] == target].iloc[0]
    st.header(f"PLANETA: {target.upper()}")
    
    m1, m2, m3, m4, _ = st.columns([1, 1, 1, 1, 2])
    m1.metric("Distância", f"{data['Distancia']}M km")
    m2.metric("Temp.", f"{data['Temperatura_Media']}°C")
    m3.metric("Luas", data['Luas'])
    m4.metric("Gravidade", f"{data['Gravidade']} m/s²")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Comparativo de Diâmetro")
        c_df = df_planets[df_planets['Planeta'].isin(['Terra', 'Júpiter', target])].drop_duplicates()
        fig = px.bar(c_df, x='Planeta', y='Diametro', color='Planeta')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9e4ff', height=380)
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    with g2:
        # TÍTULO INTEGRADO NO PLOTLY PARA ALINHAMENTO ABSOLUTO
        fig = go.Figure(go.Indicator(mode="gauge+number", value=data['Gravidade'],
                                     gauge={'axis':{'range':[None, 30]}, 'bar':{'color':"#ffdd00"}}))
        fig.update_layout(
            title={'text': "Potencial Gravitacional", 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 20, 'color': '#ffdd00'}},
            paper_bgcolor='rgba(0,0,0,0)', font={'color':"#c9e4ff"}, height=380, margin=dict(t=60, b=0)
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

st.caption("BrunoJS Dev | Data Insights Solar")
