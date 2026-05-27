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


def check_connection() -> dict:
    """Diagnostikk — returner status og feilmelding fra API."""
    if not is_configured():
        return {"ok": False, "reason": "Ingen API-nøkkel konfigurert (FOOTBALL_DATA_API_KEY)"}
    try:
        r = requests.get(f"{BASE_URL}/competitions/{WC_ID}/matches",
                         headers=_headers(), timeout=10)
        if r.status_code == 200:
            matches = r.json().get("matches", [])
            return {"ok": True, "matches": len(matches),
                    "reason": f"{len(matches)} kamper hentet fra football-data.org"}
        elif r.status_code == 403:
            return {"ok": False, "reason": "403 Forbudt — nøkkelen har ikke tilgang til VM-data (krever høyere plan)"}
        elif r.status_code == 404:
            return {"ok": False, "reason": f"404 Ikke funnet — competition-kode '{WC_ID}' finnes ikke ennå"}
        elif r.status_code == 429:
            return {"ok": False, "reason": "429 Rate limit — for mange requests (maks 10/min på gratis)"}
        else:
            return {"ok": False, "reason": f"HTTP {r.status_code}: {r.text[:200]}"}
    except requests.Timeout:
        return {"ok": False, "reason": "Timeout — football-data.org svarte ikke"}
    except requests.RequestException as e:
        return {"ok": False, "reason": f"Nettverksfeil: {str(e)}"}


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
