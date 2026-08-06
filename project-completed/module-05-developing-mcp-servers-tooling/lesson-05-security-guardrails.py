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
import os
import json
import hashlib
import importlib.util
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
    enabled: bool = True,
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
        enabled: If False, returns server without security wrapping (for testing comparison)
    
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
        - Optional toggle to disable for testing comparison
    
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
    
    # If disabled, return unwrapped server (for testing comparison)
    if not enabled:
        print(f"⚠ Security guardrails DISABLED (for testing comparison)")
        return server
    
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
    
    print(f"✅ Initialized security guardrails")
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
    
    print(f"✅ Wrapped {len(wrapped_handlers)} tool handlers with security validation")
    
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
# INTERACTIVE MENU SYSTEM
# ============================================================================

def show_menu():
    """Display interactive menu options."""
    print("\n" + "=" * 70)
    print("LESSON 5.5: DEBUGGING & SECURITY - PERMISSION SANDBOXES")
    print("=" * 70)
    print("\nChoose a demonstration pattern:")
    print("  1) Permission System: Show role-based access control matrix")
    print("  2) Knowledge Server: Secure a knowledge server with guardrails")
    print("  3) Email Server: Secure an email server with guardrails")
    print("  4) Visible Toggle: Compare behavior WITH vs WITHOUT guardrails")
    print("  5) All Demonstrations: Run all security features (lectures)")
    print("  Q) Quit")
    print("-" * 70)


def pattern_1_permission_system():
    """Pattern 1: Permission system demonstration."""
    print("\n" + "=" * 70)
    print("PATTERN 1: PERMISSION SYSTEM")
    print("=" * 70)
    demo_permission_system()


def pattern_2_knowledge_server():
    """Pattern 2: Security on knowledge server."""
    print("\n" + "=" * 70)
    print("PATTERN 2: SECURE KNOWLEDGE SERVER")
    print("=" * 70)
    
    # Import knowledge server builder using importlib (handles hyphens in filename)
    try:
        lesson_03_path = Path(__file__).parent / "lesson-03-personal-knowledge-server.py"
        spec = importlib.util.spec_from_file_location("lesson_03_knowledge", lesson_03_path)
        lesson_03 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lesson_03)
        create_knowledge_server = lesson_03.create_knowledge_server
    except (ImportError, AttributeError) as e:
        print("ℹ️ Could not import knowledge server (lesson-03)")
        print("Creating mock server for demonstration...")
        # Create mock knowledge server for demo
        server = MCPServer("mock_knowledge_server")
        server.tools["search"] = Tool("search", {}, "Search knowledge base")
        server.tool_handlers["search"] = lambda query="": json.dumps({"results": ["doc1", "doc2"]})
        return
    
    # Create knowledge server
    knowledge_dir = Path(__file__).parent.parent.parent / "datasets"
    server = create_knowledge_server(str(knowledge_dir), "knowledge_srv", ['.md', '.txt'])
    
    print("\n📚 Knowledge Server Created")
    print(f"Available tools: {list(server.tool_handlers.keys())}")
    
    # Apply security guardrails
    print("\n🔒 Applying security guardrails (read_only)...")
    secure_server = add_security_guardrails(
        server,
        permission_strategy="read_only",
        enable_audit_logging=True,
        user_id="learner"
    )
    
    # Test tool access
    print("\n✅ Testing secure tool access...")
    test_result = secure_server.call_tool("search_knowledge", {"query": "AI"})
    if test_result:
        try:
            result_dict = json.loads(test_result)
            print(f"Search result: {result_dict.get('results', result_dict.get('error', test_result))[:100]}")
        except:
            print(f"Result: {test_result[:100]}")
    
    print("\n✅ Pattern 2 complete - Knowledge server is now secured")


def pattern_3_email_server():
    """Pattern 3: Security on email server."""
    print("\n" + "=" * 70)
    print("PATTERN 3: SECURE EMAIL SERVER")
    print("=" * 70)
    
    # Import email server builder using importlib (handles hyphens in filename)
    try:
        lesson_04_path = Path(__file__).parent / "lesson-04-email-analyst-server.py"
        spec = importlib.util.spec_from_file_location("lesson_04_email", lesson_04_path)
        lesson_04 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lesson_04)
        create_email_analyst_server = lesson_04.create_email_analyst_server
    except (ImportError, AttributeError) as e:
        print("ℹ️ Could not import email server (lesson-04)")
        print("Creating mock server for demonstration...")
        # Create mock email server for demo
        server = MCPServer("mock_email_server")
        server.tools["analyze"] = Tool("analyze", {}, "Analyze email")
        server.tool_handlers["analyze"] = lambda: json.dumps({"sentiment": "positive"})
        return
    
    # Create email server
    server = create_email_analyst_server("email_srv")
    
    print("\n📧 Email Server Created")
    print(f"Available tools: {list(server.tool_handlers.keys())}")
    
    # Apply security guardrails
    print("\n🔒 Applying security guardrails (power_user)...")
    secure_server = add_security_guardrails(
        server,
        permission_strategy="power_user",
        enable_audit_logging=True,
        user_id="analyst"
    )
    
    # Test tool access
    print("\n✅ Testing secure tool access...")
    test_result = secure_server.call_tool("parse_email", {})
    if test_result:
        try:
            result_dict = json.loads(test_result)
            print(f"Parse result: {list(result_dict.keys())[:5]}")
        except:
            print(f"Result: {test_result[:100]}")
    
    print("\n✅ Pattern 3 complete - Email server is now secured")


def pattern_4_visible_toggle():
    """Pattern 4: Compare WITH vs WITHOUT guardrails."""
    print("\n" + "=" * 70)
    print("PATTERN 4: VISIBLE TOGGLE TEST (WITH vs WITHOUT GUARDRAILS)")
    print("=" * 70)
    
    print("\n📊 This pattern demonstrates security by running the same")
    print("operation twice: once with guardrails, once without.\n")
    
    # Create mock server for demonstration
    server = MCPServer("test_server")
    server.tools["read_file"] = Tool("read_file", {"path": {}}, "Read a file")
    server.tools["delete_file"] = Tool("delete_file", {"path": {}}, "Delete a file")
    
    def read_handler(**kwargs):
        path = kwargs.get("path", "document.txt")
        return json.dumps({"content": f"File contents from {path}"})
    
    def delete_handler(**kwargs):
        path = kwargs.get("path", "document.txt")
        return json.dumps({"deleted": path})
    
    server.tool_handlers["read_file"] = read_handler
    server.tool_handlers["delete_file"] = delete_handler
    
    # Test 1: Without guardrails (enabled=False)
    print("─" * 70)
    print("TEST 1: WITHOUT GUARDRAILS (enabled=False)")
    print("─" * 70)
    
    insecure_server = add_security_guardrails(
        server,
        permission_strategy="read_only",
        enable_audit_logging=False,
        enabled=False
    )
    
    print("\n✓ Attempting to delete file...")
    result = insecure_server.call_tool("delete_file", {"path": "../../../etc/passwd"})
    try:
        result_dict = json.loads(result)
        print(f"Result: ❌ ALLOWED - {result_dict.get('deleted', result_dict)}")
    except:
        print(f"Result: {result}")
    
    # Test 2: With guardrails (enabled=True)
    print("\n" + "─" * 70)
    print("TEST 2: WITH GUARDRAILS (enabled=True)")
    print("─" * 70)
    
    # Reset server for fresh guardrails
    server2 = MCPServer("test_server_2")
    server2.tools["read_file"] = Tool("read_file", {"path": {}}, "Read a file")
    server2.tools["delete_file"] = Tool("delete_file", {"path": {}}, "Delete a file")
    server2.tool_handlers["read_file"] = read_handler
    server2.tool_handlers["delete_file"] = delete_handler
    
    secure_server = add_security_guardrails(
        server2,
        permission_strategy="read_only",
        enable_audit_logging=True,
        enabled=True
    )
    
    print("\n✓ Attempting to delete file...")
    result = secure_server.call_tool("delete_file", {"path": "../../../etc/passwd"})
    try:
        result_dict = json.loads(result)
        if "error" in result_dict:
            print(f"Result: ✅ BLOCKED - {result_dict['error']}")
        else:
            print(f"Result: {result_dict}")
    except:
        print(f"Result: {result}")
    
    # Show comparison
    print("\n" + "─" * 70)
    print("COMPARISON SUMMARY")
    print("─" * 70)
    print("Without guardrails: ❌ Dangerous operation ALLOWED")
    print("With guardrails:    ✅ Dangerous operation BLOCKED by permissions\n")
    print("The permission system prevents operations beyond user's role level.")
    print("  • read_only users: Can READ, cannot DELETE")
    print("  • power_user: Can READ and WRITE, but cannot DELETE critical resources")
    print("  • admin: Can perform all operations\n")


def pattern_5_all_demos():
    """Pattern 5: Run all lecture-style demonstrations."""
    print("\n" + "=" * 70)
    print("PATTERN 5: ALL SECURITY FEATURES (LECTURE MODE)")
    print("=" * 70)
    print("\nRunning comprehensive security demonstrations...\n")
    
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
    
    print("\n✅ All demonstrations complete")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Interactive menu loop
    while True:
        os.system('clear')
        show_menu()
        choice = input("Enter your choice [1-5, Q]: ").strip().upper()
        
        if choice == "1":
            pattern_1_permission_system()
            input("\nPress Enter to continue...")
        elif choice == "2":
            pattern_2_knowledge_server()
            input("\nPress Enter to continue...")
        elif choice == "3":
            pattern_3_email_server()
            input("\nPress Enter to continue...")
        elif choice == "4":
            pattern_4_visible_toggle()
            input("\nPress Enter to continue...")
        elif choice == "5":
            pattern_5_all_demos()
            input("\nPress Enter to continue...")
        elif choice == "Q":
            os.system('clear')
            print("\n" + "=" * 70)
            print("LESSON COMPLETE - Thank you for learning about security guardrails!")
            print("=" * 70)
            print("\nKey Takeaways:")
            print("  1. Permissions control which operations users can execute")
            print("  2. Input sanitization prevents path traversal and injection attacks")
            print("  3. Secret scrubbing protects credentials in logs")
            print("  4. Audit trails enable compliance and incident response")
            print("  5. Approval workflows add human oversight for dangerous operations")
            print("  6. Security guardrails can wrap ANY MCP server")
            print("  7. Toggle testing helps validate security effectiveness\n")
            print("Next Lesson:")
            print("  Lesson 5.6 combines all concepts into a complete MCP Toolkit\n")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5 or Q.")
            input("\nPress Enter to continue...")

