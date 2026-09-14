from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.vector_store import create_vector_store, search_vector_store

pdf_path = "uploads/diabetes_guidelines.pdf"

# 1. Extract PDF text
pages = extract_text_from_pdf(pdf_path)

# 2. Create chunks
chunks = create_chunks(pages)

# 3. Create embeddings
embeddings = create_embeddings(chunks)

# 4. Create FAISS index
index = create_vector_store(embeddings)

# 5. User question
question = "What is diabetes?"

# 6. Convert question into embedding
query_embedding = create_embeddings([
    {"text": question}
])

# 7. Search for relevant chunks
distances, indices = search_vector_store(
    index,
    query_embedding,
    top_k=3
)

# 8. Display results
print("\nQUESTION:", question)

for i, index_number in enumerate(indices[0]):
    print("\nRESULT:", i + 1)
    print("PAGE:", chunks[index_number]["page"])
    print("DISTANCE:", distances[0][i])
    print("TEXT:")
    print(chunks[index_number]["text"])
    print("-" * 60)