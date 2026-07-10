from pathlib import Path

import importlib.util


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "copy_project_template.py"
SPEC = importlib.util.spec_from_file_location("copy_project_template", MODULE_PATH)
copy_project_template = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(copy_project_template)


def test_copy_template_renames_project_slug_in_filenames(tmp_path: Path) -> None:
    template_dir = tmp_path / "template"
    target_dir = tmp_path / "projects" / "my-new-project"
    template_dir.mkdir(parents=True)
    (template_dir / "my_project_template.py").write_text("print('ok')\n", encoding="utf-8")
    (template_dir / "docs").mkdir()
    (template_dir / "docs" / "my-project-template.md").write_text("hello\n", encoding="utf-8")

    copy_project_template.copy_template(
        template_dir,
        target_dir,
        project_name="My New Project",
    )

    assert (target_dir / "my-new-project.py").exists()
    assert (target_dir / "docs" / "my-new-project.md").exists()
