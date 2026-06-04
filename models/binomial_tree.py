import numpy as np

def calculate_binomial_tree(S, K, T, r, sigma, N=100, option_type='call', is_american=True):
    """Prices options using a discrete Binomial Tree."""
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    
    asset_prices = np.zeros(N + 1)
    for i in range(N + 1):
        asset_prices[i] = S * (u ** (N - i)) * (d ** i)
        
    option_values = np.zeros(N + 1)
    for i in range(N + 1):
        if option_type == 'call':
            option_values[i] = max(0, asset_prices[i] - K)
        else:
            option_values[i] = max(0, K - asset_prices[i])
            
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            hold_value = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])
            if is_american:
                node_price = S * (u ** (j - i)) * (d ** i)
                exercise_value = max(0, node_price - K) if option_type == 'call' else max(0, K - node_price)
                option_values[i] = max(hold_value, exercise_value)
            else:
                option_values[i] = hold_value
                
    return option_values[0]