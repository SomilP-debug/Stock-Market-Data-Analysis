import yfinance as yf
import numpy as np
import pandas as pd

def calculate_capm(stock_returns, risk_free_rate, expected_market_return, market_ticker="^GSPC", period="5y"):
    """Calculates Beta and the CAPM expected return."""
    # Fetch Market Data
    market_data = yf.Ticker(market_ticker).history(period=period)
    market_data['Market_Return'] = np.log(market_data['Close'] / market_data['Close'].shift(1))
    market_data.dropna(inplace=True)
    
    # Align Data
    aligned_data = pd.concat([stock_returns, market_data['Market_Return']], axis=1).dropna()
    aligned_data.columns = ['Stock_Return', 'Market_Return']
    
    # Calculate Beta
    covariance = aligned_data.cov().iloc[0, 1]
    market_variance = aligned_data['Market_Return'].var()
    beta = covariance / market_variance
    
    # Calculate CAPM Expected Return
    expected_return = risk_free_rate + beta * (expected_market_return - risk_free_rate)
    
    return beta, expected_return