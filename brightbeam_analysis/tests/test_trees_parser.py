import json

from pathlib import Path

import pytest

from brightbeam_analysis.exceptions import DataValidationError, FileParsingError
from brightbeam_analysis.parsers.trees_parser import TreesParser


@pytest.fixture
def valid_json(tmp_path) -> Path:
    """Create a valid JSON file for testing."""
    json_content = {"short": {"test road": 5}, "tall": {"high street": 20}}
    json_file = tmp_path / "valid.json"
    json_file.write_text(json.dumps(json_content))
    return json_file


def test_happy_path(valid_json):
    """Test successful parsing."""
    parser = TreesParser(valid_json)
    result = parser.get_street_tree_heights()

    assert len(result) == 2
    assert result["test road"] == ("short", 5)
    assert result["high street"] == ("tall", 20)


def test_file_not_found():
    """Test FileNotFoundError -> FileParsingError."""
    parser = TreesParser("nonexistent.json")
    with pytest.raises(FileParsingError, match="Tree data file not found"):
        parser.get_street_tree_heights()


def test_invalid_json_syntax(tmp_path):
    """Test JSONDecodeError -> FileParsingError."""
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("{invalid json syntax}")

    parser = TreesParser(invalid_json)
    with pytest.raises(DataValidationError, match="Invalid JSON format"):
        parser.get_street_tree_heights()


def test_invalid_tree_height(tmp_path):
    """Test ValueError -> DataValidationError."""
    invalid_height = tmp_path / "invalid_height.json"
    json_content = {"short": {"test road": -5}, "tall": {}}  # Invalid negative height
    invalid_height.write_text(json.dumps(json_content))

    parser = TreesParser(invalid_height)
    with pytest.raises(DataValidationError, match="Invalid tree height"):
        parser.get_street_tree_heights()


def test_empty_but_valid_json(tmp_path):
    """Test handling of empty but valid JSON."""
    empty_json = tmp_path / "empty.json"
    json_content = {"short": {}, "tall": {}}
    empty_json.write_text(json.dumps(json_content))

    parser = TreesParser(empty_json)
    result = parser.get_street_tree_heights()
    assert len(result) == 0


def test_missing_required_fields(tmp_path):
    """Test missing required fields in JSON."""
    invalid_json = tmp_path / "invalid.json"
    json_content = {"short": {}}  # Missing 'tall' field
    invalid_json.write_text(json.dumps(json_content))

    parser = TreesParser(invalid_json)
    with pytest.raises(DataValidationError):
        parser.get_street_tree_heights()
