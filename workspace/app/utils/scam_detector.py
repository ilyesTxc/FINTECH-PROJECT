import re
from typing import Optional, List
import requests


ETHERSCAN_TXT_URL = "https://api.etherscan.io/api"


def fetch_contract_source(address: str, api_key: Optional[str] = None) -> Optional[str]:
    if not api_key:
        return None
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key,
    }
    try:
        resp = requests.get(ETHERSCAN_TXT_URL, params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "1" and data.get("result"):
            # result is a list with sourceCode key
            res = data["result"][0]
            return res.get("SourceCode") or res.get("ABI")
    except Exception:
        return None
    return None


def analyze_contract(address: str, etherscan_api_key: Optional[str] = None):
    issues: List[str] = []
    source = fetch_contract_source(address, etherscan_api_key)
    verified = bool(source)
    risky = False

    if not verified:
        issues.append("Contract source not publicly verified")
        risky = True
    else:
        s = source if isinstance(source, str) else str(source)
        # Simple heuristics
        if re.search(r'resolve|owner|onlyOwner|transferFrom\(|balanceOf\(|selfdestruct|delegatecall', s, re.IGNORECASE):
            issues.append("Contains functions or patterns often used in risky contracts (owner controls, delegatecall, selfdestruct, transferFrom)")
            risky = True
        if re.search(r'function\s+approve\s*\(', s):
            issues.append("Has approve function — check for unlimited approvals or unsafe patterns")

        # suspicious large constructor logic
        if len(s) > 20000:
            issues.append("Large contract source — manual audit recommended")

    return {
        "address": address,
        "verified": verified,
        "risky": risky,
        "issues": issues or None,
    }
