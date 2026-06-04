import numpy as np

def calculate_risk_metrics(final_prices, S0, percentile=5):
    """Calculates VaR, CVaR, and Expected Price."""
    expected_price = np.mean(final_prices)
    var = np.percentile(final_prices, percentile)
    cvar = final_prices[final_prices <= var].mean()
    
    var_loss_pct = (S0 - var) / S0
    
    return expected_price, var, cvar, var_loss_pct