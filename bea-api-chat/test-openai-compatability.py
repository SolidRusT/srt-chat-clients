import os
from openai import OpenAI

# get model from "/v1/models"
model = "cognitivecomputations/dolphin-2.6-mistral-7b-dpo-laser"
#model = "gpt-3.5-turbo"
openai_api_key = os.getenv('OPENAI_API_KEY')
#openai_api_base = "https://api.openai.com/v1"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

chat_response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ]
)
print("Chat response:", chat_response)
