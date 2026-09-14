from rag.pdf_loader import extract_text_from_pdf

pdf_path = "uploads/diabetes_guidelines.pdf"

pages = extract_text_from_pdf(pdf_path)

for page in pages:

    print("PAGE:", page["page"])
    print(page["text"])
    print("-" * 50)