import streamlit as st
import pandas as pd
import plotly.express as px
from models.rating_engine import get_ratings
from models.tournament_sim import simulate_tournament

st.set_page_config(page_title="Turneringssimulator – VM 2026", page_icon="🏆", layout="wide")
st.title("🏆 VM 2026 — Turneringssimulator")
st.caption("Monte Carlo-simulering — kjører 10 000 turneringer")

ratings = get_ratings()

n_sims = st.slider("Antall simuleringer", min_value=1000, max_value=10000, value=5000, step=1000)

if st.button("Kjør simulering", type="primary"):
    with st.spinner("Simulerer VM 2026..."):
        @st.cache_data(ttl=600)
        def run_sim(n):
            return simulate_tournament(ratings, n=n)
        results = run_sim(n_sims)

    rows = []
    for team, probs in results.items():
        rows.append({"Lag": team, **probs})
    df = pd.DataFrame(rows).sort_values("winner", ascending=False)
    df.columns = [c.replace("winner", "Vinner %")
                   .replace("final", "Finale %")
                   .replace("sf", "Semi %")
                   .replace("qf", "Kvartfinale %")
                   .replace("r16", "R. 16 %")
                   .replace("r32", "R. 32 %")
                   .replace("group_advance", "Videre fra gruppe %")
                  for c in df.columns]

    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: f"{x*100:.1f}%" if isinstance(x, float) else x)

    st.subheader("Vinnersannsynligheter — topp 15")
    top15 = df.head(15).copy()

    # Konverter tilbake til float for graf
    win_vals = [float(v.replace("%","")) for v in top15["Vinner %"]]
    fig = px.bar(
        x=top15["Lag"],
        y=win_vals,
        color=win_vals,
        color_continuous_scale="Greens",
        labels={"x": "Lag", "y": "Vinnersannsynlighet (%)"},
        title="Sannsynlighet for å vinne VM 2026 (%)",
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Komplett tabell")
    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.info("Trykk **Kjør simulering** for å starte Monte Carlo-analysen.")

    # Vis statiske ratinger mens vi venter
    st.subheader("Lagratinger (ELO)")
    rows = [{"Lag": t, "ELO": r["elo"], "Angrep": r["attack"], "Forsvar": r["defense"]}
            for t, r in sorted(ratings.items(), key=lambda x: x[1]["elo"], reverse=True)]
    st.dataframe(pd.DataFrame(rows).head(20), use_container_width=True, hide_index=True)
