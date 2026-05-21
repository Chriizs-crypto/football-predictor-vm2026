"""
Datahenting fra football-data.org og API-Football.
Faller tilbake til demo_data hvis API-nøkler mangler.
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from src.demo_data import GROUPS, TEAM_RATINGS, get_group_fixtures, HISTORICAL_WC_RESULTS, DEMO_ODDS

load_dotenv()

FD_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
WC_COMPETITION_ID = "WC"  # football-data.org kode for VM


def is_api_configured() -> bool:
    return bool(FD_API_KEY)


def get_teams() -> dict:
    return TEAM_RATINGS


def get_groups() -> dict:
    return GROUPS


def get_fixtures() -> list[dict]:
    if not is_api_configured():
        return get_group_fixtures()

    try:
        headers = {"X-Auth-Token": FD_API_KEY}
        r = requests.get(
            f"https://api.football-data.org/v4/competitions/{WC_COMPETITION_ID}/matches",
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()
        matches = r.json().get("matches", [])
        fixtures = []
        for m in matches:
            fixtures.append({
                "id": m["id"],
                "group": m.get("group", ""),
                "home": m["homeTeam"]["name"],
                "away": m["awayTeam"]["name"],
                "date": m["utcDate"][:10],
                "home_score": m["score"]["fullTime"].get("home"),
                "away_score": m["score"]["fullTime"].get("away"),
                "stage": m["stage"],
            })
        return fixtures
    except Exception:
        return get_group_fixtures()


def get_historical_results() -> list[dict]:
    return HISTORICAL_WC_RESULTS


def get_odds(home: str, away: str) -> dict | None:
    key = (home, away)
    return DEMO_ODDS.get(key) or DEMO_ODDS.get((away, home))


def get_fixtures_df() -> pd.DataFrame:
    return pd.DataFrame(get_fixtures())


def get_teams_df() -> pd.DataFrame:
    rows = []
    for name, r in TEAM_RATINGS.items():
        group = next((g for g, teams in GROUPS.items() if name in teams), "?")
        rows.append({"team": name, "group": group, **r})
    return pd.DataFrame(rows).sort_values("elo", ascending=False).reset_index(drop=True)
