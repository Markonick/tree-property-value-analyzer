import logging
import re

from typing import Dict, Tuple, Union

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class AnalysisResults(BaseModel):
    tall_tree_avg: float = Field(
        description="Average price of properties on streets with tall trees"
    )
    tall_tree_count: int = Field(description="Number of properties on streets with tall trees")
    short_tree_avg: float = Field(
        description="Average price of properties on streets with short trees"
    )
    short_tree_count: int = Field(description="Number of properties on streets with short trees")

    class Config:
        frozen = True  # Makes the model immutable


class Property(BaseModel):
    street_name: str = Field(alias="Street Name")
    price: float = Field(alias="Price")

    @field_validator("street_name", mode="before")
    @classmethod
    def validate_street_name(cls, v: str) -> str:
        """Validate and clean street name."""
        cleaned = str(v).lower().strip()
        return cleaned if cleaned else ""

    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, v: str) -> float:
        """Validate and convert price string to float."""
        if "-" in str(v):
            return None

        clean_price = re.sub(r"[^0-9.,]", "", str(v)).replace(",", "")
        try:
            return float(clean_price)
        except (ValueError, AttributeError):
            logger.error(f"Failed to convert '{clean_price}' to float")
            return None


class TreeData(BaseModel):
    """Root model for the tree JSON file."""

    short: Dict[str, Union[Dict, int]] = Field(description="Streets with short trees")
    tall: Dict[str, Union[Dict, int]] = Field(description="Streets with tall trees")

    def get_heights(self) -> Dict[str, Tuple[str, int]]:
        """
        Extract street heights from nested structure.
        Traverses the nested dictionary structure to find street names and their heights.
        """
        heights: Dict[str, Tuple[str, int]] = {}

        for category in ["short", "tall"]:
            data = getattr(self, category)
            stack = list(data.items())
            while stack:
                key, value = stack.pop()
                if isinstance(value, dict):
                    stack.extend((k, v) for k, v in value.items())
                elif isinstance(value, int):
                    if not value >= 0:  # Validate height
                        raise ValueError(f"Invalid tree height {value} for street {key}")
                    heights[key.lower()] = (category, value)

        return heights
