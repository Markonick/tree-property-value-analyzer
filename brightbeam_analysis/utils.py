import logging

from brightbeam_analysis.models import AnalysisResults

# Get logger for this module
logger = logging.getLogger(__name__)


class PrintAnalysisResults:
    @staticmethod
    def show_stats(results: AnalysisResults):
        """Format and print analysis results."""
        logger.info("Analysis Results:")
        logger.info("-" * 50)
        logger.info("Streets with tall trees:")
        logger.info(f"  Average price: €{results.tall_tree_avg:,.2f}")
        logger.info(f"  Sample size: {results.tall_tree_count}")
        logger.info("")
        logger.info("Streets with short trees:")
        logger.info(f"  Average price: €{results.short_tree_avg:,.2f}")
        logger.info(f"  Sample size: {results.short_tree_count}")
