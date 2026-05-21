import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_fetcher import get_teams_df, get_teams, get_groups
from src.poisson_model import predict_from_ratings

st.set_page_config(page_title="Research – VM 2026", page_icon="🔬", layout="wide")
st.title("🔬 Research & Analyse")

ratings = get_teams()
df = get_teams_df()
groups = get_groups()

tab1, tab2, tab3 = st.tabs(["Lagratinger", "H2H-analyse", "Gruppesammenligning"])

with tab1:
    st.subheader("Alle lagratinger")

    fig = px.scatter(
        df,
        x="attack",
        y="defense",
        text="team",
        color="elo",
        color_continuous_scale="Greens",
        size="elo",
        size_max=20,
        labels={"attack": "Angrep (høyere = bedre)", "defense": "Forsvar (lavere = bedre)"},
        title="Angrep vs. Forsvar — VM 2026 lag",
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Rå data")
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Hode-mot-hode prediksjon")
    all_teams = sorted(ratings.keys())

    col1, col2 = st.columns(2)
    home_team = col1.selectbox("Hjemmelag", all_teams, index=all_teams.index("Brazil"))
    away_team = col2.selectbox("Bortelag",  all_teams, index=all_teams.index("France"))

    if home_team == away_team:
        st.warning("Velg to forskjellige lag.")
    else:
        neutral = st.checkbox("Nøytral bane (VM-kamp)", value=True)
        pred = predict_from_ratings(home_team, away_team, ratings, neutral=neutral)

        c1, c2, c3 = st.columns(3)
        c1.metric(f"1 — {home_team}", f"{pred['home_win']*100:.1f}%")
        c2.metric("X — Uavgjort",     f"{pred['draw']*100:.1f}%")
        c3.metric(f"2 — {away_team}", f"{pred['away_win']*100:.1f}%")

        st.markdown(f"""
| | Verdi |
|---|---|
| Forventede mål | **{pred['exp_home_goals']} – {pred['exp_away_goals']}** |
| Over 2.5 mål | **{pred['over_25']*100:.0f}%** |
| Under 2.5 mål | **{pred['under_25']*100:.0f}%** |
| BTTS (begge scorer) | **{pred['btts_yes']*100:.0f}%** |
""")
        # Sannsynlighetskart
        matrix = pred["prob_matrix"][:6, :6]
        fig2 = go.Figure(data=go.Heatmap(
            z=matrix * 100,
            x=[str(i) for i in range(6)],
            y=[str(i) for i in range(6)],
            colorscale="Greens",
            text=[[f"{matrix[i][j]*100:.1f}%" for j in range(6)] for i in range(6)],
            texttemplate="%{text}",
        ))
        fig2.update_layout(
            title="Scoreline-sannsynligheter (%)",
            xaxis_title=f"Mål {away_team}",
            yaxis_title=f"Mål {home_team}",
            height=350,
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Sammenlign grupper etter gjennomsnitts-ELO")
    group_stats = []
    for g, teams in groups.items():
        elos = [ratings.get(t, {}).get("elo", 1500) for t in teams]
        group_stats.append({
            "Gruppe": f"Gruppe {g}",
            "Snitt ELO": round(sum(elos) / len(elos)),
            "Sterkeste lag": teams[0],
            "Lag": ", ".join(teams),
        })
    gdf = pd.DataFrame(group_stats).sort_values("Snitt ELO", ascending=False)

    fig3 = px.bar(
        gdf, x="Gruppe", y="Snitt ELO", color="Snitt ELO",
        color_continuous_scale="Greens",
        title="Gruppestyrke (gjennomsnittlig ELO)",
        text="Snitt ELO",
    )
    fig3.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(gdf, use_container_width=True, hide_index=True)
