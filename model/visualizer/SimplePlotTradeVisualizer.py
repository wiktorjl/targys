import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_trades(stock_data_dict, selected_trades_dict):
    """
    Plots the stock closing prices and overlays buy and sell signals for multiple tickers,
    and saves the plots to files instead of displaying them.

    Parameters:
    - stock_data_dict: A dictionary with tickers as keys and DataFrames of stock price data as values. 
      Each DataFrame must include a 'close' column.
    - selected_trades_dict: A dictionary with tickers as keys and DataFrames of selected trades as values. 
      Each trades DataFrame must include a 'positions' column with 1.0 for buy signals and -1.0 for sell signals.
    """

    # Define the directory to save the plots
    save_dir = "data/visualizer"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for ticker, stock_data in stock_data_dict.items():
        # Ensure the trades DataFrame for the ticker is present
        if ticker in selected_trades_dict:
            trades = selected_trades_dict[ticker]
            
            # Create a figure and a plot for each ticker
            fig, ax = plt.subplots(figsize=(14, 7))

            # Plot the closing prices
            stock_data['close'].plot(ax=ax, color='gray', lw=2., title=f"{ticker} Stock Price and Trade Signals")

            # Plot buy signals
            buy_signals = trades[trades['positions'] == 1.0]
            ax.plot(buy_signals.index, stock_data['close'][buy_signals.index], '^', markersize=10, color='g', lw=0, label='Buy Signal')

            # Plot sell signals
            sell_signals = trades[trades['positions'] == -1.0]
            ax.plot(sell_signals.index, stock_data['close'][sell_signals.index], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

            # Customize plot
            ax.set_xlabel('Date')
            ax.set_ylabel('Close Price')
            ax.legend(loc='best')

            # Save plot to file
            save_path = os.path.join(save_dir, f"{ticker}.png")
            plt.savefig(save_path)
            plt.close() 