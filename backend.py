import pandas as pd
import numpy as np
import requests
import random
from datetime import datetime

# ---------------------------
# User Data + Tokens
# ---------------------------
USERS = {}   # username -> portfolio list
TOKENS = {}  # username -> remaining tokens
DEFAULT_TOKENS = 10

# ---------------------------
# Market Data
# ---------------------------
def fetch_crypto_price(asset):
    crypto_ids = {"Bitcoin": "bitcoin", "Ethereum": "ethereum", "Cardano": "cardano"}
    if asset not in crypto_ids:
        return random.randint(100, 50000)
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_ids[asset]}&vs_currencies=usd"
        data = requests.get(url, timeout=5).json()
        return data[crypto_ids[asset]]["usd"]
    except:
        return random.randint(1000, 50000)

def fetch_stock_price(asset):
    stock_prices = {"Stock A": 150, "Stock B": 250, "Stock C": 75}
    return stock_prices.get(asset, random.randint(10, 500))

def get_market_price(asset, asset_type):
    if asset_type == "Crypto":
        return fetch_crypto_price(asset)
    elif asset_type == "Stock":
        return fetch_stock_price(asset)
    else:
        return random.randint(50, 200)

# ---------------------------
# Risk & Recommendations
# ---------------------------
def calculate_risk(asset):
    base_risk = {"Stock": 5, "Crypto": 7, "Bond": 3}
    volatility = random.uniform(0,3)
    risk = base_risk.get(asset["Type"], 5) + volatility
    return min(max(int(risk), 1), 10)

def generate_recommendation(asset, risk):
    if risk >= 8:
        return "⚠️ High Risk: Reduce Exposure"
    elif risk >= 5:
        return "⚠️ Medium Risk: Hold"
    else:
        return "✅ Low Risk: Consider Increasing"

def calculate_diversification_score(portfolio):
    types = [a["Type"] for a in portfolio]
    if not types: return 0
    type_counts = pd.Series(types).value_counts()
    diversification = len(type_counts)/3 * 10
    return min(int(diversification), 10)

# ---------------------------
# Portfolio Management
# ---------------------------
def create_user(username):
    if username not in USERS:
        USERS[username] = []
        TOKENS[username] = DEFAULT_TOKENS
        return True
    return False

def get_tokens(username):
    return TOKENS.get(username, 0)

def use_token(username):
    if TOKENS.get(username,0) > 0:
        TOKENS[username] -= 1
        return True
    return False

def add_asset(username, asset_name, amount, asset_type):
    portfolio = USERS.get(username, [])
    portfolio.append({"Asset": asset_name, "Amount": amount, "Type": asset_type})
    USERS[username] = portfolio

def get_portfolio(username):
    return USERS.get(username, [])

def get_portfolio_summary(portfolio):
    df = pd.DataFrame(portfolio)
    if df.empty: return df

    df["MarketPrice"] = df.apply(lambda row: get_market_price(row["Asset"], row["Type"]), axis=1)
    df["CurrentValue"] = df["Amount"] * df["MarketPrice"]
    df["Risk"] = df.apply(calculate_risk, axis=1)
    df["Recommendation"] = df.apply(lambda row: generate_recommendation(row, row["Risk"]), axis=1)
    df["LastUpdated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Portfolio-level metrics
    diversification = calculate_diversification_score(portfolio)
    df.attrs["DiversificationScore"] = diversification
    df.attrs["MVP"] = {
        "TotalValue": df["CurrentValue"].sum(),
        "AverageRisk": round(df["Risk"].mean(),1),
        "HighRiskCount": len(df[df["Risk"]>=8])
    }
    return df

# ---------------------------
# AI Chatbot
# ---------------------------
def chatbot_response(user_input, portfolio):
    df = get_portfolio_summary(portfolio)
    user_input = user_input.lower()

    if "risk" in user_input:
        high_risk_assets = df[df["Risk"]>=8]["Asset"].tolist()
        return f"High-risk assets: {', '.join(high_risk_assets)}" if high_risk_assets else "No high-risk assets."
    elif "summary" in user_input:
        return df[["Asset","Amount","MarketPrice","Risk","Recommendation"]].to_string(index=False)
    elif "recommend" in user_input or "advice" in user_input:
        return df[["Asset","Recommendation"]].to_string(index=False)
    elif "price" in user_input or "value" in user_input:
        return df[["Asset","MarketPrice","CurrentValue"]].to_string(index=False)
    elif "best" in user_input:
        low_risk_assets = df[df["Risk"]<=4]["Asset"].tolist()
        if low_risk_assets:
            return f"Lower-risk assets to consider increasing: {', '.join(low_risk_assets)}"
        return "All assets have medium/high risk. Consider diversification."
    else:
        return "I can provide portfolio summary, risk report, recommendations, or current market values."

# ---------------------------
# Demo for Presentation
# ---------------------------
def example_demo():
    username = "finance_demo"
    create_user(username)
    add_asset(username, "Bitcoin", 0.5, "Crypto")
    add_asset(username, "Ethereum", 2, "Crypto")
    add_asset(username, "Stock A", 5000, "Stock")
    add_asset(username, "Bond B", 10000, "Bond")
    
    print(f"Tokens Remaining: {get_tokens(username)}")
    
    portfolio = get_portfolio(username)
    summary = get_portfolio_summary(portfolio)
    print("Portfolio Summary:")
    print(summary)
    
    print("\nMVP Metrics:")
    print(summary.attrs["MVP"])
    
    questions = ["Show summary", "What is the risk?", "Give me recommendations", "Current prices", "Best action"]
    for q in questions:
        if use_token(username):
            print(f"\nQuestion: {q} (Token used)")
            print(chatbot_response(q, portfolio))
        else:
            print("No tokens left to ask questions.")

if __name__ == "__main__":
    example_demo()
