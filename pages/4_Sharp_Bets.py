import streamlit as st
import pandas as pd
from services.odds_service import get_sharp_bets
from models.rating_engine import get_ratings

st.set_page_config(page_title="Sharp Bets – VM 2026", page_icon="💰", layout="wide")
st.title("💰 Sharp Bets — VM 2026")
st.markdown("Kamper der modellen har **positiv edge** mot bookmaker. Kelly Criterion angir optimal stake.")

ratings = get_ratings()

col1, col2 = st.columns(2)
bankroll = col1.number_input("Bankroll (kr)", min_value=100, max_value=100000,
                              value=1000, step=100)
min_edge = col2.slider("Minimum edge (%)", 1, 20, 3)


@st.cache_data(ttl=900)
def load_bets(br, me):
    bets = get_sharp_bets(ratings, bankroll=br)
    return [b for b in bets if b["edge_%"] >= me]


bets = load_bets(bankroll, min_edge)

if not bets:
    st.info(f"Ingen bets med edge ≥ {min_edge}% funnet.")
    st.stop()

st.metric("Antall sharp bets", len(bets))

df = pd.DataFrame(bets)
stake_col = f"stake_{int(bankroll)}kr"
show_cols = ["kamp", "gruppe", "dato", "bet", "edge_%", "odds", "model_%", "book_%", "EV", "kelly_%", stake_col]
show_cols = [c for c in show_cols if c in df.columns]

st.dataframe(
    df[show_cols].rename(columns={
        "kamp": "Kamp", "gruppe": "Gruppe", "dato": "Dato",
        "bet": "Bet", "edge_%": "Edge %", "odds": "Odds",
        "model_%": "Modell %", "book_%": "Bookmaker %",
        "EV": "Forventet verdi", "kelly_%": "Kelly %",
        stake_col: f"Stake ({bankroll}kr)",
    }),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.caption("**Edge %** = differansen mellom modellens og bookmakerens sannsynlighet. **Kelly %** = anbefalt andel av bankroll (1/4 Kelly). Gamble ansvarlig.")
