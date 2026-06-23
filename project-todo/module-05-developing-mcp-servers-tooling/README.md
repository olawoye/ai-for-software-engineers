# Module 5: Developing MCP Servers & Tooling — TODO Scaffold

This is the student workbook for building MCP servers. Each lesson builds complete tool and resource servers with PHASE comments.

## Lessons

### Lesson 5.3: Personal Knowledge Server

**PHASE 1:** MCPServer basics and JSON-RPC
- Create MCPServer class
- Implement list_resources and list_tools

**PHASE 2:** Resources registration
- Register file-based resources
- Implement resource reading

**PHASE 3:** Tools registration
- Register search tool
- Implement tool handlers

### Lesson 5.4: Email Analyst Server

**PHASE 1:** Tool definition
- Define email parsing tools
- Create input schemas

**PHASE 2:** Tool handlers
- Implement email parsing
- Add categorization and analysis

**PHASE 3:** Workflow integration
- Combine multiple tools
- Create complex workflows

### Lesson 5.5: Security & Guardrails

**PHASE 1:** Permissions
- Role-based access control
- Check permissions

**PHASE 2:** Validation
- Validate inputs
- Sanitize user data

**PHASE 3:** Rate limiting
- Implement rate limiter
- Track usage

### Lesson 5.6: MCP Toolkit (Capstone)

**PHASE 1:** Combine tools
- Add multiple tool categories
- Register permissions

**PHASE 2:** Complete workflows
- Test tool interactions
- Demonstrate capabilities

**PHASE 3:** Production readiness
- Error handling
- Deployment patterns

## Shared Modules

- **mcp_server.py**: Base MCPServer class, JSON-RPC handling
- **resources.py**: FileResource, KnowledgebaseResource
- **tools.py**: EmailTools, DataTools, TextTools
- **permissions.py**: PermissionManager, ActionValidator
- **validation.py**: SchemaValidator, InputSanitizer, RateLimiter
- **registry.py**: ToolRegistry, ResourceRegistry

Each with PHASE 1-3 comments.

## Running Code

```bash
source .venv/bin/activate
pip install -r requirements-module-05.txt
python lesson-03-personal-knowledge-server.py
python lesson-04-email-analyst-server.py
python lesson-05-security-guardrails.py
python lesson-06-mcp-toolkit-server.py
```

## Next Steps

After Module 5, ready for Module 6: AI Agents & Autonomy
