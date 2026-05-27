import streamlit as st
from apis.openfootball_api import get_fixtures as of_fixtures
from apis.odds_api import is_configured as odds_configured
from services.data_service import get_data_source

st.set_page_config(page_title="Datakilde Status – VM 2026", page_icon="⚙️", layout="centered")
st.title("⚙️ Datakilde Status")

st.markdown("---")

# ── Aktiv datakilde ───────────────────────────────────────────────────────────
source = get_data_source()
if "live" in source:
    st.success(f"✅ Aktiv datakilde: **{source}**")
elif "gratis" in source:
    st.info(f"ℹ️ Aktiv datakilde: **{source}** — oppdateres automatisk etter kampene")
else:
    st.info(f"🧮 Aktiv datakilde: **{source}** — prediksjonsmodellen bruker ELO-ratinger for alle 48 lag")

st.markdown("---")

# ── openfootball ──────────────────────────────────────────────────────────────
st.subheader("openfootball (aktiv datakilde fra 11. juni)")
st.markdown("Gratis kilde som henter VM-kampdata fra GitHub. Ingen nøkkel nødvendig.")
with st.spinner("Sjekker GitHub..."):
    of = of_fixtures()
if of:
    st.success(f"✅ {len(of)} kamper tilgjengelig")
else:
    st.info("⏳ Data ikke publisert ennå — openfootball legger ut resultater etter kampstart (11. juni 2026)")

st.markdown("---")

# ── API-Football (valgfri) ────────────────────────────────────────────────────
st.subheader("API-Football (valgfri, betalt)")
st.caption(
    "API-Football tilbyr live data, men krever betalt abonnement ($19+/mnd). "
    "Appen fungerer fullt ut uten det via openfootball og prediksjonsmodellen."
)

st.markdown("---")

# ── The Odds API ──────────────────────────────────────────────────────────────
st.subheader("The Odds API (valgfri)")
if not odds_configured():
    st.caption("Ikke konfigurert — appen bruker demo-odds. Legg til `ODDS_API_KEY` i Streamlit Secrets for live odds.")
else:
    st.success("✅ Konfigurert")

st.markdown("---")

# ── Forklaring ────────────────────────────────────────────────────────────────
st.subheader("Slik fungerer appen uten API-nøkler")
st.markdown("""
Appen er **fullt funksjonell** uten betalte API-er:

- **Prediksjoner**: Beregnes fra ELO-ratinger og Poisson-fordeling for alle 48 VM-lag
- **Turnering**: Monte Carlo-simulering (10 000 runder) gir vinnersannsynligheter
- **Value bets**: Sammenlignes mot demo-odds — bytt inn `ODDS_API_KEY` for live bookmaker-odds
- **Live kampdata**: Aktiveres automatisk via openfootball når VM starter **11. juni 2026**
""")
