import streamlit as st
from generator import generate_answer
from evaluator import evaluate_answer
from guardrails import apply_guardrails

st.set_page_config(page_title="Honey Badger AI Assistant")
st.title("Honey Badger AI Assistant")

question = st.text_input("Ask a question")

if st.button("Generate Answer"):
    if question.strip():
        with st.spinner("Generating answer..."):
            try:
                answer = generate_answer(question)
                evaluation = evaluate_answer(question, answer)
                decision = apply_guardrails(evaluation)

                st.subheader("Evaluation Score")
                st.write(f"{evaluation['score']} / 100")

                if decision["approved"]:
                    st.subheader("Approved Answer")
                    st.write(answer)
                else:
                    st.subheader("Answer Rejected")
                    st.warning(decision["message"])

                st.subheader("Evaluation Details")
                for reason in evaluation["reasons"]:
                    st.write(f"- {reason}")

            except Exception as e:
                st.error(str(e))
    else:
        st.warning("Please enter a question.")
