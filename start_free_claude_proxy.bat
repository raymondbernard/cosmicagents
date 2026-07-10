@echo off
setlocal

cd /d "%~dp0"

if "%PORT%"=="" set "PORT=8082"

echo Starting Free Claude Code proxy on port %PORT%...

echo.

where py >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python launcher "py" was not found.
    echo Install Python 3.13+ and try again.
    echo.
    pause
    exit /b 1
)

py -m pip install -q -r requirements.txt 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies failed. Trying to use uv instead...
    py -m uv run python server.py
) else (
    py -m uv run python server.py
)

