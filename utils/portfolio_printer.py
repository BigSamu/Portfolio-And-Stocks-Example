class PortfolioPrinter:
    """
    Utility class responsible for rendering portfolio data to the console.

    This class contains only static methods and does not maintain state.
    It formats portfolio metrics into human-readable tabular output.
    """

    @staticmethod
    def print_snapshot(portfolio, metrics: dict):
        """
        Print a formatted snapshot of the current portfolio state.

        Displays:
        - Total portfolio market value
        - Per-stock quantity
        - Current price
        - Market value
        - Current allocation percentage
        - Target allocation percentage

        Args:
            portfolio (Portfolio):
                Portfolio instance used to calculate total market value.

            metrics (dict):
                Dictionary produced by Portfolio.build_stock_metrics().
                Expected structure:

                {
                    "AAPL": {
                        "quantity": float,
                        "price": float,
                        "market_value": float,
                        "current_pct": float,
                        "target_pct": float,
                        ...
                    },
                    ...
                }
        """

        total_value = portfolio.total_value()

        print("\n=== PORTFOLIO SNAPSHOT ===\n")
        print(f"Total Value: ${total_value:,.2f}\n")

        print(f"{'Ticker':<8}{'Qty':<8}{'Price':<10}{'Value':<12}{'Alloc':<8}{'Target'}")
        print("-" * 60)

        for ticker, data in metrics.items():
            print(
                f"{ticker:<8}"
                f"{data['quantity']:<8}"
                f"{data['price']:<10.2f}"
                f"{data['market_value']:<12,.2f}"
                f"{data['current_pct']*100:<8.2f}"
                f"{data['target_pct']*100:.2f}"
            )

    @staticmethod
    def print_rebalance_plan(metrics: dict):
        """
        Print the calculated rebalance plan based on target allocation.

        For each stock whose current allocation deviates meaningfully
        from its target allocation, this method displays:

        - Target market value
        - Current market value
        - Dollar difference (Δ)
        - Required action (BUY / SELL)
        - Number of shares to trade

        Small differences (< $0.01) are ignored to prevent noise.

        Args:
            metrics (dict):
                Dictionary produced by Portfolio.build_stock_metrics().
                Must contain:

                {
                    "difference_value": float,
                    "price": float,
                    "target_value": float,
                    "market_value": float,
                    ...
                }
        """

        print("\n=== REBALANCE PLAN ===\n")

        print(f"{'Ticker':<8}{'Target $':<12}{'Current $':<12}{'Δ $':<12}{'Action'}")
        print("-" * 65)

        for ticker, data in metrics.items():

            diff = data["difference_value"]
            price = data["price"]

            if abs(diff) < 0.01:
                continue

            shares = diff / price
            action = "BUY" if diff > 0 else "SELL"

            print(
                f"{ticker:<8}"
                f"{data['target_value']:<12,.2f}"
                f"{data['market_value']:<12,.2f}"
                f"{diff:<12,.2f}"
                f"{action} {abs(shares):.4f}"
            )