import streamlit as st
from src.data_fetcher import is_api_configured

st.set_page_config(
    page_title="VM 2026 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not is_api_configured():
    st.warning("Demo-modus: API-nøkler ikke konfigurert. Data er simulert. Se .env.example for oppsett.", icon="ℹ️")

st.title("⚽ VM 2026 Prediction App")
st.markdown("**FIFA World Cup 2026** — USA, Canada & Mexico | 11. juni – 19. juli 2026")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Lag", "48")
col2.metric("Grupper", "12")
col3.metric("Kamper", "104")
col4.metric("Start", "11. juni")

st.markdown("---")
st.markdown("""
### Navigasjon
Bruk menyen til venstre for å utforske:

| Side | Beskrivelse |
|---|---|
| 📊 **Grupper** | Alle 12 VM-grupper med sannsynlighet for å gå videre |
| ⚽ **Kamper** | Kampresultat-prediksjoner (1X2, over/under, BTTS) |
| 🏆 **Turnering** | Monte Carlo-simulator — hvem vinner VM? |
| 💰 **Value Bets** | Kamper med positiv edge mot bookmaker-odds |
| 🔬 **Research** | Lagratinger, statistikk og analyse |
""")

st.markdown("---")
st.caption("Modell: Poisson-distribusjon + Monte Carlo (10 000 simuleringer) | Data: football-data.org")
