from typing import TypedDict


class TeamRating(TypedDict):
    attack: float
    defense: float
    elo: float
    form: float
    momentum: float


class Fixture(TypedDict):
    id: int
    group: str
    home: str
    away: str
    date: str
    home_score: int | None
    away_score: int | None
    stage: str


class Odds(TypedDict):
    home: float
    draw: float
    away: float
    source: str


class ValueBet(TypedDict):
    match: str
    group: str
    date: str
    bet: str
    edge: float
    odds: float
    model_prob: float
    book_prob: float
    ev: float
    kelly_fraction: float
    kelly_stake: float
