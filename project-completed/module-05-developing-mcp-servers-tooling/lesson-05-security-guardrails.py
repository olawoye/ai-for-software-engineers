"""
Lesson 5.5: Debugging & Security - Permission Sandboxes

Build security guardrails that protect MCP servers from unsafe operations,
data leaks, and privilege escalation. This lesson demonstrates how to wrap
existing servers with validation, logging, and access control.

This lesson demonstrates the core add_security_guardrails() template method
that learners can reuse to secure any MCP server with minimal configuration.

Run:
    python lesson-05-security-guardrails.py
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
# CORE TEMPLATE METHOD: add_security_guardrails()
# ============================================================================
# This method wraps an existing MCP server with security validation.
# It intercepts tool execution to enforce permissions, sanitize inputs,
# log actions, and optionally require approvals for dangerous operations.
#
# Template structure:
#   - Input: MCPServer, permission_strategy, enable_audit_logging, enable_approval
#   - Processing: wrap tool handlers with security checks
#   - Output: secured MCPServer with same interface but protected execution
#
# Reusability: Wrap ANY MCPServer (Knowledge, Email, Custom) with these guardrails
# ============================================================================

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
        self.arguments = arguments  # Original, for reference
        self.arguments_hash = hashlib.sha256(
            json.dumps(arguments, sort_keys=True).encode()
        ).hexdigest()[:8]  # Hash for quick comparison, not full log
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
    """Core template method: Wrap an MCP Server with security validation and guardrails.
    
    This is the production-ready security wrapper pattern for protecting tool execution.
    Learners can extract this method and wrap any MCPServer with these guardrails.
    
    Args:
        server: MCPServer instance to secure
        permission_strategy: One of "read_only", "power_user", "admin"
        enable_audit_logging: Whether to log all tool executions
        enable_approval_workflow: Require manual approval for dangerous operations
        user_id: User identifier for permission checking
    
    Returns:
        MCPServer: Same interface, but with security validation intercepting
        all tool execution. Tool handlers are wrapped with permission checks,
        input sanitization, and audit logging.
    
    Features:
        - Role-based permission checking before tool execution
        - Input sanitization (path traversal, injection attacks, etc.)
        - Sensitive data scrubbing from logs and outputs
        - Complete audit trail with timestamps and hashes
        - Optional approval workflow for high-risk operations
    
    Example:
        >>> server = create_knowledge_server('/data/knowledge')
        >>> secure_server = add_security_guardrails(
        ...     server,
        ...     permission_strategy='read_only',
        ...     enable_audit_logging=True
        ... )
        >>> # Now all tool calls go through security validation
        >>> result = secure_server.call_tool('search_knowledge', {'query': 'RAG'})
    """
    
    # Step 1: Initialize security infrastructure
    permission_manager = PermissionManager()
    resource_permissions = ResourcePermissions()
    audit_trail: List[AuditEntry] = []
    
    # Map strategy to role
    strategy_to_role = {
        "read_only": Role.USER,
        "power_user": Role.POWER_USER,
        "admin": Role.ADMIN,
    }
    user_role = strategy_to_role.get(permission_strategy, Role.USER)
    
    print(f"✓ Initialized security guardrails")
    print(f"  Permission strategy: {permission_strategy} (role: {user_role.value})")
    print(f"  Audit logging: {'enabled' if enable_audit_logging else 'disabled'}")
    print(f"  Approval workflow: {'enabled' if enable_approval_workflow else 'disabled'}")
    
    # Step 2: Determine which operations require approval
    dangerous_operations = {
        "delete": True,
        "remove": True,
        "drop": True,
        "truncate": True,
        "write": enable_approval_workflow,
        "modify": enable_approval_workflow,
    }
    
    # Step 3: Wrap all tool handlers with security validation
    original_handlers = dict(server.tool_handlers)
    wrapped_handlers = {}
    
    for tool_name, original_handler in original_handlers.items():
        # Create wrapped handler with security checks
        def make_secure_handler(tool, orig_handler, tool_name):
            """Create closure for wrapped handler."""
            
            def secure_handler(**kwargs):
                # Check 1: Permission validation
                required_permission = _infer_permission_for_tool(tool_name)
                if not permission_manager.has_permission(user_role, required_permission):
                    audit_msg = f"Permission denied: {user_role.value} lacks {required_permission.value}"
                    if enable_audit_logging:
                        entry = AuditEntry(tool_name, user_id, kwargs, None, False, audit_msg)
                        audit_trail.append(entry)
                    return json.dumps({
                        "error": f"Permission denied: insufficient privileges for {tool_name}",
                        "required_permission": required_permission.value,
                        "user_role": user_role.value
                    })
                
                # Check 2: Detect dangerous operation
                is_dangerous = any(
                    keyword in tool_name.lower() 
                    for keyword in dangerous_operations.keys()
                )
                
                if is_dangerous and enable_approval_workflow:
                    # Would require human approval in production
                    approval_msg = f"[APPROVAL REQUIRED] {user_id} requesting: {tool_name}"
                    if enable_audit_logging:
                        entry = AuditEntry(tool_name, user_id, kwargs, None, False, 
                                         "Awaiting approval for dangerous operation")
                        audit_trail.append(entry)
                    return json.dumps({
                        "status": "approval_required",
                        "tool": tool_name,
                        "user": user_id,
                        "message": approval_msg
                    })
                
                # Check 3: Input sanitization
                sanitized_kwargs = {}
                for key, value in kwargs.items():
                    if isinstance(value, str):
                        # Sanitize file paths
                        if "path" in key.lower() or "file" in key.lower():
                            value = InputSanitizer.sanitize_filename(value)
                        # Sanitize email addresses
                        elif "email" in key.lower():
                            sanitized = InputSanitizer.sanitize_email(value)
                            if not sanitized:
                                return json.dumps({
                                    "error": f"Invalid {key}: {value}"
                                })
                            value = sanitized
                        # Remove potential secrets from queries
                        value = _scrub_secrets(value)
                    sanitized_kwargs[key] = value
                
                # Check 4: Execute original handler
                try:
                    result = orig_handler(**sanitized_kwargs)
                    
                    # Check 5: Scrub sensitive data from result
                    if result:
                        result = _scrub_secrets(result)
                    
                    # Log success
                    if enable_audit_logging:
                        entry = AuditEntry(tool_name, user_id, sanitized_kwargs, result, True)
                        audit_trail.append(entry)
                    
                    return result
                
                except Exception as e:
                    error_msg = str(e)
                    if enable_audit_logging:
                        entry = AuditEntry(tool_name, user_id, sanitized_kwargs, None, False, error_msg)
                        audit_trail.append(entry)
                    
                    return json.dumps({
                        "error": f"Tool execution failed: {error_msg}"
                    })
            
            return secure_handler
        
        # Get tool definition to infer permissions
        tool_def = server.tools.get(tool_name)
        wrapped_handlers[tool_name] = make_secure_handler(
            tool_def, 
            original_handler, 
            tool_name
        )
    
    # Step 4: Replace handlers with wrapped versions
    server.tool_handlers = wrapped_handlers
    
    print(f"✓ Wrapped {len(wrapped_handlers)} tool handlers with security validation")
    
    # Step 5: Store audit trail for retrieval
    server.audit_trail = audit_trail
    
    return server


def _infer_permission_for_tool(tool_name: str) -> Permission:
    """Infer required permission from tool name."""
    tool_lower = tool_name.lower()
    
    if any(word in tool_lower for word in ["delete", "drop", "remove", "truncate"]):
        return Permission.DELETE
    elif any(word in tool_lower for word in ["write", "create", "update", "modify"]):
        return Permission.WRITE
    elif any(word in tool_lower for word in ["execute", "run", "call"]):
        return Permission.EXECUTE
    else:
        return Permission.READ


def _scrub_secrets(text: str) -> str:
    """Remove potential secrets from text (API keys, passwords, tokens)."""
    import re
    
    patterns = [
        (r'[Aa][Pp][Ii][_-]?[Kk][Ee][Yy]["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', '[REDACTED_API_KEY]'),
        (r'[Pp]assword["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', '[REDACTED_PASSWORD]'),
        (r'[Tt]oken["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', '[REDACTED_TOKEN]'),
        (r'[Ss]ecret["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', '[REDACTED_SECRET]'),
        (r'[Kk]ey["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', '[REDACTED_KEY]'),
    ]
    
    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)
    
    return result


# ============================================================================
# DEMONSTRATIONS: Show how the template works
# ============================================================================

def demo_permission_system():
    """Demonstration 1: Role-based permission system."""
    print("\n" + "=" * 70)
    print("DEMO 1: PERMISSION SYSTEM")
    print("=" * 70)
    
    permission_manager = PermissionManager()
    
    print("\nRole-Based Permission Matrix:")
    print("-" * 70)
    
    roles = [Role.USER, Role.POWER_USER, Role.ADMIN]
    permissions = [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE]
    
    # Header
    print(f"{'Role':<15} | ", end="")
    for perm in permissions:
        print(f"{perm.value:<10} | ", end="")
    print()
    print("-" * 70)
    
    # Rows
    for role in roles:
        print(f"{role.value:<15} | ", end="")
        for perm in permissions:
            has_perm = permission_manager.has_permission(role, perm)
            status = "✅ yes" if has_perm else "❌ no"
            print(f"{status:<10} | ", end="")
        print()
    
    print("\n✅ Permission system complete")
    print("\nLearning Point:")
    print("  Roles determine what operations users can perform.")
    print("  READ_ONLY users can query; POWER_USERs can modify; ADMINs have full access.")


def demo_input_sanitization():
    """Demonstration 2: Input sanitization and validation."""
    print("\n" + "=" * 70)
    print("DEMO 2: INPUT SANITIZATION")
    print("=" * 70)
    
    print("\nPath Traversal Protection:")
    print("-" * 70)
    
    dangerous_paths = [
        "../../../etc/passwd",
        "../../secret.key",
        "/etc/shadow",
        "~/.ssh/id_rsa",
        "./documents/report.pdf",
    ]
    
    for path in dangerous_paths:
        sanitized = InputSanitizer.sanitize_filename(path)
        is_safe = "/" not in sanitized and ".." not in sanitized
        status = "✅ safe" if is_safe else "⚠️ risky"
        print(f"{status}: '{path}' → '{sanitized}'")
    
    print("\nEmail Validation:")
    print("-" * 70)
    
    test_emails = [
        "valid@example.com",
        "invalid.email",
        "user+tag@domain.co.uk",
        "no-at-sign.com",
    ]
    
    for email in test_emails:
        sanitized = InputSanitizer.sanitize_email(email)
        is_valid = sanitized is not None
        status = "✅ valid" if is_valid else "❌ invalid"
        print(f"{status}: {email}")
    
    print("\n✅ Input sanitization complete")
    print("\nLearning Point:")
    print("  Sanitization prevents path traversal, SQL injection, and format attacks.")
    print("  Validation ensures inputs match expected patterns before processing.")


def demo_secret_scrubbing():
    """Demonstration 3: Sensitive data scrubbing."""
    print("\n" + "=" * 70)
    print("DEMO 3: SECRET SCRUBBING")
    print("=" * 70)
    
    print("\nRemoving Secrets from Logs:")
    print("-" * 70)
    
    log_entries = [
        'User called search_knowledge with api_key="sk-1234567890abcdef"',
        'Email check with password="MySecure!Pass123"',
        'Database connect: token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"',
        'Config loaded with secret="prod-key-12345"',
    ]
    
    for entry in log_entries:
        scrubbed = _scrub_secrets(entry)
        print(f"Original:  {entry}")
        print(f"Scrubbed:  {scrubbed}")
        print()
    
    print("✅ Secret scrubbing complete")
    print("\nLearning Point:")
    print("  Secrets are removed before audit logging to prevent accidental exposure.")
    print("  Hashes are used instead for verification without revealing data.")


def demo_audit_trail():
    """Demonstration 4: Audit logging and trail."""
    print("\n" + "=" * 70)
    print("DEMO 4: AUDIT TRAIL")
    print("=" * 70)
    
    print("\nSample Audit Entries (Execution Log):")
    print("-" * 70)
    
    sample_entries = [
        {
            "timestamp": "2026-07-02T12:30:15.123456",
            "tool": "search_knowledge",
            "user": "alice",
            "operation": "READ",
            "args_hash": "a1b2c3d4",
            "success": True,
            "result_hash": "f5e6d7c8",
        },
        {
            "timestamp": "2026-07-02T12:31:22.456789",
            "tool": "delete_document",
            "user": "bob",
            "operation": "DELETE",
            "args_hash": "x9y8z7w6",
            "success": False,
            "reason": "Permission denied: user lacks DELETE permission",
        },
        {
            "timestamp": "2026-07-02T12:32:45.789012",
            "tool": "parse_email",
            "user": "alice",
            "operation": "READ",
            "args_hash": "m1n2o3p4",
            "success": True,
            "result_hash": "q5r6s7t8",
        },
    ]
    
    print(f"{'Timestamp':<26} | {'Tool':<20} | {'User':<8} | {'Op':<8} | {'Result':<10}")
    print("-" * 70)
    
    for entry in sample_entries:
        result = "✅ success" if entry.get('success') else "❌ denied"
        print(
            f"{entry['timestamp']:<26} | "
            f"{entry['tool']:<20} | "
            f"{entry['user']:<8} | "
            f"{entry['operation']:<8} | "
            f"{result:<10}"
        )
    
    print("\n✅ Audit trail demonstration complete")
    print("\nLearning Point:")
    print("  Audit trails track who did what, when, and whether it succeeded.")
    print("  This enables compliance, debugging, and security incident response.")


def demo_approval_workflow():
    """Demonstration 5: Approval workflow for sensitive operations."""
    print("\n" + "=" * 70)
    print("DEMO 5: APPROVAL WORKFLOW")
    print("=" * 70)
    
    print("""
Approval Workflow for Sensitive Operations
===========================================

When enable_approval_workflow=True, dangerous operations require approval:

1. USER ATTEMPTS HIGH-RISK OPERATION
   ├─ Tool: delete_document
   ├─ User: alice
   ├─ Resource: important_file.txt
   └─ Status: ⏳ AWAITING APPROVAL

2. SYSTEM CREATES APPROVAL REQUEST
   ├─ Request ID: 2026-07-02-001
   ├─ Timestamp: 2026-07-02T12:30:15
   ├─ User: alice
   ├─ Operation: delete_document(important_file.txt)
   ├─ Risk Level: HIGH
   └─ Requires: ADMIN approval

3. ADMIN REVIEWS REQUEST
   ├─ Admin reviews context and reasoning
   ├─ Verifies user identity and permissions
   └─ Makes decision: APPROVE or DENY

4a. IF APPROVED
   ├─ Operation executes
   ├─ Audit log: Operation approved by admin
   └─ User notified: Action completed

4b. IF DENIED
   ├─ Operation rejected
   ├─ Audit log: Operation denied by admin
   └─ User notified: Action not permitted

Dangerous Operations Triggering Approval:
─────────────────────────────────────────
  • delete_* (file, document, entry)
  • drop_* (table, database, schema)
  • truncate_*
  • write_* (if strict mode)
  • modify_permissions
  • execute_script

Security Benefits:
──────────────────
  • Prevents accidental destructive operations
  • Creates human oversight for critical actions
  • Enables audit trail for compliance
  • Allows rollback/review before execution
""")
    
    print("✅ Approval workflow demonstration complete")
    print("\nLearning Point:")
    print("  High-risk operations require human review to prevent accidents.")
    print("  Combined with audit trails, this creates defense in depth.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LESSON 5.5: DEBUGGING & SECURITY - PERMISSION SANDBOXES")
    print("=" * 70)
    print("\nThis lesson demonstrates how to protect MCP servers with security")
    print("guardrails that validate, log, and approve tool execution.\n")
    
    # Run all demonstrations
    demo_permission_system()
    print("\n" + "-" * 70 + "\n")
    
    demo_input_sanitization()
    print("\n" + "-" * 70 + "\n")
    
    demo_secret_scrubbing()
    print("\n" + "-" * 70 + "\n")
    
    demo_audit_trail()
    print("\n" + "-" * 70 + "\n")
    
    demo_approval_workflow()
    
    print("\n" + "=" * 70)
    print("LESSON COMPLETE")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  1. Permissions control which operations users can execute")
    print("  2. Input sanitization prevents path traversal and injection attacks")
    print("  3. Secret scrubbing protects credentials in logs")
    print("  4. Audit trails enable compliance and incident response")
    print("  5. Approval workflows add human oversight for dangerous operations\n")
    print("Next Lesson:")
    print("  Lesson 5.6 combines all concepts into a complete MCP Toolkit\n")
