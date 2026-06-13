# Gemini RAG Assistant

A Retrieval-Augmented Generation (RAG) application that enables users to ask questions about PDF documents using Google's Gemini model. The system retrieves relevant information from the uploaded document using semantic search and generates grounded answers with source references.

## What This Project Does

* Extracts text from PDF documents
* Splits content into searchable chunks
* Generates semantic embeddings using Sentence Transformers
* Stores embeddings in ChromaDB
* Retrieves the most relevant document sections for a user query
* Uses Google Gemini to generate context-aware answers
* Provides source references for transparency
* Reduces hallucinations by answering only from document content

---

## Technologies Used

* Python
* Google Gemini 2.5 Flash
* ChromaDB
* Sentence Transformers
* PyPDF2
* NumPy
* Python Dotenv

---

## Architecture

```text
PDF Document
     │
     ▼
Text Extraction (PyPDF2)
     │
     ▼
Document Chunking
     │
     ▼
Embeddings (Sentence Transformers)
     │
     ▼
ChromaDB Vector Store
     │
     ▼
Semantic Retrieval
     │
     ▼
Google Gemini
     │
     ▼
Answer + Source References
```

---

## Key Features

* PDF Question Answering
* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Source Attribution
* Hallucination Prevention
* Local Vector Database
* Google Gemini Integration
* Easy-to-Use Command Line Interface

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/gemini-rag-assistant.git

cd gemini-rag-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Update the PDF path in the code:

```python
PDF_PATH = r"ADD_YOUR_PDF_FILE_PATH_HERE"
```

Example:

```python
PDF_PATH = r"C:\Users\John\Documents\sample.pdf"
```

---

## How to Run

```bash
python rag_gemini.py
```

Example:

```text
Ask Question (type exit):
```

---

## Sample Questions

```text
What is Novatech's refund policy?

Is free shipping available?

What warranty covers?

Summarize the document.

What are the return conditions?
```

---

## Sample Output

### Question

```text
Ask Question (type exit): What warranty covers?
```

### Answer

```text
The warranty covers manufacturing defects,
hardware failures, hardware malfunctions,
and faulty components.

Sources:
- Novatech_Company_Policies.pdf (Page 2)
- Novatech_Company_Policies.pdf (Page 1)
```

### Hallucination Prevention Example

```text
Ask Question (type exit): Give me the customer email support and toll free number
```

```text
I don't have enough information to answer this.

Sources:
- Novatech_Company_Policies.pdf (Page 2)
- Novatech_Company_Policies.pdf (Page 3)
```

---

## Future Enhancements

* Multi-PDF Support
* Streamlit Web Interface
* Conversational Memory
* Hybrid Search (Keyword + Vector Search)
* Agentic RAG with Web Search
* LangChain Integration

---

## Author

Built to learn and demonstrate:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Embeddings
* Google Gemini Integration
* AI Application Development
