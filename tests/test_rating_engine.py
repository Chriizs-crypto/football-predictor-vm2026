from models.rating_engine import (
    get_ratings, compute_form_multiplier, bayesian_shrink, get_confidence_score
)


def test_ratings_returns_all_48_teams():
    r = get_ratings()
    assert len(r) == 48


def test_all_teams_have_required_fields():
    for team, r in get_ratings().items():
        assert "attack" in r
        assert "defense" in r
        assert "elo" in r


def test_form_good_results_above_one():
    f = compute_form_multiplier([1.0, 1.0, 1.0, 1.0, 1.0])
    assert f > 1.0


def test_form_bad_results_below_one():
    f = compute_form_multiplier([0.0, 0.0, 0.0, 0.0, 0.0])
    assert f < 1.0


def test_bayesian_shrink_pulls_toward_mean():
    high = bayesian_shrink(2.0, mean=1.0, weight=0.15)
    assert high < 2.0
    assert high > 1.0


def test_confidence_score_range():
    ratings = get_ratings()
    for team in ratings:
        c = get_confidence_score(team, ratings)
        assert 30 <= c <= 100
