import requests


def generate_answer(question, context):

    prompt = f"""
You are a medical document question-answering assistant.

Answer the user's question using ONLY the context provided below.

If the answer cannot be found in the context, say:

"The information was not found in the uploaded document."

Do not invent information.

Context:
{context}

Question:
{question}
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except Exception as e:

        print("OLLAMA ERROR:", repr(e))

        return (
            "Ollama is currently unavailable.\n\n"
            "Relevant information retrieved from the uploaded document:\n\n"
            + context
        )