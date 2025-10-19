from app.utils.volatility import compute_volatility_score
from app.utils import scam_detector


def test_personalized_neutral_no_contract():
    prices = [100, 101, 99, 100.5, 102]
    vol_score, sigma = compute_volatility_score(prices)
    # no contract, so final should weigh only volatility (scam_penalty 0)
    # emulate weights from main: neutral -> w_vol 0.55, w_scam 0.45
    final = int(min(100, round(0.55 * vol_score + 0.45 * 0)))
    assert final >= 0 and final <= 100


def test_scam_detector_unverified():
    res = scam_detector.analyze_contract("0x0000000000000000000000000000000000000000", etherscan_api_key=None)
    assert res["verified"] is False
    assert res["risky"] is True
    assert "source not" in (res["issues"][0].lower())
