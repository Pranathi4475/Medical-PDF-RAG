# Medical PDF Question Answering using RAG

A Generative AI application that allows users to upload medical PDF documents and ask natural-language questions. The system retrieves relevant information from the uploaded document and generates an answer using Retrieval-Augmented Generation (RAG).

## Features

- Upload medical PDF documents
- Extract text from PDFs
- Split text into smaller chunks
- Generate embeddings for document chunks
- Store embeddings using FAISS
- Perform semantic search
- Generate answers using a local LLM
- Display source pages used for the answer
- Simple Flask web interface

## Technologies Used

- Python
- Flask
- PyMuPDF
- Sentence Transformers
- FAISS
- NumPy
- Ollama
- Llama 3.2
- HTML/CSS
- Retrieval-Augmented Generation (RAG)

## RAG Workflow

PDF Upload  
↓  
Text Extraction  
↓  
Text Chunking  
↓  
Embeddings  
↓  
FAISS Vector Database  
↓  
Semantic Search  
↓  
Relevant Context  
↓  
Llama 3.2  
↓  
Answer + Source Pages

## Project Structure

```text
Medical-PDF-RAG/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── rag/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── llm.py
│   └── rag_pipeline.py
│
├── templates/
│   └── index.html
│
└── test files