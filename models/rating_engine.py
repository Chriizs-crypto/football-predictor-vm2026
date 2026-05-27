"""
Rating Engine 2.0.
ELO + form + momentum + kontinental vekting + Bayesian regression.
"""
import numpy as np
from data.demo_data import TEAM_RATINGS, HISTORICAL_WC_RESULTS

LEAGUE_WEIGHTS = {
    "Premier League":   1.00,
    "La Liga":          0.98,
    "Bundesliga":       0.95,
    "Serie A":          0.93,
    "Ligue 1":          0.90,
    "Eredivisie":       0.85,
    "Brasileirao":      0.82,
    "Argentine Liga":   0.80,
    "Scottish Prem":    0.78,
    "Saudi Pro League": 0.72,
    "Liga MX":          0.72,
    "MLS":              0.70,
}

CONTINENTAL_BOOST = {
    "UEFA": 1.00,
    "CONMEBOL": 0.97,
    "CAF": 0.88,
    "AFC": 0.90,
    "CONCACAF": 0.88,
    "OFC": 0.80,
}

TEAM_CONFEDERATION = {
    # CONMEBOL
    "Brazil": "CONMEBOL", "Argentina": "CONMEBOL", "Colombia": "CONMEBOL",
    "Ecuador": "CONMEBOL", "Uruguay": "CONMEBOL", "Paraguay": "CONMEBOL",
    # UEFA
    "France": "UEFA", "Germany": "UEFA", "Spain": "UEFA", "England": "UEFA",
    "Portugal": "UEFA", "Netherlands": "UEFA", "Croatia": "UEFA",
    "Austria": "UEFA", "Turkey": "UEFA", "Switzerland": "UEFA",
    "Scotland": "UEFA", "Norway": "UEFA", "Sweden": "UEFA",
    "Czech Republic": "UEFA", "Bosnia & Herzegovina": "UEFA",
    # CAF
    "Morocco": "CAF", "Senegal": "CAF", "Ivory Coast": "CAF",
    "Egypt": "CAF", "South Africa": "CAF", "Tunisia": "CAF",
    "Algeria": "CAF", "Ghana": "CAF", "DR Congo": "CAF", "Cape Verde": "CAF",
    # AFC
    "Japan": "AFC", "South Korea": "AFC", "Iran": "AFC", "Saudi Arabia": "AFC",
    "Australia": "AFC", "Iraq": "AFC", "Uzbekistan": "AFC",
    "Qatar": "AFC", "Jordan": "AFC",
    # CONCACAF
    "USA": "CONCACAF", "Canada": "CONCACAF", "Mexico": "CONCACAF",
    "Panama": "CONCACAF", "Haiti": "CONCACAF", "Curaçao": "CONCACAF",
    # OFC
    "New Zealand": "OFC",
    # Belgium (UEFA — explicitly listed)
    "Belgium": "UEFA",
}


def get_confederation(team: str) -> str:
    return TEAM_CONFEDERATION.get(team, "UEFA")


def elo_expected(ra: float, rb: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))


def update_elo(ra: float, rb: float, score_a: float, k: float = 30.0) -> tuple[float, float]:
    exp = elo_expected(ra, rb)
    return ra + k * (score_a - exp), rb + k * ((1 - score_a) - (1 - exp))


def compute_form_multiplier(results: list[float]) -> float:
    """
    results: liste med 1.0 (seier), 0.5 (uavgjort), 0.0 (tap) — nyeste sist.
    Returnerer multiplier 0.85–1.15.
    """
    if not results:
        return 1.0
    weights = np.array([0.1, 0.15, 0.2, 0.25, 0.3])[:len(results)]
    weights /= weights.sum()
    score = np.dot(weights, results[-len(weights):])
    return round(0.85 + (score * 0.30), 4)


def bayesian_shrink(value: float, mean: float = 1.0, weight: float = 0.15) -> float:
    return (1 - weight) * value + weight * mean


def get_ratings(historical: list[dict] | None = None) -> dict:
    ratings = {k: dict(v) for k, v in TEAM_RATINGS.items()}

    if historical is None:
        historical = HISTORICAL_WC_RESULTS

    elo = {team: r["elo"] for team, r in ratings.items()}

    for match in historical:
        home, away = match["home"], match["away"]
        hs, as_ = match["home_score"], match["away_score"]
        if home not in elo: elo[home] = 1500
        if away not in elo: elo[away] = 1500
        score = 1.0 if hs > as_ else (0.5 if hs == as_ else 0.0)
        elo[home], elo[away] = update_elo(elo[home], elo[away], score)

    for team in ratings:
        if team in elo:
            ratings[team]["elo"] = round(elo[team], 1)

        conf = get_confederation(team)
        boost = CONTINENTAL_BOOST.get(conf, 0.90)

        ratings[team]["attack"]  = round(bayesian_shrink(ratings[team]["attack"]) * boost, 4)
        ratings[team]["defense"] = round(bayesian_shrink(ratings[team]["defense"], mean=1.0), 4)
        ratings[team].setdefault("form", 1.0)
        ratings[team].setdefault("momentum", 0.0)
        ratings[team]["confederation"] = conf

    return ratings


def get_confidence_score(team: str, ratings: dict) -> float:
    r = ratings.get(team, {})
    elo = r.get("elo", 1600)
    score = max(35, min(95, (elo - 1400) / 700 * 65 + 30))
    return round(score, 1)


def get_league_weight(league: str) -> float:
    return LEAGUE_WEIGHTS.get(league, 0.65)
