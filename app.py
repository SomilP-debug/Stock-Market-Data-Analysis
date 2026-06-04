import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
# Import our custom modules
from data.fetcher import get_historical_data
from models.capm import calculate_capm
from models.black_scholes import calculate_black_scholes
from models.binomial_tree import calculate_binomial_tree
from simulations.monte_carlo import run_gbm_simulation
from simulations.risk_metrics import calculate_risk_metrics
from simulations.backtester import run_sma_crossover_strategy

# ==========================================
# UI SETUP & SIDEBAR CONTROLS
# ==========================================
st.set_page_config(page_title="Quant Risk Engine", layout="wide")
st.title("📈 Algorithmic Risk & Pricing Engine")

st.sidebar.header("Engine Parameters")
ticker = st.sidebar.text_input("Stock Ticker", "GOOGL").upper()
time_horizon = st.sidebar.slider("Forecast Horizon (Days)", 30, 252, 252)
num_simulations = st.sidebar.slider("Monte Carlo Paths", 100, 5000, 1000)

st.sidebar.header("Market & Option Inputs")
st.sidebar.header("Algorithmic Trading Rules")
short_window = st.sidebar.slider("Fast Moving Average (Days)", 5, 50, 20)
long_window = st.sidebar.slider("Slow Moving Average (Days)", 50, 200, 50)
strike_offset = st.sidebar.slider("Strike Price Offset (%)", -20, 20, 10) / 100
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", 0.0, 10.0, 4.0) / 100
expected_market_return = st.sidebar.number_input("Expected Market Return (%)", 0.0, 20.0, 10.0) / 100

# ==========================================
# ENGINE EXECUTION
# ==========================================
try:
    with st.spinner(f"Running Quantitative Engine for {ticker}..."):
        
        # 1. Fetch Data
        df = get_historical_data(ticker)
        S0 = df['Close'].iloc[-1]
        
        trading_days = 252
        mu = df['Log_Return'].mean() * trading_days
        sigma = df['Log_Return'].std() * np.sqrt(trading_days)
        
        st.write(f"### Historical Data Metrics for **{ticker}**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${S0:.2f}")
        col2.metric("Annual Drift (μ)", f"{mu:.2%}")
        col3.metric("Annual Volatility (σ)", f"{sigma:.2%}")

        # 2. CAPM
        st.write("---")
        st.write("### Capital Asset Pricing Model (CAPM)")
        beta, capm_expected_return = calculate_capm(df['Log_Return'], risk_free_rate, expected_market_return)
        
        ccol1, ccol2, ccol3 = st.columns(3)
        ccol1.metric("Asset Beta (β)", f"{beta:.3f}")
        ccol2.metric("Risk-Free Rate", f"{risk_free_rate:.2%}")
        ccol3.metric("CAPM Expected Return", f"{capm_expected_return:.2%}")

        # 3. Monte Carlo & Risk
        st.write("---")
        st.write(f"### Monte Carlo Simulation ({num_simulations} Paths over {time_horizon} Days)")
        price_paths, final_prices = run_gbm_simulation(S0, mu, sigma, time_horizon, num_simulations)
        
        fig_mc, ax_mc = plt.subplots(figsize=(10, 4))
        ax_mc.plot(price_paths[:, :200], color='blue', alpha=0.1, lw=1) 
        ax_mc.plot(price_paths.mean(axis=1), color='red', lw=2, label='Expected Path')
        ax_mc.set_title(f'Geometric Brownian Motion Forecast for {ticker}')
        ax_mc.set_ylabel('Price ($)')
        ax_mc.set_xlabel('Days')
        ax_mc.legend()
        st.pyplot(fig_mc)

        expected_price, var_95, cvar_95, var_loss_pct = calculate_risk_metrics(final_prices, S0)
        st.write("### Risk Management Metrics (95% Confidence)")
        rcol1, rcol2, rcol3 = st.columns(3)
        rcol1.metric("Expected Price", f"${expected_price:.2f}")
        rcol2.metric("Value at Risk (VaR)", f"${var_95:.2f}", f"Max loss: {var_loss_pct:.2%}", delta_color="inverse")
        rcol3.metric("Expected Shortfall (CVaR)", f"${cvar_95:.2f}", delta_color="inverse")

        # 4. Option Pricing
        st.write("---")
        st.write("### Advanced Option Pricing Models")
        
        strike_price = S0 * (1 + strike_offset)
        T = time_horizon / 252 
        
        bs_call, bs_put = calculate_black_scholes(S0, strike_price, T, risk_free_rate, sigma)
        bin_call_eur = calculate_binomial_tree(S0, strike_price, T, risk_free_rate, sigma, N=100, option_type='call', is_american=False)
        bin_call_am = calculate_binomial_tree(S0, strike_price, T, risk_free_rate, sigma, N=100, option_type='call', is_american=True)
        
        st.markdown(f"**Target Strike Price (K):** ${strike_price:.2f} | **Time to Expiration (T):** {T:.2f} Years")
        
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            st.success("#### Black-Scholes Model (Continuous)")
            st.metric("European Call", f"${bs_call:.2f}")
            st.metric("European Put", f"${bs_put:.2f}")
        with pcol2:
            st.info("#### Binomial Tree Model (Discrete)")
            st.metric("European Call", f"${bin_call_eur:.2f}")
            st.metric("American Call", f"${bin_call_am:.2f}")
            
            
# ==========================================
        # 5. ALGORITHMIC BACKTESTING
        # ==========================================
        st.write("---")
        st.write("### Algorithmic Backtesting: SMA Crossover Strategy")
        
        # Run the engine
        bt_data = run_sma_crossover_strategy(df, short_window, long_window)
        
        # Extract final returns
        buy_and_hold_return = bt_data['Cumulative_Market_Return'].iloc[-1] - 1
        strategy_return = bt_data['Cumulative_Strategy_Return'].iloc[-1] - 1
        
        tcol1, tcol2 = st.columns(2)
        tcol1.metric("Buy & Hold Return (5y)", f"{buy_and_hold_return:.2%}")
        # Color the strategy return green if it beat the market, red if it lost
        delta_val = strategy_return - buy_and_hold_return
        tcol2.metric("Strategy Return (5y)", f"{strategy_return:.2%}", f"{delta_val:.2%} vs Market")

        # Plot the Strategy
        fig_bt, ax_bt = plt.subplots(figsize=(12, 5))
        ax_bt.plot(bt_data.index, bt_data['Close'], label='Stock Price', alpha=0.5, lw=1)
        ax_bt.plot(bt_data.index, bt_data['SMA_Short'], label=f'{short_window}-Day SMA', color='orange', lw=1.5)
        ax_bt.plot(bt_data.index, bt_data['SMA_Long'], label=f'{long_window}-Day SMA', color='purple', lw=1.5)
        
        # Plot Buy Signals (Green Up Arrows)
        buy_signals = bt_data[bt_data['Position'] == 1]
        ax_bt.scatter(buy_signals.index, buy_signals['SMA_Short'], marker='^', color='green', s=100, label='Buy Signal', zorder=5)
        
        # Plot Sell Signals (Red Down Arrows)
        sell_signals = bt_data[bt_data['Position'] == -1]
        ax_bt.scatter(sell_signals.index, sell_signals['SMA_Short'], marker='v', color='red', s=100, label='Sell Signal', zorder=5)
        
        ax_bt.set_title(f'Moving Average Crossover Backtest for {ticker}')
        ax_bt.set_ylabel('Price')
        ax_bt.legend(loc='upper left')
        st.pyplot(fig_bt)

except Exception as e:
    st.error(f"Error processing data for ticker '{ticker}'. {str(e)}")