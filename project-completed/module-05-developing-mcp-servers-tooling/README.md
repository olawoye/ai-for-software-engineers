# Module 5: Developing MCP Servers & Tooling

This module introduces the Model Context Protocol (MCP), the emerging interoperability standard that allows AI systems to securely interact with tools, data sources, APIs, applications, and enterprise systems. Learn how modern AI assistants discover, access, and utilize external capabilities through standardized protocols.

By the end of this module, students will be able to build MCP servers, expose resources and tools, connect real-world systems, implement security controls, and create reusable MCP toolkits that serve as the foundation for autonomous AI agents.

## Module Overview

**Learning Path:**
1. **Lesson 5.1** (Talking Head): MCP concepts and ecosystem
2. **Lesson 5.2** (Talking Head): JSON-RPC & environments
3. **Lesson 5.3** (Code): Your First MCP Server - Personal Knowledge
4. **Lesson 5.4** (Code): Connecting Real-World Tools - Email Analyst
5. **Lesson 5.5** (Code): Debugging & Security - Permission Sandboxes
6. **Lesson 5.6** (Code): Capstone - Complete MCP Toolkit

## Lessons

### Lesson 5.1: Introduction to MCP
**Type:** Talking Head (No Code)

Introduction to MCP as the interoperability layer for AI systems.

---

### Lesson 5.2: JSON-RPC & Environments
**Type:** Talking Head (No Code)

Foundation concepts for MCP communication protocols.

---

### Lesson 5.3: Your First MCP Server - Personal Knowledge Server
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Template Pattern:** Method-level reusable template

Build a reusable MCP server that exposes local files and documents as resources, with tools for searching and retrieving knowledge base content.

#### Core Template Method
The lesson demonstrates **`create_knowledge_server()`**, the foundational server initialization pattern that learners can extract and adapt for their own projects.

**Method Signature:**
```python
def create_knowledge_server(
    knowledge_dir: str,
    server_name: str = "PersonalKnowledge",
    file_extensions: List[str] | None = None,
) -> MCPServer:
```

**Returns:** Configured MCPServer with:
- Registered Resources for each discovered file
- Tools: `search_knowledge()`, `get_document()`, `get_knowledge_stats()`
- Ready to accept JSON-RPC requests from AI clients

#### Run Instructions
```bash
source .venv/bin/activate
pip install -r requirements-module-05.txt
python lesson-03-personal-knowledge-server.py
```

**Demonstrations:**
1. **Core Template Execution** — Show `create_knowledge_server()` initializing with sample files
2. **Resource Discovery** — List registered resources with URIs and metadata
3. **Tool Invocation** — Execute search and retrieval tools with test queries
4. **JSON-RPC Protocol** — Show actual JSON-RPC request/response pairs

#### What You'll Learn
- **Resource Registration:** Discover files and expose them as discoverable resources
- **Tool Definition:** Create tools with input schemas for client requests
- **File Handling:** Implement secure file access patterns
- **JSON-RPC Protocol:** Understand MCP client-server communication
- **Template Reusability:** Extract this method for your own knowledge sources

#### Key Concepts
- MCP Resources as discoverable documents
- Tool handlers with structured input schemas
- JSON-RPC 2.0 request/response protocol
- File discovery and registration patterns
- Closure patterns for handler functions

#### Business Scenario
*A software engineer wants Claude, Cursor, or another MCP-enabled client to access local project files, notes, and documentation repositories.*

#### Template Reusability
This method is designed for extraction into your own projects. To adapt it:
1. Change `knowledge_dir` to point to your data source
2. Adjust `file_extensions` for your file types
3. Customize tool implementations (search, retrieval, analysis)
4. Add metadata fields for your domain
5. Implement additional tools as needed

#### Data Flow
```
Local Files (knowledge_dir)
    ↓
discover via file_extensions
    ↓
register as Resources (file://)
    ↓
AI Client (Claude, Cursor, etc.)
    ↓
list resources / call tools (JSON-RPC)
    ↓
search_knowledge() / get_document() / get_knowledge_stats()
    ↓
Return JSON results to client
```

---

### Lesson 5.4: Connecting Real-World Tools - Email Analyst Server
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Template Pattern:** Method-level reusable template

Build an MCP server that analyzes emails, extracts business intelligence, and routes messages for action. Demonstrates how MCP enables AI systems to participate in real business workflows.

#### Core Template Method
The lesson demonstrates **`create_email_analyst_server()`**, the foundational email analysis server initialization that learners can extract and adapt for their own email/messaging systems.

**Method Signature:**
```python
def create_email_analyst_server(
    server_name: str = "EmailAnalyst",
) -> MCPServer:
```

**Returns:** Configured MCPServer with:
- 5 registered tools for email analysis
- Tools: `parse_email()`, `categorize_email()`, `analyze_sentiment()`, `extract_action_items()`, `extract_keywords()`
- Ready to accept JSON-RPC requests from AI clients

#### Run Instructions
```bash
source .venv/bin/activate
pip install -r requirements-module-05.txt
python lesson-04-email-analyst-server.py
```

**Demonstrations:**
1. **Tool Registration** — Show all 5 tools with input schemas
2. **Email Analysis Pipeline** — Process complex email through full analysis
3. **Business Workflow** — Show email triage and routing decisions

#### What You'll Learn
- **Complex Tool Schemas:** Design inputs with multiple fields (email structure)
- **Sentiment & Urgency:** Extract emotion and priority indicators from text
- **Business Intelligence:** Identify action items, categories, and routing rules
- **Tool Composition:** Combine tools into workflows (parse → analyze → route)
- **Enterprise Integration:** Enable AI participation in business processes

#### Key Concepts
- MCP tool integration with external utilities (EmailTools, TextTools)
- JSON-RPC for email analysis requests
- Business workflow automation patterns
- Sentiment analysis and urgency scoring
- Email triage and routing logic

#### Business Scenario
*"A manager wants to know which customer emails require follow-up, which messages remain unanswered, and which communications should be escalated."*

#### Tools Provided
1. **parse_email()** — Structure raw email into components (sender, subject, body, sentiment)
2. **categorize_email()** — Classify message type (meeting, support, report, general)
3. **extract_action_items()** — Find TODOs and action requirements
4. **analyze_sentiment()** — Determine tone and urgency level
5. **extract_keywords()** — Identify important topics

#### Template Reusability
This method is designed for extraction into your own projects. To adapt it:
1. Add email data source (Gmail API, IMAP, Slack, Teams, webhooks)
2. Customize categorization rules for your business
3. Add domain-specific sentiment/urgency indicators
4. Implement custom routing logic
5. Integrate with ticketing or workflow systems

#### Data Flow
```
Raw Email (sender, subject, body)
    ↓
parse_email() → Structure + sentiment
    ↓
categorize_email() → Type classification
    ↓
analyze_sentiment() → Urgency & priority
    ↓
extract_action_items() → TODO items
    ↓
extract_keywords() → Topic extraction
    ↓
AI Client receives full analysis
    ↓
Route via workflow rules:
  - URGENT + SUPPORT → Escalate
  - MEETING_REQUEST → Calendar
  - STATUS_REPORT → Archive & notify
  - ACTION_ITEMS → Create tickets
```

#### Workflow Integration
Email analysis tools compose into automated triage workflows. Combined with security guardrails (Lesson 5.5), these tools scale email processing without human bottlenecks.

---

### Lesson 5.5: Debugging & Security - Permission Sandboxes
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Template Pattern:** Method-level reusable wrapper

Build security guardrails that protect MCP servers from unsafe operations, data leaks, and privilege escalation. Demonstrates how to wrap existing servers with validation, logging, and access control.

#### Core Template Method
The lesson demonstrates **`add_security_guardrails()`**, the foundational security wrapper that learners can extract and use to protect any MCPServer.

**Method Signature:**
```python
def add_security_guardrails(
    server: MCPServer,
    permission_strategy: str = "read_only",
    enable_audit_logging: bool = True,
    enable_approval_workflow: bool = False,
    user_id: str = "default_user",
) -> MCPServer:
```

**Returns:** Same MCPServer interface, but all tool execution now intercepts with:
- Permission checking (role-based access control)
- Input sanitization (path traversal prevention)
- Secret scrubbing (protect credentials in logs)
- Audit logging (complete execution trail)
- Optional approval workflow for dangerous operations

#### Run Instructions
```bash
source .venv/bin/activate
pip install -r requirements-module-05.txt
python lesson-05-security-guardrails.py
```

**Demonstrations:**
1. **Permission System** — Show role-based access matrix (USER, POWER_USER, ADMIN)
2. **Input Sanitization** — Demonstrate path traversal and injection protection
3. **Secret Scrubbing** — Show removal of API keys/passwords from logs
4. **Audit Trail** — Display complete execution log with timestamps
5. **Approval Workflow** — Show human-in-the-loop for dangerous operations

#### What You'll Learn
- **Role-Based Access Control:** Enforce permissions before tool execution
- **Input Validation:** Sanitize paths, emails, and user inputs
- **Secret Protection:** Automatically remove credentials from logs
- **Audit Logging:** Maintain compliance trail with operation hashes
- **Approval Workflows:** Require human review for dangerous operations
- **Defense in Depth:** Layer multiple security mechanisms

#### Key Concepts
- Permission inference from tool names (delete → DELETE, write → WRITE, etc.)
- Closure-based handler wrapping to intercept execution
- Regex-based secret scrubbing for common patterns
- Hash-based audit trails (preserve privacy, enable verification)
- Role strategy mapping to enforce different security postures

#### Business Scenario
*"An organization wants AI systems to access business tools while preventing data leaks, accidental deletions, privilege escalation, and unsafe actions."*

#### Security Features
1. **Permission Strategy** — "read_only" (default), "power_user", "admin"
2. **Input Sanitization** — Clean paths, emails, prevent injection attacks
3. **Secret Protection** — Remove API keys, passwords, tokens from logs
4. **Audit Logging** — Track all operations with user, timestamp, result hash
5. **Approval Workflow** — Flag delete/drop operations for human review

#### Template Reusability
This method wraps ANY MCPServer (Knowledge, Email, Custom). To adapt it:
1. Wrap existing server: `secure_server = add_security_guardrails(my_server, 'read_only')`
2. Adjust permission_strategy for your use case
3. Customize secret patterns for your environment
4. Add resource-specific permissions using ResourcePermissions
5. Implement approval handlers for your workflow system

#### Permission Matrix
```
Operation    | USER  | POWER_USER | ADMIN
─────────────┼───────┼────────────┼─────
READ         | ✅    | ✅         | ✅
WRITE        | ❌    | ✅         | ✅
DELETE       | ❌    | ❌         | ✅
EXECUTE      | ❌    | ✅         | ✅
ADMIN        | ❌    | ❌         | ✅
```

#### Data Flow
```
Tool Call Request
    ↓
add_security_guardrails() wrapper intercepts
    ├─ Check 1: Permission validation
    │   └─ If denied → Return error + audit log
    ├─ Check 2: Dangerous operation detection
    │   └─ If dangerous + approval → Return pending + audit log
    ├─ Check 3: Input sanitization
    │   └─ Clean paths, emails, remove secrets
    ├─ Check 4: Execute original handler
    │   └─ With sanitized inputs
    ├─ Check 5: Scrub secrets from results
    ├─ Check 6: Log to audit trail
    └─ Return result to client

Audit Trail Entry:
  Timestamp | Tool | User | Operation | Args Hash | Success | Result Hash
```

#### Integration with Other Lessons
- **5.3 (Knowledge Server):** Wrap to limit READ access to documents
- **5.4 (Email Analyst):** Wrap to require approval for deletions
- **5.6 (MCP Toolkit):** Apply security to all tools in single call

---

### Lesson 5.6: MCP Toolkit (Capstone)
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Template Pattern:** Orchestration method combining all module concepts

This capstone lesson combines everything learned throughout Module 5 into a complete, production-ready MCP toolkit for autonomous AI agents (Module 6). Demonstrates how to orchestrate multiple MCP servers, implement cross-tool workflows, and apply unified security across all tools.

#### Core Template Method
The lesson demonstrates **`create_mcp_toolkit()`**, the orchestration method that combines:
- Personal Knowledge Server (lesson 5.3)
- Email Analyst Server (lesson 5.4)
- Security Guardrails (lesson 5.5)

**Method Signature:**
```python
def create_mcp_toolkit(
    knowledge_dir: str = "./knowledge",
    email_data_dir: str = "./emails",
    permission_strategy: str = "power_user",
    enable_audit_logging: bool = True,
) -> MCPServer:
```

**Returns:** Complete MCPServer with:
- Unified tool registry (10 tools total)
- Categorized by type (knowledge, email, system)
- Shared security layer applied to all tools
- Complete audit trail for compliance
- Ready for agent integration

#### Run Instructions
```bash
source .venv/bin/activate
pip install -r requirements-module-05.txt
python lesson-06-mcp-toolkit-server.py
```

#### Demonstrations (5 Total)

1. **Tool Discovery** — Show all tools grouped by category (knowledge: 2, email: 5, system: 3)
2. **Resource Access** — Demonstrate querying knowledge base with example searches
3. **Tool Execution** — Execute email analysis pipeline on sample email
4. **Cross-Tool Workflow** — Link email analysis results to knowledge base search
5. **Security Across Toolkit** — Show unified permission matrix and audit trail

#### What You'll Learn
- **Tool Orchestration:** Combine resources and tools from different sources
- **Tool Registry:** Implement discovery mechanism for agents
- **Cross-Tool Workflows:** Compose tools into complex multi-step processes
- **Unified Security:** Apply consistent permissions across all tools
- **Audit Compliance:** Maintain complete execution trail
- **Agent Readiness:** Build toolkit that agents can discover and use

#### Toolkit Structure

**Knowledge Tools (2):**
- `search_knowledge` — Full-text search across files
- `get_document` — Retrieve specific documents

**Email Tools (5):**
- `parse_email` — Structure email data
- `categorize_email` — Classify by type
- `analyze_sentiment` — Detect urgency
- `extract_action_items` — Find TODOs
- `extract_keywords` — Extract topics

**System Tools (3):**
- `get_toolkit_info` — Toolkit metadata
- `list_tools` — Tool discovery
- `get_audit_trail` — Execution history

#### ToolkitRegistry Class
Manages tool discovery and organization:
- `register_tool(tool, category)` — Add tool to category
- `register_resource(resource)` — Register knowledge base
- `get_summary()` — Return discovery metadata

#### Cross-Tool Workflow Example

```
Email Arrives
    ↓
analyze_sentiment() → [URGENT]
    ↓
extract_keywords() → [database, connection, ...]
    ↓
search_knowledge() → [matching docs]
    ↓
get_document() → [full context]
    ↓
compose_response() → [informed reply with references]
    ↓
Agent returns result
```

#### Permission Matrix (Unified)
```
Operation    | READ_ONLY | POWER_USER | ADMIN
─────────────┼───────────┼────────────┼──────
search_*     | ✅        | ✅         | ✅
get_*        | ✅        | ✅         | ✅
analyze_*    | ✅        | ✅         | ✅
extract_*    | ✅        | ✅         | ✅
parse_*      | ✅        | ✅         | ✅
list_tools   | ✅        | ✅         | ✅
delete_*     | ❌        | ❌         | ✅
modify_*     | ❌        | ❌         | ✅
```

#### Template Reusability
This method can be adapted for:
1. Add new tool categories (support, sales, accounting, etc.)
2. Change permission strategy per environment (dev, staging, prod)
3. Customize audit logging and approval workflows
4. Integrate with external systems (CRM, help desk, databases)
5. Deploy as standalone MCP server or within larger platform

#### Data Flow
```
Agent Requests Tool Discovery
    ↓
get_toolkit_info() / list_tools()
    ↓
ToolkitRegistry returns all tools by category
    ↓
Agent selects tool(s) for workflow
    ↓
Tool execution intercepts via security layer
    ├─ Permission check
    ├─ Input sanitization
    ├─ Execute original tool
    ├─ Scrub secrets from output
    └─ Log to audit trail
    ↓
Agent receives result + audit record
```

#### Integration with Module 6
- **Agents discover tools** via `list_tools()` 
- **Agents execute workflows** using multiple tools
- **Agents verify operations** through audit trail
- **Agents operate safely** within permission boundaries
- **Agents build complex tasks** through tool composition

#### Module 5 Complete!
All 6 lessons complete. Toolkit ready for autonomous agents in Module 6.

Next Steps:
- Lesson 5.6 output files stored in `datasets/lesson-06-output.json`
- Module 6 agents will use this toolkit for autonomous workflows
- Security guardrails ensure safe agent operation
- Audit trails enable transparency and compliance

---

## Shared Resources

All lessons leverage utilities in `shared/`:

- **`mcp_server.py`** — Base MCPServer with JSON-RPC protocol
- **`resources.py`** — File and knowledge base resources
- **`tools.py`** — Email, data, and text processing tools
- **`permissions.py`** — Role-based access control
- **`validation.py`** — Input validation and sanitization
- **`registry.py`** — Tool and resource registry

## Resource Scripts

### `resource_mcp_server.py`
A lightweight, production-ready MCP (Model Context Protocol) Server implementation. Designed to be imported and extended for building MCP-compliant tool services.

**Location:** `resource_mcp_server.py`

**Class: `MCPServer`**

Implements the core MCP Server protocol handler supporting JSON-RPC 2.0 communication, tool discovery, and execution over Stdio.

**Key Features:**
- **JSON-RPC 2.0 Compliance** — Standard protocol for tool negotiation and execution
- **Tool Registration** — Dynamic registration of tools with name, description, and input schema
- **Capability Discovery** — MCP clients can discover available tools and their signatures
- **Tool Execution** — Safe execution of registered tool handlers with error handling
- **Request Routing** — Handles `initialize`, `tools/list`, and `tools/call` methods

**Methods:**

1. **`register_tool(name, description, input_schema, handler)`**
   - Registers a tool capability with JSON schema for inputs
   - `handler`: Callable that executes the tool
   - Use when: Adding new capabilities to your MCP server
   - **Example:**
     ```python
     server.register_tool(
         name="get_weather",
         description="Retrieves weather for a city",
         input_schema={
             "type": "object",
             "properties": {
                 "city": {"type": "string"},
                 "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
             },
             "required": ["city"]
         },
         handler=lambda city, units="celsius": f"Weather in {city}: 22°{units[0].upper()}"
     )
     ```

2. **`handle_request(request: dict) -> dict`**
   - Routes incoming JSON-RPC 2.0 requests to appropriate handler
   - Supports three methods:
     - `initialize` — Server initialization handshake
     - `tools/list` — Discover all available tools
     - `tools/call` — Execute a tool with arguments
   - Returns: JSON-RPC 2.0 response (result or error)
   - Use when: Processing messages from MCP clients (like Claude, VS Code)

**Usage Example:**
```python
from resource_mcp_server import MCPServer

# Create server
server = MCPServer(name="MyToolServer", version="1.0.0")

# Register tool: System metrics
def get_cpu_status(mode: str = "simple") -> str:
    if mode == "simple":
        return "CPU: 45% utilization"
    return "CPU: 45% (load avg: 2.1)\nMemory: 8GB/16GB"

server.register_tool(
    name="cpu_status",
    description="Get current CPU and memory metrics",
    input_schema={
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["simple", "detailed"]}
        }
    },
    handler=get_cpu_status
)

# Handle a tool call request
request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {"name": "cpu_status", "arguments": {"mode": "detailed"}}
}

response = server.handle_request(request)
print(response["result"]["content"][0]["text"])
# Output: CPU: 45% (load avg: 2.1)\nMemory: 8GB/16GB
```

**Request/Response Examples:**

**Initialize Handshake:**
```json
Request:
  {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}

Response:
  {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
      "protocolVersion": "2024-11-05",
      "capabilities": {"tools": {"listChanged": false}},
      "serverInfo": {"name": "MyToolServer", "version": "1.0.0"}
    }
  }
```

**Tool Discovery:**
```json
Request:
  {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

Response:
  {
    "jsonrpc": "2.0",
    "id": 2,
    "result": {
      "tools": [
        {
          "name": "get_system_metrics",
          "description": "Retrieves real-time system performance metrics.",
          "inputSchema": {...}
        }
      ]
    }
  }
```

**Design Patterns Demonstrated:**
- **Protocol Compliance** — Full JSON-RPC 2.0 support for AI tool integration
- **Tool Registry** — Centralized registration with schema validation
- **Error Handling** — Graceful error responses for missing/failed tools
- **Extensibility** — Easy to add new tools without modifying core server
- **Isolation** — Tool errors don't crash the server

**Run Sample:**
```bash
python resource_mcp_server.py
```

This demonstrates initialization, tool discovery, and tool execution flows.

---

## Setup & Dependencies

### First-Time Setup
```bash
rm -rf .venv
./setup.sh
source .venv/bin/activate

pip install -r requirements-module-05.txt
```

**Dependencies:**
- Base: No external requirements
- Optional: email-validator, pydantic for advanced validation

---

## Architecture

### MCP Server Architecture
```
┌─────────────────────────────────┐
│      AI Assistant/Client        │
└────────────┬────────────────────┘
             │ JSON-RPC
             ↓
┌─────────────────────────────────┐
│    MCP Server (This Module)     │
├─────────────────────────────────┤
│ Resources:                      │
│  • File System                  │
│  • Knowledge Base               │
│  • Documents                    │
├─────────────────────────────────┤
│ Tools:                          │
│  • Email Analysis               │
│  • Text Processing              │
│  • Data Management              │
├─────────────────────────────────┤
│ Security:                       │
│  • Permissions                  │
│  • Validation                   │
│  • Rate Limiting                │
└─────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│   External Systems              │
│  • File Systems                 │
│  • Email Services               │
│  • APIs                         │
│  • Databases                    │
└─────────────────────────────────┘
```

---

## Module Progression

```
MCP Concepts
      ↓
JSON-RPC Foundations
      ↓
Personal Knowledge Server
      ↓
Enterprise Tool Integration
      ↓
Security & Governance
      ↓
Reusable MCP Toolkit
      ↓
Agent Consumption (Module 6)
```

---

## Recommended Project Timeline

| Lesson | Time | Focus |
|--------|------|-------|
| 5.3 | 45 min | Personal knowledge server, resources |
| 5.4 | 45 min | Email tools, workflow integration |
| 5.5 | 45 min | Permissions, validation, security |
| 5.6 | 90 min | Capstone: Complete toolkit |

**Total:** ~4-5 hours of hands-on development

---

## Key Concepts

### Resources
External data that AI can read:
- Files and documents
- Knowledge bases
- APIs
- Databases
- Real-time feeds

### Tools
Actions AI can perform:
- Email processing
- Data analysis
- File manipulation
- External service calls
- Workflow automation

### Permissions
Access control:
- Role-based (user, power_user, admin)
- Resource-level ACLs
- Action restrictions
- Rate limiting

### JSON-RPC
Communication protocol:
- Requests with methods and params
- Responses with results or errors
- Tool discovery
- Resource access

---

## Next Steps

After completing Module 5:
- ✅ You can build MCP servers
- ✅ You understand tool and resource exposure
- ✅ You know security patterns
- ✅ You're ready for Module 6: **AI Agents & Autonomy**

In Module 6, you'll learn how to build autonomous agents that consume MCP servers and tools to accomplish complex multi-step tasks.

---

## Reference

- MCP Specification: https://modelcontextprotocol.io
- Full curriculum: `docs/curriculum_v1.md`
- Module 4 (RAG): `../module-04-practical-rag-context-engineering/`
