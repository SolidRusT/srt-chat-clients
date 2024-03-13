import os
import yaml
import random
from urllib.parse import urlparse
import streamlit as st
from langchain import PromptTemplate, LLMChain, HuggingFaceTextGenInference
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import load_tools, initialize_agent, AgentType

# Load configuration
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

persona = os.environ.get("PERSONA")
temperature = os.environ.get("TEMPERATURE")
app_name = persona + " AI"
use_huggingface = config["use_huggingface"]
llms = random.choice(config["tgi_default_urls"])
model_name = llms["name"]
model_type = llms["type"]
model_url = llms["url"]
server_name = llms["server"]
parsed_url = urlparse(model_url)
# example: parsed_url.hostname

# Toggle between HuggingFace and OpenAI inference
if use_huggingface:
    hostname = persona + " AI - " + server_name
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
else:
    hostname = persona + " OpenAI - " + config["open_ai_model"]
    llm = ChatOpenAI(
        max_tokens=2000,
        openai_api_key=config["openai_api_key"],
        model=config["open_ai_model"],
        temperature=temperature,
        streaming=True,
    )

tools = load_tools(["ddg-search", "wikipedia"])

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
    # verbose=True
)

# Render Streamlit Web UI
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

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I'm a chatbot who can search the web. How can I help you?",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
