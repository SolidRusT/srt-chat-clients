import yaml
import os


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as stream:
        return yaml.safe_load(stream)


def load_environment():
    return {
        "persona_name": os.environ.get("PERSONA", "Default"),
        "server_port": int(os.environ.get("PORT", 8650)),
        "server_name": os.environ.get("SERVER_NAME", "0.0.0.0"),
        "tgi_urls": os.environ.get("TGI_URLS", "tgi_default_urls"),
    }
