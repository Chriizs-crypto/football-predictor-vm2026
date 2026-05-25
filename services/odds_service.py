"""
Kombinerer live odds (The Odds API) med demo-fallback.
Beregner edge og Kelly for alle tilgjengelige kamper.
"""
from models.poisson_model import predict_from_ratings, remove_margin
from utils.kelly import quarter_kelly, expected_value, suggested_stake
from services.data_service import get_fixtures, get_odds, get_teams

MIN_EDGE = 0.03


def analyse_match(home: str, away: str, ratings: dict) -> dict | None:
    odds = get_odds(home, away)
    if not odds:
        return None

    pred = predict_from_ratings(home, away, ratings, neutral=True)
    bk_home, bk_draw, bk_away = remove_margin(odds["home"], odds["draw"], odds["away"])

    bets = []
    for label, model_p, bk_p, odd in [
        ("1 — Hjemme", pred["home_win"], bk_home, odds["home"]),
        ("X — Uavgjort", pred["draw"],   bk_draw,  odds["draw"]),
        ("2 — Borte",  pred["away_win"], bk_away,  odds["away"]),
    ]:
        edge = model_p - bk_p
        if edge >= MIN_EDGE:
            bets.append({
                "bet":        label,
                "model_prob": round(model_p * 100, 1),
                "book_prob":  round(bk_p * 100, 1),
                "edge":       round(edge * 100, 1),
                "odds":       odd,
                "ev":         round(expected_value(model_p, odd), 3),
                "kelly_pct":  round(quarter_kelly(model_p, odd) * 100, 2),
                "stake_1000": suggested_stake(model_p, odd, 1000),
            })

    return {
        "home": home, "away": away,
        "prediction": pred, "odds": odds,
        "value_bets": sorted(bets, key=lambda x: x["edge"], reverse=True),
    }


def get_sharp_bets(ratings: dict | None = None, bankroll: float = 1000.0) -> list[dict]:
    if ratings is None:
        ratings = get_teams()
    bets = []
    for f in get_fixtures():
        if f.get("home_score") is not None:
            continue
        result = analyse_match(f["home"], f["away"], ratings)
        if not result or not result["value_bets"]:
            continue
        for b in result["value_bets"]:
            bets.append({
                "kamp":       f"{f['home']} vs {f['away']}",
                "gruppe":     f.get("group", ""),
                "dato":       f.get("date", ""),
                "bet":        b["bet"],
                "edge_%":     b["edge"],
                "odds":       b["odds"],
                "model_%":    b["model_prob"],
                "book_%":     b["book_prob"],
                "EV":         b["ev"],
                "kelly_%":    b["kelly_pct"],
                f"stake_{int(bankroll)}kr": b["stake_1000"],
            })
    return sorted(bets, key=lambda x: x["edge_%"], reverse=True)
