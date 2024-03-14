# SRT Chat Clients

A collection of chat clients featured on solidrust.net.

## Flavours

- [Streamlit Clients](./client.py) used with [Requirements](./requirements.txt)
- [Gradio Clients](./client-chat.py) used with [Requirements](./requirements-gradio.txt)
- [Desktop Clients](./client-pyside.py) used with [Requirements](./requirements-pyside.txt)

## Configuration

All the configuration for the clients is done in the [config.yaml](./config-example.yaml) file. Used the provided example to create your own.

## Launching

As we have migrated to Ansible and primarily use a `systemd` service template in linux, these legacy launchers are provided as an example.

 - [Launch ALL](./launch-all.sh) intends to launch a list of chat clients all at once.
 - [Launch](./launch.sh) is intended to be called by Launch ALL, but can be used to launch a specific chat app.
 - [Launch Custom](./launch-custom.sh) is intended to launch clients using attitional parameters. It was made to enable developing a newer pattern of client (gradio).
 - [Launch Chat](./launch-chat.sh) was an earlier version of Launch Custom, that was used before migration to ansible.

## Libraries

 - [Prompt Formatters](./prompt_formatters.py) functions for abstracting the various types of model prompt templates.
 - **WIP** [Conversation Manager](./conversation_manager.py) class of functions to manage chat history.

## Supplementaty apps

We have developped several supplementary example apps that intent to be integrated into the various chat clients. Some of these projects are:

 - [text-to-speech](/text-to-speech) Production ready text-to-speech example.
 - [speech-to-text](./speech-to-text) Production ready speech to text example.
 - [vector-search](./vector-search) Example of using a vector store as long-term memory.
 - [assistants](./assistants) Framework example for a customized self-hosted personal assistant.
 - [agents](./agents) Agent framework examples, using AutoGEN, CrewAI, ect..

## Related integrations

 - [Inference Backends](https://github.com/SolidRusT/srt-inference-backends) collection of launchers for verious self-hosted inference backends for supporting these Chat Clients.
