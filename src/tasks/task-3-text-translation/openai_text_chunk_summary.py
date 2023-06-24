import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv('.env')) # read local .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

def shorten_text_chunk(text):
    prompt = f"""
    Summarize the text delimited by triple backticks using fewer tokens.
    ```{text}```
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    new_text = response.choices[0].message["content"]
    return new_text

text_chunk_1 = "Koalas typically inhabit open Eucalyptus woodland, as the leaves of these trees make up most of their diet."

print(shorten_text_chunk(text_chunk_1))