import streamlit as st
import pandas as pd
from src.data_fetcher import get_groups, get_teams
from src.poisson_model import predict_from_ratings
from src.tournament_sim import simulate_group

st.set_page_config(page_title="Grupper – VM 2026", page_icon="📊", layout="wide")
st.title("📊 VM 2026 — Gruppeoversikt")

groups = get_groups()
ratings = get_teams()

selected_group = st.selectbox(
    "Velg gruppe",
    [f"Gruppe {g}" for g in sorted(groups.keys())],
)
group_key = selected_group.split()[-1]
teams = groups[group_key]

st.subheader(f"Gruppe {group_key}")

# Simuler gruppe 5000 ganger for videre-sannsynligheter
@st.cache_data(ttl=3600)
def sim_group_probs(teams_tuple, n=5000):
    teams = list(teams_tuple)
    advance_count = {t: 0 for t in teams}
    win_count = {t: 0 for t in teams}
    for _ in range(n):
        table = simulate_group(teams, ratings)
        advance_count[table[0]["team"]] += 1
        advance_count[table[1]["team"]] += 1
        win_count[table[0]["team"]] += 1
    return (
        {t: round(v / n * 100, 1) for t, v in advance_count.items()},
        {t: round(v / n * 100, 1) for t, v in win_count.items()},
    )

advance_probs, win_probs = sim_group_probs(tuple(teams))

# Vis lag-kort
cols = st.columns(4)
for i, team in enumerate(teams):
    r = ratings.get(team, {})
    with cols[i]:
        st.metric(team, f"{advance_probs[team]}%", help="Sannsynlighet for å gå videre")
        st.caption(f"ELO: {r.get('elo', '?')} | Gruppeseier: {win_probs[team]}%")

st.markdown("---")

# Kamppredikasjoner i gruppen
st.subheader("Kampresultater i gruppen")
combos = [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i+1, len(teams))]

for home, away in combos:
    pred = predict_from_ratings(home, away, ratings, neutral=True)
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 2])
    c1.markdown(f"**{home}**")
    c2.metric("Hjemme", f"{pred['home_win']*100:.0f}%")
    c3.metric("Uavgjort", f"{pred['draw']*100:.0f}%")
    c4.metric("Borte", f"{pred['away_win']*100:.0f}%")
    c5.markdown(f"**{away}**")
    st.caption(f"Forventet: {pred['exp_home_goals']} – {pred['exp_away_goals']} | Over 2.5: {pred['over_25']*100:.0f}% | BTTS: {pred['btts_yes']*100:.0f}%")
    st.divider()

# Tabell: alle lag med ratinger
st.subheader("Lagratinger i gruppen")
rows = []
for t in teams:
    r = ratings.get(t, {})
    rows.append({
        "Lag": t,
        "ELO": r.get("elo", 0),
        "Angrep": r.get("attack", 1.0),
        "Forsvar": r.get("defense", 1.0),
        "Videre %": advance_probs[t],
        "Gruppeseier %": win_probs[t],
    })
st.dataframe(
    pd.DataFrame(rows).sort_values("ELO", ascending=False),
    use_container_width=True,
    hide_index=True,
)
