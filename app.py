import streamlit as st
import json

from generator import generate_answer, revise_answer
from evaluator import evaluate_answer
from critic import critique_answer
from guardrails import apply_guardrails

# ---------------------------
# Page Setup
# ---------------------------
st.set_page_config(
    page_title="Honey Badger AI Assistant",
    layout="wide"
)

# ---------------------------
# Custom CSS Styling
# ---------------------------
st.markdown("""
<style>
.big-title {
    font-size:40px;
    font-weight:700;
    background: linear-gradient(90deg, #6C63FF, #00D4FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.card {
    padding:20px;
    border-radius:12px;
    background-color:#1A1F2E;
    margin-bottom:15px;
}
.score-good {
    color:#00FF9C;
    font-weight:bold;
    font-size:22px;
}
.score-bad {
    color:#FF4B4B;
    font-weight:bold;
    font-size:22px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown('<div class="big-title">Honey Badger AI</div>', unsafe_allow_html=True)
st.write("Debate-driven AI with evaluation and guardrails")

st.divider()

# ---------------------------
# Layout Columns
# ---------------------------
left, right = st.columns([2, 1])

with left:
    question = st.text_input("Ask a question")
    image_file = st.file_uploader(
        "Optional Image",
        type=["png", "jpg", "jpeg"]
    )
    generate_btn = st.button("Generate Answer")

with right:
    st.markdown("### System Status")
    st.success("Model: gemma3")
    st.info("Critic: Text-based")
    st.warning("Guardrails Active")

# ---------------------------
# Main Logic
# ---------------------------
if generate_btn:
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:
        # Round 1
        with st.spinner("Generating initial answer..."):
            answer_v1 = generate_answer(question, image_file)

        # Critic
        with st.spinner("Critic evaluating..."):
            critic_raw = critique_answer(question, answer_v1)

        try:
            critic_eval = json.loads(critic_raw)
            critic_score = critic_eval.get("score", 50)
            critic_reason = critic_eval.get("reason", "")
        except:
            critic_score = 50
            critic_reason = "Critic parsing failed."

        # Revision
        with st.spinner("Refining answer..."):
            answer_v2 = revise_answer(
                question,
                answer_v1,
                critic_reason
            )

        # Rule evaluation
        rule_eval = evaluate_answer(question, answer_v2)

        final_score = int(
            (rule_eval["score"] * 0.5) +
            (critic_score * 0.5)
        )

        decision = apply_guardrails({"score": final_score})

        st.divider()

        # ---------------------------
        # Score Display
        # ---------------------------
        if final_score >= 70:
            st.markdown(
                f'<div class="score-good">Confidence: {final_score}/100</div>',
                unsafe_allow_html=True
            )
            st.progress(final_score / 100)
        else:
            st.markdown(
                f'<div class="score-bad">Confidence: {final_score}/100</div>',
                unsafe_allow_html=True
            )
            st.progress(final_score / 100)

        st.divider()

        # ---------------------------
        # Output Card
        # ---------------------------
        if decision["approved"]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Final Answer")
            st.write(answer_v2)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Answer rejected by guardrails.")
            st.warning(decision["message"])

        # ---------------------------
        # Debug Expanders
        # ---------------------------
        with st.expander("Initial Answer (v1)"):
            st.write(answer_v1)

        with st.expander("Critic Feedback"):
            st.write(critic_reason)

        with st.expander("Rule Evaluation Details"):
            for r in rule_eval["reasons"]:
                st.write(f"- {r}")

    except Exception as e:
        st.error(str(e))
