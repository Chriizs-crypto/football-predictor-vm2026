"""
Poisson-modell for kampresultat-prediksjoner.
"""
import numpy as np
from scipy.stats import poisson

AVG_GOALS = 1.35


def predict_match(home_attack: float, home_defense: float,
                  away_attack: float, away_defense: float,
                  home_advantage: float = 1.0,
                  max_goals: int = 8) -> dict:
    lam_home = home_attack * away_defense * AVG_GOALS * home_advantage
    lam_away = away_attack * home_defense * AVG_GOALS

    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_matrix[i][j] = poisson.pmf(i, lam_home) * poisson.pmf(j, lam_away)

    home_win = float(np.sum(np.tril(prob_matrix, -1)))
    draw     = float(np.sum(np.diag(prob_matrix)))
    away_win = float(np.sum(np.triu(prob_matrix, 1)))

    mask_over = np.zeros_like(prob_matrix, dtype=bool)
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            if i + j > 2:
                mask_over[i][j] = True
    over_25 = float(np.sum(prob_matrix[mask_over]))
    btts    = float(np.sum(prob_matrix[1:, 1:]))

    return {
        "home_win": home_win,
        "draw": draw,
        "away_win": away_win,
        "over_25": over_25,
        "under_25": 1 - over_25,
        "btts_yes": btts,
        "btts_no": 1 - btts,
        "exp_home_goals": round(lam_home, 2),
        "exp_away_goals": round(lam_away, 2),
        "prob_matrix": prob_matrix,
    }


def predict_from_ratings(home: str, away: str, ratings: dict, neutral: bool = True) -> dict:
    hr = ratings.get(home, {"attack": 1.0, "defense": 1.0})
    ar = ratings.get(away, {"attack": 1.0, "defense": 1.0})
    advantage = 1.0 if neutral else 1.08
    result = predict_match(hr["attack"], hr["defense"], ar["attack"], ar["defense"],
                           home_advantage=advantage)
    result["home_team"] = home
    result["away_team"] = away
    return result


def most_likely_score(prob_matrix: np.ndarray) -> tuple[int, int]:
    idx = np.unravel_index(np.argmax(prob_matrix), prob_matrix.shape)
    return int(idx[0]), int(idx[1])


def implied_probability(odds: float) -> float:
    return 1.0 / odds if odds > 0 else 0.0


def remove_margin(home_odds: float, draw_odds: float, away_odds: float) -> tuple[float, float, float]:
    raw = [implied_probability(o) for o in [home_odds, draw_odds, away_odds]]
    total = sum(raw)
    return tuple(p / total for p in raw)
