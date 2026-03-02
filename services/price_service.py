import os
import finnhub
from halo import Halo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PriceService:
    """
    Infrastructure service responsible for retrieving real-time
    stock prices from the Finnhub API.

    This class acts as an external data provider and is part of the
    application's service layer (not the domain layer).

    Requirements:
        - FINNHUB_API_KEY must be set in environment variables.
        - Network connectivity must be available.

    Raises:
        EnvironmentError:
            If the API key is not configured.
    """

    def __init__(self):
        """
        Initialize Finnhub API client using environment configuration.

        Raises:
            EnvironmentError:
                If FINNHUB_API_KEY is missing from environment variables.
        """
        api_key = os.getenv("FINNHUB_API_KEY")
        if not api_key:
            raise EnvironmentError("FINNHUB_API_KEY not set.")

        self.client = finnhub.Client(api_key=api_key)

    def fetch_prices(self, tickers: list[str]) -> dict[str, float]:
        """
        Retrieve latest market prices for a list of ticker symbols.

        This method:
            - Calls Finnhub's quote endpoint for each ticker
            - Extracts the current price field ("c")
            - Validates returned price data
            - Returns a mapping of ticker → price

        Args:
            tickers (list[str]):
                List of stock ticker symbols (e.g., ["AAPL", "META"]).

        Returns:
            dict[str, float]:
                Dictionary mapping each ticker symbol to its
                current market price.

                Example:
                    {
                        "AAPL": 189.32,
                        "META": 492.11
                    }

        Raises:
            ValueError:
                If a ticker returns no valid price.

            RuntimeError:
                If the external market data service fails or
                is unavailable.
        """

        spinner = Halo(text="Fetching market prices from Finnhub...", spinner="dots")
        spinner.start()

        prices = {}

        try:
            for ticker in tickers:
                quote = self.client.quote(ticker)

                # Finnhub response fields:
                # c  = current price
                # h  = high price of the day
                # l  = low price of the day
                # o  = open price of the day
                # pc = previous close price

                current_price = quote.get("c")

                if not current_price or current_price == 0:
                    raise ValueError(f"No valid price for {ticker}")

                prices[ticker] = float(current_price)

            spinner.succeed("Prices fetched successfully")
            return prices

        except Exception as e:
            spinner.fail("Failed to fetch prices from Finnhub")
            raise RuntimeError("Market data service unavailable") from e