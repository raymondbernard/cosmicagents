# Cosmic Agents

A self-contained, fully local AI agent stack combining **Free Claude Code proxy** (fcc-server) with **OpenClaw** — orchestration for task intake, memory, skills, approvals, and multi-agent coordination.

## Quick Start

```bat
.\start.bat
```

This kills any existing services, starts fcc-server (port 8082) and the OpenClaw gateway (port 18789), then opens both dashboards in your browser.

**FCC Admin:** http://127.0.0.1:8082/admin  
**OpenClaw Chat:** http://127.0.0.1:18789/chat  

When the OpenClaw browser opens, enter the gateway token (printed by start.bat) and click **Connect**.

## Architecture

```
OpenClaw Chat UI
      │
      ▼
OpenClaw Gateway (port 18789)
      │
      ├── Ollama (local, port 11434)  ← llama3.1:latest (default)
      │
      └── Groq API (cloud fallback)   ← llama-3.1-8b-instant / llama-3.3-70b-versatile
```

## Models

| Provider | Model | Notes |
|----------|-------|-------|
| Ollama (local) | `llama3.1:latest` | Default — no rate limits |
| Groq | `llama-3.1-8b-instant` | Fast cloud fallback |
| Groq | `llama-3.3-70b-versatile` | Higher quality cloud option |
| Groq | `moonshotai/kimi-k2-instruct` | Kimi K2 |

Switch models in `~/.openclaw/openclaw.json` → `agents.defaults.model.primary`.

## Key Config Files

| File | Purpose |
|------|---------|
| `start.bat` | One-click launcher — kills, starts, opens browsers |
| `free-claude-code/.env` | fcc-server env (Groq API key, model routing) |
| `~/.openclaw/openclaw.json` | OpenClaw model providers, WhatsApp channel, gateway token |

## WhatsApp Integration

OpenClaw's WhatsApp plugin is installed. To link your number:
1. Run `start.bat`
2. Open OpenClaw → **Settings → Channels**
3. Click **Show QR** and scan with WhatsApp on your phone (**Settings → Linked Devices → Link a Device**)

Allowed number: `+19293617136`

## Workspace Layout

```
start.bat               ← launcher
free-claude-code/       ← fcc-server proxy (git submodule, own repo)
projects/               ← individual project folders
templates/              ← starter templates (Python, Go)
tools/                  ← helper scripts
tests/                  ← workspace-level tests
```

## Requirements

- [Ollama](https://ollama.ai) with `llama3.1:latest` pulled
- Node.js (for OpenClaw: `npm i -g openclaw`)
- Python 3.x + uv (for fcc-server)
- [Groq API key](https://console.groq.com) (optional cloud fallback)

4. Document decisions in docs/
5. Reuse tools/ scripts when possible

### Create a new starter project

Use the helper script from the workspace root:

```bash
python tools/create_starter_project.py starter-python my-new-app
```

Or for Go:

```bash
python tools/create_starter_project.py starter-golang my-new-service
```

The script creates a new folder under projects/ and applies the selected starter template.

For the OpenClaw + Free Claude quick start, see the [free-claude-code README](free-claude-code/README.md#openclaw-integration).
