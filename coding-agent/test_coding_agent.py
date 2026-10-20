import pytest

from coding_agent import safe_path


def test_safe_path_optimistic_case():
    assert safe_path("calc.py").name == "calc.py"


def test_safe_path_negative_case():
    with pytest.raises(ValueError):
        safe_path("../pyproject.toml")
