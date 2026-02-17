import requests
import base64

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:latest"


def generate_answer(question: str, image_file=None) -> str:
    messages = []

    if image_file:
        # Convert image to base64
        image_bytes = image_file.read()
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        messages.append({
            "role": "user",
            "content": question,
            "images": [encoded_image]
        })
    else:
        messages.append({
            "role": "user",
            "content": question
        })

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        },
        timeout=180
    )

    response.raise_for_status()
    return response.json()["message"]["content"]


def revise_answer(question: str, original_answer: str, critique: str) -> str:
    prompt = f"""
You previously answered the question below.

Question:
{question}

Original Answer:
{original_answer}

Critique:
{critique}

Revise the answer to address the critique.
Be clearer, more specific, and more confident.
Return only the improved answer.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.3}
        },
        timeout=600
    )

    response.raise_for_status()
    return response.json()["message"]["content"]
