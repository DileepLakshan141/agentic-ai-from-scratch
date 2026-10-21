import pytest

from file_tools import safe_path, write_file


def test_safe_path_optimistic_case():
    assert safe_path("calc.py").name == "calc.py"


def test_safe_path_negative_case():
    with pytest.raises(ValueError):
        safe_path("../pyproject.toml")


def test_write_file_optimistic_case():
    result = write_file("../x.txt", "hi")
    assert result.startswith("ERROR")
