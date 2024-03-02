import pandas as pd
import numpy as np

class SignalGenerator:
    def __init__(self, data):
        """
        Initialize with a dictionary of historical data for multiple tickers.
        data should be a dict with tickers as keys and DataFrame as values.
        """
        self.data = data

    def generate_signals(self):
        """
        Generate buy/sell signals for each ticker.
        Returns a dictionary with tickers as keys and DataFrames of signals as values.
        """
        signals_dict = {}
        for ticker, df in self.data.items():
            signals = pd.DataFrame(index=df.index)
            short_window = 40
            long_window = 100
            signals['signal'] = 0.0
            signals['short_mavg'] = df['close'].rolling(window=short_window, min_periods=1, center=False).mean()
            signals['long_mavg'] = df['close'].rolling(window=long_window, min_periods=1, center=False).mean()
            signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
            signals['positions'] = signals['signal'].diff()
            signals_dict[ticker] = signals
        return signals_dict
