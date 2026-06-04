import yfinance as yf
import numpy as np
import pandas as pd

def get_historical_data(ticker, period="5y"):
    """Fetches historical stock data and calculates log returns."""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}")
        
    df = data[['Close']].copy()
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    df.dropna(inplace=True)
    return df