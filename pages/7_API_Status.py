import streamlit as st
from apis.football_data_api import check_connection, is_configured as fd_configured
from apis.odds_api import is_configured as odds_configured

st.set_page_config(page_title="API Status – VM 2026", page_icon="⚙️", layout="centered")
st.title("⚙️ API Status")
st.caption("Diagnostikk for tilkobling mot football-data.org og The Odds API")

st.markdown("---")

# ── football-data.org ────────────────────────────────────────────────────────
st.subheader("football-data.org")

if not fd_configured():
    st.error("❌ Nøkkel ikke konfigurert — legg til `FOOTBALL_DATA_API_KEY` i Streamlit Secrets")
else:
    st.info("🔑 Nøkkel funnet — tester tilkobling...")
    with st.spinner("Kobler til football-data.org..."):
        result = check_connection()

    if result["ok"]:
        st.success(f"✅ {result['reason']}")
        if result.get("matches", 0) == 0:
            st.warning(
                "⚠️ Tilkoblingen fungerer, men ingen VM 2026-kamper returnert ennå. "
                "football-data.org legger typisk til fixtures 2–4 uker før turneringsstart (11. juni). "
                "Appen bruker demo-data inntil da — det er normalt."
            )
    else:
        st.error(f"❌ {result['reason']}")

        if "403" in result["reason"]:
            st.markdown("""
**Løsning:** Gratis-planen på football-data.org inkluderer ikke VM-data.

Du trenger **Tier 1 eller høyere** for internasjonale turneringer.
Registrer deg for en høyere plan på football-data.org.

Alternativt: appen fungerer fint i demo-modus frem til VM starter.
""")
        elif "404" in result["reason"]:
            st.markdown("""
**Årsak:** VM 2026 er ikke lagt inn i football-data.org ennå.
De legger vanligvis til turneringer noen uker før start.
Prøv igjen nærmere 11. juni.
""")

st.markdown("---")

# ── The Odds API ─────────────────────────────────────────────────────────────
st.subheader("The Odds API")

if not odds_configured():
    st.warning("⚠️ Ikke konfigurert — legg til `ODDS_API_KEY` i Streamlit Secrets for live odds")
else:
    st.success("✅ Nøkkel konfigurert")
    st.caption("Live odds aktiveres automatisk når VM-kamper er tilgjengelig")

st.markdown("---")

# ── Slik legger du til Secrets ───────────────────────────────────────────────
st.subheader("Slik legger du til API-nøkler i Streamlit Cloud")
st.markdown("""
1. Gå til **share.streamlit.io** og åpne appen din
2. Klikk **Settings** (tannhjul) → **Secrets**
3. Lim inn:

```toml
FOOTBALL_DATA_API_KEY = "din_nokkel_her"
ODDS_API_KEY = "din_nokkel_her"
```

4. Klikk **Save** — appen restarter automatisk
""")
