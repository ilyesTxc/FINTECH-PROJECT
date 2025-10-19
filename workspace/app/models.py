from pydantic import BaseModel
from typing import List, Optional

class PricesIn(BaseModel):
    prices: List[float]


class MoneyMeterOut(BaseModel):
    score: int
    volatility: float
    n: int


class ContractIn(BaseModel):
    address: str
    etherscan_api_key: Optional[str] = None


class ScamCheckOut(BaseModel):
    address: str
    verified: bool
    risky: bool
    issues: Optional[List[str]] = None


class RiskProfileIn(BaseModel):
    prices: List[float]
    risk_preference: str = "neutral"  # conservative, neutral, aggressive
    contract_address: Optional[str] = None
    etherscan_api_key: Optional[str] = None


class PersonalizedScoreOut(BaseModel):
    score: int
    volatility: float
    sigma: float
    scam: Optional[ScamCheckOut] = None
    recommendation: str
