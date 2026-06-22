"""Agent utilities for lesson scaffolds."""

def agent_chain_description(steps: list[str]) -> str:
    return " -> ".join(steps)
