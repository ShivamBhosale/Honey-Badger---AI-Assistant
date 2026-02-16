import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

def generate_answer(question: str) -> str:
    prompt = f"""
You are a precise and concise assistant.

Answer the question clearly.
If you do not know the answer, say:
"I do not have enough information."

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["message"]["content"]
