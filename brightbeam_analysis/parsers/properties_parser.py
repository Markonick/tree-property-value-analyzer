import csv
import logging

from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from brightbeam_analysis.models import Property

logger = logging.getLogger(__name__)


class PropertiesParser:
    REQUIRED_COLUMNS = {"Street Name", "Price"}

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_street_prices(self) -> Dict[str, List[float]]:
        """
        Create dictionary mapping street names to their property prices.
        Parses CSV file to extract street names and prices, handling various
        data quality issues like invalid prices or missing values.
        """
        self._validate_file_exists()
        street_prices = defaultdict(list)

        try:
            with open(self.file_path, encoding="latin-1") as file:
                reader = csv.DictReader(file)

                # Validate CSV structure
                if not reader.fieldnames:
                    raise ValueError("CSV file is empty or has no headers")

                missing_columns = self.REQUIRED_COLUMNS - set(reader.fieldnames)
                if missing_columns:
                    raise ValueError(f"Missing required columns: {missing_columns}")

                for row in reader:
                    try:
                        property_row = Property.model_validate(row)
                        if property_row.street_name:  # Skip empty street names
                            street_prices[property_row.street_name].append(property_row.price)
                    except Exception as e:
                        logger.debug(f"Skipping invalid row: {e}")
                        continue
            return street_prices

        except Exception as e:
            logger.error(f"Error parsing CSV: {e}")
            raise

    def _validate_file_exists(self) -> None:
        """Check if input file exists."""
        if not Path(self.file_path).exists():
            logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"Cannot find file: {self.file_path}")
