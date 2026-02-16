def apply_guardrails(evaluation: dict, threshold: int = 70) -> dict:
    score = evaluation["score"]

    if score >= threshold:
        return {
            "approved": True,
            "message": "Answer approved."
        }

    return {
        "approved": False,
        "message": "I'm not confident enough to provide a reliable answer."
    }
