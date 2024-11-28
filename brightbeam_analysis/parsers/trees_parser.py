import logging

from typing import Dict, Tuple

from pydantic import ValidationError

from brightbeam_analysis.exceptions import DataValidationError, FileParsingError
from brightbeam_analysis.models import TreeData

logger = logging.getLogger(__name__)


class TreesParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_street_tree_heights(self) -> Dict[str, Tuple[str, int]]:
        """Parse tree heights from JSON file using Pydantic model."""
        try:
            with open(self.file_path) as file:
                try:
                    tree_data = TreeData.model_validate_json(file.read())
                    heights = tree_data.get_heights()
                except ValidationError as e:
                    if "Invalid JSON" in str(e):
                        raise FileParsingError(f"Invalid JSON format: {e}") from e
                    raise DataValidationError(str(e)) from e

            logger.info(f"Loaded {len(heights)} street heights")
            return heights

        except FileNotFoundError as e:
            raise FileParsingError(f"Tree data file not found: {self.file_path}") from e
        except Exception as e:
            raise DataValidationError(f"Error parsing tree data: {e}") from e
