from pathlib import Path
import pymupdf4llm

DATA_FOLDER = Path("data")
MARKDOWN_FOLDER = DATA_FOLDER / "markdown"


def pdf_to_markdown(pdf_path: Path):

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    markdown = pymupdf4llm.to_markdown(pdf_path)

    MARKDOWN_FOLDER.mkdir(parents=True, exist_ok=True)

    markdown_path = MARKDOWN_FOLDER / f"{pdf_path.stem}.md"

    markdown_path.write_text(markdown, encoding="utf-8")

    print(f"Created: {markdown_path}")


if __name__ == "__main__":

    pdf_files = list(DATA_FOLDER.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in data folder.")

    for pdf_file in pdf_files:
        pdf_to_markdown(pdf_file)