import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

def critique_answer(question: str, answer: str) -> dict:
    prompt = f"""
You are an AI evaluator.

Evaluate the following answer to the question.

Question:
{question}

Answer:
{answer}

Rate the answer from 0 to 100 based on:
- Relevance
- Specificity
- Clarity
- Confidence

Respond ONLY in this JSON format:

{{
    "score": <number>,
    "reason": "<short explanation>"
}}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.2}
        },
        timeout=120
    )

    response.raise_for_status()

    try:
        return response.json()["message"]["content"]
    except:
        return '{"score": 50, "reason": "Critic failed to evaluate properly."}'
