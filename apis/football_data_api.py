"""
Klient for football-data.org v4 API.
Gratis tier: 10 req/min, VM 2026 inkludert.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.football-data.org/v4"
API_KEY  = os.getenv("FOOTBALL_DATA_API_KEY", "")
WC_ID    = "WC"


def _headers() -> dict:
    return {"X-Auth-Token": API_KEY}


def is_configured() -> bool:
    return bool(API_KEY)


def get_wc_matches() -> list[dict]:
    if not is_configured():
        return []
    try:
        r = requests.get(f"{BASE_URL}/competitions/{WC_ID}/matches",
                         headers=_headers(), timeout=10)
        r.raise_for_status()
        return r.json().get("matches", [])
    except requests.RequestException:
        return []


def get_wc_standings() -> list[dict]:
    if not is_configured():
        return []
    try:
        r = requests.get(f"{BASE_URL}/competitions/{WC_ID}/standings",
                         headers=_headers(), timeout=10)
        r.raise_for_status()
        return r.json().get("standings", [])
    except requests.RequestException:
        return []


def get_wc_teams() -> list[dict]:
    if not is_configured():
        return []
    try:
        r = requests.get(f"{BASE_URL}/competitions/{WC_ID}/teams",
                         headers=_headers(), timeout=10)
        r.raise_for_status()
        return r.json().get("teams", [])
    except requests.RequestException:
        return []


def normalize_match(m: dict) -> dict:
    return {
        "id": m["id"],
        "group": m.get("group", ""),
        "home": m["homeTeam"]["shortName"] or m["homeTeam"]["name"],
        "away": m["awayTeam"]["shortName"] or m["awayTeam"]["name"],
        "date": m["utcDate"][:10],
        "home_score": m["score"]["fullTime"].get("home"),
        "away_score": m["score"]["fullTime"].get("away"),
        "stage": m["stage"],
        "status": m.get("status", "SCHEDULED"),
    }
