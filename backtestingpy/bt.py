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
import time
import concurrent.futures

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


tickers = sp500 = ["A", "AAL", "AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN", "ANET", "ANSS", "AON", "AOS", "APA", "APD", "APH", "APTV", "ARE", "ASML", "ATO", "AVB", "AVGO", "AVY", "AWK", "AXON", "AXP", "AZN", "AZO", "BA", "BAC", "BALL", "BAX", "BBWI", "BBY", "BDX", "BEN", "BG", "BIIB", "BIO", "BK", "BKNG", "BKR", "BLDR", "BLK", "BMY", "BR", "BRO", "BSX", "BWA", "BX", "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCEP", "CCI", "CCL", "CDNS", "CDW", "CE", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COO", "COP", "COR", "COST", "CPB", "CPRT", "CPT", "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX", "CTAS", "CTLT", "CTRA", "CTSH", "CTVA", "CVS", "CVX", "CZR", "D", "DAL", "DASH", "DAY", "DD", "DDOG", "DE", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOC", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA", "DVN", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EG", "EIX", "EL", "ELV", "EMN", "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ES", "ESS", "ETN", "ETR", "ETSY", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FCX", "FDS", "FDX", "FE", "FFIV", "FI", "FICO", "FIS", "FITB", "FLT", "FMC", "FOX", "FOXA", "FRT", "FSLR", "FTNT", "FTV", "GD", "GE", "GEHC", "GEN", "GFS", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC", "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", "HES", "HIG", "HII", "HLT", "HOLX", "HON", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUM", "HWM", "IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN", "INCY", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JBL", "JCI", "JKHY", "JNJ", "JNPR", "JPM", "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KLAC", "KMB", "KMI", "KMX", "KO", "KR", "KVUE", "L", "LDOS", "LEN", "LH", "LHX", "LIN", "LKQ", "LLY", "LMT", "LNT", "LOW", "LRCX", "LULU", "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDB", "MDLZ", "MDT", "MELI", "MET", "META", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR", "MRK", "MRNA", "MRO", "MRVL", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX", "NI", "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWS", "NWSA", "NXPI", "O", "ODFL", "OKE", "OMC", "ON", "ORCL", "ORLY", "OTIS", "OXY", "PANW", "PARA", "PAYC", "PAYX", "PCAR", "PCG", "PDD", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PM", "PNC", "PNR", "PNW", "PODD", "POOL", "PPG", "PPL", "PRU", "PSA", "PSX", "PTC", "PWR", "PXD", "PYPL", "QCOM", "QQQ", "QRVO", "RCL", "REG", "REGN", "RF", "RHI", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "RVTY", "SBAC", "SBUX", "SCHW", "SHW", "SIRI", "SJM", "SLB", "SNA", "SNPS", "SO", "SPG", "SPGI", "SPLK", "SPY", "SRE", "STE", "STLD", "STT", "STX", "STZ", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TEAM", "TECH", "TEL", "TER", "TFC", "TFX", "TGT", "TJX", "TMO", "TMUS", "TPR", "TRGP", "TRMB", "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTD", "TTWO", "TXN", "TXT", "TYL", "UAL", "UBER", "UDR", "UHS", "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V", "VFC", "VICI", "VLO", "VLTO", "VMC", "VRSK", "VRSN", "VRTX", "VTR", "VTRS", "VZ", "WAB", "WAT", "WBA", "WBD", "WDAY", "WDC", "WEC", "WELL", "WFC", "WHR", "WM", "WMB", "WMT", "WRB", "WRK", "WST", "WTW", "WY", "WYNN", "XEL", "XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY", "XOM", "XRAY", "XYL", "YUM", "ZBH", "ZBRA", "ZION", "ZS", "ZTS"]
idx = 0

highest_return = None
highest_return_ticker = None

# for ticker in tickers:
#     start_time = time.time()

#     csv_data = ''
#     with open('data/combined.csv', 'r') as file:
#         csv_data = file.read()

#     data = pd.read_csv(StringIO(csv_data))
#     data = data[data['Code'] == ticker]
#     data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
#     data = data.set_index('Date')
#     data.index = pd.to_datetime(data.index)
#     data = data.sort_index(ascending=True)

#     bt = Backtest(data, MovingAverageStrategy, commission=.002, exclusive_orders=True)
#     stats = bt.run()
#     stats.to_csv(f'data/stats/{ticker}.csv', index=True)
#     stats.head()
#     # get value "Return [%]" from stats
#     return_value = stats['Return [%]']

#     if highest_return is None or return_value > highest_return:
#         highest_return = return_value
#         highest_return_ticker = ticker
#         print(f"New highest return: {highest_return} for {highest_return_ticker}")

#     # print(f"Return for {ticker}: {return_value}")

#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"[{idx}/{len(sp500)}] Backtest for {ticker} completed in {execution_time} seconds.")
#     idx += 1

# print(f"Highest return: {highest_return} for {highest_return_ticker}")


def task(ticker, data):
    global highest_return
    global highest_return_ticker

    start_time = time.time()
    
    data = data[data['Code'] == ticker]
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    data = data.set_index('Date')
    data.index = pd.to_datetime(data.index)
    data = data.sort_index(ascending=True)

    bt = Backtest(data, MovingAverageStrategy, commission=.002, exclusive_orders=True)
    stats = bt.run()
    # stats.to_csv(f'data/stats/{ticker}.csv', index=True)
    # stats.head()
    # get value "Return [%]" from stats
    return_value = stats['Return [%]']

    if highest_return is None or return_value > highest_return:
        highest_return = return_value
        highest_return_ticker = ticker
        print(f"New highest return: {highest_return} for {highest_return_ticker}")

    # print(f"Return for {ticker}: {return_value}")
    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"[{idx}/{len(sp500)}] Backtest for {ticker} completed in {execution_time} seconds.")

csv_data = ''
with open('data/combined.csv', 'r') as file:
    csv_data = file.read()

data = pd.read_csv(StringIO(csv_data))

idx = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:

    futures = [executor.submit(task, ticker, data) for ticker in sp500]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        idx += 1
        print(f"[{idx}/{len(sp500)}] Completed")

