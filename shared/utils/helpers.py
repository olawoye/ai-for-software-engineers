"""Reusable helpers for lesson explorers."""

from pathlib import Path


def list_lessons(base: Path) -> dict[str, list[Path]]:
    modules: dict[str, list[Path]] = {}
    for module_dir in sorted(base.glob("module-*")):
        if module_dir.is_dir():
            lesson_files = sorted(module_dir.glob("*.py"))
            modules[module_dir.name] = lesson_files
    return modules


def describe_lesson(path: Path) -> str:
    lines: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
        for line in content.splitlines()[:4]:
            lines.append(line.strip())
    except FileNotFoundError:
        return "Lesson file missing."
    return " | ".join(lines)
