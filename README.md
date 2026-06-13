# Gemini RAG Assistant

A simple Retrieval-Augmented Generation (RAG) application built using **Google Gemini**, **Sentence Transformers**, and **ChromaDB**.

This project allows users to upload PDF documents and ask natural language questions. The system retrieves the most relevant document chunks using semantic search and generates grounded answers using Gemini.

---

## Features

* PDF document ingestion
* Text cleaning and preprocessing
* Recursive text chunking
* Semantic embeddings using Sentence Transformers
* Vector storage with ChromaDB
* Retrieval-Augmented Generation (RAG)
* Google Gemini 2.5 Flash integration
* Source attribution for retrieved content
* Interactive command-line chat interface

---

## Architecture

```text
PDF Documents
      │
      ▼
Text Extraction (PyPDF2)
      │
      ▼
Text Cleaning
      │
      ▼
Chunking
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
Gemini 2.5 Flash
      │
      ▼
Grounded Answer
```

---

## Tech Stack

* Python 3.10+
* Google Gemini 2.5 Flash
* ChromaDB
* Sentence Transformers
* PyPDF2
* NumPy

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/gemini-rag-assistant.git

cd gemini-rag-assistant
```

Install dependencies:

```bash
pip install google-generativeai
pip install sentence-transformers
pip install chromadb
pip install pypdf2
pip install numpy
```

Or:

```bash
pip install -r requirements.txt
```

---

## Configuration

Open the Python file and update:

```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

PDF_PATH = r"C:\path\to\your\document.pdf"
```

Get a Gemini API key from:

https://aistudio.google.com/

---

## Running the Application

```bash
python rag_gemini.py
```

Example output:

```text
Loading PDF...
Loaded 3 pages

Creating chunks...
Created 12 chunks

Creating vector database...

RAG System Ready!
```

---

## Example Questions

### Policy Documents

```text
What is the remote work policy?

How many vacation days are employees entitled to?

What are the standard working hours?

Summarize the employee handbook.

What benefits are available to employees?
```

### Financial Reports

```text
What was the total revenue?

Summarize the annual report.

What are the key business highlights?

What are the major risks discussed in the report?

Who are the company's strategic partners?
```

---

## Project Structure

```text
gemini-rag-assistant/
│
├── rag_gemini.py
├── requirements.txt
├── README.md
└── sample_documents/
```

---

## How It Works

### Step 1: Load PDF

Documents are loaded page-by-page using PyPDF2.

### Step 2: Clean Text

Removes unwanted characters and normalizes whitespace.

### Step 3: Chunking

Splits large documents into smaller chunks for better retrieval.

### Step 4: Embeddings

Converts chunks into vector representations using:

```text
BAAI/bge-base-en-v1.5
```

or

```text
all-MiniLM-L6-v2
```

### Step 5: Vector Database

Stores embeddings and metadata in ChromaDB.

### Step 6: Retrieval

User queries are converted into embeddings and matched against stored vectors.

### Step 7: Generation

Retrieved context is passed to Gemini to generate grounded responses.

---

## Sample Query

```text
Ask Question: How many vacation days are employees entitled to?
```

Response:

```text
Employees receive 20 days of paid vacation annually.
```

Sources:

```text
Company_Policies.pdf (Page 2)
```

---

## Future Improvements

* Support multiple PDFs
* Web UI using Streamlit
* Conversational memory
* Hybrid search (BM25 + Vector Search)
* Metadata filtering
* Persistent ChromaDB storage
* Agentic RAG with Web Search
* LangChain integration

---

## License

MIT License

---

## Author

Built as a learning project for understanding:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Embeddings
* Semantic Search
* Google Gemini Integration
