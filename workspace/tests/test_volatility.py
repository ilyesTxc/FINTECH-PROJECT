from app.utils.volatility import compute_volatility_score


def test_volatility_constant_prices():
    prices = [100, 100, 100, 100]
    score, sigma = compute_volatility_score(prices)
    assert sigma == 0
    assert score == 0


def test_volatility_increasing_prices():
    prices = [100, 110, 121, 133.1]
    score, sigma = compute_volatility_score(prices)
    assert score >= 0 and score <= 100
    assert sigma > 0
