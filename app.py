import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Calculadora +EV & Simulador", layout="wide")

st.title("🎯 Analizador Estadístico de Apuestas (+EV & Kelly)")

# Panel Lateral: Gestión de Banca
st.sidebar.header("Gestión de Bankroll")
bankroll = st.sidebar.number_input("Banca Total ($)", value=1000.0, step=100.0)
kelly_fraction = st.sidebar.slider("Fracción de Kelly (Seguridad)", 0.1, 1.0, 0.25, step=0.05)

tab1, tab2 = st.tabs(["📊 Calculadora +EV Directa", "⚽ Simulador Monte Carlo (xG)"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        p_modelo = st.slider("Probabilidad estimada por tu análisis (%)", 1.0, 99.0, 55.0) / 100
        cuota_casa = st.number_input("Cuota ofrecida por el casino (Decimal)", value=2.10, step=0.05)
    
    with col2:
        prob_mercado = 1 / cuota_casa
        ev = (p_modelo * cuota_casa) - 1
        b = cuota_casa - 1
        q = 1 - p_modelo
        kelly_pct = max(0.0, (b * p_modelo - q) / b) * kelly_fraction
        apuesta_sugerida = bankroll * kelly_pct

        st.metric("Valor Esperado (EV)", f"{ev * 100:.2f}%", delta=f"{ev * 100:.2f}%" if ev > 0 else f"{ev * 100:.2f}%")
        st.write(f"**Probabilidad Implícita del Casino:** {prob_mercado * 100:.2f}%")
        st.write(f"**Ventaja sobre la Casa:** {(p_modelo - prob_mercado) * 100:.2f}%")
        
        if ev > 0:
            st.success(f"✅ **Apuesta con Valor (+EV):** Apostar **${apuesta_sugerida:.2f}** ({kelly_pct * 100:.2f}% de tu banca).")
        else:
            st.error("❌ **Sin Valor (-EV):** La cuota ofrecida no compensa el riesgo a largo plazo.")

with tab2:
    st.subheader("Simulación Bivariada por Goles Esperados (xG)")
    c1, c2, c3 = st.columns(3)
    with c1:
        xg_local = st.number_input("xG Estimado Local", value=1.65, step=0.05)
    with c2:
        xg_visitante = st.number_input("xG Estimado Visitante", value=1.10, step=0.05)
    with c3:
        simulaciones = st.selectbox("Simulaciones Monte Carlo", [10000, 50000, 100000], index=0)

    if st.button("Ejecutar Simulación"):
        goles_locales = np.random.poisson(xg_local, simulaciones)
        goles_visitantes = np.random.poisson(xg_visitante, simulaciones)
        
        p_gana_local = np.mean(goles_locales > goles_visitantes)
        p_empate = np.mean(goles_locales == goles_visitantes)
        p_gana_visita = np.mean(goles_locales < goles_visitantes)
        p_over_25 = np.mean((goles_locales + goles_visitantes) > 2.5)
        
        res_df = pd.DataFrame({
            "Mercado": ["Victoria Local (1)", "Empate (X)", "Victoria Visitante (2)", "Over 2.5 Goles"],
            "Probabilidad Real": [f"{p_gana_local*100:.2f}%", f"{p_empate*100:.2f}%", f"{p_gana_visita*100:.2f}%", f"{p_over_25*100:.2f}%"],
            "Cuota Justa (Fair Odds)": [f"{1/p_gana_local:.2f}", f"{1/p_empate:.2f}", f"{1/p_gana_visita:.2f}", f"{1/p_over_25:.2f}"]
        })
        st.table(res_df)
