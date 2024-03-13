import autogen
import streamlit as st

config_list = autogen.config_list_from_json(env_or_file="config.json")

llm_config={
    "request_timeout": 600,
    "seed": 44,                     # for caching and reproducibility
    "config_list": config_list,     # which models to use
    "temperature": 0,               # for sampling
}

agent_assistant = autogen.AssistantAgent(
    name="agent_assistant",
    llm_config=llm_config,
)

agent_proxy = autogen.UserProxyAgent(
    name="agent_proxy",
    human_input_mode="NEVER",           # NEVER, TERMINATE, or ALWAYS 
                                            # TERMINATE - human input needed when assistant sends TERMINATE 
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "agent_output",     # path for file output of program
        "use_docker": False,            # True or image name like "python:3" to use docker image
    },
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
                      Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

def main():
    st.title('AutoGen Streamlit Interface')

    # Input for the prompt
    user_input = st.text_area("Enter your prompt:", "Type here...")

    if st.button('Submit'):
        # Initiate chat with the input prompt
        response = agent_proxy.initiate_chat(
            agent_assistant,
            message=user_input
        )

        # Display the response
        st.write('Response:', response)

if __name__ == "__main__":
    main()
