from groq_llm import llm


def ask() -> None:
    prompt = str(input("Enter a suitable prompt: "))
    cleaned = prompt.strip()
    if not cleaned:
        raise ValueError("Prompt can not be empty!")
    response = llm(cleaned)
    print(response)


if __name__ == "__main__":
    ask()
