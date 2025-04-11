import os
from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdfs(source_dir: str, target_dir: str) -> None:
    """Extract text from PDFs and save in .txt files in target dir.

    Args:
        source_dir: An existing directory containing PDFs.
        target_dir: A directory where .txt files will be saved.
    """
    os.makedirs(target_dir, exist_ok=True)
    for filename in os.listdir(source_dir):
        if filename.endswith(".pdf"):
            pdf_path = Path(source_dir, filename)
            text = ""
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text += page.extract_text()

            txt_path = Path(target_dir, filename).with_suffix(".txt")
            with open(txt_path, "w") as f:
                f.write(text)


def main():
    source_dir = "data/spec_sheets/indoor"
    target_dir = "data/spec_sheets_text/indoor"
    extract_text_from_pdfs(source_dir, target_dir)


if __name__ == "__main__":
    main()
