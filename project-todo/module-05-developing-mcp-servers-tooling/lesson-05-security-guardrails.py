"""
Lesson 5.5: Security Guardrails — TODO Scaffold

Learn to add security layers to MCP servers including input validation, rate limiting,
and access controls to protect AI systems from malicious usage.

BUSINESS SCENARIO:
AI-powered tools need safety mechanisms before production deployment. This lesson
teaches building robust guardrails that validate inputs, limit resource usage,
and control access to sensitive operations.

Run: python lesson-05-security-guardrails.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Callable

# Import from shared module
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Tool


# ============================================================================
# STAGE 1: Input Validation & Sanitization
# ============================================================================
# Implement validation functions for inputs to prevent injection and misuse.
# Available utilities: regex patterns, type checking, sanitization helpers
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Rate Limiting & Resource Control
# ============================================================================
# Implement rate limiting and resource quotas to prevent abuse.
# Available utilities: time module, counters, quota tracking
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Access Control Wrapper
# ============================================================================
# Create add_security_guardrails() wrapper that applies all protections.
# Available utilities: decorator pattern, authentication checks, logging
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Demonstrations & Testing
# ============================================================================
# Show guardrails protecting against attacks and malicious inputs.
# Available utilities: attack scenarios, logging output, test suite
# TODO: Add your Stage 4 implementation here
