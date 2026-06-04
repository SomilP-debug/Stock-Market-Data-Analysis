import numpy as np

def run_gbm_simulation(S0, mu, sigma, time_horizon, num_simulations, trading_days=252):
    """Runs a Monte Carlo simulation using Geometric Brownian Motion."""
    delta_t = 1 / trading_days
    
    # Generate random shocks
    Z = np.random.standard_normal((time_horizon, num_simulations))
    
    # Calculate daily returns matrix
    daily_returns = np.exp((mu - 0.5 * sigma**2) * delta_t + sigma * np.sqrt(delta_t) * Z)
    
    # Build price paths
    price_paths = np.zeros((time_horizon + 1, num_simulations))
    price_paths[0] = S0
    
    for t in range(1, time_horizon + 1):
        price_paths[t] = price_paths[t-1] * daily_returns[t-1]
        
    final_prices = price_paths[-1]
    
    return price_paths, final_prices