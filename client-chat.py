import yaml
import os
import logging
import random
import time
from huggingface_hub import InferenceClient
from prompt_formatters import formatters
import gradio as gr
import requests

# Load configuration
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

debug = False

# Environment variables and configuration
persona_name = os.environ.get("PERSONA", "Default")
server_port = int(os.environ.get("PORT", 8650))
server_name = os.environ.get("SERVER_NAME", "0.0.0.0")
tgi_urls = os.environ.get("TGI_URLS", "tgi_default_urls")

ui_theme = config["personas"][persona_name]["theme"]
persona_full_name = config["personas"][persona_name]["name"]
app_title = config["personas"][persona_name]["title"]
persona_avatar_image = f"images/{config['personas'][persona_name]['avatar']}"
description = config["personas"][persona_name]["description"]
system_message = config["personas"][persona_name]["system_message"]
persona = config["personas"][persona_name]["persona"]
chat_examples = config["personas"][persona_name]["topic_examples"]
temperature = config["personas"][persona_name]["temperature"]
preferences = config["personas"][persona_name]["preferences"] # this should go into persona

# Logging configuration
log_level = logging.DEBUG if debug else logging.INFO
logs_path = config["logs_path"]
if not os.path.exists(logs_path):
    os.makedirs(logs_path)
logging.basicConfig(
    filename=logs_path + "/client-chat-" + persona_full_name + ".log",
    level=log_level,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


# Cache for model parameters to avoid repeated fetches
model_parameters_cache = {}


def fetch_model_info(llm):
    if llm in model_parameters_cache:
        return model_parameters_cache[llm]
    try:
        response = requests.get(f"{llm}/info")
        if response.status_code == 200:
            model_info = response.json()
            model_parameters_cache[llm] = model_info
            return model_info
        else:
            logging.error(
                f"Failed to fetch model info for {llm}: HTTP {response.status_code}"
            )
    except Exception as e:
        logging.error(f"Error fetching model info for {llm}: {str(e)}")
    return {"max_input_length": 1024, "max_total_tokens": 4096}


def inference(message, history):
    timestamp = current_timestamp()
    llms = random.choice(config[tgi_urls])
    llm = llms["url"]
    model_info = fetch_model_info(llm)

    max_input_length = model_info.get("max_input_length", 1024)
    max_total_tokens = model_info.get("max_total_tokens", 4096)

    prompt_type = llms["type"]
    max_new_tokens = llms["max_tokens"]

    # Simplified for demonstration: trim history based on max_input_length
    # Real implementation would adjust based on token estimation
    trimmed_history = history[-max_input_length:]

    model_formatted_input = formatters.get(prompt_type)(
        trimmed_history, message, system_message, preferences, timestamp, persona
    )
    if debug:
        logging.info(f"= PROMPT:\n{model_formatted_input}\n")

    input_tokens = len(model_formatted_input.split())  # Simplified token counting
    max_new_tokens_allowed = min(
        max_new_tokens - input_tokens, max_total_tokens - input_tokens
    )

    client = InferenceClient(model=llm)
    partial_message = ""
    try:
        for token in client.text_generation(
            model_formatted_input,
            best_of=1,
            max_new_tokens=max_new_tokens_allowed,
            repetition_penalty=1.1,
            do_sample=True,
            seed=None,
            temperature=temperature,
            top_k=40,
            top_p=0.95,
            typical_p=0.95,
            watermark=False,
            stream=True,
        ):
            partial_message += token
            if "<|im_end|>" in partial_message:
                partial_message = partial_message.replace("<|im_end|>", "").strip()
            yield partial_message
    except Exception as e:
        yield f"An error occurred: {str(e)}"


chat_interface = gr.ChatInterface(
    inference,
    title=app_title,
    description=description,
    chatbot=gr.Chatbot(
        height=500,
        avatar_images=[None, persona_avatar_image],
        likeable=True,
        show_copy_button=True,
    ),
    textbox=gr.Textbox(
        placeholder="Hello! What would you like to talk about?",
        container=False,
        scale=7,
    ),
    retry_btn="Rephrase",
    undo_btn="Undo",
    clear_btn="Clear",
    examples=chat_examples,
    theme=ui_theme,
    analytics_enabled=False,
)

if __name__ == "__main__":
    chat_interface.queue().launch(server_name=server_name, server_port=server_port)
