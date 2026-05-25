from utils.kelly import kelly_fraction, quarter_kelly, expected_value, suggested_stake


def test_positive_edge_gives_positive_kelly():
    assert kelly_fraction(0.6, 2.0) > 0


def test_negative_edge_gives_zero():
    assert kelly_fraction(0.4, 2.0) == 0.0


def test_quarter_kelly_less_than_full():
    full = kelly_fraction(0.6, 2.0)
    quarter = quarter_kelly(0.6, 2.0)
    assert quarter == full * 0.25


def test_positive_ev_on_value_bet():
    ev = expected_value(0.55, 2.0)
    assert ev > 0


def test_negative_ev_on_no_value():
    ev = expected_value(0.45, 2.0)
    assert ev < 0


def test_suggested_stake_within_bankroll():
    stake = suggested_stake(0.6, 2.0, bankroll=1000)
    assert 0 <= stake <= 1000
