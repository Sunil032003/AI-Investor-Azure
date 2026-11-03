import os

from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import AzureOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()


# ============================================================
# Azure OpenAI Configuration
# ============================================================

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


# ============================================================
# Pinecone Configuration
# ============================================================

PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY"
)

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME"
)


# ============================================================
# Validate Environment Variables
# ============================================================

required_variables = {
    "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
    "AZURE_OPENAI_API_KEY": AZURE_OPENAI_API_KEY,
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT": AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    "AZURE_OPENAI_API_VERSION": AZURE_OPENAI_API_VERSION,
    "PINECONE_API_KEY": PINECONE_API_KEY,
    "PINECONE_INDEX_NAME": PINECONE_INDEX_NAME,
}


for name, value in required_variables.items():

    if not value:
        raise ValueError(
            f"{name} is not set in the environment."
        )


# ============================================================
# Azure Embedding Model
# ============================================================

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION,
)


# ============================================================
# Pinecone
# ============================================================

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX_NAME
)


# ============================================================
# Vector Store
# ============================================================

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)


# ============================================================
# Targeted Retrieval
# ============================================================

def retrieve_documents(
    k: int = 3
):
    """
    Retrieve relevant chunks from Pinecone using
    multiple targeted financial queries.
    """

    queries = [

        "company name and fiscal year",

        "total revenue sales net sales",

        "net income net earnings",

        "operating income",

        "cash flow from operating activities operating cash flow",

        "total assets",

        "total liabilities",

        "risk factors risks uncertainties",

        "growth drivers business growth growth opportunities",

    ]


    retrieved_documents = []


    # --------------------------------------------------------
    # Search Pinecone for each query
    # --------------------------------------------------------

    for query in queries:

        documents = vector_store.similarity_search(
            query=query,
            k=k
        )

        retrieved_documents.extend(
            documents
        )


    # --------------------------------------------------------
    # Remove duplicate chunks
    # --------------------------------------------------------

    unique_documents = []

    seen_content = set()


    for document in retrieved_documents:

        content = document.page_content.strip()

        if not content:
            continue

        if content in seen_content:
            continue

        seen_content.add(content)

        unique_documents.append(
            document
        )


    return unique_documents


# ============================================================
# Test Retriever
# ============================================================

if __name__ == "__main__":

    print(
        "\nTesting targeted Pinecone retrieval..."
    )

    documents = retrieve_documents(
        k=3
    )

    print(
        f"\nTotal unique documents retrieved: "
        f"{len(documents)}"
    )

    for i, document in enumerate(
        documents,
        start=1
    ):

        print(
            "\n" + "=" * 80
        )

        print(
            f"Document {i}"
        )

        print(
            "=" * 80
        )

        print(
            document.page_content
        )

        print(
            "\nMetadata:"
        )

        print(
            document.metadata
        )