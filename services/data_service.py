"""
Sentralt datanivå. Kildeprioritet:
  1. API-Football (RapidAPI) — live, 100 req/dag gratis
  2. openfootball/worldcup.json — gratis fallback, oppdateres etter kampene
  3. Demo-data — alltid tilgjengelig
"""
import pandas as pd
from services.cache_service import get as cache_get, set as cache_set
from apis.api_football import (
    get_fixtures as af_get_fixtures,
    normalize_fixture,
    is_configured as af_configured,
)
from apis.openfootball_api import get_fixtures as of_get_fixtures
from apis.odds_api import get_odds_map, is_configured as odds_configured
from data.demo_data import GROUPS, TEAM_RATINGS, get_group_fixtures, HISTORICAL_WC_RESULTS, DEMO_ODDS


def api_status() -> dict:
    return {
        "api_football":  af_configured(),
        "odds_api":      odds_configured(),
        "football_data": af_configured(),   # bakoverkompatibilitet med app.py-banner
    }


def get_fixtures(use_cache: bool = True) -> list[dict]:
    """
    Henter fixtures med fallback-kjede:
    API-Football → openfootball → demo-data
    """
    cache_key = "wc2026_fixtures"
    if use_cache:
        cached = cache_get(cache_key)
        if cached:
            return cached

    # 1. API-Football
    if af_configured():
        raw = af_get_fixtures()
        if raw:
            fixtures = [normalize_fixture(f) for f in raw]
            cache_set(cache_key, fixtures, ttl=1800)
            return fixtures

    # 2. openfootball (gratis, ingen nøkkel)
    of_fixtures = of_get_fixtures()
    if of_fixtures:
        cache_set(cache_key, of_fixtures, ttl=3600)
        return of_fixtures

    # 3. Demo-data
    return get_group_fixtures()


def get_fixtures_df() -> pd.DataFrame:
    return pd.DataFrame(get_fixtures())


def get_groups() -> dict:
    return GROUPS


def get_teams() -> dict:
    return TEAM_RATINGS


def get_teams_df() -> pd.DataFrame:
    rows = []
    for name, r in TEAM_RATINGS.items():
        group = next((g for g, teams in GROUPS.items() if name in teams), "?")
        rows.append({"team": name, "group": group, **r})
    return pd.DataFrame(rows).sort_values("elo", ascending=False).reset_index(drop=True)


def get_historical_results() -> list[dict]:
    return HISTORICAL_WC_RESULTS


def get_odds(home: str, away: str) -> dict | None:
    cache_key = "wc2026_odds"
    cached = cache_get(cache_key)
    odds_map = cached if cached else {}

    if not cached and odds_configured():
        odds_map = {f"{k[0]}|{k[1]}": v for k, v in get_odds_map().items()}
        cache_set(cache_key, odds_map, ttl=900)

    for key in [f"{home}|{away}", f"{away}|{home}"]:
        if key in odds_map:
            return odds_map[key]

    return DEMO_ODDS.get((home, away)) or DEMO_ODDS.get((away, home))


def get_data_source() -> str:
    """Returner hvilken datakilde som er aktiv."""
    if af_configured():
        return "API-Football (live)"
    of_fixtures = of_get_fixtures()
    if of_fixtures:
        return "openfootball (gratis)"
    return "Demo-data"
