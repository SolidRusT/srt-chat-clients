---
description: Set up and test chat clients
allowed-tools: Bash(pip:*), Bash(python:*), Read, Glob
---

Set up the chat clients environment:

1. Create virtual environment if needed: `python -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. For Gradio clients: `pip install -r requirements-gradio.txt`
4. For PySide clients: `pip install -r requirements-pyside.txt`

Test a client:
```bash
python client.py --help
```

Report setup status and any issues.
