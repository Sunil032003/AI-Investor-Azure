
from pathlib import Path
import pymupdf4llm


# ============================================================
# Directory Configuration
# ============================================================

APP_DIR = Path(__file__).resolve().parents[1]

DATA_FOLDER = APP_DIR / "data"
PDF_FOLDER = DATA_FOLDER / "pdfs"
MARKDOWN_FOLDER = DATA_FOLDER / "markdown"


# ============================================================
# PDF to Markdown Conversion
# ============================================================

def pdf_to_markdown(pdf_path: Path):

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    markdown = pymupdf4llm.to_markdown(pdf_path)

    MARKDOWN_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    markdown_path = (
        MARKDOWN_FOLDER / f"{pdf_path.stem}.md"
    )

    markdown_path.write_text(
        markdown,
        encoding="utf-8"
    )

    print(f"Markdown created: {markdown_path}")

    return markdown_path


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    pdf_files = list(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {PDF_FOLDER}"
        )

    for pdf_file in pdf_files:
        pdf_to_markdown(pdf_file)
