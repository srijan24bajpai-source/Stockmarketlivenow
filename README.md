# AlgoTrader
Dependency-free Python stock app with algo trading: SMA-crossover and RSI strategies, backtester, paper broker, web dashboard.

    python -m algotrader.server   # http://localhost:8000
    python -m unittest discover tests

Data is simulated; this is not financial advice. For live trading, replace `data.py` with a real feed and `broker.py` with a broker API.
