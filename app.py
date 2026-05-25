import streamlit as st
import datetime
from services.data_service import api_status, get_fixtures, get_odds
from services.odds_service import get_sharp_bets
from models.rating_engine import get_ratings
from models.poisson_model import predict_from_ratings, most_likely_score
from utils.formatters import flag_emoji

st.set_page_config(
    page_title="VM 2026 Predictor",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS: mobilvennlig padding ────────────────────────────────────────────────
st.markdown("""
<style>
.match-card {
    background: #1A1D27;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.bet-card {
    background: #1a2e1a;
    border: 1px solid #2d5a2d;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.team-name { font-size: 1.05rem; font-weight: 600; }
.prob-row { font-size: 0.9rem; color: #aaa; margin-top: 0.3rem; }
.edge-badge {
    background: #1DB954;
    color: #000;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.8rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── API-banner ───────────────────────────────────────────────────────────────
status = api_status()
if not status["football_data"] and not status["odds_api"]:
    st.caption("⚙️ Demo-modus — legg til API-nøkler for live data")

# ── Header ───────────────────────────────────────────────────────────────────
today = datetime.date.today()
vm_start = datetime.date(2026, 6, 11)
days_left = (vm_start - today).days

st.markdown(f"""
<div style="text-align:center; padding: 1.2rem 0 0.5rem 0;">
    <div style="font-size: 2.8rem;">⚽</div>
    <h1 style="font-size: 2rem; margin: 0.1rem 0;">VM 2026 Predictor</h1>
    <p style="color: #888; margin: 0.2rem 0 0 0; font-size: 0.95rem;">
        FIFA World Cup 2026 · 11. juni – 19. juli
    </p>
</div>
""", unsafe_allow_html=True)

if days_left > 0:
    st.markdown(f"<div style='text-align:center; font-size:1.4rem; color:#1DB954; font-weight:700; padding-bottom:0.8rem;'>🗓️ {days_left} dager til kampstart</div>", unsafe_allow_html=True)

st.markdown("---")

# ── Last inn data ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def load_data():
    ratings = get_ratings()
    fixtures = get_fixtures()
    bets = get_sharp_bets(ratings)
    return ratings, fixtures, bets

ratings, fixtures, bets = load_data()

# Finn relevante kamper: i dag, eller første dag med kamper
def get_display_date(fixtures, today):
    upcoming = sorted(
        [f for f in fixtures if f.get("home_score") is None],
        key=lambda x: x.get("date", "")
    )
    if not upcoming:
        return None, []
    today_str = str(today)
    today_matches = [f for f in upcoming if f.get("date") == today_str]
    if today_matches:
        return today_str, today_matches
    next_date = upcoming[0].get("date")
    return next_date, [f for f in upcoming if f.get("date") == next_date]

display_date, day_fixtures = get_display_date(fixtures, today)

# ── Dagens kamper ─────────────────────────────────────────────────────────────
if display_date:
    try:
        d = datetime.date.fromisoformat(display_date)
        label = "I dag" if d == today else d.strftime("%-d. %B").replace(
            "January","januar").replace("February","februar").replace(
            "March","mars").replace("April","april").replace("May","mai").replace(
            "June","juni").replace("July","juli")
    except Exception:
        label = display_date

    st.subheader(f"📅 {label}s kamper")

    for f in day_fixtures:
        home, away = f["home"], f["away"]
        pred = predict_from_ratings(home, away, ratings, neutral=True)
        score_h, score_a = most_likely_score(pred["prob_matrix"])
        odds = get_odds(home, away)

        hw = pred["home_win"] * 100
        dr = pred["draw"] * 100
        aw = pred["away_win"] * 100

        odds_str = ""
        if odds:
            odds_str = f"Odds: {odds['home']} / {odds['draw']} / {odds['away']}"

        st.markdown(f"""
<div class="match-card">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <span class="team-name">{flag_emoji(home)} {home}</span>
    <span style="color:#555; font-size:0.85rem;">Gruppe {f.get('group','')}</span>
    <span class="team-name">{away} {flag_emoji(away)}</span>
  </div>
  <div class="prob-row" style="display:flex; justify-content:space-between; margin-top:0.5rem;">
    <span>1: <b style="color:#fff">{hw:.0f}%</b></span>
    <span>Mest sannsynlig: <b style="color:#1DB954">{score_h}–{score_a}</b></span>
    <span>2: <b style="color:#fff">{aw:.0f}%</b></span>
  </div>
  <div style="font-size:0.8rem; color:#666; margin-top:0.3rem;">{odds_str} &nbsp;|&nbsp; Over 2.5: {pred['over_25']*100:.0f}% &nbsp;|&nbsp; BTTS: {pred['btts_yes']*100:.0f}%</div>
</div>
""", unsafe_allow_html=True)

    st.page_link("pages/2_Kamper.py", label="Se alle kampdetaljer →", use_container_width=True)
else:
    st.info("Ingen kommende kamper funnet i demo-data.")

st.markdown("---")

# ── Beste bets i dag ─────────────────────────────────────────────────────────
day_bets = [b for b in bets if b.get("dato") == display_date] if display_date else []
top_bets  = day_bets[:3] if day_bets else bets[:3]

if top_bets:
    st.subheader("💰 Beste bets akkurat nå")
    for b in top_bets:
        st.markdown(f"""
<div class="bet-card">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <span style="font-weight:600">{b['kamp']}</span>
    <span class="edge-badge">+{b['edge_%']}% edge</span>
  </div>
  <div style="margin-top:0.4rem; font-size:0.9rem;">
    <b>{b['bet']}</b> @ <b style="color:#1DB954">{b['odds']}</b>
    &nbsp;·&nbsp; Modell: {b['model_%']}% vs. book: {b['book_%']}%
  </div>
  <div style="font-size:0.8rem; color:#888; margin-top:0.2rem;">
    EV: {b['EV']} &nbsp;·&nbsp; Kelly: {b['kelly_%']}% av bankroll
  </div>
</div>
""", unsafe_allow_html=True)
    st.page_link("pages/4_Sharp_Bets.py", label="Se alle sharp bets →", use_container_width=True)

st.markdown("---")

# ── Navigasjon ────────────────────────────────────────────────────────────────
st.subheader("Utforsk mer")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/3_Turnering.py", label="🏆 Turneringssimulator",  use_container_width=True)
    st.page_link("pages/1_Grupper.py",   label="📊 Gruppeoversikt",       use_container_width=True)
with col2:
    st.page_link("pages/6_AI_Analyst.py", label="🤖 AI Analyst",          use_container_width=True)
    st.page_link("pages/5_Research.py",   label="🔬 Research & analyse",  use_container_width=True)

st.markdown("---")
st.caption("Modell: Poisson + Monte Carlo · Historisk VM-kalibrering · Gamble ansvarlig 🎗️")
