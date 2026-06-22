"""CLI assistant to guide manual editing of the lesson scaffolds."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Guide editing of project-todo lessons.")
    parser.add_argument("lesson", help="Path to the lesson file inside project-todo/.")
    args = parser.parse_args()
    lesson_path = Path(args.lesson)

    if not lesson_path.exists():
        raise SystemExit(f"Lesson file not found: {lesson_path}")

    print("Course Companion CLI")
    print("Lesson:", lesson_path)
    print("Instructions:")
    print("1. Focus on a single lesson file per run.")
    print("2. Update the TODO comments per phase as you implement the content.")
    print("3. Reference project-completed/ for finished implementations.")
    print("----")
    content = lesson_path.read_text(encoding="utf-8")
    print(content)


if __name__ == "__main__":
    main()
