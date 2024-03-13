import requests
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

def fetch_model_info(llm, model_parameters_cache):
    """Fetch model information for the given language model."""
    if llm in model_parameters_cache:
        return model_parameters_cache[llm]
    url = f"{llm}info"
    logger.debug(f"Fetching model info from URL: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            model_info = response.json()
            model_parameters_cache[llm] = model_info
            return model_info
        else:
            logger.error(f"Failed to fetch model info for {llm}: HTTP {response.status_code}, Response: {response.text}")
    except Exception as e:
        logger.error(f"Error fetching model info for {llm}: {str(e)}")
    return {"max_input_length": 1024, "max_total_tokens": 4096}
