from pathlib import Path

import importlib.util


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "copy_project_template.py"
SPEC = importlib.util.spec_from_file_location("copy_project_template", MODULE_PATH)
copy_project_template = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(copy_project_template)


def test_copy_template_updates_python_internal_names(tmp_path: Path) -> None:
    template_dir = tmp_path / "template"
    target_dir = tmp_path / "projects" / "my-new-project"
    template_dir.mkdir(parents=True)
    (template_dir / "my_project_template.py").write_text(
        "from my_project_template import helper\n\n"
        "import my_project_template as pkg\n\n"
        "print(helper(), pkg.__name__)\n",
        encoding="utf-8",
    )

    copy_project_template.copy_template(
        template_dir,
        target_dir,
        project_name="My New Project",
    )

    content = (target_dir / "my-new-project.py").read_text(encoding="utf-8")
    assert "from my_new_project import helper" in content
    assert "import my_new_project as pkg" in content
