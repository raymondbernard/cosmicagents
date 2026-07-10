# Cosmic Agents Workspace

This workspace is organized to support multiple projects with a consistent and scalable structure.

## Top-level layout

- projects/ - individual project folders, with the starter Python sample project in place
- shared/ - reusable assets, libraries, and common utilities
- templates/ - starter templates for new projects, including starter-python and starter-golang
- docs/ - documentation and planning notes
- tools/ - helper scripts and automation

## Recommended project structure

Each project should follow this pattern:

- docs/ - requirements, architecture, and notes
- src/ - application code
- tests/ - automated tests
- config/ - environment and configuration files
- scripts/ - setup and maintenance scripts
- assets/ - images, diagrams, and other static files
- AGENTS.md - project-specific AI agent instructions
- CLAUDE.md - project-specific Claude instructions

## Suggested workflow

1. Create a new project in projects/
2. Copy the structure from templates/starter-python/ for Python or templates/starter-golang/ for Go
3. Keep shared logic in shared/
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
