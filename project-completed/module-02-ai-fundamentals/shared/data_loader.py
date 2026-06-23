"""
Data utilities for loading shared corpus across Module 2 lessons.
Provides transparent data sourcing with path indicators.
"""

import json
from pathlib import Path
from typing import Dict, Tuple

def load_sample_corpus() -> Tuple[Dict[str, str], str]:
    """
    Load shared sample corpus from datasets/sample-corpus.json.

    Returns:
        Tuple of (corpus_dict, data_source_path_for_ui)

    Example:
        corpus, data_source = load_sample_corpus()
        st.caption(f"📁 Sample data loaded from: {data_source}")
    """
    # Try loading from module 2 datasets
    module_path = Path(__file__).parent.parent / "datasets" / "sample-corpus.json"

    # Fallback to project-level datasets
    if not module_path.exists():
        module_path = Path(__file__).parent.parent.parent.parent / "datasets" / "sample-corpus.json"

    if module_path.exists():
        with open(module_path, "r") as f:
            data = json.load(f)
            corpus = data.get("sample_corpus", {})
            # Return relative path for UI display
            try:
                display_path = str(module_path.relative_to(Path.cwd()))
            except ValueError:
                # If file is outside cwd, compute relative to project root instead
                project_root = Path(__file__).parent.parent.parent.parent
                try:
                    display_path = str(module_path.relative_to(project_root))
                except ValueError:
                    # Fallback to absolute path
                    display_path = str(module_path)
            return corpus, display_path

    # Fallback to empty dict if file not found
    return {}, "datasets/sample-corpus.json (not found)"
