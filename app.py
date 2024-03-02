
from datetime import datetime

import os
import json
from eod import EodHistoricalData
from dotenv import load_dotenv

from model.SignalGenerator import SignalGenerator
from model.TradingModel import TradingModel 
from model.TradeTrigger import TradeTriggers
from model.TradeSelection import TradeSelection

    
import pandas as pd
import numpy as np


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

            # Check if we already have the data and if so, move on.
            if os.path.exists(f"data/{ds['name']}/{ticker}.csv"):
                continue

            data = client.get_prices_eod(ticker, period=ds["period"], from_=ds["start_date"])
            print(data)
            with open(f"data/{ds['name']}/{ticker}.csv", "w") as f:
                f.write("date,open,high,low,close,volume\n")
                for row in data:
                    f.write(f"{row['date']},{row['open']},{row['high']},{row['low']},{row['close']},{row['volume']}\n")


def load_symbol_for_dataset(name, symbol):
    return pd.read_csv(f"data/{name}/{symbol}.csv", index_col="date", parse_dates=True)


if __name__ == "__main__":        
    load_dotenv()
    
    get_dataset_data("dataset1")
    
    data_dict = {symbol: load_symbol_for_dataset("dataset1", symbol) for symbol in find_dataset_definition("dataset1")["symbols"]}


    signal_generator = SignalGenerator(data_dict)
    signals_dict = signal_generator.generate_signals()
    trading_model = TradingModel(signals_dict)
    processed_signals_dict = trading_model.process_signals()
    trade_triggers = TradeTriggers(processed_signals_dict)
    trades_dict = trade_triggers.evaluate_triggers()
    trade_selection = TradeSelection(trades_dict)
    selected_trades_dict = trade_selection.select_trades()

    for ticker, selected_trades in selected_trades_dict.items():
        print(f"Selected trades for {ticker}:")
        print(selected_trades)

    from model.visualizer.SimplePlotTradeVisualizer import plot_trades
    from model.ModelEvaluator import ModelEvaluator

    # plot_trades(data_dict, selected_trades_dict)


    evaluator = ModelEvaluator(data_dict, selected_trades_dict)
    evaluator.compute_metrics()
    evaluator.output_to_console()
    evaluator.output_to_html('data/visualizer/model_evaluation.html')
