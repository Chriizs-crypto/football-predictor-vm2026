"""
Fallback-datakilde: openfootball/worldcup.json på GitHub.
Ingen API-nøkkel. Oppdateres etter at kampresultater er spilt.
"""
import requests

URLS = [
    "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json",
    "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.groups.json",
]


def get_fixtures() -> list[dict]:
    """Prøv å hente VM 2026-data fra openfootball. Returnerer [] hvis ikke tilgjengelig."""
    for url in URLS:
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                data = r.json()
                return _normalize(data)
        except requests.RequestException:
            continue
    return []


def _normalize(data: dict) -> list[dict]:
    """Konverter openfootball-format til internt Fixture-format."""
    fixtures = []
    match_id = 10000

    rounds = data.get("rounds", [])
    for rnd in rounds:
        round_name = rnd.get("name", "")
        for match in rnd.get("matches", []):
            team1 = match.get("team1", {})
            team2 = match.get("team2", {})
            score = match.get("score", {})
            ft    = score.get("ft", [None, None]) if score else [None, None]

            fixtures.append({
                "id":         match_id,
                "group":      _extract_group(round_name),
                "home":       team1.get("name", "") if isinstance(team1, dict) else str(team1),
                "away":       team2.get("name", "") if isinstance(team2, dict) else str(team2),
                "date":       match.get("date", ""),
                "home_score": ft[0] if ft and len(ft) > 0 else None,
                "away_score": ft[1] if ft and len(ft) > 1 else None,
                "stage":      round_name,
                "status":     "FT" if ft and ft[0] is not None else "NS",
            })
            match_id += 1

    return fixtures


def _extract_group(round_name: str) -> str:
    """'Matchday 1 (Group A)' → 'A'"""
    if "Group" in round_name:
        parts = round_name.split("Group")
        if len(parts) > 1:
            return parts[-1].strip().strip("()")
    return ""
