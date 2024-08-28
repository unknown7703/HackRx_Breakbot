import os

from groq import Groq
#os.environ['GROQ_API_KEY']
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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


