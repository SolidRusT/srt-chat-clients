import os
import yaml
import random
from urllib.parse import urlparse
import streamlit as st
from text_generation import Client
from langchain import PromptTemplate, LLMChain, HuggingFaceTextGenInference

# Load configuration
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

# Configure UI Defaults
app_name = "Translation AI"
persona = os.environ.get("PERSONA")
temperature = os.environ.get("TEMPERATURE")
model = os.environ.get("LANGUAGE_MODEL")
model_options = ["flan", "bloom", "random"]
sorted_models = sorted(model_options)
model_index = sorted_models.index(model)


def translate_button(
    prompt, llm, input_language, response_language, input_text, hostname
):
    # Ask for user to submit the completed input
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response_text = llm_chain.run(
        {
            "input_language": input_language,
            "response_language": response_language,
            "input_text": input_text,
        }
    )
    return response_text


def configure_model_options(model):
    match model:
        case "flan":
            # "Quebecois", "Russian" is not supported by Bloomz, only by Flan-T5
            languages = [
                "English",
                "Spanish",
                "Quebecois",
                "Japanese",
                "Persian",
                "Hindi",
                "French",
                "Chinese",
                "Bengali",
                "Gujarati",
                "German",
                "Telugu",
                "Italian",
                "Arabic",
                "Polish",
                "Tamil",
                "Marathi",
                "Malayalam",
                "Oriya",
                "Panjabi",
                "Portuguese",
                "Urdu",
                "Galician",
                "Hebrew",
                "Korean",
                "Catalan",
                "Thai",
                "Dutch",
                "Indonesian",
                "Vietnamese",
                "Bulgarian",
                "Filipino",
                "Central Khmer",
                "Lao",
                "Turkish",
                "Russian",
                "Croatian",
                "Swedish",
                "Yoruba",
                "Kurdish",
                "Burmese",
                "Malay",
                "Czech",
                "Finnish",
                "Somali",
                "Tagalog",
                "Swahili",
                "Sinhala",
                "Kannada",
                "Zhuang",
                "Igbo",
                "Xhosa",
                "Romanian",
                "Haitian",
                "Estonian",
                "Slovak",
                "Lithuanian",
                "Greek",
                "Nepali",
                "Assamese",
                "Norwegian",
            ]
            llm_url = random.choice(config["tgi_flan_urls"])
            selected_url = llm_url["url"]
            input_language = "English"
            response_language = "Quebecois"
            model_name = llm_url["name"]
        case "bloom":
            # https://huggingface.co/datasets/bigscience/xP3
            # https://huggingface.co/datasets/mc4
            languages = [
                "English",
                "Spanish",
                "Portugese",
                "French",
                "Arabic",
                "Indonesian",
                "Chinese",
                "Hindi",
                "Vietnamese",
                "code",
                "Urdu",
                "Telugu",
                "Tamil",
                "Bangla",
                "Marathi",
                "Swahili",
                "Gujarati",
                "Punjabi",
                "Nepali",
                "Yoruba",
                "Igbo",
            ]
            llm_url = random.choice(config["tgi_bloom_urls"])
            selected_url = llm_url["url"]
            input_language = "English"
            response_language = "Spanish"
            model_name = llm_url["name"]
        case _:
            languages = ["English", "Spanish", "French"]
            llm_url = random.choice(config["tgi_translate_urls"])
            selected_url = llm_url["url"]
            input_language = "English"
            response_language = "Spanish"
            model_name = llm_url["name"]
            model = llm_url["type"]
    sorted_languages = sorted(languages)
    parsed_url = urlparse(selected_url)
    hostname = model_name + " on " + parsed_url.hostname + "'s"
    input_language_index = sorted_languages.index(input_language)
    response_language_index = sorted_languages.index(response_language)
    col1, col2 = st.columns(2)
    with col1:
        input_language = st.selectbox(
            "Choose input language", sorted_languages, index=input_language_index
        )

    with col2:
        response_language = st.selectbox(
            "Choose response language", sorted_languages, index=response_language_index
        )

    # Configure selected inference llm defaults
    llm = HuggingFaceTextGenInference(
        inference_server_url=selected_url,
        max_new_tokens=2000,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=temperature,
        repetition_penalty=1.03,
    )
    # Create Translator prompt
    template = (
        """translate from {input_language} to {response_language}: \"{input_text}\""""
    )
    prompt = PromptTemplate(
        template=template,
        input_variables=["input_language", "response_language", "input_text"],
    )

    return (
        model,
        model_name,
        languages,
        selected_url,
        sorted_languages,
        parsed_url,
        hostname,
        input_language,
        input_language_index,
        response_language,
        response_language_index,
        llm,
        template,
        prompt,
    )


# def get_languages(model):
#    model, model_name, languages, selected_url, input_language, response_language = configure_model_options(model)
#    languages = languages
#    return languages

##### UI Stuff
## Render Streamlit Web UI
st.title(app_name)

# Add back button
st.markdown(
    f"""
    <style>
        a.myLink:link, a.myLink:visited {{
            color: #C88A2F;  /* primaryColor */
            text-decoration: none;
        }}
        a.myLink:hover, a.myLink:active {{
            color: #C88A2F;  /* textColor */
            text-decoration: underline;
        }}
    </style>
    <a class="myLink" href="{config['website_url']}" target="_self">Back to Main Website</a>
    """,
    unsafe_allow_html=True,
)

# Ask for user input
model = st.selectbox("Choose AI model:", sorted_models, index=model_index)
st.write(
    f"""
    * `bloom` - BigScience BloomZ & mT0
    * `flan` - Google Flan-T5 model
    """
)
(
    model,
    model_name,
    languages,
    selected_url,
    sorted_languages,
    parsed_url,
    hostname,
    input_language,
    input_language_index,
    response_language,
    response_language_index,
    llm,
    template,
    prompt,
) = configure_model_options(model)
input_text = st.text_area("Enter something to translate", "")

if st.button("Translate"):
    response_text = translate_button(
        prompt, llm, input_language, response_language, input_text, hostname
    )
    st.markdown(
        f"""
        <p><b>{hostname} ({temperature}) response:</b></p>
        <div style="
            background-color:#000000; 
            color:white; 
            padding:10px; 
            border-radius:5px; 
            margin-bottom:10px;
        ">
        {response_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

# footer
st.markdown(
    f"""
    <style>
        a.myLink:link, a.myLink:visited {{
            color: #C88A2F;  /* primaryColor */
            text-decoration: none;
        }}
        a.myLink:hover, a.myLink:active {{
            color: #C88A2F;  /* textColor */
            text-decoration: underline;
        }}
    </style>
    <p style='text-align: center;'>
        © 2023 <a class="myLink" href="{config['website_url']}">SolidRusT Networks</a> - <a class="myLink" href="{config['website_url']}/privacy.html">Privacy Policy</a>
    </p>
    """,
    unsafe_allow_html=True,
)
