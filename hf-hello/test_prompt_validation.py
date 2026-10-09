import pytest
from ask import validate_prompt


def test_validate_good_promot() -> None:
    assert validate_prompt("   hello     ") == "hello"


@pytest.mark.parametrize("prompt", ["", "   ", "\n", "\t"])
def test_validate_bad_prompt(prompt: str) -> None:
    with pytest.raises(ValueError):
        validate_prompt(prompt)
