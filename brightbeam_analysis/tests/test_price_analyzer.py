import pytest

from brightbeam_analysis.analysis_service import AnalysisService
from brightbeam_analysis.exceptions import InsufficientDataError
from brightbeam_analysis.parsers.properties_parser import PropertiesParser
from brightbeam_analysis.parsers.trees_parser import TreesParser
from brightbeam_analysis.price_analyzer import PriceAnalyzer


@pytest.fixture
def sample_data(tmp_path):
    # Create a sample JSON file for testing
    json_content = """
    {
        "short": {"road": {"test": {"test road": 5}}},
        "tall": {"street": {"sample": {"sample street": 20}}}
    }
    """
    json_file = tmp_path / "test_trees.json"
    json_file.write_text(json_content)

    # Create a sample CSV file for testing
    csv_content = (
        "Date of Sale (dd/mm/yyyy),Address,Street Name,Price\n"
        '2020-01-01,"1 Test Road",test road,"€100,000.00"\n'
        '2020-01-02,"2 Test Road",Test Road,"€200,000.00"\n'
        '2020-01-03,"1 Sample Street",Sample Street,"€300,000.00"\n'
    )
    csv_file = tmp_path / "test_properties.csv"
    csv_file.write_text(csv_content)
    return json_file, csv_file


def test_analyzer_run(sample_data):
    json_file, csv_file = sample_data
    analysis_service = AnalysisService(
        trees_parser=TreesParser(json_file),
        properties_parser=PropertiesParser(csv_file),
        price_analyzer=PriceAnalyzer(),
    )
    results = analysis_service.get_results()
    assert results.short_tree_avg == 150000.00
    assert results.tall_tree_avg == 300000.00
    assert results.short_tree_count == 2
    assert results.tall_tree_count == 1


def test_insufficient_data(tmp_path):
    """Test handling of insufficient data."""
    # Create empty files
    json_file = tmp_path / "empty.json"
    json_file.write_text('{"short": {}, "tall": {}}')

    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("Date,Address,Street Name,Price\n")

    analysis_service = AnalysisService(
        trees_parser=TreesParser(json_file),
        properties_parser=PropertiesParser(csv_file),
        price_analyzer=PriceAnalyzer(),
    )

    with pytest.raises(
        InsufficientDataError, match="No data provided for analysis: empty tree data"
    ):
        analysis_service.get_results()


def test_empty_property_data(tmp_path):
    """Test handling of empty property data."""
    # Create tree data but empty property data
    json_file = tmp_path / "trees.json"
    json_file.write_text('{"short": {"test street": 5}, "tall": {}}')

    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("Date,Address,Street Name,Price\n")

    analysis_service = AnalysisService(
        trees_parser=TreesParser(json_file),
        properties_parser=PropertiesParser(csv_file),
        price_analyzer=PriceAnalyzer(),
    )

    with pytest.raises(
        InsufficientDataError, match="No data provided for analysis: empty property data"
    ):
        analysis_service.get_results()
