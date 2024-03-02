
from datetime import datetime

import os
import json
from eod import EodHistoricalData
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



if __name__ == "__main__":        
    load_dotenv()
    get_dataset_data("dataset1")