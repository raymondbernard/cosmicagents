# Ollama Windows Setup

This guide gives you a simple local setup for using Ollama with the Free Claude Code proxy on Windows.

## Quick Start

1. Install Ollama for Windows
   - Download it from https://ollama.com/download/windows
   - Install and restart your terminal

2. Pull a model
   ```powershell
   ollama pull llama3.2
   ```

3. Start Ollama
   ```powershell
   ollama serve
   ```
   Keep this terminal open.

4. Start the proxy
   - Double-click [start_free_claude_proxy.bat](start_free_claude_proxy.bat)
   - Or run this in PowerShell:
   ```powershell
   .\start_free_claude_proxy.bat
   ```

5. Open the Admin UI
   - Open the local URL shown in the proxy terminal, usually:
   ```text
   http://127.0.0.1:8082/admin
   ```

6. Configure Ollama in the Admin UI
   - Set `OLLAMA_BASE_URL` to:
   ```text
   http://localhost:11434
   ```
   - Set `MODEL` to a value such as:
   ```text
   ollama/llama3.2
   ```

7. Test it
   - Start using Claude Code or Codex through the proxy
   - If needed, confirm the model exists with:
   ```powershell
   ollama list
   ```

## Notes

- Do not add `/v1` to `OLLAMA_BASE_URL`.
- The proxy expects the base URL to be the Ollama root, such as `http://localhost:11434`.
- If the service does not respond, make sure `ollama serve` is still running.

## Troubleshooting

### Ollama is not found
Install Ollama from the official Windows installer and reopen PowerShell.

### Proxy cannot reach Ollama
Check that the Ollama server is running on port 11434.

### Model not available
Pull the model again:
```powershell
ollama pull llama3.2
```
