# srt-chat-clients

Collection of chat client implementations for SolidRusT Networks AI inference platform.

## Overview

This repository contains various chat interface implementations that connect to the Artemis inference proxy or local vLLM endpoints.

## Available Clients

| Client | Type | Description |
|--------|------|-------------|
| `client.py` | CLI | Basic command-line chat client |
| `client-chat.py` | CLI | Enhanced chat with conversation history |
| `client-pyside.py` | GUI | Qt/PySide desktop application |
| `client-search.py` | CLI | Search-enabled chat client |
| `client-translate.py` | CLI | Translation-focused client |

## Directories

- `agents/` - Agent implementations
- `api-chat/` - API-based chat interfaces
- `assistants/` - Assistant configurations
- `function-calling/` - Function calling examples
- `speech-to-text/` - STT implementations
- `text-to-speech/` - TTS implementations
- `vector-search/` - Vector search integrations

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# For Gradio UI
pip install -r requirements-gradio.txt

# Run basic client
python client.py
```

## Configuration

Copy `config-example.yaml` to `config.yaml` and update with your endpoints:
- Artemis: `https://artemis.hq.solidrust.net/v1`
- Local vLLM: `http://localhost:8000/v1`

---

## Claude Code Configuration

**Commands** (`.claude/commands/`):
| Command | Description |
|---------|-------------|
| `/status` | Check chat clients status |
| `/build` | Set up and test chat clients |

**MCP Tools** (`.mcp.json`):
- `time` - Date calculations via uvx mcp-server-time
- `calculator` - Math operations via uvx mcp-server-calculator
- `github` - PR/issue management
- `gitea` - Gitea PR/issue management
