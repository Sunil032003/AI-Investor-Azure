from pathlib import Path
import pymupdf4llm


PDF_FOLDER = Path("data")
OUTPUT_FOLDER = Path("data/markdown")


if not PDF_FOLDER.exists():
    raise FileNotFoundError(f"PDF folder not found: {PDF_FOLDER}")


OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


pdf_files = list(PDF_FOLDER.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError(f"No PDF files found in: {PDF_FOLDER}")


for pdf_file in pdf_files:
    print(f"Converting: {pdf_file.name}")

    markdown = pymupdf4llm.to_markdown(pdf_file)

    output_file = OUTPUT_FOLDER / f"{pdf_file.stem}.md"
    output_file.write_text(markdown, encoding="utf-8")

    print(f"Saved: {output_file}")


print("PDF to Markdown conversion completed.")