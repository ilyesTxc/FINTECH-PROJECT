import numpy as np

def calculate_combined_risk(assets):
    """Calculate combined financial and security risk"""
    
    financial_scores = {
        'BTC': 8.5, 'ETH': 7.5, 
        'AAPL': 4.0, 'TSLA': 6.5, 
        'GOOGL': 3.5, 'MSFT': 3.0,
        'BOND': 1.5, 'GOLD': 2.0
    }
    
    security_scores = {
        'BTC': 6.0, 'ETH': 7.0, 
        'AAPL': 2.0, 'TSLA': 2.5, 
        'GOOGL': 2.0, 'MSFT': 2.0,
        'BOND': 1.0, 'GOLD': 1.5
    }
    
    fin_risks = [financial_scores.get(asset, 5.0) for asset in assets]
    sec_risks = [security_scores.get(asset, 5.0) for asset in assets]
    
    financial = np.mean(fin_risks) if fin_risks else 5.0
    security = np.mean(sec_risks) if sec_risks else 5.0
    
    combined = 0.6 * financial + 0.4 * security
    
    
    if combined <= 3:
        recommendation = " Low Risk - Good to proceed"
    elif combined <= 6:
        recommendation = "Medium Risk - Consider diversification"
    else:
        recommendation = "High Risk - Strong caution advised"
    
    return {
        'combined_score': round(combined, 2),
        'financial_risk': round(financial, 2),
        'security_risk': round(security, 2),
        'recommendation': recommendation
    }

# Test function
if __name__ == "__main__":
    test_result = calculate_combined_risk(['BTC', 'AAPL', 'BOND'])
    print(" AI Risk Engine Test:")
    for key, value in test_result.items():

        print(f"  {key}: {value}")
