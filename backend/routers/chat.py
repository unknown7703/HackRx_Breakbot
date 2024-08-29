import os
from groq import Groq

from config import Settings

settings = Settings()
api_key = settings.groq_api_key

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=api_key)

def post_chat_query(query_string: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query_string,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


