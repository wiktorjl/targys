# Read all CSVs with OHLC stock data from data/symbols and merge it into one CSV file, ordered by date. Make sure the CSV file has the following columns: date, open, high, low, close, adjusted_close, volume. Save the merged CSV file in data/combined.csv

import pandas as pd
import os

symbols = os.listdir("data/symbols")
dfs = []
for symbol in symbols:
    print(f"Processing {symbol} ({symbols.index(symbol) + 1} out of {len(symbols)})")


    df = pd.read_csv(f"data/symbols/{symbol}")
    # Add column for the symbol name as the first column
    df.insert(0, "symbol", symbol.split(".")[0])
    dfs.append(df)
    
combined = pd.concat(dfs)
combined = combined.sort_values(by="date")

combined.to_csv("data/combined.csv", index=False)
print("Combined CSV file saved successfully")
