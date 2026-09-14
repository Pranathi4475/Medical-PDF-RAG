from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.vector_store import create_vector_store, search_vector_store
from rag.llm import generate_answer


def answer_question(question, pdf_path):

    # 1. Extract PDF text
    pages = extract_text_from_pdf(pdf_path)

    # 2. Create chunks
    chunks = create_chunks(pages)

    # 3. Create embeddings
    embeddings = create_embeddings(chunks)

    # 4. Create vector store
    index = create_vector_store(embeddings)

    # 5. Create question embedding
    query_embedding = create_embeddings([
        {"text": question}
    ])

    # 6. Retrieve more results
    distances, indices = search_vector_store(
        index,
        query_embedding,
        top_k=8
    )

    # 7. Build context
    context = ""
    source_pages = []

    for i, index_number in enumerate(indices[0]):

        page_number = chunks[index_number]["page"]
        chunk_text = chunks[index_number]["text"]

        # Skip reference/search-strategy pages
        if page_number >= 80:
            continue

        context += (
            f"Page {page_number}:\n"
            f"{chunk_text}\n\n"
        )

        if page_number not in source_pages:
            source_pages.append(page_number)

        # Keep only the best 5 useful chunks
        if len(source_pages) >= 5:
            break

    # 8. Generate answer
    answer = generate_answer(question, context)

    return answer, source_pages