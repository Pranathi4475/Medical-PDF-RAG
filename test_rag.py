from rag.rag_pipeline import answer_question

pdf_path = "uploads/diabetes_guidelines.pdf"

question = "What is diabetes?"

answer = answer_question(question, pdf_path)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)