import pandas as pd
import numpy as np


class TradeTriggers:
    def __init__(self, processed_signals_dict):
        """
        Initialize with processed signals for multiple tickers.
        """
        self.processed_signals_dict = processed_signals_dict

    def evaluate_triggers(self):
        """
        Evaluate triggers for each ticker.
        Returns a dictionary with tickers as keys and lists of trade actions as values.
        """
        trades_dict = {}
        for ticker, signals in self.processed_signals_dict.items():
            trades = signals[signals['positions'] != 0]
            trades_dict[ticker] = trades
        return trades_dict
