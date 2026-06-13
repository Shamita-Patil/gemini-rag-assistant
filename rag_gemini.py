import os
import re
import uuid
import PyPDF2
import chromadb
import google.generativeai as genai

from sentence_transformers import SentenceTransformer
from config import GEMINI_API_KEY

# ============================================================
# CONFIGURATION
# ============================================================

#GEMINI_API_KEY = ""

PDF_PATH = r"C:\Users\YourName\Desktop\sample.pdf"
CHUNK_SIZE = 500
TOP_K = 3

# ============================================================
# GEMINI SETUP
# ============================================================

genai.configure(api_key=GEMINI_API_KEY)

llm = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)

# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ============================================================
# LOAD PDF
# ============================================================

def load_pdf(pdf_path):

    documents = []

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page_num, page in enumerate(reader.pages):

            text = page.extract_text()

            if text:

                documents.append(
                    {
                        "content": text,
                        "metadata": {
                            "source": os.path.basename(pdf_path),
                            "page": page_num + 1
                        }
                    }
                )

    return documents

# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    text = text.encode(
        "utf-8",
        errors="ignore"
    ).decode("utf-8")

    text = re.sub(r"\s+", " ", text)

    text = re.sub(
        r"[^a-zA-Z0-9\s.,\-']",
        "",
        text
    )

    return text.strip().lower()

# ============================================================
# RECURSIVE CHUNKING
# ============================================================

def recursive_chunk(
        text,
        chunk_size=500,
        delimiters=[". ", "\n", " "]
):

    if len(text) <= chunk_size:
        return [text]

    for delimiter in delimiters:

        if delimiter in text:

            parts = text.split(delimiter)

            chunks = []
            current_chunk = ""

            for part in parts:

                candidate = (
                    current_chunk +
                    delimiter +
                    part
                ) if current_chunk else part

                if len(candidate) <= chunk_size:

                    current_chunk = candidate

                else:

                    if current_chunk:
                        chunks.append(current_chunk)

                    current_chunk = part

            if current_chunk:
                chunks.append(current_chunk)

            return chunks

    return [
        text[i:i + chunk_size]
        for i in range(
            0,
            len(text),
            chunk_size
        )
    ]

# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(documents):

    chunks = []

    for doc in documents:

        text = clean_text(doc["content"])

        split_chunks = recursive_chunk(
            text,
            chunk_size=CHUNK_SIZE
        )

        for chunk in split_chunks:

            chunks.append(
                {
                    "id": str(uuid.uuid4()),
                    "content": chunk,
                    "metadata": doc["metadata"]
                }
            )

    return chunks

# ============================================================
# EMBEDDINGS
# ============================================================

def get_embeddings(texts):

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings.tolist()

# ============================================================
# CHROMADB
# ============================================================

def create_vector_store(chunks):

    client = chromadb.Client()

    collection = client.create_collection(
        name="rag_collection"
    )

    documents = [
        c["content"]
        for c in chunks
    ]

    ids = [
        c["id"]
        for c in chunks
    ]

    metadatas = [
        c["metadata"]
        for c in chunks
    ]

    embeddings = get_embeddings(
        documents
    )

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return collection

# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(
        query,
        collection,
        top_k=3
):

    query_embedding = get_embeddings(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    return results

# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(
        query,
        retrieved_docs,
        retrieved_metadata
):

    context = ""

    for i, (
            doc,
            metadata
    ) in enumerate(
        zip(
            retrieved_docs,
            retrieved_metadata
        ),
        start=1
    ):

        source = metadata.get(
            "source",
            "Unknown"
        )

        page = metadata.get(
            "page",
            "-"
        )

        context += f"""
Document {i}
Source: {source}
Page: {page}

{doc}

"""

    prompt = f"""
You are a helpful document assistant.

Answer ONLY from the supplied context.

If the answer is not available,
reply exactly:

I don't have enough information to answer this.

CONTEXT:

{context}

QUESTION:

{query}
"""

    return prompt

# ============================================================
# GEMINI ANSWER
# ============================================================

def ask_gemini(
        query,
        collection
):

    results = retrieve(
        query,
        collection,
        TOP_K
    )

    docs = results["documents"][0]

    metadata = results["metadatas"][0]

    prompt = build_prompt(
        query,
        docs,
        metadata
    )

    response = llm.generate_content(
        prompt
    )

    return {
        "answer": response.text,
        "sources": metadata
    }

# ============================================================
# BUILD PIPELINE
# ============================================================

print("\nLoading PDF...")

documents = load_pdf(
    PDF_PATH
)

print(
    f"Loaded {len(documents)} pages"
)

print(
    "Creating chunks..."
)

chunks = create_chunks(
    documents
)

print(
    f"Created {len(chunks)} chunks"
)

print(
    "Creating vector database..."
)

collection = create_vector_store(
    chunks
)

print(
    "RAG System Ready!"
)

# ============================================================
# CHAT LOOP
# ============================================================

while True:

    query = input(
        "\nAsk Question (type exit): "
    )

    if query.lower() == "exit":
        break

    result = ask_gemini(
        query,
        collection
    )

    print("\nAnswer:\n")

    print(
        result["answer"]
    )

    print("\nSources:")

    for source in result["sources"]:

        print(
            f"- {source.get('source')} "
            f"(Page {source.get('page')})"
        )