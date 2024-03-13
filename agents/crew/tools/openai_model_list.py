# Usage:
#   From the autocrew root directory:
#   - python tools/openai_model_list.py --list
#   - python tools/openai_model_list.py --filter openai

import openai
import yaml
import requests
import argparse
import logging


class ConfigLoader:
    """Class to load and manage configuration from YAML files."""

    @staticmethod
    def load(file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)


class ConfigInitializer:
    """Class to handle the initialization of configuration."""

    @staticmethod
    def initialize():
        return ConfigLoader.load("config.yaml")


def list_openai_models(api_key):
    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        logging.error(f"An error occurred while fetching models: {e}")
        return []


def filter_models_by_owner(models, owner):
    return [model for model in models if model.get("owned_by") == owner]


def sort_models_by_owner(models):
    return sorted(models, key=lambda model: model.get("owned_by", ""))


def display_models(models):
    for model in models:
        print(f"Model ID: {model['id']}")
        print(f"Owned By: {model.get('owned_by', 'Not specified')}")
        print("")


def main():
    parser = argparse.ArgumentParser(description="OpenAI Model Information Tool")
    parser.add_argument("--list", help="List all models", action="store_true")
    parser.add_argument(
        "--model", help="Get detailed information about a specific model"
    )
    parser.add_argument("--filter", help="Filter models by owner")
    parser.add_argument("--sort", help="Sort models by owner", action="store_true")
    args = parser.parse_args()

    config = ConfigInitializer.initialize()
    openai.api_key = config["openai_api_key"]

    models = list_openai_models(openai.api_key)

    if args.list:
        display_models(models)
    elif args.model:
        specific_model = next((m for m in models if m["id"] == args.model), None)
        if specific_model:
            display_models([specific_model])
        else:
            print(f"No model found with ID: {args.model}")
    elif args.filter:
        filtered_models = filter_models_by_owner(models, args.filter)
        display_models(filtered_models)
    elif args.sort:
        sorted_models = sort_models_by_owner(models)
        display_models(sorted_models)
    else:
        parser.print_help()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
