```python
import streamlit as st
from transformers import pipeline

st.title("ChatGPT App")

# Create an input box for user to enter text
user_input = st.text_area("Enter your text here", height=200)

# Create a ChatGPT pipeline
chatbot = pipeline("text2text-generation", model="microsoft/DialoGPT-medium")

# Generate response using ChatGPT
if st.button("Generate Response"):
    response = chatbot(user_input)[0]['generated_text']
    st.write(response)
```