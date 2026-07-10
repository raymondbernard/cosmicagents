@echo off
title CosmicAgents Launcher

echo === Stopping existing services ===
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8082 " ^| findstr "LISTENING"') do (
    echo Killing PID %%a on port 8082
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":18789 " ^| findstr "LISTENING"') do (
    echo Killing PID %%a on port 18789
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

echo === Starting fcc-server ===
start "fcc-server" cmd /k "cd /d c:\Users\RayBe\OneDrive\Documents\cosmicagents\free-claude-code && .venv\Scripts\activate.bat && fcc-server"

echo Waiting for fcc-server...
:wait_fcc
timeout /t 2 /nobreak >nul
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:8082/health 2>nul | findstr "200" >nul
if errorlevel 1 goto wait_fcc
echo fcc-server ready.

echo === Starting OpenClaw Gateway ===
start "openclaw-gateway" cmd /k "openclaw gateway"

echo Waiting for gateway...
:wait_gw
timeout /t 2 /nobreak >nul
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:18789/health 2>nul | findstr "200" >nul
if errorlevel 1 goto wait_gw
echo Gateway ready.

echo === Opening browsers ===
start "" "http://127.0.0.1:8082/admin"
start "" "http://127.0.0.1:18789/chat"

echo.
echo === Done! ===
echo FCC Admin:  http://127.0.0.1:8082/admin
echo OpenClaw:   http://127.0.0.1:18789/chat
echo Token:      1a5904a909646f2688126eccc30353cd09c202ffee265a9c
