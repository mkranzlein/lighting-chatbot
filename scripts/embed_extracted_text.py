"""Embed the extracted text of spec sheets for RAG pipeline.

Uses Chroma to store embeddings."""

import sys

from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings

# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_chroma import Chroma  # noqa E402


def main():
    spec_sheets_dir = "./data/spec_sheets_text/indoor"
    loader = DirectoryLoader(spec_sheets_dir, glob="**/*.txt")
    documents = loader.load()

    model_name = "all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vector_dir = "./data/chroma_db"

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=vector_dir
    )

    print(f"Successfully created and persisted ChromaDB with embeddings in '{vector_dir}'")


if __name__ == "__main__":
    main()
