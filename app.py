
from tickerdata.ticker_data import TickerData
from tickerdata.csv_data_provider import CsvDataProvider

import pandas as pd;
from datetime import datetime
from dotenv import load_dotenv

    
def find_dataset_definition(name):
    ds = json.loads(open("data/datasets.json").read())
    for d in ds:
        if d["name"] == name:
            return d
    return None


def get_dataset_data(name):
    ds = find_dataset_definition(name)
    if ds is None:
        return None
    if ds["type"] == "eod":
        API_KEY = os.getenv("EOD_API_KEY")
        client = EodHistoricalData(API_KEY)

        if not os.path.exists(f"data/{ds['name']}"):
            os.makedirs(f"data/{ds['name']}")

        for ticker in ds["symbols"]:
            data = client.get_prices_eod(ticker, period=ds["period"], from_=ds["start_date"])
            print(data)
            with open(f"data/{ds['name']}/{ticker}.csv", "w") as f:
                f.write("date,open,high,low,close,volume\n")
                for row in data:
                    f.write(f"{row['date']},{row['open']},{row['high']},{row['low']},{row['close']},{row['volume']}\n")



class App:
    def __init__(self):
        self.ticker_data = TickerData(CsvDataProvider('AAPL', './datafiles', stream_start_time=datetime(2020, 1, 1)))
        self.df = None

    def handle_live_data(self, data):
        # Append incomming pandas Series object, using data.name to preserve the date index
        self.df.loc[data.name] = data
        
        # calculate SMA-50 for incomming events
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
