from flask import Flask, render_template, request
from rag.rag_pipeline import answer_question
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store the currently selected PDF
current_pdf = None


@app.route("/")
def home():
    return render_template(
        "index.html",
        pdf_uploaded=current_pdf is not None,
        pdf_name=os.path.basename(current_pdf) if current_pdf else None
    )


@app.route("/upload", methods=["POST"])
def upload():
    global current_pdf

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

    # Remember the uploaded PDF
    current_pdf = file_path

    return render_template(
        "index.html",
        message=f"PDF uploaded successfully: {pdf.filename}",
        pdf_uploaded=True,
        pdf_name=pdf.filename
    )


@app.route("/ask", methods=["POST"])
def ask():

    if not current_pdf:
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

    answer, source_pages = answer_question(
        question,
        current_pdf
    )

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        source_pages=source_pages,
        pdf_uploaded=True,
        pdf_name=os.path.basename(current_pdf)
    )


if __name__ == "__main__":
    app.run(debug=True)