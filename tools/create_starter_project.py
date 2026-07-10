from __future__ import annotations

import shutil
import sys
from pathlib import Path

from copy_project_template import copy_template


def main() -> int:
    if len(sys.argv) not in (3, 4):
        print(
            "Usage: python tools/create_starter_project.py <starter-name> <new-project-name> [project-name]"
        )
        print("Examples:")
        print("  python tools/create_starter_project.py starter-python my-new-app")
        print("  python tools/create_starter_project.py starter-golang my-new-service")
        return 1

    starter_name = sys.argv[1]
    project_dir_name = sys.argv[2]
    project_name = sys.argv[3] if len(sys.argv) == 4 else None

    workspace_root = Path(__file__).resolve().parent.parent
    template_dir = workspace_root / "templates" / starter_name
    target_dir = workspace_root / "projects" / project_dir_name

    if not template_dir.exists():
        print(f"Unknown starter template: {starter_name}", file=sys.stderr)
        print("Choose one of: starter-python, starter-golang", file=sys.stderr)
        return 2

    if target_dir.exists():
        print(f"Target project already exists: {target_dir}", file=sys.stderr)
        return 3

    copy_template(template_dir, target_dir, project_name=project_name)
    print(f"Created project from {starter_name}: {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
