# SRT Function Calling

This repository contains the code for perfoming function calling with SRT inference engines.

## Installation

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Usage
### Function calling

To run the function call inference with a query, use the following command:

```bash
python functioncall.py --query "I need the current stock price of Tesla (TSLA)"
```

### Json mode

To run the json mode inference with a query, use the following command:

```bash
python jsonmode.py --query "Please return a json object to represent Goku from the anime Dragon Ball Z?"

```

#### Command Line Arguments

- `--model_path`: Path to the model folder (default: "NousResearch/Nous-Hermes-2-PlusPlus-Mistral-7B").
- `--chat_template`: Chat template for prompt formatting (default: "chatml").
- `--num_fewshot`: Option to include few-shot examples (default: None).
- `--load_in_4bit`: Option to load in 4bit with bitsandbytes (default: "False").
- `--query`: Query to be used for function call inference (default: "I need the current stock price of Tesla (TSLA)").
- `--max_depth`: Maximum number of recursive iterations (default: 5).