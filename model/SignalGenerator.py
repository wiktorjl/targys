import pandas as pd
import numpy as np


def make_name_literal(namespace, analysis_name, analysis_type, attr_1 = None, attr_2 = None):
    return f"{namespace}___{analysis_name}_{analysis_type}___{attr_1}___{attr_2}"


def make_analysis_name_literal(analysis_name, analysis_type, attr_1 = None, attr_2 = None):
    return make_name_literal("ANALYSIS", analysis_name, analysis_type, attr_1, attr_2)


def make_signal_name_literal(analysis_name, analysis_type, attr_1 = None, attr_2 = None):
    return make_name_literal("SIGNAL", analysis_name, analysis_type, attr_1, attr_2)


def simple_moving_average(df, window):
    return df.rolling(window=window, min_periods=1, center=False).mean()


def series_over(series1, series2):
    return (series1 > series2).astype(float)


def series_under(series1, series2):
    return (series1 < series2).astype(float)


def cross_over(series1, series2):
    return ((series1 > series2) & (series1.shift(1) < series2.shift(1))).astype(float)


def cross_under(series1, series2):
    return ((series1 < series2) & (series1.shift(1) > series2.shift(1))).astype(float)


def moving_average_convergence_divergence(df, short_window, long_window, signal_window):
    short_ema = df['close'].ewm(span=short_window, min_periods=1, adjust=False).mean()
    long_ema = df['close'].ewm(span=long_window, min_periods=1, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, min_periods=1, adjust=False).mean()
    return macd, signal


def relative_strength_index(df, window):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()
    return 100 - (100 / (1 + (gain / loss)))


def stochastic_oscillator(df, window):
    low_min = df['low'].rolling(window=window, min_periods=1).min()
    high_max = df['high'].rolling(window=window, min_periods=1).max()
    return 100 * (df['close'] - low_min) / (high_max - low_min)


def bollinger_bands(df, window, num_std):
    rolling_mean = df['close'].rolling(window=window, min_periods=1).mean()
    rolling_std = df['close'].rolling(window=window, min_periods=1).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return rolling_mean, upper_band, lower_band


def average_true_range(df, window):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift(1)).abs()
    low_close = (df['low'] - df['close'].shift(1)).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.rolling(window=window, min_periods=1).mean()


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

            signals[make_signal_name_literal("movingaverage", "crossover", short_window, long_window)] = 0.0
            signals[make_analysis_name_literal("movingaverage", "simple", short_window)] = simple_moving_average(df['close'], short_window)
            signals[make_analysis_name_literal("movingaverage", "simple", long_window)] = simple_moving_average(df['close'], long_window)
            signals[make_signal_name_literal("movingaverage", "crossover", short_window, long_window)] = series_over(signals[make_analysis_name_literal("movingaverage", "simple", short_window)], signals[make_analysis_name_literal("movingaverage", "simple", long_window)])
            signals['positions'] = signals[make_signal_name_literal("movingaverage", "crossover", short_window, long_window)].diff()

            signals_dict[ticker] = signals


        return signals_dict
