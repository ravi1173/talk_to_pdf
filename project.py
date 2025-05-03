from google import genai
import streamlit as st
import os
from helper_functions import extract_text
from dotenv import load_dotenv

load_dotenv()  

GEMINI_KEY = os.getenv('GEMINI_KEY')

# client = genai.Client(api_key=GEMINI_KEY)
client = genai.Client(api_key='AIzaSyAvbfPeC8Be4dMTN732tz16plRQ-Z4Rc7Y')

st.set_page_config(page_title="PDF Chatbot", layout="wide")
st.title("Chat with Your PDF")


if "messages" not in st.session_state:
    st.session_state.messages = []


col1, col2 = st.columns(2)


with col1:
    st.markdown("<div style='height:25vh'></div>", unsafe_allow_html=True)  # top spacer
    pdf_file = st.file_uploader("Upload File", type="pdf")
    st.markdown("<div style='height:25vh'></div>", unsafe_allow_html=True)  # bottom spacer



with col2:
    document_text = ""
    if pdf_file is not None:
        document_text = extract_text(pdf_file)


    if document_text:
        user_input = st.chat_input("Ask a question about your PDF")


        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                response = client.models.generate_content(
                                                model="gemini-2.0-flash", contents=f"Document:\n{document_text}\n\nQuestion: {user_input}"
                                            )
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})


