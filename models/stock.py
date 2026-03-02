class Stock:
    """
    Domain model representing a single stock holding in a portfolio.

    A Stock encapsulates:
        - Ticker symbol (e.g., "AAPL")
        - Quantity of shares owned (supports fractional shares)
        - Current market price (must be set before valuation)

    This class does not fetch prices itself.
    Price injection is handled externally (e.g., via PriceService).
    """

    def __init__(self, ticker: str, quantity: float):
        """
        Initialize a Stock instance.

        Args:
            ticker (str):
                Stock ticker symbol. Automatically converted to uppercase.

            quantity (float):
                Number of shares owned. Can be fractional if supported
                by the brokerage (e.g., 0.25 shares).
        """
        self.ticker = ticker.upper()
        self.quantity = quantity
        self._price = None

    def set_price(self, price: float):
        """
        Set the current market price of the stock.

        Args:
            price (float):
                Latest market price per share.
        """
        self._price = price

    def current_price(self) -> float:
        """
        Retrieve the current market price.

        Returns:
            float: Price per share.

        Raises:
            RuntimeError:
                If price has not been set prior to calling this method.
        """
        if self._price is None:
            raise RuntimeError(f"Price for {self.ticker} not set.")
        return self._price

    def market_value(self) -> float:
        """
        Calculate total market value of this stock position.

        Returns:
            float: quantity × current_price()

        Raises:
            RuntimeError:
                If price has not been set.
        """
        return self.quantity * self.current_price()