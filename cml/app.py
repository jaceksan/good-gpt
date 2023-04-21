import streamlit as st
import openai
import os
from gpt import call_openapi, create_openapi_request, extract_code_block, supported_models
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    layout="wide", page_icon="favicon.ico", page_title="Streamlit-GPT demo"
)

# Page title
st.title("Chat with AI")

supported_models = supported_models()
model = st.selectbox(label="Models", options=supported_models, index=supported_models.index("gpt-3.5-turbo"))

# Text input box
text_input = st.text_area(
    "Enter your text here:", 
    value="""Create a Streamlit app:
    1. Input box (area) for larger texts
    2. Call ChatGPT, send the text from the input box.
    3. Display the result from the ChatGPT"""
)

# Button to send text to OpenAI
if st.button("Send"):
    print(f"{text_input=}")
    markdown_response = call_openapi(create_openapi_request(text_input), model)
    final_code = extract_code_block(markdown_response)

    st.markdown(markdown_response, unsafe_allow_html=True)
