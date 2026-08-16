import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="DeepBetting AI", page_icon="⚡", layout="wide")

# Inyección de CSS para estética Dark / Neon Cyberpunk
st.markdown("""
<style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #07090e;
        color: #f3f4f6;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Navbar superior estilo SaaS */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 30px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 25px;
    }
    .logo {
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #00f0ff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Badge de deportes */
    .badge {
        display: inline-block;
        background: rgba(255, 0, 127, 0.15);
        color: #ff007f;
        border: 1px solid #ff007f;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 48px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 15px;
        color: #ffffff;
    }
    .hero-title span {
        background: linear-gradient(90deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: #9ca3af;
        font-size: 16px;
        max-width: 650px;
        margin-bottom: 30px;
    }
    
    /* Tarjetas oscuras con borde iluminado */
    .stat-card {
        background: #0d111a;
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    
    /* Botones con degradado neon */
    .stButton>button {
        background: linear-gradient(90deg, #00f0ff, #0072ff);
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado estilo DeepBetting
st.markdown("""
<div class="navbar">
    <div class="logo">PAQUITO-BETTING AI</div>
    <div style="color: #9ca3af; font-size: 14px;">IA & ANÁLISIS &nbsp;•&nbsp; MODELOS &nbsp;•&nbsp; EN VIVO</div>
</div>
<div class="badge">🔥 MODELOS PREDICTIVOS 2026</div>
<div class="hero-title">Deja que el poder de la <span>IA y la Estadística</span> mejore tus pronósticos</div>
<div class="hero-subtitle">Algoritmos de valor esperado (+EV), distribución de Poisson y simulaciones Monte Carlo aplicados a mercados deportivos en tiempo real.</div>
""", unsafe_allow_html=True)

# Pestañas principales
tab1, tab2 = st.tabs(["⚡ Calculadora +EV & Kelly", "⚽ Motor de Simulación Monte Carlo"])

with tab1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        p_modelo = st.slider("Probabilidad estimada por tu modelo (%)", 1.0, 99.0, 56.0) / 100
        cuota_casa = st.number_input("Cuota de la casa de apuestas", value=2.05, step=0.05)
    with c2:
        bankroll = st.number_input("Banca total disponible ($)", value=1000.0, step=50.0)
        prob_mercado = 1 / cuota_casa
        ev = (p_modelo * cuota_casa) - 1
        b = cuota_casa - 1
        q = 1 - p_modelo
        kelly_pct = max(0.0, (b * p_modelo - q) / b) * 0.25
        monto = bankroll * kelly_pct
        
        st.metric("Valor Esperado (+EV)", f"{ev*100:.2f}%", delta=f"Ventaja: {(p_modelo-prob_mercado)*100:.1f}%")
        if ev > 0:
            st.success(f"💎 **Apuesta Recomendada:** Invertir **${monto:.2f}** ({kelly_pct*100:.2f}% de la banca).")
        else:
            st.error("⚠️ **Sin Valor:** La cuota está castigada por el margen del casino.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    c_loc, c_vis, c_sim = st.columns(3)
    with c_loc:
        xg_l = st.number_input("xG Local (Alineación titular)", value=1.75, step=0.05)
    with c_vis:
        xg_v = st.number_input("xG Visitante (Alineación titular)", value=1.15, step=0.05)
    with c_sim:
        n_sim = st.selectbox("Iteraciones Monte Carlo", [10000, 50000, 100000], index=1)
    
    if st.button("🚀 Ejecutar Simulación Predictiva"):
        g_l = np.random.poisson(xg_l, n_sim)
        g_v = np.random.poisson(xg_v, n_sim)
        
        p_1 = np.mean(g_l > g_v)
        p_x = np.mean(g_l == g_v)
        p_2 = np.mean(g_l < g_v)
        p_o25 = np.mean((g_l + g_v) > 2.5)
        
        res = pd.DataFrame({
            "Mercado": ["Victoria Local (1)", "Empate (X)", "Victoria Visitante (2)", "Más de 2.5 Goles"],
            "Probabilidad Real": [f"{p_1*100:.2f}%", f"{p_x*100:.2f}%", f"{p_2*100:.2f}%", f"{p_o25*100:.2f}%"],
            "Cuota Justa (Sin Margen)": [f"{1/p_1:.2f}", f"{1/p_x:.2f}", f"{1/p_2:.2f}", f"{1/p_o25:.2f}"]
        })
        st.dataframe(res, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
