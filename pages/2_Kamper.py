import streamlit as st
import datetime
import plotly.graph_objects as go
from services.data_service import get_fixtures_df, get_odds
from models.rating_engine import get_ratings
from models.poisson_model import predict_from_ratings, most_likely_score
from utils.formatters import flag_emoji

st.set_page_config(page_title="Kamper – VM 2026", page_icon="⚽", layout="centered")

# ── CSS — broadcast-inspirert design ─────────────────────────────────────────
st.markdown("""
<style>
.match-card {
    background: linear-gradient(135deg, #141929 0%, #0f1520 100%);
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    padding: 1.2rem 1.4rem 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.match-meta {
    font-size: 0.7rem;
    color: #00dc82;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1rem;
}
.teams-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.team-block {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}
.team-block.away { flex-direction: row-reverse; }
.team-flag { font-size: 1.6rem; line-height: 1; }
.team-name-main {
    font-size: 1rem;
    font-weight: 700;
    color: #f0f4ff;
    line-height: 1.2;
}
.vs-box {
    background: #0a0e1a;
    color: #4a5a7a;
    font-size: 0.75rem;
    font-weight: 800;
    padding: 0.3rem 0.7rem;
    border-radius: 8px;
    letter-spacing: 0.05em;
    margin: 0 0.8rem;
    white-space: nowrap;
}
.prob-bar-wrap {
    height: 8px;
    border-radius: 4px;
    background: #0a0e1a;
    display: flex;
    overflow: hidden;
    margin-bottom: 0.8rem;
    gap: 2px;
}
.pb-h { background: #00dc82; border-radius: 4px 0 0 4px; }
.pb-d { background: #4a5a7a; }
.pb-a { background: #f97316; border-radius: 0 4px 4px 0; }
.prob-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 0.9rem;
}
.prob-cell {
    background: #0a0e1a;
    border-radius: 10px;
    padding: 0.55rem 0.4rem;
    text-align: center;
}
.pc-label { font-size: 0.65rem; color: #6b7fa3; text-transform: uppercase; letter-spacing: 0.06em; }
.pc-pct { font-size: 1.25rem; font-weight: 900; line-height: 1.1; }
.pc-odds { font-size: 0.7rem; color: #6b7fa3; margin-top: 0.1rem; }
.ph .pc-pct { color: #00dc82; }
.pd .pc-pct { color: #94a3b8; }
.pa .pc-pct { color: #f97316; }
.stats-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.stat-pill {
    background: #0a0e1a;
    border: 1px solid #1e2d4a;
    border-radius: 20px;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    color: #c0ccdd;
    white-space: nowrap;
}
.stat-pill b { color: #f0f4ff; }
.date-banner {
    font-size: 0.75rem;
    color: #00dc82;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 1.6rem 0 0.7rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e2d4a;
}
.no-matches {
    text-align: center;
    color: #6b7fa3;
    padding: 2rem;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.title("⚽ Kamper — VM 2026")

# ── Cache predictions — kjøres én gang per (home, away)-par ──────────────────
@st.cache_data(show_spinner=False)
def _predict(home: str, away: str) -> dict:
    return predict_from_ratings(home, away, get_ratings(), neutral=True)

@st.cache_data(show_spinner=False)
def _load_fixtures():
    return get_fixtures_df()

df = _load_fixtures()
upcoming = df[df["home_score"].isna()].copy()

# ── Filter ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
groups = ["Alle"] + sorted(df["group"].dropna().unique().tolist())
sel_group = col1.selectbox("Gruppe", groups, key="grp")
all_teams = sorted(set(df["home"].tolist() + df["away"].tolist()))
sel_team  = col2.selectbox("Lag", ["Alle"] + all_teams, key="team")

if sel_group != "Alle":
    upcoming = upcoming[upcoming["group"] == sel_group]
if sel_team != "Alle":
    upcoming = upcoming[(upcoming["home"] == sel_team) | (upcoming["away"] == sel_team)]

if upcoming.empty:
    st.markdown('<div class="no-matches">Ingen kommende kamper å vise.</div>', unsafe_allow_html=True)
    st.stop()

# ── Vis kamper gruppert per dato ──────────────────────────────────────────────
upcoming = upcoming.sort_values(["date", "group"])
today = datetime.date.today()

for date_str in upcoming["date"].unique():
    try:
        d = datetime.date.fromisoformat(str(date_str))
        if d == today:
            label = f"I DAG — {d.strftime('%d. %B')}"
        elif d == today + datetime.timedelta(days=1):
            label = f"I MORGEN — {d.strftime('%d. %B')}"
        else:
            label = d.strftime("%A %d. %B").upper().replace("MONDAY","MANDAG").replace("TUESDAY","TIRSDAG").replace("WEDNESDAY","ONSDAG").replace("THURSDAY","TORSDAG").replace("FRIDAY","FREDAG").replace("SATURDAY","LØRDAG").replace("SUNDAY","SØNDAG")
    except Exception:
        label = str(date_str)

    st.markdown(f'<div class="date-banner">📅 {label}</div>', unsafe_allow_html=True)

    day_rows = upcoming[upcoming["date"] == date_str]

    for _, row in day_rows.iterrows():
        home, away = row["home"], row["away"]
        group = row.get("group", "")

        # Cached prediction — ingen re-beregning ved filter-bytte
        pred = _predict(home, away)
        score_h, score_a = most_likely_score(pred["prob_matrix"])
        odds = get_odds(home, away)

        hw = pred["home_win"] * 100
        dw = pred["draw"] * 100
        aw = pred["away_win"] * 100

        odds_h = f"@ {odds['home']}" if odds else "–"
        odds_d = f"@ {odds['draw']}" if odds else "–"
        odds_a = f"@ {odds['away']}" if odds else "–"

        flag_h = flag_emoji(home)
        flag_a = flag_emoji(away)

        card_html = f"""
<div class="match-card">
  <div class="match-meta">GRUPPE {group} &nbsp;·&nbsp; VM 2026</div>
  <div class="teams-row">
    <div class="team-block">
      <span class="team-flag">{flag_h}</span>
      <span class="team-name-main">{home}</span>
    </div>
    <div class="vs-box">VS</div>
    <div class="team-block away">
      <span class="team-flag">{flag_a}</span>
      <span class="team-name-main">{away}</span>
    </div>
  </div>
  <div class="prob-bar-wrap">
    <div class="pb-h" style="width:{hw:.0f}%"></div>
    <div class="pb-d" style="width:{dw:.0f}%"></div>
    <div class="pb-a" style="width:{aw:.0f}%"></div>
  </div>
  <div class="prob-grid">
    <div class="prob-cell ph">
      <div class="pc-label">1 — Hjemme</div>
      <div class="pc-pct">{hw:.0f}%</div>
      <div class="pc-odds">{odds_h}</div>
    </div>
    <div class="prob-cell pd">
      <div class="pc-label">X — Uavgjort</div>
      <div class="pc-pct">{dw:.0f}%</div>
      <div class="pc-odds">{odds_d}</div>
    </div>
    <div class="prob-cell pa">
      <div class="pc-label">2 — Borte</div>
      <div class="pc-pct">{aw:.0f}%</div>
      <div class="pc-odds">{odds_a}</div>
    </div>
  </div>
  <div class="stats-row">
    <span class="stat-pill">🎯 <b>{score_h}–{score_a}</b></span>
    <span class="stat-pill">⬆️ Over 2.5: <b>{pred['over_25']*100:.0f}%</b></span>
    <span class="stat-pill">🥅 BTTS: <b>{pred['btts_yes']*100:.0f}%</b></span>
    <span class="stat-pill">⚽ xG: <b>{pred['exp_home_goals']}–{pred['exp_away_goals']}</b></span>
  </div>
</div>
"""
        st.markdown(card_html, unsafe_allow_html=True)

        # ── Detalj-ekspander med heatmap ──────────────────────────────────
        with st.expander(f"Scoreline-matrise — {home} vs {away}"):
            matrix = pred["prob_matrix"][:6, :6]
            fig = go.Figure(data=go.Heatmap(
                z=matrix * 100,
                x=[f"{away} {i}" for i in range(6)],
                y=[f"{home} {i}" for i in range(6)],
                colorscale=[[0,"#0a0e1a"],[0.5,"#00856e"],[1,"#00dc82"]],
                text=[[f"{matrix[i][j]*100:.1f}%" for j in range(6)] for i in range(6)],
                texttemplate="%{text}",
                showscale=False,
            ))
            fig.update_layout(
                paper_bgcolor="#0f1520",
                plot_bgcolor="#0f1520",
                font=dict(color="#c0ccdd", size=11),
                height=260,
                margin=dict(l=60, r=10, t=20, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)
