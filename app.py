import streamlit as st
from services.data_service import api_status

st.set_page_config(
    page_title="VM 2026 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Banner ──────────────────────────────────────────────────────────────────
status = api_status()
if not status["football_data"] and not status["odds_api"]:
    st.warning("Demo-modus: Ingen API-nøkler konfigurert. Se .env.example.", icon="ℹ️")
elif not status["odds_api"]:
    st.info("Odds API ikke konfigurert — bruker demo-odds for value bets.", icon="💡")

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0;">
    <div style="font-size: 4rem;">⚽</div>
    <h1 style="font-size: 2.6rem; margin: 0.2rem 0;">VM 2026 Predictor</h1>
    <p style="font-size: 1.1rem; color: #888; margin-top: 0.3rem;">
        FIFA World Cup 2026 · USA, Canada & Mexico · 11. juni – 19. juli
    </p>
</div>
""", unsafe_allow_html=True)

# ── Stats ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Lag", "48")
c2.metric("Grupper", "12")
c3.metric("Kamper", "104")
c4.metric("Dager til start", str((
    __import__("datetime").date(2026, 6, 11) -
    __import__("datetime").date.today()
).days))

st.markdown("---")

# ── Start-knapper ────────────────────────────────────────────────────────────
st.subheader("Velg hva du vil gjøre")

b1, b2, b3 = st.columns(3)
with b1:
    st.page_link("pages/2_Kamper.py",    label="⚽  Se kampresultater",   use_container_width=True)
    st.caption("Prediksjoner, scoreline-heatmap, over/under og BTTS")

with b2:
    st.page_link("pages/4_Sharp_Bets.py", label="💰  Sharp Bets",         use_container_width=True)
    st.caption("Edge mot bookmaker-odds + Kelly Criterion stake")

with b3:
    st.page_link("pages/3_Turnering.py", label="🏆  Simular turneringen", use_container_width=True)
    st.caption("Monte Carlo — hvem vinner VM 2026?")

b4, b5, b6 = st.columns(3)
with b4:
    st.page_link("pages/1_Grupper.py",   label="📊  Gruppeoversikt",      use_container_width=True)
    st.caption("Alle 12 grupper med videre-sannsynligheter")

with b5:
    st.page_link("pages/5_Research.py",  label="🔬  Research & analyse",  use_container_width=True)
    st.caption("H2H, lagratinger og gruppesammenligning")

with b6:
    st.page_link("pages/6_AI_Analyst.py", label="🤖  AI Analyst",         use_container_width=True)
    st.caption("Regelbasert AI-analyse — lag, kamper og dark horses")

st.markdown("---")
st.caption("Modell: Poisson-distribusjon + Monte Carlo (10 000 simuleringer) · Poisson-kalibrert mot historiske VM-data")
