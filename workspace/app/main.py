from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.utils.volatility import compute_volatility_score
from app.utils.scam_detector import analyze_contract
from app.models import PricesIn, MoneyMeterOut, RiskProfileIn, PersonalizedScoreOut, ContractIn, ScamCheckOut

app = FastAPI(title="AI Assistant - Financial Risk Layer")


@app.post("/money_meter", response_model=MoneyMeterOut)
def money_meter(data: PricesIn):
    if len(data.prices) < 2:
        raise HTTPException(status_code=400, detail="Need at least two price points")
    score, sigma = compute_volatility_score(data.prices)
    return MoneyMeterOut(score=score, volatility=sigma, n=len(data.prices))


@app.post("/scam_check", response_model=ScamCheckOut)
def scam_check(data: ContractIn):
    result = analyze_contract(data.address, etherscan_api_key=data.etherscan_api_key)
    return result


@app.post("/personalized_score", response_model=PersonalizedScoreOut)
def personalized_score(data: RiskProfileIn):
    if len(data.prices) < 2:
        raise HTTPException(status_code=400, detail="Need at least two price points")
    vol_score, sigma = compute_volatility_score(data.prices)
    scam = analyze_contract(data.contract_address, etherscan_api_key=data.etherscan_api_key) if data.contract_address else None

    # base weights depending on user preference
    pref = data.risk_preference.lower()
    if pref == "conservative":
        w_vol, w_scam = 0.7, 0.3
    elif pref == "aggressive":
        w_vol, w_scam = 0.4, 0.6
    else:  # neutral
        w_vol, w_scam = 0.55, 0.45

    scam_penalty = 0
    scam_notes = None
    if scam:
        scam_notes = scam.issues
        if scam.risky:
            scam_penalty = 40

    # final score is 0-100 where higher means riskier. We'll combine vol_score and scam_penalty
    final_score = min(100, round(w_vol * vol_score + w_scam * scam_penalty))

    if pref == "conservative":
        if final_score > 50:
            recommendation = "Avoid — too risky for a conservative profile"
        else:
            recommendation = "Acceptable for conservative investors"
    elif pref == "aggressive":
        if final_score > 80:
            recommendation = "High risk — suitable for aggressive investors with caution"
        else:
            recommendation = "Within acceptable risk for aggressive investors"
    else:
        recommendation = "Matches neutral risk profile"

    return PersonalizedScoreOut(score=final_score, volatility=vol_score, sigma=sigma, scam=scam, recommendation=recommendation)
