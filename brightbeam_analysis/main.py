import logging

from brightbeam_analysis.analysis_service import AnalysisService
from brightbeam_analysis.parsers.properties_parser import PropertiesParser
from brightbeam_analysis.parsers.trees_parser import TreesParser
from brightbeam_analysis.price_analyzer import PriceAnalyzer
from brightbeam_analysis.utils import PrintAnalysisResults

# Configure logging at the start of your script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # This will output to console
)

# Get logger for this module
logger = logging.getLogger(__name__)


def main():
    # Initialize components
    trees_parser = TreesParser("data/dublin-trees.json")
    properties_parser = PropertiesParser("data/dublin-property.csv")
    price_analyzer = PriceAnalyzer()

    # Create service
    analysis_service = AnalysisService(
        trees_parser=trees_parser,
        properties_parser=properties_parser,
        price_analyzer=price_analyzer,
    )

    try:
        # Run analysis
        results = analysis_service.get_results()

        # Print results
        PrintAnalysisResults.show_stats(results)

    except FileNotFoundError as e:
        logger.error(f"Error: Could not find data file - {e}")
    except Exception as e:
        logger.error(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()
