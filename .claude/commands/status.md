---
description: Check chat clients status
allowed-tools: Bash(python:*), Read, Glob
---

Check the status of chat client implementations:

1. List available clients: `ls -la *.py`
2. List client directories: `ls -d */`
3. Check Python version: `python --version`
4. Check if dependencies are installed: `pip list | grep -E "gradio|openai|pyside" || echo "Dependencies not installed"`

Report available chat clients and their status.
