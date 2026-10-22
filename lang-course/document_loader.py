import os
import tempfile
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from dotenv import load_dotenv

load_dotenv()


def load_text_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(
            b"Hello this is a sample text file.\nThis file is used to demonstrate text loader"
        )
        temp_file_path = temp_file.name

    try:
        loader = TextLoader(temp_file_path)
        documents = loader.load()

        for doc in documents:
            print("Document Content: ")
            print(doc)
            print(doc.page_content)

    finally:
        os.remove(temp_file_path)


def load_pdf_file(path: str):
    loader = PyPDFLoader(path)
    documents = loader.load()

    for i, doc in enumerate(documents):
        print(f"Document {i+1} content preview: {doc.page_content[300:]}...")
        print(f"Metadata: {doc.metadata}")


if __name__ == "__main__":
    # load_text_file()
    load_pdf_file("./docs/prod_rad_v1.pdf")
