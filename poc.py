import openai
import os
import re

openai.api_key = os.environ["OPENAI_API_KEY"]

model_engine = "gpt-3.5-turbo"
# model_engine = "code-davinci-002"


def call_openapi(conversation):
    return openai.ChatCompletion.create(
        model=model_engine,
        temperature=0,
        messages=conversation
    )

with open("design.txt") as fp:
    design = fp.read()

messages = [
    {"role": "system", "content": "You are a Python developer. Return only pure code, no explanation text."},
    {
        "role": "user",
        "content": design
    },
    # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    # {"role": "user", "content": "Where was it played?"}
]

response = call_openapi(messages)
output_text = response['choices'][0]['message']['content']
print("ChatGPT API reply:", output_text)


def extract_code_blocks(markdown):
    """Extracts code blocks from a markdown string"""
    pattern = r"```[\w\s]*\n([\s\S]*?)\n```"
    code_blocks = re.findall(pattern, markdown)
    return code_blocks


final_code = next(iter(extract_code_blocks(output_text)))
if final_code:
    with open("solution.py", "w") as fp:
        fp.write(final_code)
else:
    raise Exception("Response does not contain any code block!")

messages.append(
    {"role": "assistant", "content": "It must return Integer! Please, fix it."}
)
response = call_openapi(messages)
output_text = response['choices'][0]['message']['content']
print("ChatGPT API reply:", output_text)

final_code = next(iter(extract_code_blocks(output_text)))
if final_code:
    with open("solution2.py", "w") as fp:
        fp.write(final_code)
else:
    raise Exception("Response does not contain any code block!")
