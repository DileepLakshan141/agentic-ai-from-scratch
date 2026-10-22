from dotenv import load_dotenv
from importlib.metadata import version
import os

load_dotenv()

core_version = version("langchain_core")
lg_version = version("langgraph")
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI

print(f"lang core version: {core_version}")
print(f"lang graph version: {lg_version}")


def main():
    # groq chat
    llm_groq = ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0.2,
        model=os.environ["GROQ_MODEL"],
    )
    response_groq = llm_groq.invoke("say setup is complete in one word")
    print(f"Response from groq: {response_groq}")

    llm_mistral = ChatMistralAI(
        api_key=os.environ["MISTRAL_API_KEY"],
        temperature=0.2,
        model=os.environ["MISTRAL_MODEL"],
    )
    response_mistral = llm_mistral.invoke("say setup is complete in one word")
    print(f"Response from mistral: {response_mistral}")


if __name__ == "__main__":
    main()
