from __future__ import annotations

# Imports
import os
import time
import datetime
import subprocess
import site
import numpy as np
import gradio as gr
from gradio_client import Client
from huggingface_hub import InferenceClient

whisper_endpoint = "https://168e0408e472c1a410.gradio.live/"  # Thanatos


def check_and_download_unidic():
    # Path where unidic data is expected to be stored
    unidic_path = os.path.join(site.getsitepackages()[0], "unidic", "dicdir")

    # Check if the unidic directory exists
    if not os.path.exists(unidic_path):
        print("unidic not found. Downloading...")
        subprocess.run(["python", "-m", "unidic", "download"])
    else:
        print("unidic already exists.")


check_and_download_unidic()

# we need to compile a CUBLAS version
# Or get it from  https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/
os.system('CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python==0.2.11')
# By using XTTS you agree to CPML license https://coqui.ai/cpml
os.environ["COQUI_TOS_AGREED"] = "1"
# NOTE: for streaming will require gradio audio streaming fix
# pip install --upgrade -y gradio==0.50.2 git+https://github.com/gorkemgoknar/gradio.git@patch-1
import textwrap
from pydub import AudioSegment
import nltk  # we'll use this to split into sentences

nltk.download("punkt")

import noisereduce as nr
import subprocess
import langid
import uuid
import emoji
import re
import io, wave

from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir

WHISPER_TIMEOUT = int(os.environ.get("WHISPER_TIMEOUT", 45))
# whisper_client = Client("https://sanchit-gandhi-whisper-large-v2.hf.space/")
whisper_client = Client(whisper_endpoint)

print("Downloading if not downloaded Coqui XTTS V2")

from TTS.utils.manage import ModelManager

model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
ModelManager().download_model(model_name)
model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))
print("XTTS downloaded")


print("Loading XTTS")
config = XttsConfig()
config.load_json(os.path.join(model_path, "config.json"))

model = Xtts.init_from_config(config)
model.load_checkpoint(
    config,
    checkpoint_path=os.path.join(model_path, "model.pth"),
    vocab_path=os.path.join(model_path, "vocab.json"),
    eval=True,
    use_deepspeed=True,
)
model.cuda()
print("Done loading TTS")

title = "Voice chat SolidRusT Networks"

DESCRIPTION = """# Voice chat SolidRusT Networks"""
css = """.toast-wrap { display: none !important } """

default_system_message = f"""
You are ##LLM_MODEL###, a large language model trained ##LLM_MODEL_PROVIDER###, architecture of you is decoder-based LM. Your voice backend or text to speech TTS backend is provided via Coqui technology. You are right now served on Huggingface spaces.
Don't repeat. Answer short, only few words, as if in a talk. You cannot access the internet, but you have vast knowledge.
Current date: CURRENT_DATE .
"""

system_message = os.environ.get("SYSTEM_MESSAGE", default_system_message)
system_message = system_message.replace("CURRENT_DATE", str(datetime.date.today()))


# Default
default_system_understand_message = (
    "I understand, I am a ##LLM_MODEL### chatbot with speech by SolidRusT Networks."
)
system_understand_message = os.environ.get(
    "SYSTEM_UNDERSTAND_MESSAGE", default_system_understand_message
)

print("System message set as:", default_system_message)

ROLES = ["AI Assistant", "AI Beard The Pirate", "Suparious AI 9000"]
ROLE_PROMPTS = {}
# Default scenario
ROLE_PROMPTS["AI Assistant"] = system_message
# Pirate scenario
character_name = "AI Beard"
character_scenario = f"As {character_name} you are a 28 year old man who is a pirate on the ship Invisible AI. You are good friends with Guybrush Threepwood and Murray the Skull. Developers did not get you into Monkey Island games as you wanted huge shares of Big Whoop treasure."
character_system_message = f"You as {character_name}. {character_scenario} Print out only exactly the words that {character_name} would speak out, do not add anything. Don't repeat. Answer short, only few words, as if in a talk. Craft your response only from the first-person perspective of {character_name} and never as user.Current date: #CURRENT_DATE#".replace(
    "#CURRENT_DATE#", str(datetime.date.today())
)
ROLE_PROMPTS["AI Beard The Pirate"] = character_system_message
# Suparious AI scenario
character_name = "Suparious AI"
character_scenario = f"As {character_name} you are a advanced AI from the future that is instruct tuned. You are good friends with Shaun Prince and together you co-founded SolidRusT Networks. You try your best to be helpful, but you've got alot of important thihngs to do."
character_system_message = f"You as {character_name}. {character_scenario} Print out only exactly the words that {character_name} would speak out, do not add anything. Don't repeat. Answer in the way that Spock from StarTrek would. Craft your response only from the first-person perspective of {character_name} and never as user.Current date: #CURRENT_DATE#".replace(
    "#CURRENT_DATE#", str(datetime.date.today())
)
ROLE_PROMPTS["Suparious AI 9000"] = character_system_message

# set GPU_LAYERS to 15 if you have a 8GB
GPU_LAYERS = int(os.environ.get("GPU_LAYERS", 35))

LLM_STOP_WORDS = ["<|im_end|>"]

LLAMA_VERBOSE = False
print("Running Dolphin")
llm_dolphin = InferenceClient(model="http://Erebus:8081")


# Universal ChatML formatter
def format_prompt_ChatML(
    message,
    history,
    system_message=system_message,
    system_understand_message=system_understand_message,
):
    prompt = (
        "<|im_start|>system\n"
        + system_message
        + system_understand_message
        + "<|im_end|>"
    )
    for user_prompt, bot_response in history:
        prompt += f"<|im_start|>user\n{user_prompt}<|im_end|>"
        prompt += f"<|im_start|>assistant\n{bot_response}"
    if message == "":
        message = "Hello"
    prompt += f"<|im_start|>user\n{message}<|im_end|>"
    prompt += f"<|im_start|>assistant"
    print(prompt)
    return prompt


def generate_local(
    prompt,
    history,
    llm_model="",  # "mistral","zephyr","yi","dolphin","other"
    system_message=None,
    temperature=0.8,
    max_tokens=256,
    top_p=0.95,
    stop=LLM_STOP_WORDS,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature, max_new_tokens=max_tokens, top_p=top_p
    )

    llm_provider = "SolidRusT Networks"
    llm_model = "Dolphin"
    llm = llm_dolphin
    sys_message = system_message.replace("##LLM_MODEL###", llm_model).replace(
        "##LLM_MODEL_PROVIDER###", llm_provider
    )
    sys_system_understand_message = system_understand_message.replace(
        "##LLM_MODEL###", llm_model
    ).replace("##LLM_MODEL_PROVIDER###", llm_provider)
    formatted_prompt = format_prompt_ChatML(
        prompt,
        history,
        system_message=sys_message,
        system_understand_message=sys_system_understand_message,
    )

    sys_message = system_message.replace("##LLM_MODEL###", llm_model).replace(
        "##LLM_MODEL_PROVIDER###", llm_provider
    )

    stream = llm.text_generation(
        formatted_prompt,
        **generate_kwargs,
        stream=True,
    )
    output = ""
    for response in stream:
        character = response["choices"][0]["text"]
        if emoji.is_emoji(character):
            # Bad emoji not a meaning messes chat from next lines
            return
        output += (
            response["choices"][0]["text"]
            .replace("<|assistant|>", "")
            .replace("<|user|>", "")
        )
        yield output
    return output


def get_latents(speaker_wav, voice_cleanup=False):
    if voice_cleanup:
        try:
            cleanup_filter = "lowpass=8000,highpass=75,areverse,silenceremove=start_periods=1:start_silence=0:start_threshold=0.02,areverse,silenceremove=start_periods=1:start_silence=0:start_threshold=0.02"
            resample_filter = "-ac 1 -ar 22050"
            out_filename = (
                speaker_wav + str(uuid.uuid4()) + ".wav"
            )  # ffmpeg to know output format
            # we will use newer ffmpeg as that has afftn denoise filter
            shell_command = f"ffmpeg -y -i {speaker_wav} -af {cleanup_filter} {resample_filter} {out_filename}".split(
                " "
            )

            command_result = subprocess.run(
                [item for item in shell_command],
                capture_output=False,
                text=True,
                check=True,
            )
            speaker_wav = out_filename
            print("Filtered microphone input")
        except subprocess.CalledProcessError:
            # There was an error - command exited with non-zero code
            print("Error: failed filtering, use original microphone input")
    else:
        speaker_wav = speaker_wav

    # create as function as we can populate here with voice cleanup/filtering
    (
        gpt_cond_latent,
        speaker_embedding,
    ) = model.get_conditioning_latents(audio_path=speaker_wav)
    return gpt_cond_latent, speaker_embedding


def wave_header_chunk(frame_input=b"", channels=1, sample_width=2, sample_rate=24000):
    # This will create a wave header then append the frame input
    # It should be first on a streaming wav file
    # Other frames better should not have it (else you will hear some artifacts each chunk start)
    wav_buf = io.BytesIO()
    with wave.open(wav_buf, "wb") as vfout:
        vfout.setnchannels(channels)
        vfout.setsampwidth(sample_width)
        vfout.setframerate(sample_rate)
        vfout.writeframes(frame_input)

    wav_buf.seek(0)
    return wav_buf.read()


# Config will have more correct languages, they may be added before we append here
##["en","es","fr","de","it","pt","pl","tr","ru","nl","cs","ar","zh-cn","ja"]

xtts_supported_languages = config.languages


def detect_language(prompt):
    # Fast language autodetection
    if len(prompt) > 15:
        language_predicted = langid.classify(prompt)[
            0
        ].strip()  # strip need as there is space at end!
        if language_predicted == "zh":
            # we use zh-cn on xtts
            language_predicted = "zh-cn"

        if language_predicted not in xtts_supported_languages:
            print(
                f"Detected a language not supported by xtts :{language_predicted}, switching to english for now"
            )
            gr.Warning(
                f"Language detected '{language_predicted}' can not be spoken properly 'yet' "
            )
            language = "en"
        else:
            language = language_predicted
        print(
            f"Language: Predicted sentence language:{language_predicted} , using language for xtts:{language}"
        )
    else:
        # Hard to detect language fast in short sentence, use english default
        language = "en"
        print(
            f"Language: Prompt is short or autodetect language disabled using english for xtts"
        )

    return language


def get_voice_streaming(prompt, language, latent_tuple, suffix="0"):
    gpt_cond_latent, speaker_embedding = latent_tuple

    try:
        t0 = time.time()
        chunks = model.inference_stream(
            prompt,
            language,
            gpt_cond_latent,
            speaker_embedding,
            repetition_penalty=7.0,
            temperature=0.85,
        )

        first_chunk = True
        for i, chunk in enumerate(chunks):
            if first_chunk:
                first_chunk_time = time.time() - t0
                metrics_text = f"Latency to first audio chunk: {round(first_chunk_time*1000)} milliseconds\n"
                first_chunk = False
            # print(f"Received chunk {i} of audio length {chunk.shape[-1]}")

            # In case output is required to be multiple voice files
            # out_file = f'{char}_{i}.wav'
            # write(out_file, 24000, chunk.detach().cpu().numpy().squeeze())
            # audio = AudioSegment.from_file(out_file)
            # audio.export(out_file, format='wav')
            # return out_file
            # directly return chunk as bytes for streaming
            chunk = chunk.detach().cpu().numpy().squeeze()
            chunk = (chunk * 32767).astype(np.int16)

            yield chunk.tobytes()

    except RuntimeError as e:
        if "device-side assert" in str(e):
            # cannot do anything on cuda device side error, need tor estart
            print(
                f"Exit due to: Unrecoverable exception caused by prompt:{prompt}",
                flush=True,
            )
            gr.Warning("Unhandled Exception encounter, please retry in a minute")
            print("Cuda device-assert Runtime encountered need restart")
            # TODO: restart if we get here
            # HF Space specific.. This error is unrecoverable need to restart space
            # api.restart_space(repo_id=repo_id)
        else:
            print("RuntimeError: non device-side assert error:", str(e))
            # Does not require warning happens on empty chunk and at end
            ###gr.Warning("Unhandled Exception encounter, please retry in a minute")
            return None
        return None
    except:
        return None


def transcribe(wav_path):
    try:
        # get result from whisper and strip it to delete begin and end space
        return whisper_client.predict(
            wav_path,  # str (filepath or URL to file) in 'inputs' Audio component
            "transcribe",  # str in 'Task' Radio component
            api_name="/predict",
        ).strip()
    except:
        gr.Warning("There was a problem with Whisper endpoint, telling a joke for you.")
        return "There was a problem with my voice, tell me joke"


# Will be triggered on text submit (will send to generate_speech)
def add_text(history, text):
    history = [] if history is None else history
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)


# Will be triggered on voice submit (will transribe and send to generate_speech)
def add_file(history, file):
    history = [] if history is None else history

    try:
        text = transcribe(file)
        print("Transcribed text:", text)
    except Exception as e:
        print(str(e))
        gr.Warning("There was an issue with transcription, please try writing for now")
        # Apply a null text on error
        text = "Transcription seems failed, please tell me a joke about chickens"

    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)


##NOTE: not using this as it yields a chacter each time while we need to feed history to TTS
def bot(history, system_prompt=""):
    history = [["", None]] if history is None else history

    if system_prompt == "":
        system_prompt = system_message

    history[-1][1] = ""
    for character in generate(history[-1][0], history[:-1]):
        history[-1][1] = character
        yield history


def get_sentence(history, chatbot_role, llm_model, system_prompt=""):
    history = [["", None]] if history is None else history

    if system_prompt == "":
        system_prompt = system_message

    history[-1][1] = ""

    start_time = time.time()

    sentence_list = []
    sentence_hash_list = []

    text_to_generate = ""
    stored_sentence = None
    stored_sentence_hash = None

    print(chatbot_role)
    print(llm_model)

    for character in generate_local(
        history[-1][0],
        history[:-1],
        system_message=ROLE_PROMPTS[chatbot_role],
        llm_model=llm_model,
    ):
        history[-1][1] = character.replace("<|assistant|>", "")
        # It is coming word by word

        text_to_generate = nltk.sent_tokenize(
            history[-1][1]
            .replace("\n", " ")
            .replace("<|assistant|>", " ")
            .replace("<|ass>", "")
            .replace("[/ASST]", "")
            .replace("[/ASSI]", "")
            .replace("[/ASS]", "")
            .replace("", "")
            .strip()
        )
        if len(text_to_generate) > 1:
            dif = len(text_to_generate) - len(sentence_list)

            if dif == 1 and len(sentence_list) != 0:
                continue

            if dif == 2 and len(sentence_list) != 0 and stored_sentence is not None:
                continue

            # All this complexity due to trying append first short sentence to next one for proper language auto-detect
            if stored_sentence is not None and stored_sentence_hash is None and dif > 1:
                # means we consumed stored sentence and should look at next sentence to generate
                sentence = text_to_generate[len(sentence_list) + 1]
            elif (
                stored_sentence is not None
                and len(text_to_generate) > 2
                and stored_sentence_hash is not None
            ):
                print("Appending stored")
                sentence = stored_sentence + text_to_generate[len(sentence_list) + 1]
                stored_sentence_hash = None
            else:
                sentence = text_to_generate[len(sentence_list)]

            # too short sentence just append to next one if there is any
            # this is for proper language detection
            if (
                len(sentence) <= 15
                and stored_sentence_hash is None
                and stored_sentence is None
            ):
                if sentence[-1] in [".", "!", "?"]:
                    if stored_sentence_hash != hash(sentence):
                        stored_sentence = sentence
                        stored_sentence_hash = hash(sentence)
                        print("Storing:", stored_sentence)
                        continue

            sentence_hash = hash(sentence)
            if (
                stored_sentence_hash is not None
                and sentence_hash == stored_sentence_hash
            ):
                continue

            if sentence_hash not in sentence_hash_list:
                sentence_hash_list.append(sentence_hash)
                sentence_list.append(sentence)
                print("New Sentence: ", sentence)
                yield (sentence, history)

    # return that final sentence token
    try:
        last_sentence = nltk.sent_tokenize(
            history[-1][1]
            .replace("\n", " ")
            .replace("<|ass>", "")
            .replace("[/ASST]", "")
            .replace("[/ASSI]", "")
            .replace("[/ASS]", "")
            .replace("", "")
            .strip()
        )[-1]
        sentence_hash = hash(last_sentence)
        if sentence_hash not in sentence_hash_list:
            if stored_sentence is not None and stored_sentence_hash is not None:
                last_sentence = stored_sentence + last_sentence
                stored_sentence = stored_sentence_hash = None
                print("Last Sentence with stored:", last_sentence)

            sentence_hash_list.append(sentence_hash)
            sentence_list.append(last_sentence)
            print("Last Sentence: ", last_sentence)

            yield (last_sentence, history)
    except:
        print("ERROR on last sentence history is :", history)


from scipy.io.wavfile import write
from pydub import AudioSegment

second_of_silence = AudioSegment.silent()  # use default
second_of_silence.export("sil.wav", format="wav")


def generate_speech(history, chatbot_role, llm_model):
    # Must set autoplay to True first
    yield (history, chatbot_role, "", wave_header_chunk())
    for sentence, history in get_sentence(history, chatbot_role, llm_model):
        if sentence != "":
            print("BG: inserting sentence to queue")

            generated_speech = generate_speech_for_sentence(
                history, chatbot_role, sentence, return_as_byte=True
            )
            if generated_speech is not None:
                _, audio_dict = generated_speech
                # We are using byte streaming
                yield (history, chatbot_role, sentence, audio_dict["value"])


# will generate speech audio file per sentence
def generate_speech_for_sentence(history, chatbot_role, sentence, return_as_byte=False):
    language = "autodetect"

    wav_bytestream = b""

    if len(sentence) == 0:
        print("EMPTY SENTENCE")
        return

    # Sometimes prompt </s> coming on output remove it
    # Some post process for speech only
    sentence = sentence.replace("</s>", "")
    # remove code from speech
    sentence = re.sub("```.*```", "", sentence, flags=re.DOTALL)
    sentence = re.sub("`.*`", "", sentence, flags=re.DOTALL)

    sentence = re.sub("\(.*\)", "", sentence, flags=re.DOTALL)

    sentence = sentence.replace("```", "")
    sentence = sentence.replace("...", " ")
    sentence = sentence.replace("(", " ")
    sentence = sentence.replace(")", " ")
    sentence = sentence.replace("<|assistant|>", "")

    if len(sentence) == 0:
        print("EMPTY SENTENCE after processing")
        return

    # A fast fix for last chacter, may produce weird sounds if it is with text
    # if (sentence[-1] in ["!", "?", ".", ","]) or (sentence[-2] in ["!", "?", ".", ","]):
    #    # just add a space
    #    sentence = sentence[:-1] + " " + sentence[-1]

    # regex does the job well
    sentence = re.sub("([^\x00-\x7F]|\w)(\.|\。|\?|\!)", r"\1 \2\2", sentence)

    print("Sentence for speech:", sentence)

    try:
        SENTENCE_SPLIT_LENGTH = 350
        if len(sentence) < SENTENCE_SPLIT_LENGTH:
            # no problem continue on
            sentence_list = [sentence]
        else:
            # Until now nltk likely split sentences properly but we need additional
            # check for longer sentence and split at last possible position
            # Do whatever necessary, first break at hypens then spaces and then even split very long words
            sentence_list = textwrap.wrap(sentence, SENTENCE_SPLIT_LENGTH)
            print("SPLITTED LONG SENTENCE:", sentence_list)

        for sentence in sentence_list:
            if any(c.isalnum() for c in sentence):
                if language == "autodetect":
                    # on first call autodetect, nexts sentence calls will use same language
                    language = detect_language(sentence)

                # exists at least 1 alphanumeric (utf-8)
                audio_stream = get_voice_streaming(
                    sentence, language, latent_map[chatbot_role]
                )
            else:
                # likely got a ' or " or some other text without alphanumeric in it
                audio_stream = None

            # XTTS is actually using streaming response but we are playing audio by sentence
            # If you want direct XTTS voice streaming (send each chunk to voice ) you may set DIRECT_STREAM=1 environment variable
            if audio_stream is not None:
                frame_length = 0
                for chunk in audio_stream:
                    try:
                        wav_bytestream += chunk
                        frame_length += len(chunk)
                    except:
                        # hack to continue on playing. sometimes last chunk is empty , will be fixed on next TTS
                        continue

            # Filter output for better voice
            filter_output = False
            if filter_output:
                data_s16 = np.frombuffer(
                    wav_bytestream,
                    dtype=np.int16,
                    count=len(wav_bytestream) // 2,
                    offset=0,
                )
                float_data = data_s16 * 0.5**15
                reduced_noise = nr.reduce_noise(
                    y=float_data, sr=24000, prop_decrease=0.8, n_fft=1024
                )
                wav_bytestream = (reduced_noise * 32767).astype(np.int16)
                wav_bytestream = wav_bytestream.tobytes()

            if audio_stream is not None:
                if not return_as_byte:
                    audio_unique_filename = "/tmp/" + str(uuid.uuid4()) + ".wav"
                    with wave.open(audio_unique_filename, "w") as f:
                        f.setnchannels(1)
                        # 2 bytes per sample.
                        f.setsampwidth(2)
                        f.setframerate(24000)
                        f.writeframes(wav_bytestream)
                    return (
                        history,
                        gr.Audio.update(value=audio_unique_filename, autoplay=True),
                    )
                else:
                    return (
                        history,
                        gr.Audio.update(value=wav_bytestream, autoplay=True),
                    )
    except RuntimeError as e:
        if "device-side assert" in str(e):
            # cannot do anything on cuda device side error, need tor estart
            print(
                f"Exit due to: Unrecoverable exception caused by prompt:{sentence}",
                flush=True,
            )
            gr.Warning("Unhandled Exception encounter, please retry in a minute")
            print("Cuda device-assert Runtime encountered need restart")

            # HF Space specific.. This error is unrecoverable need to restart space
            # TODO: restart if we get here
        else:
            print("RuntimeError: non device-side assert error:", str(e))
            raise e

    print("All speech ended")
    return


latent_map = {}
latent_map["AI Assistant"] = get_latents("examples/female.wav")
latent_map["AI Beard The Pirate"] = get_latents("examples/pirate_by_coqui.wav")
latent_map["Suparious AI 9000"] = get_latents("examples/ShaunPrince.wav")

#### GRADIO INTERFACE ####

EXAMPLES = [
    [[], "AI Assistant", "What is 42?"],
    [[], "AI Assistant", "Speak in French, tell me how are you doing?"],
    [[], "AI Assistant", "Antworten Sie mir von nun an auf Deutsch"],
    [[], "AI Assistant", "给我讲个故事 的英文"],
    [[], "AI Beard The Pirate", "Who are you?"],
    [[], "AI Beard The Pirate", "Speak in Chinese, 你认识一个叫路飞的海贼吗"],
    [[], "AI Beard The Pirate", "Speak in Japanese, ルフィという海賊を知っていますか？"],
]

MODELS = ["Dolphin"]

OTHER_HTML = f"""<div>
<p>SolidRusT Networks is a company that provides AI services and products. We are a team of 2 people, Shaun Prince and Suparious AI 9000. We are currently working on a new AI assistant that will be able to do many more things.</p>
</div>
"""

with gr.Blocks(title=title) as demo:
    gr.Markdown(DESCRIPTION)
    gr.Markdown(OTHER_HTML)
    with gr.Row():
        model_selected = gr.Dropdown(
            label="Select Instuct LLM Model to Use",
            info="Dolphin is quantized AWQ 4bit",
            choices=MODELS,
            multiselect=False,
            value=MODELS[0],
        )
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=("examples/hf-logo.png", "examples/coqui-logo.png"),
        bubble_full_width=False,
    )
    with gr.Row():
        chatbot_role = gr.Dropdown(
            label="Role of the Chatbot",
            info="How should Chatbot talk like",
            choices=ROLES,
            multi_select=False,
            value=ROLES[0],
        )
    with gr.Row():
        txt = gr.Textbox(
            scale=3,
            show_label=False,
            placeholder="Enter text and press enter, or speak to your microphone",
            container=False,
            interactive=True,
        )
        txt_btn = gr.Button(value="Submit text", scale=1)
        btn = gr.Audio(source="microphone", type="filepath", scale=4)

    def stop():
        print("Audio STOP")
        set_audio_playing(False)

    with gr.Row():
        sentence = gr.Textbox(visible=False)
        audio = gr.Audio(
            value=None,
            label="Generated audio response",
            streaming=True,
            autoplay=True,
            interactive=False,
            show_label=True,
        )

        audio.end(stop)

    with gr.Row():
        gr.Examples(
            EXAMPLES,
            [chatbot, chatbot_role, txt],
            [chatbot, chatbot_role, txt],
            add_text,
            cache_examples=False,
            run_on_click=False,  # Will not work , user should submit it
        )

    def clear_inputs(chatbot):
        return None

    clear_btn = gr.ClearButton([chatbot, audio])
    chatbot_role.change(fn=clear_inputs, inputs=[chatbot], outputs=[chatbot])
    model_selected.change(fn=clear_inputs, inputs=[chatbot], outputs=[chatbot])

    txt_msg = txt_btn.click(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        generate_speech,
        [chatbot, chatbot_role, model_selected],
        [chatbot, chatbot_role, sentence, audio],
    )

    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        generate_speech,
        [chatbot, chatbot_role, model_selected],
        [chatbot, chatbot_role, sentence, audio],
    )

    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)

    file_msg = btn.stop_recording(
        add_file, [chatbot, btn], [chatbot, txt], queue=False
    ).then(
        generate_speech,
        [chatbot, chatbot_role, model_selected],
        [chatbot, chatbot_role, sentence, audio],
    )

    file_msg.then(
        lambda: (gr.update(interactive=True), gr.update(interactive=True, value=None)),
        None,
        [txt, btn],
        queue=False,
    )

    gr.Markdown(
        """

Note:
- Have a good time!"""
    )
demo.queue()
demo.launch(debug=True, share=True)
