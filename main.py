"""
main.py

Entry point of the portfolio rebalancing application.

Responsibilities:
- Create portfolio objects
- Fetch market prices
- Inject prices into stocks
- Trigger portfolio analysis
- Display results

This file acts as the composition root of the application.
"""

from models.stock import Stock
from models.portfolio import Portfolio
from services.price_service import PriceService
from utils.portfolio_printer import PortfolioPrinter


def main():
    """
    Main execution flow of the portfolio rebalancing program.
    """

    # ---------------------------------------------------------
    # 1️⃣ Define initial portfolio holdings
    # ---------------------------------------------------------
    # We create Stock objects with ticker symbol and quantity.
    # Prices are not set yet — they will be fetched from the API.
    stocks = [
        Stock("AAPL", 10),
        Stock("META", 5),
    ]

    # ---------------------------------------------------------
    # 2️⃣ Define target allocation strategy
    # ---------------------------------------------------------
    # Allocation must sum to 1.0 (100%).
    # This represents the desired portfolio distribution.
    target_allocation = {
        "AAPL": 0.6,  # 60%
        "META": 0.4,  # 40%
    }

    # ---------------------------------------------------------
    # 3️⃣ Fetch latest market prices
    # ---------------------------------------------------------
    # Extract tickers from stock objects
    tickers = [stock.ticker for stock in stocks]

    # Initialize external pricing service (Finnhub)
    price_service = PriceService()

    # Retrieve current market prices
    prices = price_service.fetch_prices(tickers)

    # Inject fetched prices into each Stock object
    for stock in stocks:
        stock.set_price(prices[stock.ticker])

    # ---------------------------------------------------------
    # 4️⃣ Create Portfolio object
    # ---------------------------------------------------------
    # Portfolio now contains fully hydrated Stock objects
    # (with quantity and current market price)
    portfolio = Portfolio(stocks, target_allocation)

    # Build computed metrics (market value, allocation %, etc.)
    metrics = portfolio.build_stock_metrics()

    # ---------------------------------------------------------
    # 5️⃣ Display portfolio snapshot and rebalance plan
    # ---------------------------------------------------------
    PortfolioPrinter.print_snapshot(portfolio, metrics)
    PortfolioPrinter.print_rebalance_plan(metrics)

    # ---------------------------------------------------------
    # 6️⃣ Compute final rebalance actions
    # ---------------------------------------------------------
    # This calculates how many shares must be bought or sold
    # to match the target allocation.
    actions = portfolio.rebalance()

    print("\n--- FINAL ACTIONS ---\n")

    # Display trading instructions
    if not actions:
        print("Portfolio is already balanced.")
    else:
        for ticker, data in actions.items():
            print(f"{data['action']} {data['shares']} shares of {ticker}")


if __name__ == "__main__":
    main()