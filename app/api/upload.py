
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.pdf_to_markdown import pdf_to_markdown


router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)


# ============================================================
# Directory Configuration
# ============================================================

APP_DIR = Path(__file__).resolve().parents[1]

UPLOAD_FOLDER = APP_DIR / "data" / "pdfs"

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Upload PDF + Convert to Markdown
# ============================================================

@router.post("/")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    if Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file."
        )

    file_path = (
        UPLOAD_FOLDER / Path(file.filename).name
    )

    if file_path.exists():
        raise HTTPException(
            status_code=409,
            detail="A file with this name already exists."
        )

    try:

        # Save uploaded PDF
        file_path.write_bytes(content)

        print(f"PDF uploaded: {file_path}")

        # Convert PDF to Markdown
        markdown_path = pdf_to_markdown(
            file_path
        )

        return {
            "message": "PDF uploaded and converted successfully.",
            "filename": file.filename,
            "pdf_path": str(file_path),
            "markdown_path": str(markdown_path)
        }

    except Exception as error:

        # Remove incomplete upload if processing fails
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
