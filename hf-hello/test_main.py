from main import greet


def test_greet_func() -> None:
    names = ["Dileepa", "Alex", "James"]
    for name in names:
        result = greet(name, "Good Morning")
        assert result == f"Good Morning, {name}!"
