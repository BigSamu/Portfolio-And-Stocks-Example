from typing import Dict, List
from models.stock import Stock


class Portfolio:
    """
    Represents an investment portfolio composed of multiple stocks
    and a desired target allocation strategy.

    Responsibilities:
        - Validate allocation constraints
        - Compute total portfolio value
        - Build derived portfolio metrics
        - Calculate required rebalance actions

    The portfolio assumes all Stock objects have a valid
    current market price set before calculations are performed.
    """

    def __init__(self, stocks: List[Stock], target_allocation: Dict[str, float]):
        """
        Initialize a Portfolio instance.

        Args:
            stocks (List[Stock]):
                List of Stock objects representing current holdings.

            target_allocation (Dict[str, float]):
                Mapping of ticker symbol to target allocation percentage.
                Values must sum to 1.0 (100%).

                Example:
                    {
                        "AAPL": 0.6,
                        "META": 0.4
                    }

        Raises:
            ValueError:
                If target allocation does not sum to 1.
        """
        self.stocks = stocks
        self.target_allocation = target_allocation
        self._validate_allocation()

    def _validate_allocation(self):
        """
        Ensure that target allocation percentages sum to 1.0.

        Raises:
            ValueError:
                If the total allocation differs from 1.0
                (rounded to 5 decimal places to handle float precision).
        """
        total = sum(self.target_allocation.values())
        if round(total, 5) != 1:
            raise ValueError("Target allocation must sum to 1.")

    def total_value(self) -> float:
        """
        Calculate total market value of the portfolio.

        Returns:
            float: Sum of market value of all stocks.
        """
        return sum(stock.market_value() for stock in self.stocks)

    def build_stock_metrics(self) -> Dict[str, dict]:
        """
        Compute derived financial metrics for each stock in the portfolio.

        Metrics include:
            - quantity
            - current price
            - current market value
            - current allocation percentage
            - target allocation percentage
            - target market value
            - dollar difference from target

        Returns:
            Dict[str, dict]:
                Dictionary keyed by ticker symbol.

                Example structure:
                {
                    "AAPL": {
                        "quantity": float,
                        "price": float,
                        "market_value": float,
                        "current_pct": float,
                        "target_pct": float,
                        "target_value": float,
                        "difference_value": float,
                    }
                }
        """

        total_value = self.total_value()
        metrics = {}

        for stock in self.stocks:
            market_value = stock.market_value()
            target_pct = self.target_allocation.get(stock.ticker, 0)
            target_value = total_value * target_pct

            metrics[stock.ticker] = {
                "quantity": stock.quantity,
                "price": stock.current_price(),
                "market_value": market_value,
                "current_pct": market_value / total_value if total_value else 0,
                "target_pct": target_pct,
                "target_value": target_value,
                "difference_value": target_value - market_value,
            }

        return metrics

    def rebalance(self) -> Dict[str, dict]:
        """
        Calculate required trades to achieve target allocation.

        For each stock, this method determines:
            - Whether to BUY or SELL
            - Number of shares required (fractional supported)
            - Ignores negligible differences (< $0.01)

        Returns:
            Dict[str, dict]:
                Dictionary keyed by ticker symbol containing:

                {
                    "AAPL": {
                        "action": "BUY" | "SELL",
                        "shares": float
                    }
                }

            Empty dictionary if portfolio is already balanced.
        """

        metrics = self.build_stock_metrics()
        actions = {}

        for ticker, data in metrics.items():

            diff = data["difference_value"]
            price = data["price"]

            if abs(diff) < 0.01:
                continue

            shares = diff / price
            action = "BUY" if diff > 0 else "SELL"

            actions[ticker] = {
                "action": action,
                "shares": round(abs(shares), 4)
            }

        return actions