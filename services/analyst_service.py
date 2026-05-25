"""
Regelbasert AI-analyse. Genererer innsikter per lag og per kamp.
"""
from models.rating_engine import get_ratings, get_confidence_score
from models.poisson_model import predict_from_ratings
from utils.formatters import flag_emoji


def team_insight(team: str, ratings: dict | None = None) -> str:
    if ratings is None:
        ratings = get_ratings()
    r = ratings.get(team)
    if not r:
        return f"Ingen data tilgjengelig for {team}."

    attack  = r.get("attack", 1.0)
    defense = r.get("defense", 1.0)
    elo     = r.get("elo", 1600)
    conf    = get_confidence_score(team, ratings)

    lines = []

    if attack > 1.6:
        lines.append(f"{flag_emoji(team)} **{team}** er en av de farligste angrepsteamene i turneringen.")
    elif attack > 1.3:
        lines.append(f"{flag_emoji(team)} **{team}** har et solid angrep over snittet.")
    else:
        lines.append(f"{flag_emoji(team)} **{team}** sliter offensivt og vil trenge effektivitet.")

    if defense < 0.80:
        lines.append("Defensivt er de svært vanskelige å bryte ned.")
    elif defense < 1.0:
        lines.append("Defensivt er de over snittet — vanskelig å score mot.")
    else:
        lines.append("Forsvaret er en potensiell svakhet som motstandere kan utnytte.")

    if elo > 1950:
        lines.append(f"Med ELO {elo:.0f} er de favoritter til å gå langt.")
    elif elo > 1750:
        lines.append(f"ELO {elo:.0f} plasserer dem blant de solide midtsjikts-lagene.")
    else:
        lines.append(f"ELO {elo:.0f} — betraktes som underdog i de fleste kamper.")

    lines.append(f"Modell-confidence: **{conf}/100**")
    return " ".join(lines)


def match_preview(home: str, away: str, ratings: dict | None = None) -> str:
    if ratings is None:
        ratings = get_ratings()
    pred = predict_from_ratings(home, away, ratings, neutral=True)
    hr = ratings.get(home, {})
    ar = ratings.get(away, {})

    lines = []
    lines.append(f"### {flag_emoji(home)} {home} vs {away} {flag_emoji(away)}")

    if pred["home_win"] > 0.55:
        lines.append(f"**{home}** er klar favoritt med {pred['home_win']*100:.0f}% vinnersannsynlighet.")
    elif pred["away_win"] > 0.55:
        lines.append(f"**{away}** er klar favoritt med {pred['away_win']*100:.0f}% vinnersannsynlighet.")
    else:
        lines.append(f"Jevn kamp — uavgjort har {pred['draw']*100:.0f}% sannsynlighet.")

    exp_total = pred["exp_home_goals"] + pred["exp_away_goals"]
    if exp_total > 2.8:
        lines.append(f"Modellen forventer en åpen kamp med {exp_total:.1f} mål totalt — over 2.5 er sannsynlig.")
    elif exp_total < 2.0:
        lines.append(f"Lav scoringsforventning ({exp_total:.1f} mål) — under 2.5 er favoritt.")
    else:
        lines.append(f"Forventet {exp_total:.1f} mål — kamp på grensen til over/under 2.5.")

    if pred["btts_yes"] > 0.55:
        lines.append("BTTS (begge lag scorer) er sannsynlig.")

    if (hr.get("attack", 1.0) > 1.5 and ar.get("defense", 1.0) > 1.0):
        lines.append(f"**{home}** kan utnytte et sårbart forsvar hos {away}.")
    if (ar.get("attack", 1.0) > 1.5 and hr.get("defense", 1.0) > 1.0):
        lines.append(f"**{away}** vil true bakover mot {home}s forsvar.")

    return "\n\n".join(lines)


def tournament_dark_horses(ratings: dict | None = None, top_n: int = 5) -> list[dict]:
    if ratings is None:
        ratings = get_ratings()

    horses = []
    elo_values = [r["elo"] for r in ratings.values()]
    avg_elo = sum(elo_values) / len(elo_values)

    for team, r in ratings.items():
        attack_surplus = r.get("attack", 1.0) - 1.0
        elo_deficit = (avg_elo - r.get("elo", avg_elo)) / 400
        dark_horse_score = attack_surplus + elo_deficit * 0.5
        if dark_horse_score > 0.05:
            horses.append({
                "team":             team,
                "dark_horse_score": round(dark_horse_score, 3),
                "attack":           r.get("attack", 1.0),
                "elo":              r.get("elo", 1600),
                "insight":          team_insight(team, ratings),
            })

    return sorted(horses, key=lambda x: x["dark_horse_score"], reverse=True)[:top_n]


def overrated_teams(ratings: dict | None = None, top_n: int = 5) -> list[dict]:
    if ratings is None:
        ratings = get_ratings()
    teams = []
    for team, r in ratings.items():
        overrate_score = (r.get("elo", 1600) / 2000) - r.get("attack", 1.0)
        if overrate_score > 0:
            teams.append({"team": team, "score": round(overrate_score, 3),
                          "elo": r.get("elo"), "attack": r.get("attack")})
    return sorted(teams, key=lambda x: x["score"], reverse=True)[:top_n]
