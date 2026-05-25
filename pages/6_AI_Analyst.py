import streamlit as st
from models.rating_engine import get_ratings
from services.analyst_service import (
    team_insight, match_preview, tournament_dark_horses, overrated_teams
)

st.set_page_config(page_title="AI Analyst – VM 2026", page_icon="🤖", layout="centered")
st.title("🤖 AI Analyst — VM 2026")

ratings = get_ratings()

tab1, tab2, tab3 = st.tabs(["Laganalyse", "Kampforhåndsvisning", "Turneringsinnsikt"])

with tab1:
    team = st.selectbox("Velg lag", sorted(ratings.keys()))
    st.markdown(team_insight(team, ratings))

with tab2:
    all_teams = sorted(ratings.keys())
    c1, c2 = st.columns(2)
    home = c1.selectbox("Hjemmelag", all_teams, index=all_teams.index("Brazil"))
    away = c2.selectbox("Bortelag",  all_teams, index=all_teams.index("France"))
    if home != away:
        st.markdown(match_preview(home, away, ratings))
    else:
        st.warning("Velg to forskjellige lag.")

with tab3:
    st.subheader("Mørke hester")
    st.caption("Lag som er undervurdert av markedet — sterk angrepsrating relativt til ELO.")
    for h in tournament_dark_horses(ratings):
        with st.expander(f"🐎 {h['team']} — score {h['dark_horse_score']}"):
            st.markdown(h["insight"])

    st.subheader("Potensielt overvurderte lag")
    st.caption("Høy ELO men svakere angrepsstyrke enn forventet.")
    for r in overrated_teams(ratings):
        st.markdown(f"- **{r['team']}** — ELO {r['elo']}, angrep {r['attack']}")
