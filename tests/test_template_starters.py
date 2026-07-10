from __future__ import annotations

from pathlib import Path

from tools import copy_project_template


def test_copy_template_supports_python_and_golang_starters(tmp_path: Path) -> None:
    workspace_root = Path(__file__).resolve().parents[1]

    python_target = tmp_path / "python-starter-project"
    go_target = tmp_path / "golang-starter-project"

    copy_project_template.copy_template(
        workspace_root / "templates" / "starter-python",
        python_target,
        project_name="Python Starter Project",
    )
    copy_project_template.copy_template(
        workspace_root / "templates" / "starter-golang",
        go_target,
        project_name="Golang Starter Project",
    )

    assert python_target.exists()
    assert (python_target / "src" / "python_starter_project").exists()
    assert (python_target / "README.md").exists()

    assert go_target.exists()
    assert (go_target / "cmd" / "golang_starter_project").exists()
    assert (go_target / "go.mod").exists()
