from typing import Dict, List

from brightbeam_analysis.exceptions import AnalysisError, InsufficientDataError
from brightbeam_analysis.models import AnalysisResults


class PriceAnalyzer:
    @staticmethod
    def calculate_averages(
        street_heights: Dict[str, tuple], street_prices: Dict[str, List[float]]
    ) -> AnalysisResults:
        """Calculate average prices for streets with tall and short trees."""
        # Check input data first
        if not street_heights:
            raise InsufficientDataError("No data provided for analysis: empty tree data")
        if not street_prices:
            raise InsufficientDataError("No data provided for analysis: empty property data")

        tall_prices = []
        short_prices = []

        try:
            for street, (category, _) in street_heights.items():
                if street in street_prices:
                    prices = street_prices[street]
                    if category == "tall":
                        tall_prices.extend(prices)
                    else:  # category == 'short'
                        short_prices.extend(prices)

            if not tall_prices and not short_prices:
                raise InsufficientDataError(
                    "No matching streets found between tree and property data"
                )
            return AnalysisResults(
                tall_tree_avg=sum(tall_prices) / len(tall_prices) if tall_prices else 0,
                short_tree_avg=sum(short_prices) / len(short_prices) if short_prices else 0,
                tall_tree_count=len(tall_prices),
                short_tree_count=len(short_prices),
            )
        except Exception as e:
            if isinstance(e, InsufficientDataError):
                raise
            raise AnalysisError(f"Error calculating averages: {e}") from e
