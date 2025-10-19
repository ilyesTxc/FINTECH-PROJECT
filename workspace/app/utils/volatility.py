import math
from typing import List, Tuple


def compute_log_returns(prices: List[float]) -> List[float]:
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] <= 0 or prices[i] <= 0:
            continue
        r = math.log(prices[i] / prices[i-1])
        returns.append(r)
    return returns


def compute_volatility_score(prices: List[float]) -> Tuple[int, float]:
    """Compute daily volatility (sigma) from price list and map to 0-100 risk score.

    Returns (score, sigma) where sigma is the standard deviation of log returns.
    """
    rets = compute_log_returns(prices)
    if not rets:
        return 0, 0.0
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / len(rets)
    sigma = math.sqrt(var)

    # Map sigma to 0-100. We'll pick a heuristic: sigma 0 -> 0, sigma 0.05 -> 20, 0.2 -> 80, 0.5 -> 100
    # Use a piecewise mapping by scaling with a tanh for smoothness
    normalized = math.tanh(sigma * 2)  # roughly maps larger sigmas to near 1
    score = int(min(100, round(normalized * 100)))
    return score, sigma
