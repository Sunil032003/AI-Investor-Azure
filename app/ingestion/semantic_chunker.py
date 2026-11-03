from pathlib import Path
import json
import os

from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import AzureOpenAIEmbeddings


load_dotenv()


embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)


def semantic_chunk_markdown(md_path: Path):

    if not md_path.exists():
        raise FileNotFoundError(
            f"Markdown file not found: {md_path}"
        )

    text = md_path.read_text(
        encoding="utf-8"
    )

    if not text.strip():
        raise ValueError(
            f"Markdown file is empty: {md_path}"
        )

    chunker = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile"
    )

    chunks = chunker.split_text(text)

    print(f"File: {md_path.name}")
    print(f"Total chunks: {len(chunks)}")

    return chunks


if __name__ == "__main__":

    markdown_file = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "markdown"
        / "2024_Apple.md"
    )

    chunks = semantic_chunk_markdown(
        markdown_file
    )

    # Create chunks folder
    chunks_folder = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "chunks"
    )

    chunks_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save chunks
    output_file = (
        chunks_folder
        / "2024_Apple_chunks.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Chunks saved to: {output_file}"
    )