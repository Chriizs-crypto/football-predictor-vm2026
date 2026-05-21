import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_fetcher import get_fixtures_df, get_teams, get_odds
from src.poisson_model import predict_from_ratings, most_likely_score

st.set_page_config(page_title="Kamper – VM 2026", page_icon="⚽", layout="wide")
st.title("⚽ Kampresultat-prediksjoner")

ratings = get_teams()
df = get_fixtures_df()
upcoming = df[df["home_score"].isna()].copy()

# Filtrer
col1, col2 = st.columns(2)
groups = ["Alle"] + sorted(df["group"].dropna().unique().tolist())
sel_group = col1.selectbox("Gruppe", groups)
sel_team  = col2.selectbox("Søk lag", ["Alle"] + sorted(
    set(df["home"].tolist() + df["away"].tolist())
))

if sel_group != "Alle":
    upcoming = upcoming[upcoming["group"] == sel_group]
if sel_team != "Alle":
    upcoming = upcoming[(upcoming["home"] == sel_team) | (upcoming["away"] == sel_team)]

if upcoming.empty:
    st.info("Ingen kommende kamper funnet.")
    st.stop()

for _, row in upcoming.iterrows():
    home, away = row["home"], row["away"]
    pred = predict_from_ratings(home, away, ratings, neutral=True)
    score_h, score_a = most_likely_score(pred["prob_matrix"])
    odds = get_odds(home, away)

    with st.expander(f"⚽ {home} vs {away}  —  Gruppe {row.get('group','')}  |  {row.get('date','')}"):
        c1, c2, c3 = st.columns(3)
        c1.metric(f"1 — {home}", f"{pred['home_win']*100:.1f}%",
                  delta=f"Odds {odds['home']}" if odds else None)
        c2.metric("X — Uavgjort", f"{pred['draw']*100:.1f}%",
                  delta=f"Odds {odds['draw']}" if odds else None)
        c3.metric(f"2 — {away}", f"{pred['away_win']*100:.1f}%",
                  delta=f"Odds {odds['away']}" if odds else None)

        st.caption(f"Mest sannsynlig resultat: **{score_h} – {score_a}** | "
                   f"Over 2.5: {pred['over_25']*100:.0f}% | "
                   f"BTTS: {pred['btts_yes']*100:.0f}% | "
                   f"Forv. mål: {pred['exp_home_goals']} – {pred['exp_away_goals']}")

        # Sannsynlighetskart (heatmap)
        matrix = pred["prob_matrix"][:6, :6]
        fig = go.Figure(data=go.Heatmap(
            z=matrix * 100,
            x=[str(i) for i in range(6)],
            y=[str(i) for i in range(6)],
            colorscale="Greens",
            text=[[f"{matrix[i][j]*100:.1f}%" for j in range(6)] for i in range(6)],
            texttemplate="%{text}",
            showscale=False,
        ))
        fig.update_layout(
            title=f"Scoreline-sannsynligheter (%)",
            xaxis_title=f"Mål {away}",
            yaxis_title=f"Mål {home}",
            height=280,
            margin=dict(l=40, r=10, t=40, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)
