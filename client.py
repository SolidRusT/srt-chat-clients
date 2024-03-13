#
import os
import yaml
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain

# Load configuration file. Create from 'config.yaml-example' if you need one
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)
temperature = os.environ.get("TEMPERATURE")
use_huggingface = config["use_huggingface"]
# Configure persona
persona = os.environ.get("PERSONA", "Default")
persona_model = config["personas"].get(persona, config["personas"]["Default"])
persona_model_name = persona_model["name"]
persona_model_description = persona_model["description"]
persona_model_prompt = persona_model["prompt"]
app_name = persona_model_name + " AI"
# Configure inference server
if use_huggingface:
    import random
    from urllib.parse import urlparse
    from langchain.llms import HuggingFaceTextGenInference

    # from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    llms = random.choice(config["tgi_default_urls"])
    model_name = llms["name"]
    model_type = llms["type"]
    model_url = llms["url"]
    server_name = llms["server"]
    parsed_url = urlparse(model_url)
    # example: parsed_url.hostname
    hostname = persona_model_name + " - " + model_name + " on " + server_name
    llm = HuggingFaceTextGenInference(
        inference_server_url=model_url,
        max_new_tokens=2000,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=temperature,
        repetition_penalty=1.03,
        streaming=True,
    )
    # - max_new_tokens: The maximum number of tokens to generate.
    # - top_k: The number of top-k tokens to consider when generating text.
    # - top_p: The cumulative probability threshold for generating text.
    # - typical_p: The typical probability threshold for generating text.
    # - temperature: The temperature to use when generating text.
    # - repetition_penalty: The repetition penalty to use when generating text.
    # - truncate: truncate inputs tokens to the given size
    # - stop_sequences: A list of stop sequences to use when generating text.
    # - seed: The seed to use when generating text.
    # - inference_server_url: The URL of the inference server to use.
    # - timeout: The timeout value in seconds to use while connecting to inference server.
    # - server_kwargs: The keyword arguments to pass to the inference server.
    # - client: The client object used to communicate with the inference server.
    # - async_client: The async client object used to communicate with the server.
else:
    from langchain.chat_models import ChatOpenAI

    hostname = persona_model_name + " OpenAI - " + config["open_ai_model"]
    llm = ChatOpenAI(
        max_tokens=2000,
        openai_api_key=config["openai_api_key"],
        model=config["open_ai_model"],
        temperature=temperature,
        streaming=True,
    )

prompt = PromptTemplate(template=persona_model_prompt, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)
# Render Streamlit UI
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
input_text = st.text_area("Type a question or instruction", "")
if st.button("Send"):
    # Run inference
    response_text = llm_chain.run(input_text)
    # Show result with header
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

# Display footer
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
