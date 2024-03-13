#..\..\..\venv-PySide6\Scripts\activate
#pip install --upgrade -r .\requirements-pyside.txt
import sys
import os
import yaml
import logging
import random
import time
from huggingface_hub import InferenceClient
from prompt_formatters import formatters
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QComboBox,
)
from PySide6.QtCore import QThread, Signal

with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

available_personas = list(config["personas"].keys())
app_title = config["app_name"]

debug = True

tgi_urls = os.environ.get("TGI_URLS", "tgi_default_urls")

log_level = logging.DEBUG if debug else logging.INFO
logs_path = config["logs_path"]
if not os.path.exists(logs_path):
    os.makedirs(logs_path)
logging.basicConfig(
    filename=logs_path + "/pyside-chat.log",
    level=log_level,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def inference(message, history):
    timestamp = current_timestamp()
    llms = random.choice(config[tgi_urls])
    llm = llms["url"]
    prompt_type = llms["type"]
    max_new_tokens = llms["max_tokens"]
    format_for_model = formatters.get(prompt_type)
    model_formatted_input = format_for_model(
        history, message, system_message, persona, timestamp
    )
    if debug:
        logging.info(f"= PROMPT:\n{model_formatted_input}\n")
    input_tokens = len(model_formatted_input.split())
    max_new_tokens_allowed = max_new_tokens - input_tokens

    client = InferenceClient(model=llm)
    logging.info(
        f"=== INFERENCE inputs:{input_tokens} / max new:{max_new_tokens_allowed}) on: {llm}"
    )
    full_message = ""
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
            # top_n_token=5,
            top_p=0.95,
            typical_p=0.95,
            watermark=False,
            stream=True,
        ):
            full_message += token
        yield full_message.strip()
    except Exception as e:
        yield f"An error occurred: {str(e)}"


class InferenceThread(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, message, history):
        super().__init__()
        self.message = message
        self.history = history

    def run(self):
        try:
            # Get the complete response
            for response in inference(self.message, self.history):
                self.finished.emit(response)
                break  # Exit after receiving the complete response

        except Exception as e:
            self.error.emit(f"An error occurred: {str(e)}")


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(app_title)
        self.layout = QVBoxLayout(self)
        self.persona_dropdown = QComboBox(self)
        self.persona_dropdown.addItems(available_personas)
        self.persona_dropdown.currentIndexChanged.connect(self.on_persona_change)
        self.layout.addWidget(self.persona_dropdown)
        default_persona_name = os.environ.get("PERSONA", "Default")
        self.update_persona_config(default_persona_name)
        self.label = QLabel(description)
        self.layout.addWidget(self.label)
        self.input = QLineEdit()
        self.layout.addWidget(self.input)
        self.button = QPushButton("Send Message")
        self.button.clicked.connect(self.onStart)
        self.layout.addWidget(self.button)
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

    def on_persona_change(self, index):
        persona_name = self.persona_dropdown.itemText(index)
        self.update_persona_config(persona_name)

    def update_persona_config(self, persona_name):
        global ui_theme, app_title, persona_avatar_image, description, system_message, persona, chat_examples, temperature
        ui_theme = config["personas"][persona_name]["theme"]
        app_title = config["personas"][persona_name]["title"]
        persona_avatar_image = f"images/{config['personas'][persona_name]['avatar']}"
        description = config["personas"][persona_name]["description"]
        system_message = config["personas"][persona_name]["system_message"]
        persona = config["personas"][persona_name]["persona"]
        chat_examples = config["personas"][persona_name]["topic_examples"]
        temperature = config["personas"][persona_name]["temperature"]
        self.refresh_ui()

    def refresh_ui(self):
        pass

    def onStart(self):
        user_message = self.input.text().strip()
        if user_message:  # Ensure there's a message to process
            # Update history with the new user message
            self.history.append((user_message, ""))
            self.updateUIForNewMessage(user_message)
            self.worker = InferenceThread(user_message, self.history)
            self.worker.finished.connect(self.onPartialMessage)
            self.worker.error.connect(self.onError)
            self.worker.start()

    def onPartialMessage(self, bot_response):
        # Update the UI
        self.text_edit.append(bot_response)

        # Update the last entry in history with the bot's response
        if self.history:
            self.history[-1] = (self.history[-1][0], bot_response)

        # Enable the button for new messages
        self.button.setEnabled(True)

    def updateUIForNewMessage(self, user_message):
        self.text_edit.append(f"User: {user_message}")
        self.input.clear()

    def onError(self, message):
        self.text_edit.append(message)
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
