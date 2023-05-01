import openai
import os
import re
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
GPT_USER = "GoodGPT"
APPS_FOLDER = "apps"


@st.cache_data
def call_openapi(conversation: list[dict], model_engine: str = "gpt-3.5-turbo", temperature: int = 0) -> str:
    """Calls the OpenAI ChatGPT API

    Args:
        conversation (list[dict]): Conversation, optionally can contain the history
        model_engine (str, optional): Model engine to be used. Defaults to "gpt-3.5-turbo".
        temperature (int, optional): Temperature dictates the predicability of the responses. Defaults to 0.

    Returns:
        str: Response from the OpenAI API
    """
    response = openai.ChatCompletion.create(
        model=model_engine,
        temperature=temperature,
        messages=conversation
    )
    output_text = response['choices'][0]['message']['content']
    # print(f"ChatGPT API reply: {output_text}")
    return output_text


def create_simple_openapi_request_body(request: str, system_message: str) -> list[dict]:
    """Creates a simple request body for the OpenAI ChatGPT API

    Args:
        request (str): Request from the user
        system_message (str): System message, dictating the context of the request

    Returns:
        list[dict]: Request body for the OpenAI ChatGPT API
    """
    return [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": request
        },
    ]


def extract_code_block(markdown: str) -> str:
    """Extracts code blocks from a markdown string
    
    Args:
        markdown (str): Markdown string
    
    Returns:
        str: Code block
    """
    pattern = r"```[\w\s]*\n([\s\S]*?)\n```"
    code_blocks = re.findall(pattern, markdown)
    return next(iter(code_blocks))


@st.cache_data
def supported_models() -> list[str]:
    models = openai.Model.list()
    return [m["id"] for m in models["data"]]
