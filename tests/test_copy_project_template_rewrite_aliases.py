from pathlib import Path

import importlib.util


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "copy_project_template.py"
SPEC = importlib.util.spec_from_file_location("copy_project_template", MODULE_PATH)
copy_project_template = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(copy_project_template)


def test_copy_template_rewrites_relative_and_aliased_imports(tmp_path: Path) -> None:
    template_dir = tmp_path / "template"
    target_dir = tmp_path / "projects" / "my-new-project"
    template_dir.mkdir(parents=True)
    (template_dir / "src").mkdir()
    (template_dir / "src" / "my_project_template").mkdir()
    (template_dir / "src" / "my_project_template" / "__init__.py").write_text(
        "from .my_project_template.module import helper as alias_helper\n",
        encoding="utf-8",
    )
    (template_dir / "src" / "my_project_template" / "module.py").write_text(
        "import src.my_project_template.module as pkg\n",
        encoding="utf-8",
    )

    copy_project_template.copy_template(
        template_dir,
        target_dir,
        project_name="My New Project",
    )

    init_content = (target_dir / "src" / "my_new_project" / "__init__.py").read_text(encoding="utf-8")
    module_content = (target_dir / "src" / "my_new_project" / "module.py").read_text(encoding="utf-8")
    assert "from .my_new_project.module import helper as alias_helper" in init_content
    assert "import src.my_new_project.module as pkg" in module_content
