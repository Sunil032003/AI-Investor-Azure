import os
import json

from dotenv import load_dotenv
from openai import AzureOpenAI
from pydantic import BaseModel, Field

from app.rag_system.retrival import retrieve_documents
from database.insert_data import insert_investor_data


# ============================================================
# Load Environment Variables
# ============================================================

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

AZURE_OPENAI_API_VERSION = os.getenv(
    "AZURE_OPENAI_API_VERSION"
)

AZURE_OPENAI_LLM_MODEL = os.getenv(
    "AZURE_OPENAI_LLM_MODEL"
)


# ============================================================
# Validate Environment Variables
# ============================================================

if not AZURE_OPENAI_ENDPOINT:
    raise ValueError(
        "AZURE_OPENAI_ENDPOINT is not set."
    )

if not AZURE_OPENAI_API_KEY:
    raise ValueError(
        "AZURE_OPENAI_API_KEY is not set."
    )

if not AZURE_OPENAI_API_VERSION:
    raise ValueError(
        "AZURE_OPENAI_API_VERSION is not set."
    )

if not AZURE_OPENAI_LLM_MODEL:
    raise ValueError(
        "AZURE_OPENAI_LLM_MODEL is not set."
    )


# ============================================================
# Azure OpenAI Client
# ============================================================

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
)


# ============================================================
# Financial Output Schema
# ============================================================

class FinancialMetrics(BaseModel):

    company: str | None = Field(
        default=None,
        description="Company name mentioned in the document."
    )

    fiscal_year: str | None = Field(
        default=None,
        description="Fiscal year mentioned in the document."
    )

    revenue: str | None = Field(
        default=None,
        description="Company revenue."
    )

    net_income: str | None = Field(
        default=None,
        description="Company net income."
    )

    operating_income: str | None = Field(
        default=None,
        description="Company operating income."
    )

    operating_cash_flow: str | None = Field(
        default=None,
        description="Cash flow from operating activities."
    )

    total_assets: str | None = Field(
        default=None,
        description="Company total assets."
    )

    total_liabilities: str | None = Field(
        default=None,
        description="Company total liabilities."
    )

    risk_factors: list[str] = Field(
        default_factory=list,
        description="Important risk factors mentioned in the report."
    )

    growth_drivers: list[str] = Field(
        default_factory=list,
        description="Important growth drivers mentioned in the report."
    )


# ============================================================
# Extract Financial Information
# ============================================================

def extract_financial_metrics(
    context: str
) -> FinancialMetrics:

    prompt = f"""
You are given retrieved sections from a company's financial document.

Your task is to extract financial information ONLY from the
provided document context.

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

Extract the following information:

1. Company name
2. Fiscal year
3. Revenue
4. Net income
5. Operating income
6. Operating cash flow
7. Total assets
8. Total liabilities
9. Important risk factors
10. Important growth drivers

IMPORTANT RULES:

- Use ONLY the information available in the provided context.
- Do NOT use outside knowledge.
- Do NOT guess or invent information.
- If a value is not available, return null.
- Keep financial values exactly as stated in the document.
- Extract the fiscal year from the document.
- Extract the company name from the document.
- Risk factors should be concise.
- Growth drivers should be concise.
- Return the information according to the required schema.
"""

    completion = client.beta.chat.completions.parse(

        model=AZURE_OPENAI_LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert financial analyst. "
                    "Extract financial information accurately "
                    "from the provided document context. "
                    "Never invent information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        response_format=FinancialMetrics,
    )

    message = completion.choices[0].message

    # --------------------------------------------------------
    # Check for refusal
    # --------------------------------------------------------

    if message.refusal:

        raise RuntimeError(
            f"Azure OpenAI refused the request: "
            f"{message.refusal}"
        )

    # --------------------------------------------------------
    # Check structured output
    # --------------------------------------------------------

    if message.parsed is None:

        raise RuntimeError(
            "Azure OpenAI did not return structured output."
        )

    return message.parsed


# ============================================================
# Analyze Document
# ============================================================

def analyze_document():

    print(
        "\nSearching Pinecone for financial information..."
    )

    # --------------------------------------------------------
    # Retrieve relevant chunks from Pinecone
    # --------------------------------------------------------

    documents = retrieve_documents(
        k=3
    )

    if not documents:

        raise RuntimeError(
            "No relevant documents were retrieved from Pinecone."
        )

    print(
        f"Retrieved {len(documents)} unique documents."
    )

    # --------------------------------------------------------
    # Combine retrieved chunks
    # --------------------------------------------------------

    context_parts = []

    for i, document in enumerate(
        documents,
        start=1
    ):

        context_parts.append(
            f"""
--- Retrieved Document {i} ---

{document.page_content}
"""
        )

    context = "\n".join(
        context_parts
    )

    # --------------------------------------------------------
    # Extract financial information
    # --------------------------------------------------------

    print(
        "\nExtracting financial information using Azure OpenAI..."
    )

    financial_data = extract_financial_metrics(
        context=context
    )

    # --------------------------------------------------------
    # Save financial information to PostgreSQL
    # --------------------------------------------------------

    print(
        "\nSaving financial information to PostgreSQL..."
    )

    insert_investor_data(
        financial_data
    )

    return financial_data


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print(
        "\nStarting AI Investor Intelligence..."
    )

    try:

        financial_data = analyze_document()

        # ----------------------------------------------------
        # Display extracted information
        # ----------------------------------------------------

        print(
            "\nExtracted Financial Information"
        )

        print(
            "=" * 60
        )

        print(
            json.dumps(
                financial_data.model_dump(),
                indent=4,
                ensure_ascii=False
            )
        )

    except Exception as error:

        print(
            "\nError:"
        )

        print(error)