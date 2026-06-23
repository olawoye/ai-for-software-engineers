"""
Permission and security controls for MCP servers.
Implements role-based access control and action restrictions.
"""

from typing import Dict, List, Set, Optional
from enum import Enum


class Permission(Enum):
    """Available permissions."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"


class Role(Enum):
    """User roles."""

    USER = "user"
    POWER_USER = "power_user"
    ADMIN = "admin"


class PermissionManager:
    """Manages permissions and access control."""

    def __init__(self):
        self.role_permissions: Dict[Role, Set[Permission]] = {
            Role.USER: {Permission.READ},
            Role.POWER_USER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
            Role.ADMIN: {
                Permission.READ,
                Permission.WRITE,
                Permission.DELETE,
                Permission.EXECUTE,
                Permission.ADMIN,
            },
        }

    def has_permission(self, role: Role, permission: Permission) -> bool:
        """Check if role has permission."""
        return permission in self.role_permissions.get(role, set())

    def grant_permission(self, role: Role, permission: Permission) -> None:
        """Grant permission to role."""
        if role not in self.role_permissions:
            self.role_permissions[role] = set()
        self.role_permissions[role].add(permission)

    def revoke_permission(self, role: Role, permission: Permission) -> None:
        """Revoke permission from role."""
        if role in self.role_permissions:
            self.role_permissions[role].discard(permission)


class ResourcePermissions:
    """Fine-grained resource access control."""

    def __init__(self):
        self.resource_acl: Dict[str, Dict[str, List[Permission]]] = {}

    def grant_access(self, resource: str, user: str, permissions: List[Permission]) -> None:
        """Grant user access to resource."""
        if resource not in self.resource_acl:
            self.resource_acl[resource] = {}

        self.resource_acl[resource][user] = permissions

    def has_access(self, resource: str, user: str, permission: Permission) -> bool:
        """Check if user has permission for resource."""
        if resource not in self.resource_acl:
            return False

        if user not in self.resource_acl[resource]:
            return False

        return permission in self.resource_acl[resource][user]

    def list_permissions(self, resource: str) -> Dict[str, List[str]]:
        """List all permissions for resource."""
        return {
            user: [p.value for p in perms]
            for user, perms in self.resource_acl.get(resource, {}).items()
        }


class ActionValidator:
    """Validates actions against security policies."""

    def __init__(self):
        self.restricted_words = {"DROP", "DELETE", "TRUNCATE", "rm", "-rf"}
        self.allowed_extensions = {".txt", ".md", ".json", ".csv"}

    def validate_file_access(self, filename: str, action: str) -> bool:
        """Validate file access request."""
        # Check extension
        if not any(filename.endswith(ext) for ext in self.allowed_extensions):
            return False

        # Validate action
        if action == "write" and any(word in filename.upper() for word in self.restricted_words):
            return False

        return True

    def validate_command(self, command: str) -> bool:
        """Validate command execution."""
        # Reject dangerous commands
        dangerous = {"rm -rf", "dd if=", ":(){ :|:& };:", "fork()"}
        for danger in dangerous:
            if danger in command:
                return False

        return True

    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input."""
        # Remove potentially dangerous characters
        sanitized = user_input.replace(";", "").replace("|", "").replace("&", "")
        return sanitized.strip()
