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

### Lesson 5.3: Your First MCP Server
**Type:** Code Screencast  
**Status:** ✅ Complete

Build a local "Second Brain" MCP server that allows AI assistants to access files, notes, and documentation.

#### Run Instructions
```bash
source .venv/bin/activate
pip install -r requirements-module-05.txt
python lesson-03-personal-knowledge-server.py
```

**What You'll Learn:**
- Create MCPServer implementing JSON-RPC protocol
- Register resources (file access, documents)
- Register tools (search, retrieval)
- Handle server requests and responses
- Build knowledge base integrations

**Key Concepts:**
- Resource registration and discovery
- Tool definition with input schemas
- JSON-RPC request/response handling
- Local knowledge access patterns

---

### Lesson 5.4: Connecting Real-World Tools
**Type:** Code Screencast  
**Status:** ✅ Complete

Build an MCP server that integrates email processing and analysis tools.

#### Run Instructions
```bash
source .venv/bin/activate
python lesson-04-email-analyst-server.py
```

**What You'll Learn:**
- Integrate external services (email, CRM, APIs)
- Build tool handlers for business workflows
- Structure complex input schemas
- Handle tool execution and responses
- Create workflow automation patterns

**Features:**
- Email parsing and structuring
- Sentiment analysis
- Category classification
- Action item extraction

---

### Lesson 5.5: Debugging & Security
**Type:** Code Screencast  
**Status:** ✅ Complete

Learn testing, debugging, and securing MCP servers for production.

#### Run Instructions
```bash
source .venv/bin/activate
python lesson-05-security-guardrails.py
```

**What You'll Learn:**
- Implement role-based permissions
- Validate and sanitize inputs
- Rate limit tool access
- Test security boundaries
- Debug MCP interactions

**Security Patterns:**
- Role-based access control (RBAC)
- Input validation and sanitization
- Rate limiting and throttling
- Permission enforcement
- Audit logging

---

### Lesson 5.6: MCP Toolkit (Capstone)
**Type:** Code Screencast  
**Status:** ✅ Complete

Build a complete, production-ready MCP server combining all concepts.

#### Run Instructions
```bash
source .venv/bin/activate
python lesson-06-mcp-toolkit-server.py
```

**What You'll Learn:**
- Combine multiple tool categories
- Manage complex permissions
- Handle cross-tool workflows
- Implement production patterns
- Deploy ready-to-use toolkit

**Features:**
- Knowledge search
- Email processing
- Text analysis
- Permission management
- Rate limiting
- Error handling

**Output:** Production-ready MCP toolkit server

---

## Shared Resources

All lessons leverage utilities in `shared/`:

- **`mcp_server.py`** — Base MCPServer with JSON-RPC protocol
- **`resources.py`** — File and knowledge base resources
- **`tools.py`** — Email, data, and text processing tools
- **`permissions.py`** — Role-based access control
- **`validation.py`** — Input validation and sanitization
- **`registry.py`** — Tool and resource registry

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
