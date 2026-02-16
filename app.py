import streamlit as st
import json

from generator import generate_answer
from evaluator import evaluate_answer
from critic import critique_answer
from guardrails import apply_guardrails

st.set_page_config(page_title="Honey Badger AI Assistant")
st.title("Honey Badger AI Assistant")

question = st.text_input("Ask a question")

if st.button("Generate Answer"):
    if question.strip():
        try:
            # Generate
            answer = generate_answer(question)

            # Rule evaluation
            rule_eval = evaluate_answer(question, answer)

            # AI critic
            critic_raw = critique_answer(question, answer)

            try:
                critic_eval = json.loads(critic_raw)
                critic_score = critic_eval.get("score", 50)
                critic_reason = critic_eval.get("reason", "")
            except:
                critic_score = 50
                critic_reason = "Critic parsing failed."

            # Combine scores
            final_score = int((rule_eval["score"] * 0.5) + (critic_score * 0.5))

            decision = apply_guardrails({"score": final_score})

            st.subheader("Final Score")
            st.write(f"{final_score} / 100")

            if decision["approved"]:
                st.subheader("Approved Answer")
                st.write(answer)
            else:
                st.subheader("Answer Rejected")
                st.warning(decision["message"])

            st.subheader("Rule Evaluation")
            for r in rule_eval["reasons"]:
                st.write(f"- {r}")

            st.subheader("AI Critic Feedback")
            st.write(critic_reason)

        except Exception as e:
            st.error(str(e))
    else:
        st.warning("Please enter a question.")
