from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import create_chunks

pdf_path = "uploads/diabetes_guidelines.pdf"

pages = extract_text_from_pdf(pdf_path)

chunks = create_chunks(pages)

print("Total pages:", len(pages))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5]):
    print("\nCHUNK:", i + 1)
    print("PAGE:", chunk["page"])
    print(chunk["text"])
    print("-" * 50)