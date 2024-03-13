import os
import requests

# Load API keys from environment variables
bea_api_key = os.getenv('BEA_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_url = os.getenv('OPENAI_API_URL', 'https://api.openai.com')

if not bea_api_key or not openai_api_key:
    print("One or more API keys are missing.")
    exit(1)

headers = {"Authorization": f"Bearer {openai_api_key}"}

def query_openai(question):
    try:
        response = requests.post(
            f"{openai_api_url}/v1/chat/completions",
            headers=headers,
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": question}
                ],
            },
        )
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        print(f"Failed to query OpenAI: {str(e)}")
        return None

def fetch_bea_data(dataset, parameters):
    pass

def format_response(data):
    pass

def main():
    user_question = input("Please enter your question: ")
    try:
        response = query_openai(user_question)
        if response:
            print(f"Response: {response}")
        else:
            print("No response from OpenAI.")
    except TypeError as e:
        print("Error processing OpenAI response:", str(e))

if __name__ == "__main__":
    main()
