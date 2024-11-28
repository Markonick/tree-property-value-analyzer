import logging

from brightbeam_analysis.exceptions import AnalysisError, InsufficientDataError
from brightbeam_analysis.models import AnalysisResults
from brightbeam_analysis.parsers.properties_parser import PropertiesParser
from brightbeam_analysis.parsers.trees_parser import TreesParser
from brightbeam_analysis.price_analyzer import PriceAnalyzer

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(
        self,
        trees_parser: TreesParser,
        properties_parser: PropertiesParser,
        price_analyzer: PriceAnalyzer,
    ):
        self.trees_parser = trees_parser
        self.properties_parser = properties_parser
        self.price_analyzer = price_analyzer

    def get_results(self) -> AnalysisResults:
        """
        Run the complete analysis pipeline.
        Coordinates the parsing of tree and property data, then calculates
        average property prices for streets with tall vs short trees.
        """
        logger.info("Running property analysis service")
        try:
            street_heights = self.trees_parser.get_street_tree_heights()
            street_prices = self.properties_parser.get_street_prices()

            return self.price_analyzer.calculate_averages(street_heights, street_prices)

        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            if isinstance(e, (AnalysisError, InsufficientDataError)):
                raise
            raise AnalysisError(f"Analysis pipeline failed: {e}") from e
