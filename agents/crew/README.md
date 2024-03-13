# AutoCrewAI

## Introduction

AutoCrewAI is a python application that with an optional Qt6 GUI that uses the [LangChain Community](https://pypi.org/project/langchain-community/) tools with an agent library to automate the creation of missions and tasks for the [CrewAI](https://pypi.org/project/crewai/) project framework.

## Requirements

- Python 3.9+ (only tested with 3.12.1)
- [CrewAI](https://pypi.org/project/crewai/) project framework
- [LangChain](https://pypi.org/project/langchain/) project framework
- [LangChain Community](https://pypi.org/project/langchain-community/) tools and templates
- [PyYAML](https://pypi.org/project/PyYAML/) template engine
- [PySide6](https://pypi.org/project/PySide6/) (optional for running the **experimental** UI)

## Install

Optional: Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment using one of the following commands, depending on your operating system and shell:

```bash
source venv/bin/activate # Linux, MacOS, WSL2 Shell (bash/zsh)
venv\Scripts\activate.bat # Windows Command (cmd.exe)
venv\Scripts\Activate.ps1 # Windows PowerShell
venv\Scripts\activate # Windows Git Bash (mingw64)
```

Update pip and install the required packages

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

## Configure API keys

Edit the `config.yaml` file and add your API keys. Using the provided `config-example.yaml` file as a template.

```bash
cp config-example.yaml config.yaml
```

## Configure the agent library

```bash
python agent_manager_ui.py
```

## Run AutoCrewAI

Use the UI to run AutoCrewAI. Copy the provided `config-tasks-example.yaml` file to start with a example mission and task list.

```bash
cp config-tasks-example.yaml config-tasks.yaml
python autocrew_ui.py
```

## Notes

Some things to do:

- We'll make a temporary directory to avoid clutter
- TODO: [https://python.langchain.com/docs/integrations/tools/filesystem](https://python.langchain.com/docs/integrations/tools/filesystem)
- working_directory = TemporaryDirectory()
- TODO: [https://python.langchain.com/docs/integrations/tools/bash](https://python.langchain.com/docs/integrations/tools/bash)

## Qt Designer - PySide6

[PySide6 GUI Torotial](https://www.pythonguis.com/pyside6-tutorial/)

```bash
pip install --upgrade pip
pip install --upgrade PySide6
pyside6-designer
```

## Check for duplicate agent names

```bash
grep "^- name:" config-agents.yaml | cut -d ' ' -f 3- | sort | uniq -d
```
