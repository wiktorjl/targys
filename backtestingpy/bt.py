from io import StringIO
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import datetime
from backtesting.test import SMA, GOOG
import csv


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()



class MovingAverageStrategy(Strategy):
    n1 = 10
    n2 = 30

    def init(self):
        self.ma1 = self.I(SMA, self.data.Close, self.n1)
        self.ma2 = self.I(SMA, self.data.Close, self.n2)
    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif self.data.Close[-1] < self.data.Close[-2] * 0.95:
            self.sell()

class BollingerBandsStrategy(Strategy):
    n = 20
    k = 2

    def init(self):
        close_series = pd.Series(self.data.Close)
        self.ma = self.I(close_series.rolling(self.n).mean)
        self.std = self.I(close_series.rolling(self.n).std)
        self.upper = self.I(lambda: self.ma + self.k * self.std)
        self.lower = self.I(lambda: self.ma - self.k * self.std)

    def next(self):
        if self.data.Close[-1] > self.upper[-1]:
            self.buy()
        elif self.data.Close[-1] < self.data.Close[-2] and self.data.Close[-2] < self.data.Close[-3]:
            self.sell()


csv_data = ''
with open('data/combined.csv', 'r') as file:
    csv_data = file.read()

data = pd.read_csv(StringIO(csv_data))
data = data[data['Code'] == 'AMZN']
data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
data = data.set_index('Date')
data.index = pd.to_datetime(data.index)
data = data.sort_index(ascending=True)

print(data.head())

bt = Backtest(data, MovingAverageStrategy, commission=.002,
               exclusive_orders=True)
stats = bt.run()

print(stats)
            



