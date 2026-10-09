from groq_llm import llm


def validate_prompt(raw: str) -> str:
    cleaned = raw.strip()
    if not cleaned:
        raise ValueError("Prompt can not be empty!")
    return cleaned


def ask() -> None:
    prompt = validate_prompt(input("Enter a suitable prompt: "))
    response = llm(prompt)
    print(response)


if __name__ == "__main__":
    ask()
