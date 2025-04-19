import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個親切的LINE客服助理"},
            {"role": "user", "content": message}
        ]
    )
    return response["choices"][0]["message"]["content"]
