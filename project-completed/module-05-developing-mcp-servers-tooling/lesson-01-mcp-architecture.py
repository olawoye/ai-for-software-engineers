"""Lesson 01: MCP server architecture."""

def server_summary():
    return {
        "name": "lesson-mcp-backend",
        "tools": ["FastAPI", "Uvicorn"],
        "auth": "API keys"
    }


if __name__ == "__main__":
    print(server_summary())
