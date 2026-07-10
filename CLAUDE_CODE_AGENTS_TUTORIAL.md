# Best Practices for Claude Code Agents

This repository already includes agent guidance in [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md). Claude Code works best when you give it clear context, tight scope, and a verification step.

## 1. Start with the repository context

Before requesting a change, make sure the agent can see the repo rules:

```bash
cd free-claude-code
```

The agent should inherit:
- repository conventions from [AGENTS.md](AGENTS.md)
- coding environment and validation expectations from [CLAUDE.md](CLAUDE.md)

## 2. Give the agent a narrow, specific task

Good prompts are focused and outcome-driven.

Examples:

```text
Add a Windows batch launcher that starts the proxy locally.
```

```text
Create a short README for the Ollama Windows setup and include a quick start.
```

```text
Fix the failing parser behavior and add tests for the edge cases.
```

Avoid broad prompts like:

```text
Improve the whole project.
```

```text
Make this better in every way.
```

## 3. Be explicit about constraints

If you want the agent to preserve behavior, say so directly.

Examples:

```text
Keep the existing API behavior the same. Only add a Windows-friendly launcher.
```

```text
Do not change the public config format. Add the docs and helper script only.
```

```text
Preserve backward compatibility and avoid touching unrelated modules.
```

## 4. Ask for debugging in a structured way

When something is broken, ask the agent to investigate the cause first rather than patching blindly.

Good debugging prompt:

```text
Investigate this issue root cause first, then implement the smallest fix and verify it.
```

A more concrete version:

```text
The proxy launcher is failing on Windows. Reproduce the issue, identify the cause, and fix it with the smallest change possible.
```

Useful follow-ups:

```text
Show the failing behavior and explain the root cause before changing code.
```

```text
If the fix changes behavior, call out the impact clearly.
```

## 5. Ask for tests, not just code

For logic changes, request validation explicitly.

Examples:

```text
Add unit tests for the new edge cases and keep the current behavior intact.
```

```text
If this change affects parsing or config handling, add regression tests.
```

```text
Run the relevant tests and report the results.
```

If you are working on a bug, a strong prompt is:

```text
Write a regression test that captures the bug first, then fix the implementation.
```

## 6. Ask for verification and evidence

A reliable workflow is:

```text
Implement the change, run the relevant checks, and report what passed or failed.
```

For this repository, a good follow-up is:

```text
Run the relevant local checks, summarize the results, and call out any remaining issues.
```

## 7. Use a repeatable GitHub workflow

Agents can help with GitHub tasks, but they should be guided carefully.

Example prompt:

```text
Prepare this repository change for GitHub: stage the relevant files, create a commit, and push to the configured remote.
```

A safer version:

```text
Create a local commit for the documented change, but do not push until I confirm the remote.
```

When a remote is involved, ask for specifics:

```text
Verify the current Git remote, then update it to the correct repository if needed.
```

Useful GitHub workflow prompts:

```text
Check git status first, then summarize the changes before committing.
```

```text
Create a commit message that explains the scope clearly.
```

```text
If the push fails, report the exact GitHub error and the next step.
```

## 8. Example workflow for a real task

### Example: add a helper script

Prompt:

```text
Add a Windows helper script for starting the proxy locally. Keep the change minimal and do not alter the existing runtime behavior.
```

Follow-up:

```text
Add a short README entry and verify the script path is correct.
```

### Example: fix a bug

Prompt:

```text
Investigate the Windows launcher failure, reproduce it if possible, identify the root cause, and implement the smallest fix.
```

Follow-up:

```text
Add a regression test or an explicit validation step so this does not break again.
```

## 9. Write good code comments

Comments should explain why something exists, not just restate the code.

Good comments:

```python
# Keep the proxy on localhost to avoid exposing the admin UI externally.
```

```python
# This path is intentionally limited to Windows because the launcher uses batch semantics.
```

Avoid comments like:

```python
# Increment i by 1
```

```python
# This function does something
```

When asking an agent to add comments, be specific:

```text
Add concise comments only where the intent is not obvious from the code.
```

```text
Do not add redundant comments; explain the rationale or the non-obvious constraint.
```

## 10. Recommended prompt template

Use this when you want predictable results:

```text
In this repo, implement the following change:
- goal: [what you want]
- constraints: [what must stay the same]
- validation: [tests or checks to run]
- output: [summary, diff, or next steps]
```

## 11. Best practices summary

- Keep prompts specific and scoped.
- Ask for root cause analysis before making fixes.
- Require tests for behavior changes.
- Ask for verification evidence, not just assumptions.
- Review the diff before accepting the work.
- Make GitHub actions explicit and safe.
- Prefer small, reviewable changes over large rewrites.

This approach helps the agent stay useful, predictable, and aligned with the repository rules.
