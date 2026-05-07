import os

from dotenv import load_dotenv
from openai import OpenAI
from config import Config

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(messages):

    response = client.chat.completions.create(model=Config.OPENAI_MODEL, messages=messages)

    return response.choices[0].message.content