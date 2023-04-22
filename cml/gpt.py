import openai
import os
import re
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]


@st.cache_data
def call_openapi(conversation: list[dict], model_engine: str = "gpt-3.5-turbo") -> str:
    response = openai.ChatCompletion.create(
        model=model_engine,
        temperature=0,
        messages=conversation
    )
    output_text = response['choices'][0]['message']['content']
    print(f"ChatGPT API reply: {output_text}")
    return output_text


def create_openapi_request(content: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a Python developer. Return only pure code, no explanation text. Return as markdown code block."},
        {
            "role": "user",
            "content": content
        },
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        # {"role": "user", "content": "Where was it played?"}
    ]

def create_openapi_redo_request(content: str, code_context: str, pr_comment: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a Python developer. Return only pure code, no explanation text. Return as markdown code block."},
        {
            "role": "user",
            "content": content
        },
        {
            "role": "assistant",
            "content": code_context
         },
        {
            "role": "user",
            "content": pr_comment
        }
    ]



def create_openapi_PR_comment_request(content: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a Python developer. You are expert at code review."},
        {
            "role": "user",
            "content": "Please review this code:" + content
        },
    ]


def extract_code_block(markdown: str) -> str:
    """Extracts code blocks from a markdown string"""
    pattern = r"```[\w\s]*\n([\s\S]*?)\n```"
    code_blocks = re.findall(pattern, markdown)
    return next(iter(code_blocks))


@st.cache_data
def supported_models() -> list[str]:
    models = openai.Model.list()
    return [m["id"] for m in models["data"]]
