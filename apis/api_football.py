"""
Klient for API-Football via RapidAPI.
Gratis tier: 100 requests/dag.
Registrer på rapidapi.com → søk "API-Football" → abonner på Free-plan.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL  = "https://api-football-v1.p.rapidapi.com/v3"
API_KEY   = os.getenv("API_FOOTBALL_KEY", "")
HEADERS   = {
    "X-RapidAPI-Key":  API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
}

WC_LEAGUE_ID = 1      # FIFA World Cup
WC_SEASON    = 2026


def is_configured() -> bool:
    return bool(API_KEY)


def _get(endpoint: str, params: dict) -> dict:
    if not is_configured():
        return {}
    try:
        r = requests.get(
            f"{BASE_URL}/{endpoint}",
            headers={**HEADERS, "X-RapidAPI-Key": API_KEY},
            params=params,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return {}


def get_fixtures() -> list[dict]:
    """Hent alle VM 2026-fixtures."""
    data = _get("fixtures", {"league": WC_LEAGUE_ID, "season": WC_SEASON})
    return data.get("response", [])


def get_standings() -> list[dict]:
    """Hent gruppetabeller."""
    data = _get("standings", {"league": WC_LEAGUE_ID, "season": WC_SEASON})
    return data.get("response", [])


def normalize_fixture(f: dict) -> dict:
    """Konverter API-Football fixture til internt Fixture-format."""
    fixture  = f.get("fixture", {})
    teams    = f.get("teams", {})
    goals    = f.get("goals", {})
    league   = f.get("league", {})

    home_score = goals.get("home")
    away_score = goals.get("away")

    round_str = league.get("round", "")
    group = ""
    if "Group" in round_str:
        # "Group Stage - 2" → vi trenger gruppe-bokstav fra lagnavn-mapping
        group = round_str.replace("Group Stage - ", "R")

    return {
        "id":         fixture.get("id"),
        "group":      group,
        "home":       teams.get("home", {}).get("name", ""),
        "away":       teams.get("away", {}).get("name", ""),
        "date":       fixture.get("date", "")[:10],
        "home_score": home_score,
        "away_score": away_score,
        "stage":      round_str,
        "status":     fixture.get("status", {}).get("short", "NS"),
    }


def check_connection() -> dict:
    """Diagnostikk — test tilkobling og returner status."""
    if not is_configured():
        return {"ok": False, "reason": "Ingen API-nøkkel konfigurert (API_FOOTBALL_KEY)"}
    try:
        r = requests.get(
            f"{BASE_URL}/fixtures",
            headers={**HEADERS, "X-RapidAPI-Key": API_KEY},
            params={"league": WC_LEAGUE_ID, "season": WC_SEASON},
            timeout=10,
        )
        if r.status_code == 200:
            data     = r.json()
            fixtures = data.get("response", [])
            errors   = data.get("errors", {})
            if errors:
                return {"ok": False, "reason": f"API-feil: {errors}"}
            remaining = r.headers.get("x-ratelimit-requests-remaining", "?")
            return {
                "ok":       True,
                "fixtures": len(fixtures),
                "remaining": remaining,
                "reason":   f"{len(fixtures)} VM 2026-kamper hentet · {remaining} requests igjen i dag",
            }
        elif r.status_code == 403:
            return {"ok": False, "reason": "403 Ugyldig API-nøkkel — sjekk RapidAPI-nøkkelen din"}
        elif r.status_code == 429:
            return {"ok": False, "reason": "429 Daglig grense nådd (100 req/dag) — prøv igjen i morgen"}
        else:
            return {"ok": False, "reason": f"HTTP {r.status_code}: {r.text[:200]}"}
    except requests.Timeout:
        return {"ok": False, "reason": "Timeout — API svarte ikke innen 10 sek"}
    except requests.RequestException as e:
        return {"ok": False, "reason": f"Nettverksfeil: {str(e)}"}
