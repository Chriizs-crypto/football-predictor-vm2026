"""
Value bet-detektor.
Sammenligner modell-sannsynligheter mot bookmaker-odds og finner positiv edge.
"""

from src.poisson_model import predict_from_ratings, remove_margin, implied_probability
from src.data_fetcher import get_odds, get_fixtures, get_teams


MIN_EDGE = 0.04  # 4% minimum edge for å flagge


def analyse_fixture(home: str, away: str, ratings: dict) -> dict | None:
    """Returner value-bet-analyse for en kamp, eller None hvis ingen odds."""
    odds = get_odds(home, away)
    if not odds:
        return None

    pred = predict_from_ratings(home, away, ratings, neutral=True)

    bk_home, bk_draw, bk_away = remove_margin(
        odds["home"], odds["draw"], odds["away"]
    )

    edge_home = pred["home_win"] - bk_home
    edge_draw = pred["draw"]     - bk_draw
    edge_away = pred["away_win"] - bk_away

    bets = []
    for label, model_p, bk_p, odd in [
        ("1 (Hjemme)", pred["home_win"], bk_home, odds["home"]),
        ("X (Uavgjort)", pred["draw"],    bk_draw,  odds["draw"]),
        ("2 (Borte)",  pred["away_win"], bk_away,  odds["away"]),
    ]:
        edge = model_p - bk_p
        if edge >= MIN_EDGE:
            bets.append({
                "bet": label,
                "model_prob": round(model_p * 100, 1),
                "bookmaker_prob": round(bk_p * 100, 1),
                "edge": round(edge * 100, 1),
                "odds": odd,
                "ev": round((model_p * odd) - 1, 3),
            })

    return {
        "home": home,
        "away": away,
        "prediction": pred,
        "odds": odds,
        "value_bets": sorted(bets, key=lambda x: x["edge"], reverse=True),
    }


def get_all_value_bets(ratings: dict | None = None) -> list[dict]:
    """Analyser alle kommende kamper og returner value bets sortert etter edge."""
    if ratings is None:
        ratings = get_teams()

    fixtures = get_fixtures()
    value_bets = []

    for f in fixtures:
        if f["home_score"] is not None:
            continue  # allerede spilt
        result = analyse_fixture(f["home"], f["away"], ratings)
        if result and result["value_bets"]:
            for bet in result["value_bets"]:
                value_bets.append({
                    "kamp": f"{f['home']} vs {f['away']}",
                    "gruppe": f.get("group", ""),
                    "dato": f.get("date", ""),
                    "bet": bet["bet"],
                    "edge": bet["edge"],
                    "odds": bet["odds"],
                    "model_%": bet["model_prob"],
                    "book_%": bet["bookmaker_prob"],
                    "EV": bet["ev"],
                })

    return sorted(value_bets, key=lambda x: x["edge"], reverse=True)
