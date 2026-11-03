import os
import json
from pathlib import Path

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import AzureOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()


# Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT"
)

AZURE_OPENAI_API_KEY = os.getenv(
    "AZURE_OPENAI_API_KEY"
)

AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
)

AZURE_OPENAI_API_VERSION = os.getenv(
    "AZURE_OPENAI_API_VERSION"
)


# Pinecone
PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY"
)

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME"
)


# Azure embedding model
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION,
)


# Connect to Pinecone
pc = Pinecone(
    api_key=PINECONE_API_KEY
)


# Create index if it doesn't exist
if not pc.has_index(PINECONE_INDEX_NAME):

    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )


# Get index
index = pc.Index(
    PINECONE_INDEX_NAME
)


# Create vector store
vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)


if __name__ == "__main__":

    # Path to saved chunks
    chunks_file = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "chunks"
        / "2024_Apple_chunks.json"
    )

    if not chunks_file.exists():

        raise FileNotFoundError(
            f"Chunks file not found: {chunks_file}"
        )


    # Read chunks
    with open(
        chunks_file,
        "r",
        encoding="utf-8"
    ) as file:

        chunks = json.load(file)


    print(
        f"Total chunks loaded: {len(chunks)}"
    )


    # Store chunks in Pinecone
    vector_store.add_texts(
        texts=chunks,
        metadatas=[
            {
                "source": "2024_Apple.md",
                "chunk_id": i
            }
            for i in range(len(chunks))
        ]
    )


    print(
        "Embeddings created and stored in Pinecone successfully."
    )