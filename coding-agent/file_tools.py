from pathlib import Path

SANDBOX = Path(__file__).parent / "sandbox"


def safe_path(relative_path: str) -> Path:
    path = (SANDBOX / relative_path).resolve()
    if not path.is_relative_to(SANDBOX.resolve()):
        raise ValueError(f"path '{relative_path}' is outside the sandbox")
    return path


def read_file(path: str) -> str:
    try:
        return safe_path(path).read_text(encoding="utf-8")
    except (ValueError, OSError) as exc:
        return f"ERROR: {exc}"


if __name__ == "__main__":
    print(read_file("calc.py"))
    print(read_file("../pyproject.toml"))
    print(read_file("nope.py"))
    print(read_file("sub/../calc.py"))
    print(read_file(r"C:\Windows\win.ini"))
