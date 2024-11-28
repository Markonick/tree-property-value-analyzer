from collections import defaultdict

import pytest

from brightbeam_analysis.parsers.properties_parser import PropertiesParser


@pytest.fixture
def sample_csv(tmp_path):
    csv_content = (
        "Date of Sale (dd/mm/yyyy),Address,Street Name,Price\n"
        '01/01/2024,"123 Sample Street",sample street,"€100,000.00"\n'
        '02/01/2024,"456 Sample Street",sample street,"€120,000.00"\n'
        '12/01/2024,"456 Main St",main st,"€150,000.00"\n'
        '13/02/2024,"789 Main St",main st,"€200,000.00"\n'
        '24/03/2024,"101 Test Road",test road,"€250,000.00"\n'
        '25/03/2024,"102 Test Road",test road,"€230,000.00"\n'
    )

    csv_file = tmp_path / "test_properties.csv"
    csv_file.write_text(csv_content)
    return csv_file


def test_get_street_prices(sample_csv):
    parser = PropertiesParser(sample_csv)
    result = parser.get_street_prices()

    # Check that the result is a defaultdict of lists
    assert isinstance(result, defaultdict)
    assert len(result) == 3
    assert result["sample street"] == [100000, 120000]
    assert result["main st"] == [150000, 200000]
    assert result["test road"] == [250000, 230000]


def test_empty_csv(tmp_path):
    """Test handling of empty CSV file."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("Date of Sale,Address,Street Name,Price\n")

    parser = PropertiesParser(str(csv_file))
    result = parser.get_street_prices()
    assert len(result) == 0


def test_invalid_price_formats(tmp_path):
    """Test handling of various invalid price formats."""
    csv_content = (
        "Date of Sale (dd/mm/yyyy),Address,Street Name,Price\n"
        '01/01/2024,"123 Street",test street,"€-100,000.00"\n'  # Negative
        '02/01/2024,"124 Street",test street,"€0.00"\n'  # Zero
        '03/01/2024,"125 Street",test street,"invalid"\n'  # Non-numeric
        '04/01/2024,"126 Street",test street,"€100,000.00"\n'  # Valid
    )
    csv_file = tmp_path / "test_prices.csv"
    csv_file.write_text(csv_content)

    parser = PropertiesParser(str(csv_file))
    result = parser.get_street_prices()

    assert len(result["test street"]) == 2
    assert result["test street"] == [0.0, 100000.0]


def test_invalid_street_names(tmp_path):
    """Test handling of invalid street names."""
    csv_content = (
        "Date of Sale (dd/mm/yyyy),Address,Street Name,Price\n"
        '01/01/2024,"123 Street","","€100,000.00"\n'  # Empty street
        '02/01/2024,"124 Street"," ","€200,000.00"\n'  # Whitespace
        '03/01/2024,"125 Street","valid street","€300,000.00"\n'  # Valid
    )
    csv_file = tmp_path / "test_streets.csv"
    csv_file.write_text(csv_content)

    parser = PropertiesParser(str(csv_file))
    result = parser.get_street_prices()

    assert len(result) == 1
    assert "valid street" in result


def test_missing_columns(tmp_path):
    """Test handling of CSV with missing required columns."""
    csv_content = "Date,Address,Invalid Column,Price\n"
    csv_file = tmp_path / "invalid_columns.csv"
    csv_file.write_text(csv_content)

    parser = PropertiesParser(str(csv_file))
    with pytest.raises(ValueError, match="Missing required columns: {'Street Name'}"):
        parser.get_street_prices()
