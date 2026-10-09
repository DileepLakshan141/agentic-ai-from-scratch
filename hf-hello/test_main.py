import pytest
from main import greet


@pytest.mark.parametrize("name", ["Dileepa", "Alex", "James"])
def test_greet_includes_name(name: str) -> None:
    assert greet(name, "Good Morning") == f"Good Morning, {name}!"
