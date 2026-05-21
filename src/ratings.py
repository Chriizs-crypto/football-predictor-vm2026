"""
Beregner og justerer nasjonallag-ratinger basert på historiske resultater.
"""

import numpy as np
from src.demo_data import TEAM_RATINGS


def get_ratings() -> dict:
    """Returnerer gjeldende ratinger (demo eller kalibrerte)."""
    return TEAM_RATINGS.copy()


def elo_expected(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))


def update_elo(rating_a: float, rating_b: float,
               score_a: float, k: float = 32.0) -> tuple[float, float]:
    """Enkel Elo-oppdatering. score_a: 1=seier, 0.5=uavgjort, 0=tap."""
    exp_a = elo_expected(rating_a, rating_b)
    new_a = rating_a + k * (score_a - exp_a)
    new_b = rating_b + k * ((1 - score_a) - (1 - exp_a))
    return new_a, new_b


def calibrate_ratings(historical_results: list[dict]) -> dict:
    """
    Kjør Elo-kalibrering over historiske resultater og returner
    justerte attack/defense-ratinger.
    """
    ratings = get_ratings()
    elo = {team: r["elo"] for team, r in ratings.items()}

    for match in historical_results:
        home = match["home"]
        away = match["away"]
        hs = match["home_score"]
        as_ = match["away_score"]

        if home not in elo:
            elo[home] = 1500
        if away not in elo:
            elo[away] = 1500

        if hs > as_:
            score = 1.0
        elif hs == as_:
            score = 0.5
        else:
            score = 0.0

        elo[home], elo[away] = update_elo(elo[home], elo[away], score)

    for team in ratings:
        if team in elo:
            ratings[team]["elo"] = round(elo[team], 1)

    return ratings


def get_league_weight(league: str) -> float:
    """Ligavektingskoeffisient — høyere for sterkere ligaer."""
    weights = {
        "Premier League":    1.00,
        "La Liga":           0.98,
        "Bundesliga":        0.95,
        "Serie A":           0.93,
        "Ligue 1":           0.90,
        "Eredivisie":        0.85,
        "Scottish Prem":     0.78,
        "Brasileirao":       0.80,
        "Saudi Pro League":  0.72,
        "Argentine Liga":    0.78,
        "MLS":               0.70,
        "Liga MX":           0.72,
    }
    return weights.get(league, 0.65)
