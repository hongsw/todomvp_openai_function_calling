import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

messages = [{"role": "user", "content": "What's your api list?"}]

completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613", messages=messages)
print(completion)
