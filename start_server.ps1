# Start free-claude-code proxy
# Works in any new PowerShell window regardless of PATH state

$env:UV_TOOL_DIR = "C:\uv\tools"
$env:UV_CACHE_DIR = "C:\uv\cache"
$env:UV_LINK_MODE = "copy"
$env:Path = "C:\uv\tools\free-claude-code\Scripts;C:\Users\RayBe\.local\bin;$env:Path"

Write-Host "Starting fcc-server -> Ollama llama3.1 on port 8082..." -ForegroundColor Cyan
Write-Host "Admin UI: http://127.0.0.1:8082/admin" -ForegroundColor Green

& "C:\uv\tools\free-claude-code\Scripts\fcc-server.exe"
