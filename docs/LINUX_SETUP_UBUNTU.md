# Ubuntu Linux setup guide

This guide covers a fresh Ubuntu setup for Free Claude Code using the shell installer.

## 1. Install prerequisites

On Ubuntu 22.04+ or 24.04+, install the base tools:

```bash
sudo apt update
sudo apt install -y curl git python3 python3-venv build-essential
```

If you want to use the Claude Code or Codex CLIs, install Node.js and npm as well:

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

## 2. Install Free Claude Code

Install or update the proxy and launchers:

```bash
curl -fsSL "https://github.com/Alishahryar1/free-claude-code/blob/main/scripts/install.sh?raw=1" | sh
```

This installs or updates uv, Python 3.14, Claude Code, Codex, and the Free Claude Code tool.

## 3. Initialize configuration

Create the local config directory and template env file:

```bash
fcc-init
```

Edit the generated file:

```bash
nano ~/.fcc/.env
```

Set at least your provider credentials and the `MODEL` value before starting the server.

## 4. Start the proxy

```bash
fcc-server
```

You should see the local admin UI URL in the logs, typically at:

```text
http://127.0.0.1:8082/admin
```

## 5. Run your client

In another terminal, launch Claude Code or Codex through the proxy:

```bash
fcc-claude
```

or:

```bash
fcc-codex
```

## 6. Update later

Re-run the installer whenever you want to pull the latest release:

```bash
curl -fsSL "https://github.com/Alishahryar1/free-claude-code/blob/main/scripts/install.sh?raw=1" | sh
```
