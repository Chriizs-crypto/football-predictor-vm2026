"""
Klient for The Odds API.
Gratis tier: 500 req/mnd. Registrer: https://the-odds-api.com/
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL    = "https://api.the-odds-api.com/v4"
API_KEY     = os.getenv("ODDS_API_KEY", "")
SPORT_KEY   = "soccer_fifa_world_cup"
REGIONS     = "eu"
MARKETS     = "h2h"
ODDS_FORMAT = "decimal"


def is_configured() -> bool:
    return bool(API_KEY)


def get_upcoming_odds() -> list[dict]:
    if not is_configured():
        return []
    try:
        r = requests.get(
            f"{BASE_URL}/sports/{SPORT_KEY}/odds",
            params={
                "apiKey":      API_KEY,
                "regions":     REGIONS,
                "markets":     MARKETS,
                "oddsFormat":  ODDS_FORMAT,
                "dateFormat":  "iso",
            },
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return []


def normalize_odds(event: dict) -> dict | None:
    bookmakers = event.get("bookmakers", [])
    if not bookmakers:
        return None

    bk = next((b for b in bookmakers if "pinnacle" in b["key"]), bookmakers[0])
    markets = {m["key"]: m for m in bk.get("markets", [])}
    h2h = markets.get("h2h", {})
    outcomes = {o["name"]: o["price"] for o in h2h.get("outcomes", [])}

    home_team = event["home_team"]
    away_team = event["away_team"]

    if home_team not in outcomes or away_team not in outcomes:
        return None

    return {
        "home":   outcomes[home_team],
        "draw":   outcomes.get("Draw", 3.5),
        "away":   outcomes[away_team],
        "source": bk["title"],
    }


def get_odds_map() -> dict[tuple[str, str], dict]:
    events = get_upcoming_odds()
    result = {}
    for event in events:
        odds = normalize_odds(event)
        if odds:
            key = (event["home_team"], event["away_team"])
            result[key] = odds
    return result
