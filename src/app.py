"""Streamlit entry point for navigating the companion lessons."""

from pathlib import Path

import streamlit as st

from shared.utils import describe_lesson, list_lessons, load_settings


def main() -> None:
    st.set_page_config(page_title="AI For Software Engineers Companion", layout="wide")
    st.title("AI For Software Engineers Companion")

    settings = load_settings()
    st.caption("Configured providers: OpenAI, Anthropic, OpenRouter / Ollama")
    st.write(settings)

    todo_base = Path("project-todo")
    modules = list_lessons(todo_base)

    for module, lessons in modules.items():
        with st.expander(module, expanded=False):
            for lesson in lessons:
                st.write(f"**{lesson.name}**: {describe_lesson(lesson)}")
                if st.button(f"Open {lesson.name}", key=f"open-{lesson}"):
                    st.code(lesson.read_text(encoding="utf-8"), language="python")


if __name__ == "__main__":
    main()
