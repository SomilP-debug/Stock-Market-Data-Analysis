# Inside simulations/backtester.py
import numpy as np
import pandas as pd

def run_sma_crossover_strategy(df, short_window, long_window):
    """
    Simulates a Moving Average Crossover strategy.
    Returns the dataframe with signals and the total strategy return.
    """
    # Create a copy to avoid altering the original data
    data = df.copy()
    
    # 1. Calculate the Moving Averages
    data['SMA_Short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    
    # 2. Generate Signals (1 = Hold the stock, 0 = Sit in cash)
    # We use np.where to say: If Short > Long, give me a 1. Else, give me a 0.
    data['Signal'] = np.where(data['SMA_Short'] > data['SMA_Long'], 1, 0)
    
    # 3. Identify the exact Buy/Sell execution days
    # .diff() compares today's signal to yesterday's signal
    # 1 - 0 = 1 (Buy). 0 - 1 = -1 (Sell).
    data['Position'] = data['Signal'].diff()
    
    # 4. Calculate Returns
    # We shift the signal by 1 because if we get a buy signal today, 
    # we don't realize the return until tomorrow.
    data['Strategy_Return'] = data['Log_Return'] * data['Signal'].shift(1)
    
    # Calculate cumulative returns (Buy & Hold vs Strategy)
    data['Cumulative_Market_Return'] = np.exp(data['Log_Return'].cumsum())
    data['Cumulative_Strategy_Return'] = np.exp(data['Strategy_Return'].cumsum())
    
    return data