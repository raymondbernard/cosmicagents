@echo off
setlocal

cd /d "%~dp0"

set "GITHUB_USER=%~1"
if not defined GITHUB_USER set "GITHUB_USER=raymondbernard"

echo Configuring Git for GitHub usage...
echo.

git config --global user.name "Ray Bernard"
git config --global user.email "ray.bernard@outlook.com"
git config --global credential.helper manager-core

echo Git identity and credential helper configured.
echo.

if exist .git (
    git remote set-url origin https://github.com/%GITHUB_USER%/free-claude-code.git 2>nul
    if not errorlevel 1 (
        echo Repository remote updated for GitHub.
    ) else (
        echo Could not update the remote automatically.
    )
)

echo.
echo Trying GitHub CLI authentication...
where gh >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    gh auth status >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Starting GitHub login. Follow the browser prompt.
        gh auth login --web
    ) else (
        echo GitHub CLI is already authenticated.
    )
) else (
    echo GitHub CLI was not found. Install it from https://cli.github.com/
)

echo.
echo Setup complete.
pause
