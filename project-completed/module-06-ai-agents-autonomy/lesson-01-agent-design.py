"""Lesson 01: AI agent design fundamentals."""

def agent_tasks():
    return ["observation", "reasoning", "action", "reflection"]


def sample_agent_prompt(task: str) -> str:
    return f"Agent tasked with: {task}. Provide next command and confidence."


if __name__ == "__main__":
    print(agent_tasks())
    print(sample_agent_prompt("debug pipeline"))
