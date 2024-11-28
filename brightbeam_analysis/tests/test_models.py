import pytest

from brightbeam_analysis.models import TreeData


def test_tree_data_extraction():
    data = {
        "short": {"level1": {"test road": 5}, "direct street": 3},
        "tall": {"main street": 15, "deep": {"nested": {"high street": 20}}},
    }

    tree_data = TreeData.model_validate(data)
    heights = tree_data.get_heights()

    assert heights["test road"] == ("short", 5)
    assert heights["direct street"] == ("short", 3)
    assert heights["main street"] == ("tall", 15)
    assert heights["high street"] == ("tall", 20)


def test_invalid_height():
    data = {"short": {"test street": -2}, "tall": {}}  # Too tall

    tree_data = TreeData.model_validate(data)
    with pytest.raises(ValueError, match="Invalid tree height"):
        tree_data.get_heights()
