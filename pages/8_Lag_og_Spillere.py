import streamlit as st
from data.demo_data import GROUPS, TEAM_RATINGS
from data.players import KEY_PLAYERS
from models.rating_engine import get_ratings, get_confidence_score
from utils.formatters import flag_emoji

st.set_page_config(page_title="Lag & Spillere – VM 2026", page_icon="🎽", layout="centered")

st.markdown("""
<style>
.team-header {
    background: linear-gradient(135deg, #141929 0%, #0f1520 100%);
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    text-align: center;
}
.team-flag-big { font-size: 3rem; }
.team-name-big { font-size: 1.6rem; font-weight: 800; color: #f0f4ff; margin: 0.3rem 0; }
.team-group { font-size: 0.75rem; color: #00dc82; font-weight: 700; letter-spacing: 0.1em; }
.rating-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.rating-cell {
    background: #0a0e1a;
    border-radius: 12px;
    padding: 0.7rem;
    text-align: center;
}
.rc-label { font-size: 0.65rem; color: #6b7fa3; text-transform: uppercase; letter-spacing: 0.08em; }
.rc-value { font-size: 1.3rem; font-weight: 900; color: #00dc82; }
.rc-sub { font-size: 0.7rem; color: #4a5a7a; }
.player-card {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    background: #0f1520;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
}
.pos-badge {
    font-size: 1.1rem;
    width: 2rem;
    text-align: center;
    flex-shrink: 0;
}
.player-info { flex: 1; }
.player-name { font-size: 0.95rem; font-weight: 700; color: #f0f4ff; }
.player-club { font-size: 0.75rem; color: #6b7fa3; }
.section-title {
    font-size: 0.7rem;
    color: #00dc82;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.2rem 0 0.6rem 0;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid #1e2d4a;
}
.disclaimer {
    font-size: 0.72rem;
    color: #4a5a7a;
    margin-top: 1rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🎽 Lag & Spillere — VM 2026")

# ── Lagvelger ─────────────────────────────────────────────────────────────────
group_opts = {f"Gruppe {g}": teams for g, teams in GROUPS.items()}
col1, col2 = st.columns([1, 2])
sel_group_label = col1.selectbox("Gruppe", list(group_opts.keys()))
group_teams = group_opts[sel_group_label]

team_options = [f"{flag_emoji(t)} {t}" for t in group_teams]
sel_team_display = col2.selectbox("Lag", team_options)
team = sel_team_display.split(" ", 1)[1]  # Fjern flagg-emoji

# ── Teaminfo ──────────────────────────────────────────────────────────────────
ratings = get_ratings()
r = ratings.get(team, {})
raw = TEAM_RATINGS.get(team, {})
group_key = sel_group_label.split()[-1]

elo = r.get("elo", raw.get("elo", 1500))
attack = raw.get("attack", 1.0)
defense = raw.get("defense", 1.0)
conf = r.get("confederation", "–")
confidence = get_confidence_score(team, ratings)

flag = flag_emoji(team)

st.markdown(f"""
<div class="team-header">
  <div class="team-flag-big">{flag}</div>
  <div class="team-name-big">{team}</div>
  <div class="team-group">GRUPPE {group_key} &nbsp;·&nbsp; {conf}</div>
</div>
""", unsafe_allow_html=True)

# ELO + ratinger
st.markdown('<div class="rating-grid">'
    f'<div class="rating-cell"><div class="rc-label">ELO</div><div class="rc-value">{elo:.0f}</div><div class="rc-sub">Styrkerating</div></div>'
    f'<div class="rating-cell"><div class="rc-label">Angrep</div><div class="rc-value">{attack:.2f}</div><div class="rc-sub">xG per kamp</div></div>'
    f'<div class="rating-cell"><div class="rc-label">Forsvar</div><div class="rc-value">{defense:.2f}</div><div class="rc-sub">Slippes inn xG</div></div>'
    '</div>', unsafe_allow_html=True)

# Konfidensbar
conf_color = "#00dc82" if confidence > 65 else "#f59e0b" if confidence > 45 else "#f97316"
st.markdown(f"""
<div style="margin-bottom:1rem;">
  <div style="font-size:0.7rem;color:#6b7fa3;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;">Modell-konfidens</div>
  <div style="height:8px;background:#0a0e1a;border-radius:4px;overflow:hidden;">
    <div style="height:100%;width:{confidence}%;background:{conf_color};border-radius:4px;"></div>
  </div>
  <div style="font-size:0.75rem;color:{conf_color};margin-top:0.25rem;font-weight:700;">{confidence}%</div>
</div>
""", unsafe_allow_html=True)

# ── Nøkkelspillere ────────────────────────────────────────────────────────────
players = KEY_PLAYERS.get(team, [])

if players:
    st.markdown('<div class="section-title">Nøkkelspillere</div>', unsafe_allow_html=True)
    for p in players:
        st.markdown(f"""
<div class="player-card">
  <div class="pos-badge">{p['pos']}</div>
  <div class="player-info">
    <div class="player-name">{p['name']}</div>
    <div class="player-club">{p['club']}</div>
  </div>
</div>
""", unsafe_allow_html=True)
else:
    st.info("Ingen spillerdata tilgjengelig for dette laget.")

# ── Gruppekamper ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Gruppekamper</div>', unsafe_allow_html=True)
from services.data_service import get_fixtures
from models.poisson_model import predict_from_ratings

@st.cache_data(show_spinner=False)
def _pred(home, away):
    return predict_from_ratings(home, away, get_ratings(), neutral=True)

fixtures = [f for f in get_fixtures() if team in (f["home"], f["away"])]
for f in fixtures:
    home, away = f["home"], f["away"]
    pred = _pred(home, away)
    is_home = home == team
    opp = away if is_home else home
    hw, dw, aw = pred["home_win"]*100, pred["draw"]*100, pred["away_win"]*100
    our_pct = hw if is_home else aw
    opp_pct = aw if is_home else hw
    label = "Hjemme" if is_home else "Borte"
    date_str = f.get("date", "")

    st.markdown(f"""
<div style="background:#0a0e1a;border:1px solid #1e2d4a;border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.5rem;display:flex;justify-content:space-between;align-items:center;">
  <div>
    <span style="font-size:0.65rem;color:#6b7fa3;text-transform:uppercase;">{date_str} · {label}</span><br>
    <span style="font-weight:700;color:#f0f4ff;">{flag_emoji(team)} {team}</span>
    <span style="color:#4a5a7a;margin:0 0.4rem;">vs</span>
    <span style="color:#c0ccdd;">{flag_emoji(opp)} {opp}</span>
  </div>
  <div style="text-align:right;">
    <span style="font-size:1.1rem;font-weight:900;color:#00dc82;">{our_pct:.0f}%</span>
    <span style="font-size:0.7rem;color:#4a5a7a;"> seier</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ Spillerinfo basert på kjent tropp pr. august 2025. Skader og uttaking kan ha endret seg.</div>', unsafe_allow_html=True)
