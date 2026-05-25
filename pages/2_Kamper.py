import streamlit as st
import datetime
import plotly.graph_objects as go
from services.data_service import get_fixtures_df, get_teams, get_odds
from models.poisson_model import predict_from_ratings, most_likely_score
from utils.formatters import flag_emoji

st.set_page_config(page_title="Kamper – VM 2026", page_icon="⚽", layout="centered")
st.title("⚽ Kamper — VM 2026")

ratings = get_teams()
df = get_fixtures_df()
upcoming = df[df["home_score"].isna()].copy()

# ── Filter ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
groups = ["Alle"] + sorted(df["group"].dropna().unique().tolist())
sel_group = col1.selectbox("Gruppe", groups)
sel_team  = col2.selectbox("Lag", ["Alle"] + sorted(
    set(df["home"].tolist() + df["away"].tolist())
))

if sel_group != "Alle":
    upcoming = upcoming[upcoming["group"] == sel_group]
if sel_team != "Alle":
    upcoming = upcoming[(upcoming["home"] == sel_team) | (upcoming["away"] == sel_team)]

if upcoming.empty:
    st.info("Ingen kommende kamper funnet.")
    st.stop()

# ── Grupper etter dato ────────────────────────────────────────────────────────
upcoming = upcoming.sort_values("date")
dates = upcoming["date"].unique()

for date_str in dates:
    try:
        d = datetime.date.fromisoformat(date_str)
        today = datetime.date.today()
        if d == today:
            header = f"📅 I dag — {d.strftime('%d. %B')}"
        elif d == today + datetime.timedelta(days=1):
            header = f"📅 I morgen — {d.strftime('%d. %B')}"
        else:
            header = f"📅 {d.strftime('%d. %B %Y')}"
    except Exception:
        header = f"📅 {date_str}"

    st.subheader(header)
    day_rows = upcoming[upcoming["date"] == date_str]

    for _, row in day_rows.iterrows():
        home, away = row["home"], row["away"]
        pred = predict_from_ratings(home, away, ratings, neutral=True)
        score_h, score_a = most_likely_score(pred["prob_matrix"])
        odds = get_odds(home, away)

        title = f"{flag_emoji(home)} {home} vs {away} {flag_emoji(away)}  ·  Gruppe {row.get('group','')}"

        with st.expander(title):
            # 1X2
            c1, c2, c3 = st.columns(3)
            c1.metric(f"1 — {home}", f"{pred['home_win']*100:.1f}%",
                      delta=f"@ {odds['home']}" if odds else None)
            c2.metric("X", f"{pred['draw']*100:.1f}%",
                      delta=f"@ {odds['draw']}" if odds else None)
            c3.metric(f"2 — {away}", f"{pred['away_win']*100:.1f}%",
                      delta=f"@ {odds['away']}" if odds else None)

            # Nøkkeltall
            st.markdown(f"""
| | |
|---|---|
| 🎯 Mest sannsynlig | **{score_h} – {score_a}** |
| ⬆️ Over 2.5 mål | **{pred['over_25']*100:.0f}%** |
| ⬇️ Under 2.5 mål | **{pred['under_25']*100:.0f}%** |
| 🥅 Begge scorer (BTTS) | **{pred['btts_yes']*100:.0f}%** |
| ⚽ Forv. mål | **{pred['exp_home_goals']} – {pred['exp_away_goals']}** |
""")

            # Scoreline-heatmap
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
                title="Scoreline-sannsynligheter (%)",
                xaxis_title=f"Mål {away}",
                yaxis_title=f"Mål {home}",
                height=260,
                margin=dict(l=40, r=10, t=40, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)
