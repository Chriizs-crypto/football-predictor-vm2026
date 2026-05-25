"""
Kelly Criterion for optimal stake-beregning.
Full Kelly er aggressiv — vi anbefaler 1/4 Kelly.
"""


def kelly_fraction(prob: float, odds: float) -> float:
    """
    Beregn Kelly-fraksjon av bankroll.
    prob: modellens sannsynlighet (0–1)
    odds: desimalodds
    Returnerer fraksjon (0–1). Negativ = no bet.
    """
    if odds <= 1.0 or prob <= 0.0:
        return 0.0
    b = odds - 1.0
    return max(0.0, (b * prob - (1 - prob)) / b)


def quarter_kelly(prob: float, odds: float) -> float:
    return kelly_fraction(prob, odds) * 0.25


def suggested_stake(prob: float, odds: float, bankroll: float = 1000.0,
                    kelly_divisor: float = 4.0) -> float:
    fraction = kelly_fraction(prob, odds) / kelly_divisor
    return round(fraction * bankroll, 2)


def expected_value(prob: float, odds: float) -> float:
    return round((prob * odds) - 1.0, 4)
