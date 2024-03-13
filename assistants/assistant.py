import openai
import os
from config_loader import load_config, load_environment

config = load_config("config.yaml")
env_vars = load_environment()

openai_api_key = config["openai_api_key"]
model = config["open_ai_model"]

client = openai.OpenAI(api_key=openai_api_key)

# Create personalized assistant
#personal_assistant = client.beta.assistants.create(
#  name="My Personal Assistant",
#  instructions="""I need help with my homework. """,
#  model=model
#)
#assistant_id = personal_assistant.id
assistant_id = "asst_cvQHBH6vyRN6P6zI7zYAoGIZ"
#print(assistant.id)

# Thread: assistants/assistant.py
#thread = client.beta.threads.create(
#  messages = [
#    {
#      "role": "user",
#      "content": "I need help with my homework."
#    }
#  ]
#)
#thread_id = thread.id
thread_id = "thread_sP6ebyzIODKSnSAPlgnaquVg"
#print(thread_id)

# Create a message
message = "I need help with my homework."
message = client.beta.threads.messages.create(
  thread_id=thread_id,
  content=message,
  role="user"
)

# Run the assistant
run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id,
  model=model,
  instructions="I need help with my homework."
)
