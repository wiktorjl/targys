
from tickerdata.ticker_data import TickerData
from tickerdata.csv_data_provider import CsvDataProvider

import pandas as pd;
from datetime import datetime
from dotenv import load_dotenv


class App:
    def __init__(self):
        self.ticker_data = TickerData(CsvDataProvider('AAPL', './datafiles', stream_start_time=datetime(2020, 1, 1)))
        self.df = None

    def handle_live_data(self, data):
        # using data.name to preserve the date index
        self.df.loc[data.name] = data
        # calculate SMA-50
        print("SMA-50: ", self.df['Close'].rolling(window=50).mean().iloc[-1])
        
    def run(self):
        # historical data from / to 
        self.df = self.ticker_data.get_data(datetime(2019, 1, 1), datetime(2020, 1, 10))
        print(self.df.head(5))

        # process rest of the data (pretend stream)
        self.ticker_data.subscribe_to_live_data(self.handle_live_data)
    


def handle_live_data(data):
    print(data)


if __name__ == "__main__":        
    load_dotenv()
    App().run()