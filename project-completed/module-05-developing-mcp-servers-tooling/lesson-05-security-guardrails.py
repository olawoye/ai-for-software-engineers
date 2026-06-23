"""
Lesson 5.5: Security & Debugging - Permission Sandboxes

Learn testing, debugging, and securing MCP servers for production.
Implement permission boundaries and safety controls.

Run: python lesson-05-security-guardrails.py
"""

import json
from shared.permissions import PermissionManager, Role, Permission, ActionValidator
from shared.validation import SchemaValidator, InputSanitizer, RateLimiter


def demo_permission_system():
    """Demonstrate role-based permissions."""
    print("\n" + "=" * 60)
    print("PERMISSION SYSTEM")
    print("=" * 60)

    pm = PermissionManager()

    # Check permissions
    roles = [Role.USER, Role.POWER_USER, Role.ADMIN]
    perms = [Permission.READ, Permission.WRITE, Permission.DELETE]

    print("\nRole-Based Permissions:")
    for role in roles:
        print(f"\n{role.value}:")
        for perm in perms:
            has_perm = pm.has_permission(role, perm)
            status = "✅" if has_perm else "❌"
            print(f"  {status} {perm.value}")


def demo_input_validation():
    """Demonstrate input validation."""
    print("\n" + "=" * 60)
    print("INPUT VALIDATION")
    print("=" * 60)

    # Test cases
    test_cases = [
        ("valid_text@example.com", True),
        ("invalid.email.com", False),
        ("test@domain", False),
    ]

    print("\nEmail Validation:")
    for email, expected in test_cases:
        result = InputSanitizer.sanitize_email(email) is not None
        status = "✅" if result == expected else "❌"
        print(f"  {status} {email}: {result}")

    # Filename sanitization
    print("\nFilename Sanitization:")
    dangerous_names = [
        "../../../etc/passwd",
        "file<>name.txt",
        "../../secret.key",
    ]

    for name in dangerous_names:
        sanitized = InputSanitizer.sanitize_filename(name)
        print(f"  {name} → {sanitized}")


def demo_action_validation():
    """Demonstrate action validation."""
    print("\n" + "=" * 60)
    print("ACTION VALIDATION")
    print("=" * 60)

    validator = ActionValidator()

    # File access validation
    files = [
        ("document.txt", True),
        ("data.json", True),
        ("script.exe", False),
        ("../../password.db", False),
    ]

    print("\nFile Access Validation:")
    for filename, expected in files:
        result = validator.validate_file_access(filename, "write")
        status = "✅" if result == expected else "❌"
        print(f"  {status} {filename}: allowed={result}")

    # Command validation
    print("\nCommand Validation:")
    commands = [
        ("ls -la", True),
        ("rm -rf /", False),
        ("echo hello", True),
        ("dd if=/dev/zero", False),
    ]

    for cmd, expected in commands:
        result = validator.validate_command(cmd)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {cmd}: allowed={result}")


def demo_rate_limiting():
    """Demonstrate rate limiting."""
    print("\n" + "=" * 60)
    print("RATE LIMITING")
    print("=" * 60)

    limiter = RateLimiter(max_calls=5, window_seconds=60)

    user_id = "user_123"

    print(f"\nRate Limit: {limiter.max_calls} calls per {limiter.window_seconds} seconds")
    print(f"\nMaking requests for {user_id}:")

    for i in range(7):
        allowed = limiter.is_allowed(user_id)
        remaining = limiter.get_remaining(user_id)
        status = "✅" if allowed else "❌"
        print(f"  Request {i+1}: {status} (remaining: {remaining})")


def demo_security_patterns():
    """Demonstrate security best practices."""
    print("\n" + "=" * 60)
    print("SECURITY PATTERNS")
    print("=" * 60)

    print("""
Security Best Practices for MCP Servers:

1. INPUT VALIDATION
   ✅ Validate all user inputs
   ✅ Use schema validation
   ✅ Sanitize and normalize data
   ✅ Reject malformed requests

2. AUTHORIZATION
   ✅ Check permissions before action
   ✅ Use role-based access control
   ✅ Implement resource-level ACLs
   ✅ Log authorization failures

3. RATE LIMITING
   ✅ Limit requests per user/time
   ✅ Prevent resource exhaustion
   ✅ Implement backoff strategies
   ✅ Monitor suspicious patterns

4. SECRET MANAGEMENT
   ✅ Never log secrets
   ✅ Use environment variables
   ✅ Rotate credentials regularly
   ✅ Encrypt sensitive data at rest

5. AUDIT LOGGING
   ✅ Log all tool invocations
   ✅ Record who accessed what
   ✅ Track permission changes
   ✅ Monitor error patterns

6. ERROR HANDLING
   ✅ Don't expose system details
   ✅ Log detailed errors internally
   ✅ Return generic messages to users
   ✅ Gracefully handle exceptions
    """)


def main():
    """Run demonstrations."""
    print("\n" + "🚀 LESSON 5.5: SECURITY & GUARDRAILS".center(60, "="))

    try:
        demo_permission_system()
        demo_input_validation()
        demo_action_validation()
        demo_rate_limiting()
        demo_security_patterns()

        print("\n" + "=" * 60)
        print("✅ Security demonstrations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
