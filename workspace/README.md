# AI Assistant - Financial Risk Layer (Prototype)

This small FastAPI backend provides three main features:

- Money Meter: computes a volatility-based risk score from historical prices
- Scam Detective: basic contract verification and heuristic checks (uses Etherscan API if API key provided)
- Personalized Safety Score: combines volatility and scam checks with user risk preference

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Etherscan: For contract checks, set `etherscan_api_key` in the POST body. If not provided, the detector will only report that source is not verified.

Endpoints:
- POST /money_meter {"prices": [..]}
- POST /scam_check {"address": "0x...", "etherscan_api_key": "KEY"}
- POST /personalized_score {"prices": [..], "risk_preference": "conservative|neutral|aggressive", "contract_address": "0x...", "etherscan_api_key": "KEY"}

Notes: This is a prototype. The scam checker uses simple heuristics and is not a substitute for a security audit.
