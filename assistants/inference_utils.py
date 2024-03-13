from huggingface_hub import InferenceClient
import logging
from prompt_formatters import formatters
import time
import random
from model_utils import fetch_model_info

# Initialize the logger
logger = logging.getLogger(__name__)


def inference(tgi_urls, message, history, persona_config, model_parameters_cache):
    """Generate a response to the given message using the model."""
    timestamp = current_timestamp()
    llms = random.choice(tgi_urls)
    llm = llms["url"]
    model_info = fetch_model_info(llm, model_parameters_cache)

    max_input_length = model_info.get("max_input_length", 1024)
    max_total_tokens = model_info.get("max_total_tokens", 4096)

    prompt_type = llms["type"]
    max_new_tokens = llms["max_tokens"]

    # Simplified for demonstration: trim history based on max_input_length
    # Real implementation would adjust based on token estimation
    trimmed_history = history[-max_input_length:]

    model_formatted_input = formatters.get(prompt_type)(
        trimmed_history,
        message,
        persona_config["system_message"],
        persona_config["persona"],
        timestamp,
    )
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"= PROMPT:\n{model_formatted_input}\n")

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
            temperature=persona_config["temperature"],
            top_k=40,
            top_p=0.95,
            typical_p=0.95,
            watermark=False,
            stream=True,
        ):
            partial_message += token
            if "<im_end>" in partial_message:
                partial_message = partial_message.replace("<im_end>", "").strip()
            yield partial_message
    except Exception as e:
        logger.error(f"An error occurred during inference: {str(e)}")
        yield f"An error occurred: {str(e)}"


def current_timestamp():
    """Utility function to get the current timestamp."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
