import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Configuração de Interface Técnica
st.set_page_config(
    page_title="ASTRO-DATA | Helios System",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilização Industrial/Espacial (CSS Customizado)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp {
        background-color: #05070a;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .data-block {
        background: rgba(16, 20, 25, 0.8);
        border: 1px solid #1e262f;
        padding: 1.5rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }

    .tech-header {
        color: #00e5ff;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
        border-bottom: 1px solid #1e262f;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem !important;
        color: #ffffff !important;
    }
    
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Base de Dados Técnica (Métricas Reais)
def load_technical_data():
    data = {
        "Planeta": ["Mercúrio", "Vênus", "Terra", "Marte", "Júpiter", "Saturno", "Urano", "Netuno"],
        "Classificação": ["Telúrico", "Telúrico", "Telúrico", "Telúrico", "Gigante Gasoso", "Gigante Gasoso", "Gigante Gelado", "Gigante Gelado"],
        "Diâmetro (km)": [4879, 12104, 12742, 6779, 140000, 116000, 51000, 49000],
        "Período Sideral": ["87.97 d", "224.7 d", "365.26 d", "1.88 a", "11.86 a", "29.45 a", "84.02 a", "164.79 a"],
        "Distância (UA)": [0.39, 0.72, 1.0, 1.52, 5.20, 9.54, 19.22, 30.06],
        "Velocidade Orbital (km/s)": [47.4, 35.0, 29.8, 24.1, 13.1, 9.7, 6.8, 5.4],
        "Cor_Hex": ["#707070", "#e3bb76", "#1565c0", "#c62828", "#ef6c00", "#f9a825", "#00acc1", "#1a237e"],
        "Gravidade (m/s²)": [3.7, 8.87, 9.81, 3.71, 24.79, 10.44, 8.69, 11.15],
        "Satélites": [0, 0, 1, 2, 95, 146, 27, 14]
    }
    return pd.DataFrame(data)

df = load_technical_data()

# --- HEADER TÉCNICO ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("SOLAR SYSTEM DATA INTERFACE")
    st.caption("PROTOCOLO DE MONITORAMENTO ASTROMÉTRICO V.4.6.0 | COORDINATES: HELIOCENTRIC J2000")
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("🛰️ **STATUS:** OPERACIONAL")

st.markdown("---")

# --- VISUALIZAÇÃO DE ÓRBITAS ---
col_map, col_stats = st.columns([2, 1])

with col_map:
    st.markdown('<p class="tech-header">Projeção de Mecânica Orbital (UA)</p>', unsafe_allow_html=True)
    
    fig_orbit = go.Figure()

    # Helios (Sol central)
    fig_orbit.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        marker=dict(size=30, color='#FFCC00', symbol='hexagram-open'),
        name="HELIOS (G2V)", 
        hoverinfo="text", 
        text="HELIOS (G2V)<br>Massa: 1.989 × 10^30 kg"
    ))

    for i, row in df.iterrows():
        r = row['Distância (UA)']
        r_vis = np.log10(r * 10 + 1) * 5 
        theta = np.linspace(0, 2*np.pi, 100)
        
        fig_orbit.add_trace(go.Scatter(
            x=r_vis * np.cos(theta), y=r_vis * np.sin(theta),
            mode='lines', line=dict(color='#1e262f', width=1, dash='dot'),
            showlegend=False, hoverinfo='skip'
        ))
        
        angle = i * (np.pi / 4)
        fig_orbit.add_trace(go.Scatter(
            x=[r_vis * np.cos(angle)], y=[r_vis * np.sin(angle)],
            mode='markers',
            marker=dict(size=10, color=row['Cor_Hex'], line=dict(width=1, color='white')),
            name=row['Planeta']
        ))

    fig_orbit.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_orbit, use_container_width=True)

with col_stats:
    st.markdown('<p class="tech-header">Especificações de Alvo</p>', unsafe_allow_html=True)
    alvo = st.selectbox("IDENTIFICAR CORPO CELESTE:", df["Planeta"])
    data_alvo = df[df["Planeta"] == alvo].iloc[0]
    
    st.markdown(f"""
    <div class="data-block">
        <p style="color:#00e5ff; font-size:0.75rem; margin-bottom:5px; letter-spacing:1px;">CLASSIFICAÇÃO ASTROFÍSICA</p>
        <h2 style="margin:0; font-weight:700;">{data_alvo['Classificação'].upper()}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2 = st.columns(2)
    m1.metric("VEL. ORBITAL", f"{data_alvo['Velocidade Orbital (km/s)']} km/s")
    m2.metric("GRAVIDADE", f"{data_alvo['Gravidade (m/s²)']} m/s²")
    
    st.markdown(f"""
    <div class="data-block">
        <p style="color:#00e5ff; font-size:0.75rem; margin-bottom:5px; letter-spacing:1px;">PERÍODO SIDERAL</p>
        <h3 style="margin:0;">{data_alvo['Período Sideral'].upper()}</h3>
    </div>
    <div class="data-block">
        <p style="color:#00e5ff; font-size:0.75rem; margin-bottom:5px; letter-spacing:1px;">SATÉLITES NATURAIS</p>
        <h3 style="margin:0;">{data_alvo['Satélites']} UNIDADES</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p class="tech-header">Análise Dimensional Comparativa</p>', unsafe_allow_html=True)

fig_comp = px.bar(
    df, x="Planeta", y="Diâmetro (km)",
    color="Diâmetro (km)",
    color_continuous_scale="Viridis",
    template="plotly_dark"
)
fig_comp.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title=None),
    yaxis=dict(title="DIÂMETRO (KM)", gridcolor="#1e262f"),
    height=300,
    coloraxis_showscale=False
)
st.plotly_chart(fig_comp, use_container_width=True)

st.markdown(
    "<div style='text-align: right; color: #1e262f; font-size: 0.7rem; letter-spacing: 1px;'>"
    "DATA SOURCE: NASA PLANETARY DATA SYSTEM (PDS)"
    "</div>", 
    unsafe_allow_html=True
)
