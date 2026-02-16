import streamlit as st
from generator import generate_answer

st.set_page_config(page_title="Reliable AI Assistant")
st.title("Reliable AI Assistant — Step 1")

question = st.text_input("Ask a question")

if st.button("Generate Answer"):
    if question.strip():
        with st.spinner("Generating..."):
            try:
                answer = generate_answer(question)
                st.subheader("AI Answer")
                st.write(answer)
            except Exception as e:
                st.error(str(e))
    else:
        st.warning("Please enter a question.")
