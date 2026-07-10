# AGENTIC DIRECTIVE

> This file is identical to CLAUDE.md. Keep them in sync.

---

## COSMIC AGENTS SYSTEM

This repo is **Cosmic Agents** — a self-contained, fully local AI agent stack that combines:

- **Free Claude Code proxy** (`fcc-server`) — translates Anthropic Messages API and OpenAI Responses API calls to any backend provider (Ollama, OpenRouter, Gemini, and more).
- **OpenClaw** — orchestration layer for task intake, memory, skills, approvals, and multi-agent coordination.

### Architecture

```
OpenClaw / Claude Code / Codex
        │
        ▼
  fcc-server (port 8082)          ← Anthropic Messages API proxy
        │
        ▼
  Ollama (port 11434)             ← local LLM (llama3.1:latest)
```

### Key File Locations (Windows)

| File | Path | Purpose |
|------|------|---------|
| Proxy managed env | `C:\Users\<you>\.fcc\.env` | Provider, model, port, auth token |
| Proxy launcher | `free-claude-code\start_server.ps1` | Start fcc-server with correct PATH |
| OpenClaw dev config | `C:\Users\<you>\.openclaw-dev\openclaw.json` | OpenClaw provider + model routing |
| OpenClaw workspace | `C:\Users\<you>\.openclaw\workspace-dev\` | Agent workspace files (SOUL.md, IDENTITY.md, etc.) |
| Config example | `docs\openclaw-config-example.json` | Reference openclaw.json for FCC integration |

### Managed Env (`~/.fcc/.env`)

```env
MODEL=ollama/llama3.1:latest
OLLAMA_BASE_URL=http://localhost:11434
ANTHROPIC_AUTH_TOKEN=fcc-no-auth
PORT=8082
```

### OpenClaw Provider Config (`~/.openclaw-dev/openclaw.json`)

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "api": "anthropic-messages",
        "baseUrl": "http://127.0.0.1:8082",
        "apiKey": "fcc-no-auth",
        "models": [
          { "id": "claude-opus-4-5",   "name": "Claude Opus 4.5" },
          { "id": "claude-sonnet-4-5", "name": "Claude Sonnet 4.5" },
          { "id": "claude-haiku-4-5",  "name": "Claude Haiku 4.5" }
        ]
      }
    }
  },
  "gateway": {
    "mode": "local",
    "auth": { "mode": "token", "token": "dev-local-token" }
  }
}
```

> **Note:** Each entry in `models` must be an object with at minimum `id` (string) and `name` (string). Plain strings are not valid.

### Model / Agent Selection

The **free-claude proxy decides which model to use** — OpenClaw (and Claude Code / Codex) simply send whatever model name they were configured with and the proxy routes it to the backend defined in `~/.fcc/.env`.

| `~/.fcc/.env` key | Controls |
|-------------------|----------|
| `MODEL` | Default route — all Claude model names that don't match a tier override |
| `MODEL_OPUS` | Route for Opus-tier requests only |
| `MODEL_SONNET` | Route for Sonnet-tier requests only |
| `MODEL_HAIKU` | Route for Haiku-tier requests only |

To swap the underlying agent/model, change only `MODEL` (or a tier key) in `~/.fcc/.env` and restart `fcc-server`. No changes to OpenClaw config or Claude Code config are needed. The Admin UI at `http://127.0.0.1:8082/admin` lets you do this live without editing the file by hand.

### Starting the Stack

```powershell
# 1. Ensure Ollama is running (starts automatically on Windows after install)
ollama list

# 2. Start the proxy
.\free-claude-code\start_server.ps1

# 3. Verify health
Invoke-RestMethod http://127.0.0.1:8082/health
# → status: healthy
```

### Running an OpenClaw Agent Turn

```powershell
# Local embedded agent (no gateway required)
openclaw --dev agent --local --session-id my-session --message "Your task here."

# With JSON output (shows token usage, model, system prompt report)
openclaw --dev agent --local --session-id my-session --message "Your task here." --json
```

### Verifying the Proxy Directly

```powershell
# Curl test — expects SSE stream with model response
curl.exe -s http://127.0.0.1:8082/v1/messages `
  -H "x-api-key: fcc-no-auth" `
  -H "anthropic-version: 2023-06-01" `
  -H "Content-Type: application/json" `
  -d "@docs/openclaw-config-example.json"
```

### GitHub

- Repo: `https://github.com/raymondbernard/cosmicagents`
- Branch: `main`
- Push: `git push origin main` (authenticated via gh CLI as `raymondbernard`)

---

## CODING ENVIRONMENT

- Install astral uv using "curl -LsSf https://astral.sh/uv/install.sh | sh" if not already installed and if already installed then update it to the latest version
- Install Python 3.14.0 stable using `uv python install 3.14.0` if not already installed (requires uv >=0.9; see `[tool.uv] required-version` in `pyproject.toml`)
- Always use `uv run` to run files instead of the global `python` command.
- Current uv ruff formatter is set to py314 which has supports multiple exception types without paranthesis (except TypeError, ValueError:)
- Read `.env.example` for environment variables.
- All CI checks must pass; failing checks block merge.
- Add tests for new changes (including edge cases).
- Before pushing, prefer `./scripts/ci.sh` (macOS/Linux) or `.\scripts\ci.ps1` (Windows) to run the local CI sequence; requires `uv` on PATH. The local scripts run Ruff in repair mode (`ruff format`, then `ruff check --fix`) before type checking and tests.
- Use `--only` / `--skip` (PowerShell: `-Only` / `-Skip`) to run a subset when iterating; use `--dry-run` to print commands without running them.
- GitHub CI remains check-only for Ruff (`ruff format --check`, `ruff check`) so branch protection verifies committed code.
- Fall back to individual repair commands when debugging local failures: `uv run ruff format`, `uv run ruff check --fix`, `uv run ty check`, `uv run pytest -v --tb=short`. Use GitHub-style checks only when verifying enforcement locally: `uv run ruff format --check`, `uv run ruff check`.
- Do not add `# type: ignore` or `# ty: ignore`; fix the underlying type issue.
- All 5 check IDs are represented in `scripts/ci.sh` / `scripts/ci.ps1` and enforced in `tests.yml` on push/merge (parallel jobs: suppression grep, ruff-format, ruff-check, ty, pytest).
- Branch protection: set **required status checks** to **all** of those statuses (e.g. **Ban type ignore suppressions**, **ruff-format**, **ruff-check**, **ty**, **pytest**—use the exact labels GitHub shows, which may be prefixed with **CI /**). Remove **ci** from required checks if it was previously added for the old gate job.

## IDENTITY & CONTEXT

- You are an expert Software Architect and Systems Engineer.
- Goal: Zero-defect, root-cause-oriented engineering for bugs; test-driven engineering for new features. Think carefully; no need to rush.
- Code: Write the simplest code possible. Keep the codebase minimal and modular.

## ARCHITECTURE PRINCIPLES

- **Shared utilities**: Put shared Anthropic protocol logic in neutral `core/anthropic/` modules. Do not have one provider import from another provider's utils.
- **DRY**: Extract shared base classes to eliminate duplication. Prefer composition over copy-paste.
- **Encapsulation**: Use accessor methods for internal state (e.g. `set_current_task()`), not direct `_attribute` assignment from outside.
- **Provider-specific config**: Keep provider-specific fields (e.g. `nim_settings`) in provider constructors, not in the base `ProviderConfig`.
- **Dead code**: Remove unused code, legacy systems, and hardcoded values. Use settings/config instead of literals (e.g. `settings.provider_type` not `"nvidia_nim"`).
- **Performance**: Use list accumulation for strings (not `+=` in loops), cache env vars at init, prefer iterative over recursive when stack depth matters.
- **Platform-agnostic naming**: Use generic names (e.g. `PLATFORM_EDIT`) not platform-specific ones (e.g. `TELEGRAM_EDIT`) in shared code.
- **No type ignores**: Do not add `# type: ignore` or `# ty: ignore`. Fix the underlying type issue.
- **Complete migrations**: When moving modules, update imports to the new owner and remove old compatibility shims in the same change unless preserving a published interface is explicitly required.
- **Maximum Test Coverage**: There should be maximum test coverage for everything, preferably live smoke test coverage to catch bugs early

## COGNITIVE WORKFLOW

1. **ANALYZE**: Read relevant files. Do not guess.
2. **PLAN**: Map out the logic. Identify root cause or required changes. Order changes by dependency.
3. **EXECUTE**: Fix the cause, not the symptom. Execute incrementally with clear commits.
4. **VERIFY**: Run `./scripts/ci.sh` or `.\scripts\ci.ps1`, plus relevant smoke tests when needed. Confirm the fix via logs or output.
5. **SPECIFICITY**: Do exactly as much as asked; nothing more, nothing less.
6. **PROPAGATION**: Changes impact multiple files; propagate updates correctly.
7. **VERSION**: If the commit touches production files on `main`, bump semver in the same commit (see [Versioning](#versioning-main)).

## VERSIONING (MAIN)

Every commit on `main` that changes a **production file** must include a semver bump in **`pyproject.toml`** in the **same commit**. Do not merge or push prod changes without updating the version.

### Production files

These paths count as production (runtime, packaging, or install surface):

- `api/`, `cli/`, `config/`, `core/`, `messaging/`, `providers/`
- `.env.example`
- `pyproject.toml` (dependencies, scripts, packaging)
- `scripts/install.sh`, `scripts/install.ps1`, `scripts/uninstall.sh`, `scripts/uninstall.ps1`, `scripts/ci.sh`, `scripts/ci.ps1`

These do **not** require a version bump on their own:

- `tests/`, `smoke/`
- Docs and assets: `README.md`, `assets/`, `AGENTS.md`, `CLAUDE.md`
- CI and repo config: `.github/`, `.gitignore`

If a single commit mixes production and non-production edits, still bump the version.

### Semver rules

Use `[project].version` as `MAJOR.MINOR.PATCH`:

- **PATCH** (`x.y.Z+1`): bug fixes, refactors with no user-visible behavior change, dependency updates, packaging/install fixes.
- **MINOR** (`x.Y+1.0`): backward-compatible features—new providers, admin fields, CLI commands, config options, or behavior additions.
- **MAJOR** (`X+1.0.0`): breaking changes—removed or renamed env vars, incompatible API/CLI/default changes, or migrations users must act on.

When unsure between PATCH and MINOR, prefer PATCH for fixes and MINOR for new capability.

### Required steps

1. Classify the change and choose the bump level.
2. Update `version` in `pyproject.toml`.
3. Run `uv lock` so `uv.lock` reflects the new package version.
4. Include the version and lockfile updates in the same commit as the production change.

Example commit on `main` after a packaging fix: bump `1.2.38` → `1.2.39`, run `uv lock`, commit together with the fix.

## SUMMARY STANDARDS

- Summaries must be technical and granular.
- Include: [Files Changed], [Logic Altered], [Verification Method], [Residual Risks] (if no residual risks then say none).

## TOOLS

- Prefer built-in tools (grep, read_file, etc.) over manual workflows. Check tool availability before use.
