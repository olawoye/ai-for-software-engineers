"""
Lesson 5.5 TODO: Debugging & Security - Permission Sandboxes

In this lesson, you'll build the core template method for wrapping MCP servers
with security validation, input sanitization, and audit logging.

Your goal: Implement add_security_guardrails(), a reusable wrapper that:
  - Enforces role-based permissions before tool execution
  - Sanitizes inputs (paths, emails, etc.) to prevent attacks
  - Scrubs secrets from logs and outputs
  - Maintains complete audit trail with timestamps and hashes
  - Optionally requires approval for dangerous operations

PHASE 1: Core Template Method (add_security_guardrails)
  - Accept parameters: server, permission_strategy, enable_audit_logging, enable_approval_workflow, user_id
  - Initialize security infrastructure (PermissionManager, ResourcePermissions, audit_trail)
  - Map permission_strategy to Role (read_only → USER, power_user → POWER_USER, admin → ADMIN)
  - Wrap all existing tool handlers with security checks (see PHASE 2)
  - Store audit trail on server object
  - Return wrapped server

PHASE 2: Security Wrapper Logic (for each tool handler)
  1. Permission Check: Verify user_role has required permission for tool
  2. Dangerous Op Check: Detect if tool is delete/drop/write and check approval_workflow
  3. Input Sanitization: Clean paths, emails, remove secrets
  4. Handler Execution: Call original handler with sanitized inputs
  5. Secret Scrubbing: Remove sensitive data from results
  6. Audit Logging: Record success/failure with hashes
  7. Error Handling: Log exceptions without exposing internals

PHASE 3: Helper Functions & Demonstrations
  - _infer_permission_for_tool(): Map tool names to required permissions
  - _scrub_secrets(): Use regex to remove API keys, passwords, tokens
  - demo_permission_system(): Show role-based matrix
  - demo_input_sanitization(): Show path traversal protection
  - demo_secret_scrubbing(): Show secret removal
  - demo_audit_trail(): Show execution log
  - demo_approval_workflow(): Show dangerous op workflow
  - main(): Run all demonstrations

REFERENCE:
  - Completed implementation: project-completed/module-05-developing-mcp-servers-tooling/lesson-05-security-guardrails.py
  - Permission system: shared/permissions.py (PermissionManager, Role, Permission)
  - Validation: shared/validation.py (InputSanitizer)
  - MCP server base: shared/mcp_server.py
  - Business scenario: Prevent data leaks, accidental deletions, privilege escalation
  - Data flow: Tool call → Permission check → Input sanitization → Execution → Secret scrub → Audit log

LEARNING GOALS:
  1. Implement permission-based access control for tool execution
  2. Sanitize user inputs to prevent injection attacks
  3. Scrub secrets from audit logs automatically
  4. Maintain complete audit trail for compliance
  5. Add human-in-the-loop for dangerous operations
  6. Understand defense-in-depth security architecture
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime
from enum import Enum

# Import from shared module (reference path)
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Tool
from shared.permissions import PermissionManager, Role, Permission, ResourcePermissions
from shared.validation import SchemaValidator, InputSanitizer


# ============================================================================
# PHASE 1: Core Template Method - add_security_guardrails()
# ============================================================================
# TODO: Implement the core add_security_guardrails() function
#
# Requirements:
#   1. Accept parameters: server, permission_strategy, enable_audit_logging, enable_approval_workflow, user_id
#   2. Initialize security infrastructure
#   3. Map permission_strategy string to Role enum
#   4. Wrap all tool handlers with security checks
#   5. Store audit trail on server
#   6. Return wrapped server
#
# Hints:
#   - Use dict(server.tool_handlers) to copy original handlers
#   - Create a closure (make_secure_handler) to capture each tool's original handler
#   - Replace server.tool_handlers with wrapped versions
#   - Print status messages showing what's enabled

class PermissionStrategy(Enum):
    """Permission strategies for tool execution."""
    READ_ONLY = "read_only"
    POWER_USER = "power_user"
    ADMIN = "admin"


class AuditEntry:
    """Record of a tool execution for audit trail."""
    
    def __init__(self, tool_name: str, user: str, arguments: Dict, 
                 result: Optional[str], success: bool, reason: Optional[str] = None):
        self.timestamp = datetime.now().isoformat()
        self.tool_name = tool_name
        self.user = user
        self.arguments = arguments
        self.arguments_hash = hashlib.sha256(
            json.dumps(arguments, sort_keys=True).encode()
        ).hexdigest()[:8]
        self.result_hash = hashlib.sha256(
            json.dumps(result or {}, sort_keys=True).encode()
        ).hexdigest()[:8]
        self.success = success
        self.reason = reason or ("Execution successful" if success else "Execution failed")


def add_security_guardrails(
    server: MCPServer,
    permission_strategy: str = "read_only",
    enable_audit_logging: bool = True,
    enable_approval_workflow: bool = False,
    user_id: str = "default_user",
) -> MCPServer:
    """TODO: Wrap an MCP Server with security validation and guardrails.
    
    Args:
        server: MCPServer instance to secure
        permission_strategy: One of "read_only", "power_user", "admin"
        enable_audit_logging: Whether to log all tool executions
        enable_approval_workflow: Require manual approval for dangerous operations
        user_id: User identifier for permission checking
    
    Returns:
        MCPServer: Same interface, but with security validation intercepting all tool execution.
    """
    # TODO: Phase 1 implementation here
    # Step 1: Initialize security infrastructure
    # Step 2: Map strategy to role
    # Step 3: Wrap all tool handlers
    # Step 4: Replace handlers
    # Step 5: Store audit trail
    pass


# ============================================================================
# PHASE 2: Security Wrapper Logic (for each tool handler)
# ============================================================================
# TODO: Implement make_secure_handler closure that wraps each original handler
#
# The secure_handler(**kwargs) should:
#   1. Check permission: permission_manager.has_permission(user_role, required_permission)
#   2. Check dangerous: is_dangerous = any(keyword in tool_name.lower() ...)
#   3. Sanitize inputs: Clean paths and emails using InputSanitizer
#   4. Execute: result = orig_handler(**sanitized_kwargs)
#   5. Scrub: result = _scrub_secrets(result)
#   6. Log: if enable_audit_logging: audit_trail.append(AuditEntry(...))
#   7. Return: json.dumps({...}) or result
#
# For each check failure, return JSON error and log to audit trail

# TODO: Define secure_handler wrapper function inside add_security_guardrails
# TODO: Create make_secure_handler closure factory


# ============================================================================
# PHASE 3: Helper Functions & Demonstrations
# ============================================================================
# TODO: Implement helper functions

def _infer_permission_for_tool(tool_name: str) -> Permission:
    """TODO: Infer required permission from tool name.
    
    Examples:
    - "delete_document" → Permission.DELETE
    - "write_file" → Permission.WRITE
    - "execute_script" → Permission.EXECUTE
    - "search_knowledge" → Permission.READ
    """
    # TODO: Implement permission inference logic
    pass


def _scrub_secrets(text: str) -> str:
    """TODO: Remove potential secrets from text using regex patterns.
    
    Patterns to remove:
    - API keys: api_key="..." or apiKey: ...
    - Passwords: password="..." or pwd: ...
    - Tokens: token="..." or auth_token: ...
    - Secrets: secret="..." or key: ...
    
    Return text with secrets replaced with [REDACTED_*] placeholders.
    """
    # TODO: Implement secret scrubbing with regex
    pass


# TODO: Implement demonstration functions

def demo_permission_system():
    """TODO: Demonstrate role-based permission system."""
    # Show permission matrix: roles vs permissions (READ, WRITE, DELETE, EXECUTE)
    # Print ✅ for allowed, ❌ for denied
    # Print learning point about roles
    pass


def demo_input_sanitization():
    """TODO: Demonstrate input sanitization."""
    # Show path traversal protection
    # Show email validation
    # Print before/after for dangerous inputs
    pass


def demo_secret_scrubbing():
    """TODO: Demonstrate secret scrubbing."""
    # Show log entries with secrets
    # Show same entries scrubbed
    # Print learning point about audit log safety
    pass


def demo_audit_trail():
    """TODO: Demonstrate audit trail logging."""
    # Show sample audit entries with timestamps, tools, users, success/failure
    # Print as table with columns: timestamp, tool, user, operation, result
    # Print learning point about compliance and incident response
    pass


def demo_approval_workflow():
    """TODO: Demonstrate approval workflow for dangerous operations."""
    # Print workflow diagram showing user → approval request → admin → approve/deny
    # List dangerous operations that trigger approval
    # Print security benefits
    pass


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # TODO: Print lesson title
    # TODO: Call each demonstration
    # TODO: Print separator lines between demos
    # TODO: Print lesson completion with key takeaways
    # TODO: Reference next lesson (5.6)
    pass
