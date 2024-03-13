import os
import openai
import requests

# Load API keys from environment variables
bea_api_key = os.getenv('BEA_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

if not bea_api_key or not openai_api_key:
    print("One or more API keys are missing.")
    exit(1)

openai.api_key = openai_api_key
