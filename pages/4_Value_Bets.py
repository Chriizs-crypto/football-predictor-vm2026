import streamlit as st
import pandas as pd
from src.value_detector import get_all_value_bets
from src.data_fetcher import get_teams

st.set_page_config(page_title="Value Bets – VM 2026", page_icon="💰", layout="wide")
st.title("💰 Value Bets — VM 2026")
st.markdown("Kamper der modellens sannsynlighet overstiger bookmakerens. Edge = fordel i prosent.")

ratings = get_teams()

@st.cache_data(ttl=1800)
def load_value_bets():
    return get_all_value_bets(ratings)

bets = load_value_bets()

if not bets:
    st.info("Ingen value bets funnet med gjeldende odds og modell-parametere.")
    st.stop()

df = pd.DataFrame(bets)

# Filtrer på min. edge
min_edge = st.slider("Minimum edge (%)", min_value=1, max_value=20, value=4)
df = df[df["edge"] >= min_edge]

if df.empty:
    st.warning(f"Ingen bets med edge ≥ {min_edge}%.")
    st.stop()

st.metric("Antall value bets", len(df))

# Fargekode etter edge
def color_edge(val):
    if val >= 10:
        return "background-color: #1a4a2e; color: #1DB954"
    elif val >= 6:
        return "background-color: #1a3a1a"
    return ""

styled = df.style.applymap(color_edge, subset=["edge"])

st.dataframe(
    df.rename(columns={
        "kamp": "Kamp", "gruppe": "Gruppe", "dato": "Dato",
        "bet": "Bet", "edge": "Edge %", "odds": "Odds",
        "model_%": "Modell %", "book_%": "Bookmaker %", "EV": "Forventet verdi",
    }),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.caption("**Edge %** = Modell-sannsynlighet − Bookmaker-sannsynlighet (justert for margin). Positiv edge = potensielt value bet. Spill aldri mer enn du har råd til å tape.")
