"""
Monte Carlo-simulator for VM 2026.
"""
import numpy as np
from collections import defaultdict
from models.poisson_model import predict_match
from data.demo_data import GROUPS


def simulate_match(home: str, away: str, ratings: dict) -> tuple[str, str]:
    hr = ratings.get(home, {"attack": 1.0, "defense": 1.0})
    ar = ratings.get(away, {"attack": 1.0, "defense": 1.0})
    res = predict_match(hr["attack"], hr["defense"], ar["attack"], ar["defense"])
    r = np.random.random()
    if r < res["home_win"]:
        return home, away
    elif r < res["home_win"] + res["draw"]:
        winner = home if np.random.random() < 0.5 else away
        return winner, (away if winner == home else home)
    else:
        return away, home


def simulate_group(teams: list[str], ratings: dict) -> list[dict]:
    standing = {t: {"team": t, "pts": 0, "gf": 0, "ga": 0} for t in teams}
    for i, home in enumerate(teams):
        for away in teams[i + 1:]:
            hr = ratings.get(home, {"attack": 1.0, "defense": 1.0})
            ar = ratings.get(away, {"attack": 1.0, "defense": 1.0})
            res = predict_match(hr["attack"], hr["defense"], ar["attack"], ar["defense"])
            hg = np.random.poisson(res["exp_home_goals"])
            ag = np.random.poisson(res["exp_away_goals"])
            standing[home]["gf"] += hg; standing[home]["ga"] += ag
            standing[away]["gf"] += ag; standing[away]["ga"] += hg
            if hg > ag:   standing[home]["pts"] += 3
            elif hg == ag: standing[home]["pts"] += 1; standing[away]["pts"] += 1
            else:          standing[away]["pts"] += 3
    return sorted(standing.values(), key=lambda x: (x["pts"], x["gf"]-x["ga"], x["gf"]), reverse=True)


def simulate_tournament(ratings: dict, groups: dict | None = None, n: int = 10_000) -> dict:
    if groups is None:
        groups = GROUPS
    counters = defaultdict(lambda: defaultdict(int))
    for _ in range(n):
        qualifiers = {}
        third_place = []
        for group, teams in groups.items():
            table = simulate_group(teams, ratings)
            qualifiers[group] = [table[0]["team"], table[1]["team"]]
            third_place.append({"team": table[2]["team"], "pts": table[2]["pts"],
                                 "gd": table[2]["gf"]-table[2]["ga"], "gf": table[2]["gf"]})
            for i, row in enumerate(table):
                if i < 2: counters[row["team"]]["group_advance"] += 1
        third_sorted = sorted(third_place, key=lambda x: (x["pts"], x["gd"], x["gf"]), reverse=True)
        best_third = [t["team"] for t in third_sorted[:8]]
        for t in best_third: counters[t]["group_advance"] += 1
        r32_teams = []
        for g in sorted(groups.keys()): r32_teams.extend(qualifiers[g])
        r32_teams.extend(best_third)
        np.random.shuffle(r32_teams)
        current_round = r32_teams
        for stage in ["r32", "r16", "qf", "sf", "final"]:
            next_round = []
            for i in range(0, len(current_round), 2):
                if i + 1 < len(current_round):
                    winner, _ = simulate_match(current_round[i], current_round[i+1], ratings)
                    next_round.append(winner)
                    counters[winner][stage] += 1
            current_round = next_round
        if current_round: counters[current_round[0]]["winner"] += 1
    results = {}
    for team in ratings:
        results[team] = {s: round(counters[team].get(s, 0) / n, 4)
                         for s in ["group_advance", "r32", "r16", "qf", "sf", "final", "winner"]}
    return results
