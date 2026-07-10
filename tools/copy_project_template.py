from __future__ import annotations

from pathlib import Path
import ast
import re
import shutil
import sys


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "project"


def derive_project_name(project_dir_name: str) -> str:
    return re.sub(r"[-_]+", " ", project_dir_name).title()


def rewrite_python_imports(text: str, project_name: str) -> str:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return text

    project_slug = slugify(project_name)
    module_name = project_slug.replace("-", "_")

    def rewrite_module_path(module_path: str, level: int = 0) -> str:
        if not module_path:
            return module_path

        leading_dots = "".join(re.findall(r"^\.+", module_path))
        stripped = module_path[len(leading_dots):]
        parts = stripped.split(".") if stripped else []
        transformed = []
        for index, part in enumerate(parts):
            lowered = part.lower()
            if level > 0 and index == 0 and lowered in {"my_project_template", "my-project-template", "project_template", "template"}:
                transformed.append(module_name)
            elif level == 0 and index == 1 and lowered in {"my_project_template", "my-project-template", "project_template", "template"}:
                transformed.append(module_name)
            else:
                transformed.append(part)
        return f"{leading_dots}{'.'.join(transformed)}"

    class ImportRewriter(ast.NodeTransformer):
        def visit_Import(self, node: ast.Import) -> ast.AST:
            for alias in node.names:
                if alias.name.startswith("src.") or alias.name.startswith("my_project_template") or alias.name.startswith("my-project-template"):
                    alias.name = rewrite_module_path(alias.name)
            return self.generic_visit(node)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST:
            if node.module:
                node.module = rewrite_module_path(node.module, level=node.level)
            return self.generic_visit(node)

    rewritten = ImportRewriter().visit(tree)
    return ast.unparse(rewritten)


def replace_placeholders_in_file(path: Path, project_name: str) -> None:
    try:
        original_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return

    project_slug = slugify(project_name)
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_SLUG}}": project_slug,
        "{{PROJECT_NAME_SLUG}}": project_slug,
    }

    updated_text = original_text
    for placeholder, replacement in replacements.items():
        updated_text = updated_text.replace(placeholder, replacement)

    if path.suffix == ".py":
        updated_text = rewrite_python_imports(updated_text, project_name)

        python_module_name = project_slug.replace("-", "_")
        module_candidates = {
            path.stem,
            path.stem.replace("-", "_"),
            path.stem.replace("_", "-"),
            path.stem.replace("_template", ""),
            path.stem.replace("-template", ""),
        }
        module_candidates = {
            candidate
            for candidate in module_candidates
            if candidate
            and candidate != python_module_name
            and any(token in candidate.lower() for token in ("template", "project"))
        }
        if not any(line.lstrip().startswith(("import ", "from ")) for line in updated_text.splitlines() if line.strip()):
            for module_name in sorted(module_candidates, key=len, reverse=True):
                if module_name != python_module_name:
                    updated_text = updated_text.replace(module_name, python_module_name)
        else:
            for module_name in sorted(module_candidates, key=len, reverse=True):
                if module_name != python_module_name:
                    updated_text = updated_text.replace(module_name, python_module_name)
            if updated_text != original_text:
                updated_text = rewrite_python_imports(updated_text, project_name)

    if updated_text != original_text:
        path.write_text(updated_text, encoding="utf-8")


def rename_path_by_slug(path: Path, project_slug: str, target_dir: Path | None = None) -> Path | None:
    if path.name == path.stem and not path.is_dir():
        return None

    stem = path.stem
    suffix = path.suffix
    lowered_stem = stem.lower()
    if not any(token in lowered_stem for token in ("template", "project")):
        return None

    if path.is_dir():
        if path.name in {"src", "lib", "app", "tests", "docs", "config", "scripts", "assets"}:
            return None
        new_name = project_slug.replace("-", "_")
    else:
        if suffix in {".py", ".pyi", ".md", ".txt"} and stem not in {"__init__", "main", "setup"}:
            module_slug = project_slug.replace("-", "_")
            has_package_tree = False
            if target_dir is not None:
                has_package_tree = any(
                    child.is_dir() and (child / "__init__.py").exists()
                    for child in target_dir.rglob("*")
                    if child.is_dir()
                )

            if path.parent == target_dir and has_package_tree:
                new_name = f"{module_slug}{suffix}"
            else:
                new_name = f"{project_slug}{suffix}"
        else:
            return None

    new_path = path.with_name(new_name)
    if new_path == path:
        return None
    path.rename(new_path)
    return new_path


def copy_template(
    template_dir: Path,
    target_dir: Path,
    project_name: str | None = None,
) -> Path:
    if not template_dir.exists():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")
    if target_dir.exists():
        raise FileExistsError(f"Target directory already exists: {target_dir}")

    shutil.copytree(template_dir, target_dir)

    resolved_project_name = project_name or derive_project_name(target_dir.name)
    project_slug = slugify(resolved_project_name)

    for path in sorted(
        target_dir.rglob("*"),
        key=lambda item: (len(item.relative_to(target_dir).parts), str(item)),
        reverse=True,
    ):
        if path.is_file():
            replace_placeholders_in_file(path, resolved_project_name)
            rename_path_by_slug(path, project_slug, target_dir)
        elif path.is_dir() and path.name in {"__pycache__"}:
            continue
        elif path.is_dir():
            rename_path_by_slug(path, project_slug, target_dir)

    return target_dir


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print(
            "Usage: python tools/copy_project_template.py <template-name> <new-project-name> [project-name]"
        )
        sys.exit(1)

    workspace_root = Path(__file__).resolve().parent.parent
    template_dir = workspace_root / "templates" / sys.argv[1]
    target_dir = workspace_root / "projects" / sys.argv[2]
    project_name = sys.argv[3] if len(sys.argv) == 4 else None

    copy_template(template_dir, target_dir, project_name=project_name)
    print(f"Created project: {target_dir}")
