import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

# List the available models
models = openai.Model.list()

# Print the names of the models
for model in models["data"]:
    print(model["id"])
