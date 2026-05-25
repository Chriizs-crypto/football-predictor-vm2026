"""
Sentralt datanivå. Kombinerer API-data med demo-fallback og cache.
Alle pages og models importerer kun herfra.
"""
import pandas as pd
from services.cache_service import get as cache_get, set as cache_set
from apis.football_data_api import get_wc_matches, normalize_match, is_configured as fd_configured
from apis.odds_api import get_odds_map, is_configured as odds_configured
from data.demo_data import GROUPS, TEAM_RATINGS, get_group_fixtures, HISTORICAL_WC_RESULTS, DEMO_ODDS


def api_status() -> dict:
    return {
        "football_data": fd_configured(),
        "odds_api":      odds_configured(),
    }


def get_fixtures(use_cache: bool = True) -> list[dict]:
    cache_key = "wc2026_fixtures"
    if use_cache:
        cached = cache_get(cache_key)
        if cached:
            return cached

    if fd_configured():
        raw = get_wc_matches()
        if raw:
            fixtures = [normalize_match(m) for m in raw]
            cache_set(cache_key, fixtures, ttl=1800)
            return fixtures

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
