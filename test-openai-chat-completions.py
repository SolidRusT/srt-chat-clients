import openai

openai.api_key = "sk-not-required"
openai.base_url = "http://hades:5000/v1/"
openai.default_headers = {"x-foo": "true"}

completion = openai.chat.completions.create(
  model="not-required",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ],
  temperature=0.8,
  max_tokens=256,
  top_p=0.5,
  n=3,
  frequency_penalty=0.6,
  presence_penalty=0.8
)

print(completion.choices[0].message)
