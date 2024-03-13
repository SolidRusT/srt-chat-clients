def format_time_awareness(timestamp):
    time_prompt = f" The current date and time in the following format %Y-%m-%d %H:%M:%S (UTC-8) is: {timestamp}."
    return time_prompt


def format_for_dolphin(history, message, system_message, persona, timestamp):
    time_prompt = format_time_awareness(timestamp)
    prompt = (
        "<|im_start|>system\n" + system_message + persona + time_prompt + "<|im_end|>"
    )
    for user_prompt, bot_response in history:
        prompt += f"<|im_start|>user\n{user_prompt}<|im_end|>"
        prompt += f"<|im_start|>assistant\n{bot_response}"
    if message == "":
        message = "Hello"
    prompt += f"<|im_start|>user\n{message}<|im_end|>"
    prompt += f"<|im_start|>assistant"
    return prompt


def format_for_mistral(history, message, system_message, persona, timestamp):
    time_prompt = format_time_awareness(timestamp)
    prompt = "<s>[INST]" + system_message + "[/INST]" + persona + time_prompt + "</s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    if message == "":
        message = "Hello"
    prompt += f"[INST] {message} [/INST]"
    return prompt


def format_for_zephyr(history, message, system_message, persona, timestamp):
    time_prompt = format_time_awareness(timestamp)
    prompt = "<|system|>\n" + system_message + persona + time_prompt + "</s>"
    for user_prompt, bot_response in history:
        prompt += f"<|user|>\n{user_prompt}</s>"
        prompt += f"<|assistant|>\n{bot_response}</s>"
    if message == "":
        message = "Hello"
    prompt += f"<|user|>\n{message}</s>"
    prompt += f"<|assistant|>"
    return prompt


def format_for_yi(history, message, system_message, persona, timestamp):
    time_prompt = format_time_awareness(timestamp)
    prompt = (
        "<s>[INST] [SYS]\n"
        + system_message
        + persona
        + time_prompt
        + "\n[/SYS]\n\n[/INST]"
    )
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    if message == "":
        message = "Hello"
    prompt += f"[INST] {message} [/INST]"
    return prompt


def format_for_pygmalion(history, message, system_message, persona, timestamp):
    time_prompt = format_time_awareness(timestamp)
    prompt = "<|system|>" + system_message + persona + time_prompt + "\n"
    for user_prompt, bot_response in history:
        prompt += f"<|user|>{user_prompt}\n"
        prompt += f"<|model|>{bot_response}\n"
    if message == "":
        message = "Hello"
    prompt += f"<|user|>{message}\n"
    prompt += f"<|model|>"
    return prompt


# Mapping formatters to prompt types
formatters = {
    "dolphin": format_for_dolphin,
    "mistral": format_for_mistral,
    "zephyr": format_for_zephyr,
    "yi": format_for_yi,
    "pygmalion": format_for_pygmalion,
    # TODO: flan, bloom
}
