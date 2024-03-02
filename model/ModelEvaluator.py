import pandas as pd
import numpy as np
import os
from jinja2 import Template

class ModelEvaluator:
    def __init__(self, stock_data_dict, selected_trades_dict):
        """
        Initialize the evaluator with dictionaries for stock data and selected trades.
        - stock_data_dict: Dictionary with tickers as keys and DataFrames of stock price data as values.
        - selected_trades_dict: Dictionary with tickers as keys and DataFrames of selected trades as values.
        """
        self.stock_data_dict = stock_data_dict
        self.selected_trades_dict = selected_trades_dict
        self.results = {}

    def compute_metrics_for_ticker(self, ticker, stock_data, trades):
        """
        Compute performance metrics for a single ticker.
        """
        data = stock_data.copy()
        data['positions'] = trades['positions']

        # Assume each trade happens at the close of the trading day
        data['strategy'] = data['positions'].shift(1) * data['close'].pct_change()
        data['return'] = data['close'].pct_change()

        # Cumulative returns
        data['cumulative_return'] = (1 + data['return']).cumprod()
        data['cumulative_strategy_return'] = (1 + data['strategy']).cumprod()

        total_return = data['cumulative_strategy_return'].iloc[-1] - 1
        total_market_return = data['cumulative_return'].iloc[-1] - 1

        return {
            'Total Return': f"{total_return:.2%}",
            'Total Market Return': f"{total_market_return:.2%}",
        }

    def compute_metrics(self):
        """
        Compute performance metrics for all tickers.
        """
        for ticker, stock_data in self.stock_data_dict.items():
            if ticker in self.selected_trades_dict:
                trades = self.selected_trades_dict[ticker]
                self.results[ticker] = self.compute_metrics_for_ticker(ticker, stock_data, trades)

    def output_to_console(self):
        """
        Print the performance metrics to the console for all tickers.
        """
        for ticker, metrics in self.results.items():
            print(f"Model Performance Metrics for {ticker}:")
            for metric, value in metrics.items():
                print(f"{metric}: {value}")
            print("-" * 40)  # Separator
    
    def output_to_html(self, output_path="model_evaluation.html"):
        """
        Output the performance metrics to an HTML file for all tickers.
        """
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Model Evaluation Report</title>
        </head>
        <body>
            <h1>Model Performance Metrics</h1>
            {% for ticker, metrics in results.items() %}
                <h2>{{ ticker }}</h2>
                <ul>
                {% for metric, value in metrics.items() %}
                    <li>{{ metric }}: {{ value }}</li>
                {% endfor %}
                </ul>
            {% endfor %}
        </body>
        </html>
        """)
        html_content = html_template.render(results=self.results)

        with open(output_path, 'w') as file:
            file.write(html_content)
        print(f"HTML report saved to {output_path}")
