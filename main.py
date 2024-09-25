import sys
import yfinance as yf
from datetime import datetime, timedelta
from typing import List
from halo import Halo

class Stock:
    def __init__(self, symbol: str):
        self.symbol = symbol



    def price(self, date: datetime) -> float:

        spinner = Halo(text=f'Fetching data from Yahoo Finance...\n', spinner='line')
        spinner.start()

        try:
            stock = yf.Ticker(self.symbol)
            stock_data = stock.history(start=date.strftime("%Y-%m-%d"), end=(date + timedelta(days=1)).strftime("%Y-%m-%d"))

            spinner.stop()  # Stop the spinner

            if not stock_data.empty:
                return float(stock_data['Close'].iloc[0])
            else:
                print(f"{date.date()} is not a trading date. Please select a valid trading date.")
                sys.exit()
        except Exception as e:
            spinner.stop()  # Stop the spinner
            print(f"Error fetching data for {self.symbol}: {e}")
            return 0.0


class Portfolio:
    def __init__(self):
        self.stocks: List[Stock] = []

    def add_stock(self, stock: Stock):
        self.stocks.append(stock)

    def profit(self, start_date: datetime, end_date: datetime) -> float:
        total_start_value = 0.0
        total_end_value = 0.0

        for stock in self.stocks:
            start_price = stock.price(start_date)
            end_price = stock.price(end_date)
            total_start_value += start_price
            total_end_value += end_price

        return total_end_value - total_start_value

    def annualized_return(self, start_date: datetime, end_date: datetime) -> float:
        profit = self.profit(start_date, end_date)
        total_start_value = sum(stock.price(start_date) for stock in self.stocks)

        if total_start_value == 0:
            return 0.0

        # Calculate the number of days between the start and end date
        num_days = (end_date - start_date).days
        # Calculate annualized return
        annualized_return = ((profit / total_start_value) + 1) ** (365 / num_days) - 1
        return annualized_return * 100


# Example usage
if __name__ == "__main__":
    # Create Stock objects
    apple_stock = Stock("AAPL")
    microsoft_stock = Stock("MSFT")

    # Create a Portfolio and add stocks
    portfolio = Portfolio()
    portfolio.add_stock(apple_stock)
    portfolio.add_stock(microsoft_stock)

    # Define the start and end dates
    start_date = datetime(2023, 1, 3)  # First trading day in 2023
    end_date = datetime(2023, 6, 1)    # Any date when markets were open
    print(f"*" * 50)
    print(f"Portfolio with following stocks:")
    for stock in portfolio.stocks:
        print(f" - {stock.symbol}")
    print(f'\nCalculating profit and annualized return from {start_date.date()} to {end_date.date()}...')

    # Calculate the profit and annualized return
    total_profit = portfolio.profit(start_date, end_date)
    annualized_return = portfolio.annualized_return(start_date, end_date)

    print(f"\nTotal Profit from {start_date.date()} to {end_date.date()}: ${total_profit:.2f}")
    print(f"Annualized Return: {annualized_return:.2f}%")
    print(f"*" * 50)
