import pandas as pd
from datetime import datetime, timedelta

# Example OHLC DataFrame structure
# ohlc_data = pd.DataFrame({
#     'Symbol': ['AAPL', 'AAPL', 'MSFT', 'MSFT'],
#     'Date': ['2023-03-10', '2023-03-11', '2023-03-10', '2023-03-11'],
#     'Open': [150, 152, 250, 255],
#     'High': [155, 153, 260, 265],
#     'Low': [149, 151, 248, 253],
#     'Close': [154, 152, 258, 264]
# })

# Convert 'Date' column to datetime
ohlc_data['Date'] = pd.to_datetime(ohlc_data['Date'])

# Find the date 3 days ago and 52 weeks ago from the latest date in your DataFrame
three_days_ago = ohlc_data['Date'].max() - timedelta(days=3)
fifty_two_weeks_ago = ohlc_data['Date'].max() - timedelta(weeks=52)

def stocks_hitting_52_week_high(df):
    high_achievers = []

    # Iterate through each symbol in the DataFrame
    for symbol in df['Symbol'].unique():
        symbol_data = df[df['Symbol'] == symbol]

        # Filter data for the last 52 weeks
        last_52_weeks_data = symbol_data[symbol_data['Date'] > fifty_two_weeks_ago]

        # Calculate 52-week high
        highest_price = last_52_weeks_data['High'].max()

        # Filter data for the past 3 days
        recent_data = symbol_data[symbol_data['Date'] > three_days_ago]

        # Check if the stock hit a new 52-week high in the past 3 days
        if not recent_data.empty and recent_data['High'].max() >= highest_price:
            high_achievers.append(symbol)
    
    return high_achievers

# Get the list of stocks hitting 52-week highs
stocks_52_week_high = stocks_hitting_52_week_high(ohlc_data)

print("S&P 500 stocks hitting 52-week highs in the past 3 days:")
for stock in stocks_52_week_high:
    print(stock)
