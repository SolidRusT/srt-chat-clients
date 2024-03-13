import logging
from config_loader import load_config, load_environment
from logging_config import configure_logger
from inference_wrapper import gradio_inference_wrapper
from conversation_manager import AdvancedConversationManager
import gradio as gr

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
development_mode = True

# Load configuration and environment variables
config = load_config("config.yaml")
env_vars = load_environment()

# Initialize the model parameters cache
model_parameters_cache = {}

# Use environment variables
persona_name = env_vars["persona_name"]
server_port = env_vars["server_port"]
server_name = env_vars["server_name"]

# Extract configuration for the current persona
persona_config = config["personas"][persona_name]
# Configuration for the current persona
ui_theme = persona_config["theme"]
persona_full_name = persona_config["name"]
app_title = persona_config["title"]
persona_avatar_image = f"images/{persona_config['avatar']}"
description = persona_config["description"]
system_message = persona_config["system_message"]
persona = persona_config["persona"]
chat_examples = persona_config["topic_examples"]
temperature = persona_config["temperature"]

# Setup logging
debug_mode = config.get("debug", True)
logs_path = config.get("logs_path", "logs")
log_file_name = f"SRT-Assistant-{persona_name}.log"
logger = configure_logger(persona_full_name, debug=debug_mode, logs_path=logs_path, log_file_name=log_file_name)

# Launch the UI
chat_interface = gr.ChatInterface(
    fn=gradio_inference_wrapper,
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
    # Initialize the conversation manager without flushing Redis by default
    conversation_manager = AdvancedConversationManager(redis_host="localhost", redis_port=6379)
    
    # Optional: Conditionally flush Redis database for development or testing purposes
    if development_mode:  # Assuming you have a way to determine if you're in development mode
        conversation_manager.flush_db()
        logger.info("Redis database flushed for development.")

    logger.info("Launching the chat interface...")
    # Setup and launch your Gradio chat interface as before
    chat_interface.queue().launch(server_name=server_name, server_port=server_port)
    