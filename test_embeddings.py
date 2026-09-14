from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings

pdf_path = "uploads/diabetes_guidelines.pdf"

pages = extract_text_from_pdf(pdf_path)

chunks = create_chunks(pages)

embeddings = create_embeddings(chunks)

print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)