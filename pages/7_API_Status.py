import streamlit as st
from apis.api_football import check_connection as af_check, is_configured as af_configured
from apis.openfootball_api import get_fixtures as of_fixtures
from apis.odds_api import is_configured as odds_configured
from services.data_service import get_data_source

st.set_page_config(page_title="API Status – VM 2026", page_icon="⚙️", layout="centered")
st.title("⚙️ API Status")

st.markdown("---")

# ── Aktiv datakilde ───────────────────────────────────────────────────────────
source = get_data_source()
if "live" in source:
    st.success(f"✅ Aktiv datakilde: **{source}**")
elif "gratis" in source:
    st.info(f"ℹ️ Aktiv datakilde: **{source}** (oppdateres etter kampene)")
else:
    st.warning(f"⚠️ Aktiv datakilde: **{source}**")

st.markdown("---")

# ── API-Football ──────────────────────────────────────────────────────────────
st.subheader("API-Football (RapidAPI)")

if not af_configured():
    st.error("❌ Ikke konfigurert — legg til `API_FOOTBALL_KEY` i Streamlit Secrets")
    st.markdown("""
**Slik får du gratis nøkkel:**
1. Gå til **rapidapi.com** og lag en konto
2. Søk etter **"API-Football"**
3. Klikk **"Subscribe to Test"** → velg **Basic (Free)** — 100 req/dag
4. Kopier nøkkelen fra **"Header Parameters → X-RapidAPI-Key"**
""")
else:
    with st.spinner("Tester tilkobling..."):
        result = af_check()
    if result["ok"]:
        st.success(f"✅ {result['reason']}")
    else:
        st.error(f"❌ {result['reason']}")
        if "403" in result.get("reason", ""):
            st.caption("Sjekk at nøkkelen er riktig og at du har abonnert på API-Football på RapidAPI.")
        elif "429" in result.get("reason", ""):
            st.caption("Daglig grense på 100 requests er nådd. Tilbakestilles midnatt UTC.")

st.markdown("---")

# ── openfootball fallback ─────────────────────────────────────────────────────
st.subheader("openfootball (gratis fallback)")
with st.spinner("Sjekker GitHub..."):
    of = of_fixtures()
if of:
    st.success(f"✅ {len(of)} kamper tilgjengelig (ingen nøkkel nødvendig)")
else:
    st.warning("⚠️ Ikke tilgjengelig ennå — openfootball publiserer data nærmere turneringsstart")

st.markdown("---")

# ── The Odds API ──────────────────────────────────────────────────────────────
st.subheader("The Odds API (valgfri)")
if not odds_configured():
    st.caption("Ikke konfigurert — appen bruker demo-odds. Legg til `ODDS_API_KEY` for live odds.")
else:
    st.success("✅ Konfigurert")

st.markdown("---")

# ── Streamlit Secrets-guide ───────────────────────────────────────────────────
st.subheader("Legg til nøkler i Streamlit Cloud")
st.markdown("""
1. Gå til **share.streamlit.io** → appen din → **Settings → Secrets**
2. Lim inn:

```toml
API_FOOTBALL_KEY = "din_rapidapi_nokkel_her"
ODDS_API_KEY = "din_nokkel_her"
```

3. Klikk **Save** — appen restarter automatisk
""")
