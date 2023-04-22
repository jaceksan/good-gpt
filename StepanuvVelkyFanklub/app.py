```python
import streamlit as st
from transformers import pipeline

st.title("ChatGPT App")

# Create input box for user to enter text
user_input = st.text_area("Enter your text here", height=200)

# Create ChatGPT pipeline
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Generate response using ChatGPT and display it
if st.button("Generate Response"):
    response = chatbot(user_input)[0]['generated_text']
    st.write(response)
```