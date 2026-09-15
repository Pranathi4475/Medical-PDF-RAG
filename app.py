from flask import Flask, render_template, request
from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.vector_store import create_vector_store, search_vector_store
from rag.llm import generate_answer
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store the currently selected PDF
current_pdf = None

# Store processed RAG data
chunks = None
index = None


@app.route("/")
def home():

    return render_template(
        "index.html",
        pdf_uploaded=current_pdf is not None,
        pdf_name=os.path.basename(current_pdf) if current_pdf else None
    )


@app.route("/upload", methods=["POST"])
def upload():

    global current_pdf, chunks, index

    pdf = request.files.get("pdf")

    if not pdf or pdf.filename == "":
        return render_template(
            "index.html",
            message="Please select a PDF file."
        )

    if not pdf.filename.lower().endswith(".pdf"):
        return render_template(
            "index.html",
            message="Only PDF files are allowed."
        )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        pdf.filename
    )

    pdf.save(file_path)

    current_pdf = file_path

    # -----------------------------
    # Process PDF only once
    # -----------------------------

    print("Processing PDF...")

    pages = extract_text_from_pdf(current_pdf)

    print("Creating chunks...")

    chunks = create_chunks(pages)

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Creating FAISS vector store...")

    index = create_vector_store(embeddings)

    print("PDF processing completed.")

    return render_template(
        "index.html",
        message=f"PDF uploaded and processed successfully: {pdf.filename}",
        pdf_uploaded=True,
        pdf_name=pdf.filename
    )


@app.route("/ask", methods=["POST"])
def ask():

    if not current_pdf or chunks is None or index is None:

        return render_template(
            "index.html",
            message="Please upload a PDF first."
        )

    question = request.form.get("question")

    if not question:

        return render_template(
            "index.html",
            message="Please enter a question.",
            pdf_uploaded=True,
            pdf_name=os.path.basename(current_pdf)
        )

    # -----------------------------
    # Create embedding for question
    # -----------------------------

    query_embedding = create_embeddings([
        {"text": question}
    ])

    # -----------------------------
    # Search FAISS
    # -----------------------------

    distances, indices = search_vector_store(
        index,
        query_embedding,
        top_k=8
    )

    # -----------------------------
    # Build context
    # -----------------------------

    context = ""

    source_pages = []

    for index_number in indices[0]:

        page_number = chunks[index_number]["page"]

        chunk_text = chunks[index_number]["text"]

        # Skip reference pages
        if page_number >= 80:
            continue

        context += (
            f"Page {page_number}:\n"
            f"{chunk_text}\n\n"
        )

        if page_number not in source_pages:

            source_pages.append(page_number)

        if len(source_pages) >= 5:

            break

    # -----------------------------
    # Generate answer
    # -----------------------------

    answer = generate_answer(
        question,
        context
    )

    return render_template(
       "index.html",
      question=question,
      answer=answer,
      source_pages=source_pages,
      retrieved_context=context,
      pdf_uploaded=True,
      pdf_name=os.path.basename(current_pdf)
    ) 


if __name__ == "__main__":

    app.run(debug=True)