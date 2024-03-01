
from datetime import datetime

import os
import json
from eod import EodHistoricalData
from dotenv import load_dotenv


if __name__ == "__main__":        
    load_dotenv()
    API_KEY = os.getenv("EOD_API_KEY")
    client = EodHistoricalData(API_KEY)
    data = client.get_prices_eod("AMZN")
    print(data)