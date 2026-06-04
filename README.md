# 📈 Stock Market Data Analysis

An enterprise-grade, interactive quantitative finance and algorithmic backtesting platform. Built with Python and Streamlit, this application integrates real-time historical market data streams to evaluate capital asset pricing, model option derivatives, run predictive stochastic simulations, and backtest technical trading strategies.

## 🚀 Live Deployment
🔗 **https://somilp-debug-stock-market-data-analysis-app-1qrfuh.streamlit.app/**

---

## 🛠️ Features & Architecture

This application utilizes a clean, modular architecture separating data fetching pipelines, complex mathematical models, stochastic simulations, and the interactive UI layer:

### 1. Quantitative Risk & Pricing Models
* **Capital Asset Pricing Model (CAPM):** Dynamically calculates a stock's historical Beta relative to the broader market index to compute the forward-looking expected rate of return.
* **Black-Scholes-Merton Engine:** Computes theoretical European Call and Put option prices, alongside real-time calculations of options Greeks.
* **Binomial Options Pricing Tree:** Provides an alternative discrete-time model for option valuation.

### 2. Predictive Stochastic Simulations
* **Monte Carlo Geometric Brownian Motion (GBM):** Runs thousands of parallel, randomized price-path simulations utilizing drift and historical volatility to project asset distribution bounds over customized time horizons.
* **Value at Risk (VaR):** Calculates expected portfolio drawdowns based on stochastic risk metrics.

### 3. Algorithmic Backtesting Engine
* **SMA Crossover Strategy:** A vectorized technical analysis backtester tracking fast vs. slow simple moving averages. 
* **Performance Evaluation:** Charts historical buy/sell execution flags and evaluates total cumulative strategy returns against a passive benchmark Buy & Hold baseline.

---

## 📂 Project Directory Structure

    Quant_Finance_Engine/
    │
    ├── data/
    │   ├── __init__.py
    │   └── fetcher.py            # Cached yfinance data pipelines
    │
    ├── models/
    │   ├── __init__.py
    │   ├── capm.py               # CAPM logic & Beta calculation
    │   ├── black_scholes.py      # BSM pricing formula
    │   └── binomial_tree.py      # Discrete binomial tree math
    │
    ├── simulations/
    │   ├── __init__.py
    │   ├── monte_carlo.py        # GBM simulation engine
    │   ├── risk_metrics.py       # VaR and distribution metrics
    │   └── backtester.py         # Vectorized SMA strategy backtest
    │
    ├── app.py                    # Streamlit UI execution layer
    ├── .gitignore                # Production environment rules
    └── requirements.txt          # Package dependencies

---

## ⚙️ Local Installation & Setup

1. **Clone the repository:**

    git clone [https://github.com/YOUR_USERNAME/Stock-Market-Data-Analysis.git](https://github.com/YOUR_USERNAME/Stock-Market-Data-Analysis.git)
    cd Stock-Market-Data-Analysis

2. **Create and activate a virtual environment:**

    python -m venv venv
    venv\Scripts\activate

3. **Install dependencies:**

    pip install -r requirements.txt

4. **Run the application locally:**

    streamlit run app.py

---

## 🧮 Core Technologies
* **Frontend Application:** Streamlit 
* **Data Integration:** Yahoo Finance API (yfinance)
* **Quantitative Computation:** NumPy, Pandas, SciPy
* **Data Visualization:** Matplotlib

---
