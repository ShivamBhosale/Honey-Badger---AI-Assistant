import re

HALLUCINATION_PHRASES = [
    "generally",
    "usually",
    "it is believed",
    "often",
    "in many cases",
    "typically",
    "as an ai",
    "i think",
]

def evaluate_answer(question: str, answer: str) -> dict:
    score = 100
    reasons = []

    # 1. Empty or too short
    if len(answer.strip()) < 20:
        score -= 30
        reasons.append("Answer is too short")

    # 2. Very long answers (rambling)
    if len(answer) > 600:
        score -= 20
        reasons.append("Answer is too long")

    # 3. Hallucination phrases
    lower_answer = answer.lower()
    for phrase in HALLUCINATION_PHRASES:
        if phrase in lower_answer:
            score -= 15
            reasons.append(f"Contains vague phrase: '{phrase}'")

    # 4. Question keywords missing
    question_keywords = [
        word for word in re.findall(r"\w+", question.lower())
        if len(word) > 3
    ]

    matched = any(word in lower_answer for word in question_keywords)
    if not matched:
        score -= 25
        reasons.append("Answer may not address the question")

    # Clamp score
    score = max(score, 0)

    return {
        "score": score,
        "reasons": reasons if reasons else ["Answer looks acceptable"]
    }
