import pytest
import numpy as np
from models.poisson_model import predict_match, most_likely_score, remove_margin


def test_probabilities_sum_to_one():
    result = predict_match(1.5, 0.9, 1.2, 1.1)
    total = result["home_win"] + result["draw"] + result["away_win"]
    assert abs(total - 1.0) < 0.001


def test_stronger_team_wins_more():
    strong = predict_match(2.0, 0.7, 0.8, 1.3)
    weak   = predict_match(0.8, 1.3, 2.0, 0.7)
    assert strong["home_win"] > strong["away_win"]
    assert weak["away_win"]   > weak["home_win"]


def test_over_under_sums_to_one():
    result = predict_match(1.5, 0.9, 1.2, 1.1)
    assert abs(result["over_25"] + result["under_25"] - 1.0) < 0.001


def test_btts_range():
    result = predict_match(1.5, 0.9, 1.2, 1.1)
    assert 0.0 <= result["btts_yes"] <= 1.0


def test_most_likely_score_shape():
    result = predict_match(1.5, 0.9, 1.2, 1.1)
    h, a = most_likely_score(result["prob_matrix"])
    assert 0 <= h <= 8
    assert 0 <= a <= 8


def test_remove_margin():
    h, d, a = remove_margin(2.0, 3.5, 4.0)
    assert abs(h + d + a - 1.0) < 0.001
    assert h > d > 0
