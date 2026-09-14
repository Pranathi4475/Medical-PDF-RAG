from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.vector_store import create_vector_store

pdf_path = "uploads/diabetes_guidelines.pdf"

pages = extract_text_from_pdf(pdf_path)

chunks = create_chunks(pages)

embeddings = create_embeddings(chunks)

index = create_vector_store(embeddings)

print("Total chunks:", len(chunks))
print("Vector dimension:", index.d)
print("Vectors stored:", index.ntotal)