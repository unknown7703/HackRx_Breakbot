import os
from groq import Groq

client = Groq(
    api_key="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"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs",
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)