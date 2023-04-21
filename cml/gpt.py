import openai
import os
import re

openai.api_key = os.environ["OPENAI_API_KEY"]

model_engine = "gpt-3.5-turbo"
# model_engine = "code-davinci-002"

def call_openapi(conversation):
    response = openai.ChatCompletion.create(
        model=model_engine,
        temperature=0,
        messages=conversation
    )
    output_text = response['choices'][0]['message']['content']
    print(f"ChatGPT API reply: {output_text}")
    return output_text

def create_openapi_request(content):
    return [
        {"role": "system", "content": "You are a Python developer. Return only pure code, no explanation text."},
        {
            "role": "user",
            "content": content
        },
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        # {"role": "user", "content": "Where was it played?"}
    ]

def extract_code_block(markdown):
    """Extracts code blocks from a markdown string"""
    pattern = r"```[\w\s]*\n([\s\S]*?)\n```"
    code_blocks = re.findall(pattern, markdown)
    return next(iter(code_blocks))
