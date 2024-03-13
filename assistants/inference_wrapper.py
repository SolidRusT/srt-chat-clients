import logging
from config_loader import load_config, load_environment
from conversation_manager import AdvancedConversationManager
from inference_utils import inference

# Initialize the logger for this module
logger = logging.getLogger(__name__)

# Load configuration and environment variables
config = load_config("config.yaml")
env_vars = load_environment()

# Use environment variables
persona_name = env_vars["persona_name"]

# Initialize the conversation manager with Redis configuration
conversation_manager = AdvancedConversationManager(
    redis_host="localhost", redis_port=6379
)

def gradio_inference_wrapper(message, user_id="default_user", model_parameters_cache={}):
    # Initialize a new session for each interaction
    session_id = conversation_manager.start_session(user_id)
    logger.debug(f"New ephemeral session {session_id} started for user {user_id}.")

    # Append the current user message to the new session
    current_message = {"text": message, "importance": 1}
    conversation_manager.append_message(session_id, current_message)
    logger.debug(f"Appended user message to session {session_id}: {message}")

    # Retrieve and flatten the nested history structure if necessary
    nested_history = conversation_manager.get_conversation_history(session_id)
    history = (
        [item for sublist in nested_history for item in sublist]
        if nested_history and isinstance(nested_history[0], list)
        else nested_history
    )
    logger.debug(f"Retrieved and possibly flattened history for session {session_id}")

    # Proceed with the adjusted, flattened history
    formatted_history = []
    if (
        history
        and isinstance(history, list)
        and all(isinstance(item, dict) for item in history)
    ):
        for i in range(0, len(history), 2):
            user_prompt = history[i].get("text", "")
            bot_response = (
                history[i + 1].get("text", "") if (i + 1) < len(history) else ""
            )
            formatted_history.append((user_prompt, bot_response))
    else:
        logger.warning("History format is still unexpected after adjustment")

    # Retrieve configurations for inference
    tgi_urls = config.get("tgi_default_urls", [])
    persona_config = config["personas"][persona_name]

    # Assuming no history is required for ephemeral conversations, but if needed, retrieve it:
    # history = conversation_manager.get_conversation_history(session_id)

    # Call the inference function with necessary parameters
    responses = inference(tgi_urls, message, [], persona_config, model_parameters_cache)

    # Append and yield each part of the response
    for response_part in responses:
        model_response = {"text": response_part, "importance": 1}
        conversation_manager.append_message(session_id, model_response)
        yield response_part
