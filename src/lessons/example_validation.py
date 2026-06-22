"""Simple validation script to ensure imports load."""

import sys

import streamlit
import langchain
import chromadb


def main() -> None:
    print("Python", sys.version)
    print("Streamlit", streamlit.__version__)
    print("LangChain", langchain.__version__)
    print("ChromaDB", chromadb.__version__)


if __name__ == "__main__":
    main()
